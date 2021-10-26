# ===== Basic Import ===== #
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# For init db
from sqlalchemy import create_engine



# ===== Base Setup ===== #
Base = declarative_base()
class BaseMixin:
    # Auto init function: corresponding every keyword argument to member data
    def __init__(self, **kwargs):
        for var, value in kwargs.items():
            if var in dir(self): exec(f'self.{var}={value}')
    
    # Auto naming: class name in CamelNaming to table name camel_naming
    @declared_attr
    def __tablename__(cls):
        uppercase_index = [idx for idx, c in enumerate(cls.__name__) if c.isupper()]
        _, *remaining_index = uppercase_index
        if not remaining_index:
            return cls.__name__.lower()
        
        table_name = cls.__name__.lower()
        for idx in remaining_index[::-1]:
            table_name = table_name[:idx] + "_" + table_name[idx:]
        return table_name
    
    # Universal data: id, created time, and updated time
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment='資料建立時間')
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment='最後更新時間')
    
    

# ===== SECTION: Verdict ===== #
class Verdict(Base, BaseMixin):
    court = Column(Integer, ForeignKey("court.id"), nullable=False)
    system = Column(Integer, ForeignKey("system_type.id"), nullable=False)
    year = Column(Integer, index=True, nullable=False)
    crmid = Column(String(16), index=True, nullable=False)
    crmno = Column(Integer, index=True, nullable=False)
    sentence_date = Column(Date, index=False, nullable=False)
    verdict_type = Column(Integer, ForeignKey("verdict_type.id"), nullable=False)
    ### Above: known info after title-crawling, before text-crawling
    #text_done = Column(Boolean, default=False, index=True, nullable=False)
    ### Below: info to retrieve by text-crawling
    data_id = Column(Integer, index=False, nullable=True)
    text = Column(Text, default="", nullable=True)
    charge_s = Column(Integer, index=False, nullable=True)
    measure_s = Column(Integer, index=False, nullable=True)
    measure_e = Column(Integer, index=False, nullable=True)
    law_s = Column(Integer, index=False, nullable=True)
    law_e = Column(Integer, index=False, nullable=True)
    reason = Column(String(64), default="", index=True, nullable=True)
    


# ===== SECTION: Court ===== #
class Court(Base, BaseMixin):
    name = Column(String(64), index=True, nullable=False)
    code = Column(String(8), index=True, nullable=False)
    verdicts = relationship("Verdict")
    


# ===== SECTION: SystemType (民事、刑事等) ===== #
class SystemType(Base, BaseMixin):
    name = Column(String(16), index=True, nullable=False)
    code = Column(String(8), index=True, nullable=False)
    verdicts = relationship("Verdict")
    
    

# ===== SECTION: VerdictType (判決、裁定等) ===== #
class VerdictType(Base, BaseMixin):
    name = Column(String(16), index=True, nullable=False)
    verdicts = relationship("Verdict")
    
    
    
if __name__=="__main__":
    conn_str = "postgresql+psycopg2://postgres:password@103.124.74.104:5432/judicial"
    engine = create_engine(conn_str, echo=True)
    Base.metadata.create_all(engine)