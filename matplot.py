import matplotlib.pyplot as plt
month1=[1,2,3,4,5,6,10,12]
month2=[1,3,4,5,6,7,11,12]
sale1=[20000,40000,60000,80000,100000,120000,140000,160000]
sale2 = [10000, 20000, 30000, 40000, 50000, 60000, 200000, 400000]
plt.plot(month1,sale1,lw=2,label='Ivy Lin')
plt.plot(month2, sale2, lw=2, label='Jonhy Wu')
plt.xlabel('month')
plt.ylabel('dolars')
plt.legend()
plt.title('matplotlib Sample')
plt.show()

