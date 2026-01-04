# 项目目录结构说明

```text
project-root/                             # 项目根目录
├─ base/                                  # 基础类封装
│  ├─ base_request.py                     # 接口请求基类（封装 requests）
│  ├─ request_api.py                      # 请求 API 封装
│  ├─ get_logger.py                       # 日志处理工具
│  ├─ assertions.py                       # 断言工具
│  └─ generate_id.py                      # 生成测试编号
├─ common/                                # 公共方法封装
│  ├─ config_handler.py                   # 配置文件处理
│  ├─ reflection_handler.py               # 反射处理
│  ├─ yaml_handler.py                     # YAML 文件解析
│  └─ ding_ding_robot.py                  # 钉钉机器人通知
├─ conf/                                  # 全局配置目录
│  ├─ config.ini                          # 项目配置文件
│  └─ setting.py                          # 代码级配置
├─ data/                                  # 测试数据目录
│  ├─ business_interface/                 # 业务场景用例
│  │  └─ product_order_scenario.yaml      # 商品下单支付完整流程
│  ├─ login/                              # 登录模块
│  │  └─ login_name.yaml                  # 登录接口用例
│  ├─ product_manage/                     # 商品管理模块（单接口）
│  │  ├─ get_product_list.yaml            # 获取商品列表
│  │  ├─ get_product_detail.yaml          # 获取商品详情
│  │  ├─ commit_order.yaml                # 提交订单
│  │  └─ order_pay.yaml                   # 订单支付
│  ├─ user_manage/                        # 用户管理模块（单接口）
│  │  ├─ add_user.yaml                    # 新增用户
│  │  ├─ update_user.yaml                 # 修改用户
│  │  ├─ delete_user.yaml                 # 删除用户
│  │  └─ query_user.yaml                  # 查询用户
│  └─ extract.yaml                        # 接口依赖参数提取文件
├─ logs/                                  # 日志目录（自动生成）
│  └─ test.20251230.log                   # 按日期生成的日志
├─ report/                                # 测试报告目录（Allure）
├─ testcase/                              # 测试用例目录
│  ├─ test_product_order_scenario.py      # 业务流程测试
│  ├─ test_product_single_interface.py    # 商品单接口测试
│  ├─ test_user.py                        # 用户模块测试
│  └─ conftest.py                         # 用例级 pytest 钩子
├─ conftest.py                            # 全局 pytest 钩子
├─ environment.xml                        # Allure 环境配置
├─ pytest.ini                             # pytest 配置文件
├─ requirements.txt                       # 依赖库清单
└─ run.py                                 # 项目主入口（执行测试 + 生成报告）
