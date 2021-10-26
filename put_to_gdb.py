from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from db_models import Verdict
from ckiptagger import WS, POS, NER
from neo4j import GraphDatabase



# 建立與資料庫的連線
engine = create_engine("postgresql+psycopg2://postgres:password@103.124.74.104:5432/judicial", echo=False)
Session = sessionmaker(bind=engine, autoflush=False)
driver = GraphDatabase.driver('bolt://localhost:7687/neo4j', auth=('neo4j', 'password'))



# 載入中研院語言模型
ws = WS('D://ckip_models')
pos = POS('D://ckip_models')
ner = NER('D://ckip_models')



# 定義 Neo4j 放入資料庫功能
def put_verdict(tx, verdict_name, judge_list, defendant_list, law_list):
    # 分析法條&項次
    law_id_list = []
    for law in law_list:
        p = law.find('條')+1
        if p == len(law):
            id = tx.run("MERGE (a:法律 {name:'毒品危害防制條例'}) MERGE (a)-[:HAVE]->(l:法條 {name:$name}) RETURN ID(l) as id", name=law)
        else:
            id = tx.run("MERGE (a:法律 {name:'毒品危害防制條例'}) MERGE (a)-[:HAVE]->(l:法條 {name:$name}) MERGE (l)-[:HAVE]->(i:項次 {name:$item_name}) RETURN ID(i) as id", name=law[:p], item_name=law[p:])
        law_id_list.append([_['id'] for _ in id][0])
        
    # 製作判決、法官、被告、法條關係圖
    id = tx.run("CREATE (v:判決 {name: $verdict_name}) RETURN ID(v) as id", verdict_name=verdict_name)
    id = [_['id'] for _ in id][0]
    for judge in judge_list:
        tx.run("MATCH (v:判決) WHERE ID(v)=$id " +\
               "MERGE (j:法官 {name:$judge}) CREATE (j)-[:IN_CHARGE]->(v)", 
               judge=judge, id=id)
    for defendant in defendant_list:
        tx.run("MATCH (v:判決) WHERE ID(v)=$id " +\
               "MERGE (d:被告 {name:$defendant}) CREATE (d)-[:INVOLVE_IN]->(v)", 
               defendant=defendant, id=id)
    for law_id in law_id_list:
        tx.run("MATCH (v:判決), (l) WHERE ID(v)=$id AND ID(l)=$law_id " +\
               "CREATE (v)<-[:QUOTED_BY]-(l)", id=id, law_id=law_id)



# 提取相關資料，針對每一筆資料進行處理
session = Session()
verdicts = session.query(Verdict).filter(func.length(Verdict.text)>0).limit(20).all()



for verdict in verdicts:
    # 顯示本筆資料
    verdict_name = str(verdict.year) +"年"+ verdict.crmid +"字第" + str(verdict.crmno) +"號"
    print(f"Extracting {verdict_name}:")

    # NER 找到法官&被告身份
    sentences = verdict.text.replace(' ','').split('\n')
    ws_sentences = ws(sentences)
    pos_sentences = pos(ws_sentences)
    entity_list = ner(ws_sentences, pos_sentences)
    judge_set = set()
    defendant_set = set()
    for stc, ents in zip(sentences, entity_list):
        for ent in list(ents):
            if ent[2]!='PERSON':continue
            if stc[ent[0]-2:ent[0]] == '被告': defendant_set.add(ent[3])
            elif stc[ent[0]-2:ent[0]] == '法官': judge_set.add(ent[3])
    judge_list = list(judge_set)
    defendant_list = list(defendant_set)
    
    
    
    # 找毒品危害防制條例相關法條
    laws = verdict.text[verdict.law_s:verdict.law_e].replace(' ','')
    law_start = laws.find('毒品危害防制條例')+8
    law_end = min([laws.find(p, law_start) for p in ['，', '。'] if p in laws]+[100])
    law_list = laws[law_start:law_end].split('、') if law_end<99 else []
    


    # 整理資料放入資料庫
    print("法官：", judge_list)
    print("被告：", defendant_list)
    print("相關法條：毒品危害防制條例"+"、".join(law_list))
    with driver.session() as gdb_session:
        gdb_session.write_transaction(put_verdict, verdict_name, judge_list, defendant_list, law_list)
