1.该crm系统只要用于管理客户信息
配置如下：
1.数据库用muyql
2.用户登陆：
（1）超级管理员账号 ，通过命令创建，保存于aoth_user表
（2）普通账户，通过超级管理员登录后的页面创建，保存于 accounts_user表
功能实现：
1.设定组织架构，通过各个部门实现关联
比如，总经办-销售部/财务部 - 销售一部/销售二部，就是总经办下面有2个部门平级部门销售部和财务部，在销售部下面还有三级分支 销售一部和销售二部
实现 不同部门的员工其账号之间不能相互查看，但是上级可以查看下级的数据
比如总经办可以查看下属所有部门的信息，但是销售部和财务部不能相互查看，同时财务部不能查看销售部的分支，销售一部和销售二部，销售一部跟销售二部也不能相互查看，但是销售部可以查看销售一部和销售二部的信息
2.当员工登录，可以直接在客户列表中添加客户，这时候添加的客户信息只属于当前登陆用户，除了其上级以外，其他人是看不到该员工账号下的客户信息的