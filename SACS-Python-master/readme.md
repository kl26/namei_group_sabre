#总览

## 结构
1. config文件夹中的Configurarion.py 用以实现构建调用API所需要的token, SACSConfig.properties中的参数为Sabre提供的权限
	environment可选的环境为：
	REST:
	测试环境: https://api-crt.cert.havail.sabre.com
	生产环境: https://api.havail.sabre.com
	SOAP:
	测试环境: https://sws-crt.cert.havail.sabre.com
	生产环境: https://webservices.havail.sabre.com
2. 

## 存在问题
1. InstaFlightActivity
	输入可选参数returndate，不填的话会报错。