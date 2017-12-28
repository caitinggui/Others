# Others
A repo for something interesting.


## .gitignore说明
1. 忽略一个特定的文件：/filename.extension   # '/'表示.gitignore所在根目录
2. 忽略所有同名的文件：filename.extension    # 所有目录下的该文件都会被忽略
3. 忽略一个特定的目录：folder/static/ # 表示忽略./folder/static/下所有文件及目录, 但不在这个目录下的其他目录不受影响, 比如./fold/folder/static/目录不受影响
4. 忽略一种模式下的目录：\*\*/floder/static/  # 上面说明的./fold/floder/static/也会被屏蔽
5. 但是排除一个特定的模式：（在 3 的基础上）!folder/some/important/filename.extension
6. 忽略指定目录下所有子目录下的特定文件：folder/\*\*/filename.extension
7. 同上，但是只匹配文件扩展名：folder/\*\*/\*.extension
8. 同上，但是只匹配特定的目录：folder/\*\*/tmp/
9. 如果是子目录下的 .gitignore，在上述基础上记得不要在最前面加 '/'，否则会匹配到工作树的根路径，而不是子目录下的 .gitignore 的同级，就这个是一个坑，其他都一样。
10. 前置斜线与后置斜线的区别：
    - 前置斜线: .gitignore 是默认以相对路径为基准的，子目录下的 .gitignore 优先应用自己的规则然后再递归向上一直找到 git 的根（也就是 .git 存在的那个目录）,一般不需要使用前置斜线，除非要屏蔽以*根目录*为起点的某个特定文件
    - 后置斜线: static/ 和 static 是不一样的，前者只匹配目录 static，而后者则可以匹配同名的目录、文件名、符号链接等等

passwd = 'dbumqtpqdakubebc'  # 填入发送方邮箱的授权码
