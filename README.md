# Vps Backup
功能：借助七牛云平台，实现对于VPS服务器的文件备份。
<hr />
<pre>
程序语言：Python 2.7.9 
外部库：   sevencow 库 

注释：sevencow库基于七牛云公司标准API，具有更好的简易性。
</pre>
<hr />
工作流程：用户先在&nbsp;<font color="red">backup.config</font>&nbsp;文件中配置必要的参数信息。<br />
&nbsp;&nbsp;参数主要包括:<br />
<pre>
    AK                      七牛提供的AK密钥
    SK                      七牛提供的SK密钥
    Cloud Bucket        备份目录名
    Source Floder       服务器目录路径
</pre>
<hr />

如果你需要完成后的邮件提醒功能，请修改python代码的最后注释部分，修改SMTP的相应参数。