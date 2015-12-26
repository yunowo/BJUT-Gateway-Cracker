## BJUT 弱口令网关账号探测 ##  
  
很多用户的初始密码没有改，用默认的身份证后X位就能登进去。  
这其中又有很多用户的网关流量从来不用。  
这个脚本通过字典跑出没改密码的用户。~~不要问我字典从哪里来。~~  
这样在自己没流量的时候就可以挑选那些从来不用的幽灵账户借用流量。  
物尽其用嘛，反正他自己也不用=。=  
2.0版本还可以自动登录后台获取套餐总流量和已使用流量，防止给别人造成经济损失。  
  
  
目前的版本存在不能全自动登录的问题  
![](http://i4.tietuku.com/4a0f53b1558c94ce.png)  
  
如图，后台的登录请求分为两个包。第一个包返回一个随机的验证码，如果 session 超时会在 cookie 里返回一个新的 session ID。  
第二个包用这个 session ID 和随机码加上用户名密码去认证。  
但我在用脚本自动获取 session ID 时总是认证不成功，而使用 Fiddler 抓取的浏览器产生的老 session ID 就可以正常登录。原因不详，十分诡异。  
目前只能使用浏览器先产生一个可用的 session ID 并手动放到代码里执行。  
十分蛋疼，不过也算凑合能用。  
  
如果哪位有解决方案请务必告诉我。  
