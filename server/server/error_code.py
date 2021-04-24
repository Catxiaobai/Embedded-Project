# error_message 是前端需要展示出来的错误信息

# 成功
CLACK_SUCCESS = {"error_code": 0, "error_message": "OK"}

# 未知错误
CLACK_UNEXPECTED_ERROR = {"error_code": -1, "error_message": "未知错误"}

# 请求方法不是POST
CLACK_POST_REQUIRED = {"error_code": 1, "error_message": "请求方法不是POST,触发该错误应该是前端写挂了"}

# 请求JSON中部分必须的对象不存在
CLACK_REQUEST_JSON_ERROR = {"error_code": 2, "error_message": "请求JSON中部分必须的对象不存在,触发该错误应该是前端写挂了"}

# 传递的值为空
CLACK_NULL_ERROR = {"error_code": 3, "error_message": "存在空值"}

# 目标不存在
CLACK_NOT_EXISTS = {"error_code": 4, "error_message": "此目标不存在"}

# 名称已经存在
CLACK_NAME_EXISTS = {"error_code": 5, "error_message": "已存在"}

# 有重复的内容
CLACK_REPEAT_CONTENT = {"error_code": 6, "error_message": "有重复"}

# 登录错误
CLACK_USER_LOGIN_FAILED = {"error_code": 7, "error_message": "登录失败,用户名或密码错误"}

# 用户未登录
CLACK_LOGIN_REQUIRED = {"error_code": 8, "error_message": "请先登录"}

# 需要系统管理员权限
CLACK_SYSTEM_ADMIN_REQUIRED = {"error_code": 9, "error_message": "只有系统管理员才能进行此操作"}

# 需要系统管理员权限
CLACK_AUTORITY_SUCCESS = {"error_code": 10, "error_message": "权限合法"}

# 需要管理员权限
CLACK_ADMIN_REQUIRED = {"error_code": 11, "error_message": "只有管理员才能进行此操作"}

# 文件夹已存在
CLACK_DIR_EXISTS = {"error_code": 12, "error_message": "文件夹已存在，无法创建此项目"}

# 用户已存在
CLACK_ITEM_USER_EXISTS = {"error_code": 13, "error_message": "此用户已存在该项目中"}

# 无法删除admin
CLACK_ADMIN_NOT_DELETE = {"error_code": 14, "error_message": "无法删除超级管理员admin账号"}

# 无法修改admin
CLACK_ADMIN_NOT_EDIT = {"error_code": 15, "error_message": "无法修改超级管理员admin账号"}
