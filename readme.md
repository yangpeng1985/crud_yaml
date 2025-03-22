# 使用python语言实现两个yaml文件的增删改操作

场景：版本升级时要对配置文件，yaml格式，进行增加、删除、更新操作


## 第一个里程碑： web界面支持合并两个yaml文件，只支持增加，不支持删除和修改key的值。这个时候新增的配置如果有变量需要手动处理好。

需求：
1. 使用flask web框架开发一个系统，从web界面粘贴到三个窗口，合并三个yaml文件，合并的yaml文件支持一键复制；
一个yaml叫做 base.yaml ，在base.yaml内容的基础上，做增量处理，具体包括：key的增加和删除，key本身不能修改；
增量的yaml，叫做 add_key_to_base.yaml；删除的yaml，叫做 del_key_to_base.yaml；最终生成的yaml，叫做target.yaml；
只支持增加，不支持删除和修改key的值；新的内容要保留原有内容的注释和引号，之前是单引号就是单引号、之前是双引号就是双引号；
2. 使用pytest做自动化测试；
3. 使用虚拟环境做项目测试，环境名称叫做 myenv


## 第二个里程碑： web界面支持修改相同key的value值

改，包括两种修改。
一种修改是完全替换value，另一种改是在原有value的基础上增加内容。
在改的过程中，怎么知道是哪种修改呢？

value的场景。 
1. 将value从true修改为false，或者将false修改为true；
2. value的内容只有一个，比如： true、false、xxx.abc.com、 127.0.0.1；
3. value的内容由多个内容组成：比如 1.1.1.1,1.1.1.2; 
4. value的内容是一个列表；

第一步：先实现value的替换场景
在之前功能的基础上，增加可以输入要修改内容的地方；
先检查要修改的内容的key在base文件中是否存在，将所有的key都先检查一遍，如果有不存在的key，报错，提示信息里包括所有不存在的key，不再进行后续的替换和合并；
按照删、改、增的顺序处理；


## 使用说明
* python app.py 启动程序
* 浏览器访问 http://127.0.0.1:5000 默认是合并功能；
    * 支持在base的yaml文件的基础上做key的增加、删除，做value的修改；
    * 按照删除、修改、增加的顺序完成合并
* 浏览器访问 http://127.0.0.1:5000/compare_page 是比较功能； 
    * key和value同时比较，key和value都相同时表示是两个yaml文件都有的


## 开发相关
* python test_app.py 进行功能自动化测试
* python generate_requirements.py 更新 requirements.txt 的内容
