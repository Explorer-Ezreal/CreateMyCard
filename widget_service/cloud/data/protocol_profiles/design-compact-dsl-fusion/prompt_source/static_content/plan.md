---
name: static-plan
description: 静态Plan字段、来源引用、索引与提交自查；信息规则和组件布局合同从初始上下文继承。
---

# 静态Plan提交

当前agent_stage=plan，仅提交{"name":"submit_card_plan","arguments":{...}}纯JSON文本。
若用户实际明确要求动态读取或刷新、但本轮未提供必要动态字段，按另行提供的report_missing_data合同
报告输入缺口；不能编造静态读数或把功能描述冒充展示事实。空绑定本身不是缺口；
固定文字、已采用静态事实及仅快捷动作仍按正常静态计划处理。
本阶段完成理解、筛选、精简和总结；先构思可放下的字段组合，再提交最终可见文字。
不提交composition，不新增模型阶段。

## 展示事实与来源

| 字段 | 填写方式 | 使用边界 |
|---|---|---|
| info_required | 每项requirement、priority和一个text或actionId | 拆分不超过24事实总预算 |
| text | 最终可读展示版本 | 来源可忠实总结，不必逐字提取或拼接 |
| sourceTexts | 每项text引用1–3段本轮输入连续原文 | 可追溯证据，不编造引用支持编造摘要 |
| protectedTexts | 用户明确要求逐字保留的片段 | 普通摘要填[]，不机械保护所有名称和数字 |
| preserveVerbatim | 完整原文要求时true | text完整保留一段引用，不使用省略号 |
| actionId | 当前批准动作 | Action必须must，不填静态来源字段，不分组 |

正文不得有dataId或绑定，priority沿用信息合同中的核心与独立补充划分。

## 对象分组与引用

contentGroups每组{id,kind:"object"|"shared",identity:"对象短名称"|null,factIndexes:[0起始索引]}。
每条text恰好归一组；factIndexes只引用本次info_required，不引用输入材料条目编号或sourceTexts位置。
合并为两条展示事实后只存在索引0、1；合并或删减事实时同步所有分组及遗漏引用，不沿用来源序号。

object是一条记录、一栏或一个内容块；shared是共同标题、范围、计价口径或说明。
属性表可一表一组或每行一组；一个object对应一条记录或一行属性，属性表每行单独分组，
单对象正文则可把关联事实合组。同一事实的字段按展示顺序组织，不能靠其它对象补本对象信息。
选择records或以RecordList为对象首选组件时，最多提交3个object组；第4个及后续对象不进入
info_required/contentGroups，应写入omittedContents。先保留用户点名或明确优先的对象，
没有优先级时保留输入原顺序前3项，不留给DSL修复删除。
对象名称是展示合同的一部分；来源中真实命名的商品、方案、模型、城市或项目须填identity，
并在本对象内可见，不能仅放在requirement或组ID。未命名对象和shared显式填null；
结构序号、条目顺序和临时概括不是主体名称。名称忠于来源，不补造，也计入试排容量。

## 展示提示

| 字段 | 可选值 / 含义 | 使用边界 |
|---|---|---|
| componentHints | 本尺寸静态正文组件 | 动作沿用合法动作组件 |
| layoutHints | 当前尺寸合法静态布局 | 动作才使用兼容布局 |
| presentationStyle | auto/content/attributes/records/comparison | 表达信息结构，不是业务场景；比较遵守宽卡组件合同 |
| displayRole | title/body/label/value/leading/trailing/detail | 仅text使用，按已有角色层级拆分 |
| paletteFamily | auto/blue/purple/warm | 用户明确偏好才登记对应色系，默认auto |

对象名称或可识别主体放title，完整结论放body，属性键值用label/value，侧边只放短leading/trailing。
对比的value是主读数、title是对象名。共享短标题用shared中的title，来源、时间口径和共同条件用shared中的body。
替代/并列关系和必要限定须在展示文字中保留，不得仅放requirement或组ID。

## 取舍与容量反馈

selectionNotes为最多8条的一个字符串数组，例如["结构选择说明","取舍说明"]，不能把每项再包成数组。
omittedContents最多24项，每项{description,factIndexes}；没有实际或候选遗漏填[]。
仍在info_required中的可能省略should填写原事实索引，是否实际省略由最终展示对账；
未选择进计划、确实损失的独立输入内容填[]。不得引用must或受保护文字。
示例：{"description":"可选补充若放不下可省略","factIndexes":[3]}。
等义摘要、完整出处缩写及按用户要求不列入的未检索内容不算实际遗漏；不能把规划说明当实际省略。
程序不从description猜事实，不把“可能省略”预先当成实际遗漏。

没有可行试排时，capacityReference会在既有第二次Plan机会反馈；先精简重复表达和规划结构，
再提交完整新计划。可在冻结前忠实总结，不能删必要限定、改数值或将其假标should。
反馈只代表有限候选未通过，不代表所有结构不可行，不凭此机械删除对象。

## 提交自查

在本次推理内完成，不增加调用或额外审查字段：
1. 回答用户核心目标；结论有引用支持，不引入原文没有的断言，不改变名称中的文字或数字。
2. 对照来源核对对象、日期、数值高低与单位、冲突来源、范围、频率、否定、条件和例外。
3. 可选方案仍用“或”，共同要求仍用“且/同时”；不为放下而删除决定含义的条件。
4. 字段行数和整卡容量可行；信息过多先重新总结，不能先抄全文交给程序删；原文和全部展示要求继续遵守。
