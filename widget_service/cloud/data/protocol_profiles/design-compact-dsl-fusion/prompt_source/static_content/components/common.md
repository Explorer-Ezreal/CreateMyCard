---
name: static-components
description: 共享静态正文及辅助组件的触发条件、参数、变体和内部层级；不定义整卡布局或Plan提交格式。
---

# 组件

## 总表

| 名称 | 适用条件 | 承载内容 | 使用边界 |
|---|---|---|---|
| ContentBlock | 单对象结论或短键值集合 | title、body、attributes | 属性1–6项；至少包含一种内容 |
| RecordList | 多对象名称与说明 | items | 1–3条，通常两条更可读 |
| SingleLineTitle | 必要的短共同标题 | title | 完整单行；非必要省略 |
| SecondaryBody | 必要的共同说明 | items | 单列短说明，不承载正文对象 |
| PillButton / CardButton | 有批准动作及合法动作位 | 完整动作及handler | 不作为正文容器 |

正文只使用本尺寸登记的静态正文组件。必要辅助仅SingleLineTitle、SecondaryBody及PillButton/CardButton。
正文不使用EventCard、TextBlock、SummaryList、InfoBlock、TableText、EmphasisText、DataDisplay等旧组件，
也不直接输出基础Text、Row/Column/Stack/Group。静态正文组件不支持绑定、Expression、onClick、图标、
颜色、任意几何或嵌套组件。

## ContentBlock

### 选择条件

单对象优先此组件；四至六个短键值也可作为属性表。短键值用属性表，表内属性分别保留标签和完整值，
每行对应自己的事实，不能跨行借事实。

### 参数与变体

| 参数 | 类型 / 可选值 | 要求 |
|---|---|---|
| title / body | 静态文字 | title/body/attributes至少一个 |
| attributes | 1–6项{label?,value,valueRole?} | value必填；label若提供须有实际意义且非空 |
| variant | flow / bottom-attributes | 默认并优先flow；后者必须有属性且预算成立 |
| attributes[].valueRole | body / value | 默认body左对齐；明确短读数用value右对齐 |

没有标签直接省略，可仅填value，不写“信息”等占位词；标签或标题已承载对象名时不在value重复。
容量紧张时可把对象短名称与完整正文合入同一无标签value，避免名称额外占行，字段仍归本对象。
无label属性默认12字号、16行高。允许标签和值分层或调整标点；长值保持本行归属。

## RecordList

### 选择条件

多对象名称与说明使用记录，突出对象名称，说明弱化；能承载时不要降成无层级的整句属性表。
不为填字段补日期或价格；长条件和长名称放主区，短时间、短日期、短标签或短读数才放侧边。
活动、日程、演出、行程等由“对象名称 + 日期/时间/地点”构成的多条同构记录，
优先选择records/RecordList；每个object组只对应一条真实记录，不按类别把多条记录塞进一个长value，
也不改用content/attributes规避条目上限。名称放title，短日期、时间或地点放
description/leading/trailing；不要以“演唱会/话剧/体育”等类别为标签把多个独立场次压进同一value。

### 参数与变体

| 参数 | 类型 / 可选值 | 要求 |
|---|---|---|
| items | 1–3项{title,description?,leading?,trailing?} | title必填 |
| variant | plain / panel | 默认并优先plain；有充裕空间才panel |

通常两条更可读，三条只用于短记录。侧边挤压时尝试本条内纵排，实际总高仍须通过；
不足时按综合选型与修复合同处理。

## 辅助标题与说明

| 名称 | 参数 | 文字与容量 |
|---|---|---|
| SingleLineTitle | title、fontSize:12 | 完整单行，12字号、16行高 |
| SecondaryBody | items:[{value:文字}]、columns:1、fontSize:12 | 默认12字号、14行高，通常1–2行 |

长标题在Plan中拆出短标题与日期/口径说明，主体、必要范围与日期口径继续可见；
不能依靠裁切、maxLines隐藏或缩小标题。非必要标题省略，长标题可放正文。
说明必要时最多3行但仍检查整卡；长来源优先不选或标为should，不把正文挪到note。

## 文字档位与层级

静态正文与辅助文字可用fontSize:12|11|10，默认12，10为硬下限；不接受其它数值。
本尺寸正文组件及静态SecondaryBody支持该字段。标题、记录名称和对比主值保留原有层级字号，
行高、换行和完整文字容量按所选档位计算；不允许隐式截断、裁切、连续缩放或删除必要条件。
数值、日期时间、范围和单位按完整片段换行，不能拆数字或让单位脱离读数。
