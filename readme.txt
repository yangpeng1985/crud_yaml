使用python语言实现两个yaml文件的增删改操作
场景：版本升级时要对配置文件，yaml格式，进行增加、删除、更新操作


第一个里程碑： web界面支持合并两个yaml文件，只支持增加，不支持删除和修改key的值。这个时候新增的配置如果有变量需要手动处理好。

需求：
1. 使用flask web框架开发一个系统，从web界面粘贴到三个窗口，合并三个yaml文件，合并的yaml文件支持一键复制；
一个yaml叫做 base.yaml ，在base.yaml内容的基础上，做增量处理，具体包括：key的增加和删除，key本身不能修改；
增量的yaml，叫做 add_key_to_base.yaml；删除的yaml，叫做 del_key_to_base.yaml；最终生成的yaml，叫做target.yaml；
只支持增加，不支持删除和修改key的值；新的内容要保留原有内容的注释和引号，之前是单引号就是单引号、之前是双引号就是双引号；
2. 使用pytest做自动化测试；
3. 使用虚拟环境做项目测试，环境名称叫做 myenv

