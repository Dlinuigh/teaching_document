#!/usr/bin/env python3
"""
从 高中物理.tex 引用的各节 .tex 中，按出现顺序复制 tabularx（列格式 XX 或 |c|X|），
生成两份与手册同结构的表格：填空版右栏留白，答案版与手册一致。
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "高中物理.tex"

OUT_Q = ROOT / "formula_fill_tabularx_question_tables.tex"
OUT_A = ROOT / "formula_fill_tabularx_answer_tables.tex"


def section_inputs() -> list[str]:
    text = MAIN.read_text(encoding="utf-8")
    return re.findall(r"\\input\{(section_\d+)\}", text)


def extract_tabularx_at(content: str, start: int) -> tuple[str, int] | None:
    needle_begin = r"\begin{tabularx}"
    needle_end = r"\end{tabularx}"
    if not content.startswith(needle_begin, start):
        return None
    depth = 1
    pos = start + len(needle_begin)
    while pos < len(content) and depth:
        nb = content.find(needle_begin, pos)
        ne = content.find(needle_end, pos)
        if ne < 0:
            return None
        if nb != -1 and nb < ne:
            depth += 1
            pos = nb + len(needle_begin)
        else:
            depth -= 1
            if depth == 0:
                end = ne + len(needle_end)
                return content[start:end], end
            pos = ne + len(needle_end)
    return None


def tabularx_meta(block: str) -> tuple[str, str] | None:
    m = re.match(
        r"\\begin\{tabularx\}\{\\columnwidth\}\{([^}]+)\}(.*)\\end\{tabularx\}",
        block,
        re.DOTALL,
    )
    if not m:
        return None
    return m.group(1).strip(), m.group(2)


ALLOWED_COLSPECS = frozenset({"XX", "|c|X|"})

SKIP_LABELS = frozenset(
    {
        "牛顿环暗环半径",
        "牛顿环明环半径",
        "马吕斯定律",
        "布儒斯特角",
    }
)

# 填空卷左栏附加说明（小号字）；答案卷不使用。查找顺序：
# (section 文件名, 条目, 出现序号) > (section 文件名, 条目) > 仅条目
LEFT_HINTS_TRIPLE: dict[tuple[str, str, int], str] = {}
LEFT_HINTS_PAIR: dict[tuple[str, str], str] = {}
LEFT_HINTS_SINGLE: dict[str, str] = {}

# --- 全局（多数章节通用）---
LEFT_HINTS_SINGLE.update(
    {
        "瞬时速度": "写出极限定义式（位移对时间的极限）。",
        "平均速度": "写出位移与所用时间的比值（矢量）。",
        "瞬时速率": "写出瞬时速度的大小（标量）。",
        "平均速率": "写出路程与所用时间的比值。",
        "平均加速度": "写出速度变化量与时间的比值。",
        "速度": "匀变速直线运动：速度与时间、初速度、加速度的关系式。",
        "速度平方": "匀变速直线运动：速度与位移关系（不含时间）。",
        "中间位移速度": "匀变速过程：位移中点处的瞬时速度公式。",
        "中间时刻速度": "匀变速过程：时间中点对应的瞬时速度（平均速度）。",
        "相邻相等时间间隔位移差": "匀变速：连续相等时间 $T$ 内位移之差与加速度关系。",
        "第M段与第N段Ts时间内位移差": "匀变速：第 $M$ 段与第 $N$ 段（每段时长 $T$）位移之差。",
        "相等时间每段位移比": "从静止匀加速：各 $T$ 内位移之比。",
        "相等时间总计位移比": "从静止匀加速：前 $n$ 个 $T$ 总位移之比。",
        "相等位移间隔每段用时比": "从静止匀加速：各相等位移段所用时间之比。",
        "相等位移间隔总计用时比": "从静止匀加速：通过前 $n$ 段相等位移累计用时之比。",
        "竖直速度": "平抛：竖直分速度与下落时间或竖直位移的关系。",
        "合速度": "平抛：合速度大小（水平、竖直分量合成）。",
        "轨迹抛物线方程": "消去时间：$y$ 与 $x$ 的抛物线关系。",
        "速度偏角": "速度与水平方向夹角的正切（可用 $v_y/v_0$、时间或位移表示）。",
        "斜面抛回斜面": "落到斜面时：位移偏角等于斜面倾角，写出由此得到的关系。",
        "垂直打到斜面上": "垂直撞击斜面时速度偏角与斜面倾角的关系式。",
        "牛顿第二定律": "合外力与加速度的关系（矢量式或分量式）。",
        "牛顿第三定律": "作用力与反作用力：等大、反向、共线，作用在两个物体上。",
        "胡克定律": "弹簧弹力与形变量（劲度系数）关系（注明伸长或压缩）。",
        "线速度": "圆周运动：线速度与角速度、半径关系。",
        "角速度": "圆周运动：角速度与周期关系。",
        "球体万有引力": "均匀球体：体外与体内引力大小的分段表达式（含条件）。",
        "球体万有引力势能": "质点在球外时的引力势能（规定无穷远为零势能）。",
        "密度公式": "近地卫星测密度：由周期写平均密度。",
        "周期定律": "开普勒第三定律：半长轴立方与周期平方之比与中心天体质量。",
        "黄金代换": "地面附近：引力与重力近似时的 $GM$ 与 $g、R$ 关系。",
        "第一宇宙速度": "贴近星球表面圆轨道环绕速度。",
        "同向（最近到最远）": "同向卫星：从最近到最远经历半圈相对转角所需时间。",
        "同向（最近到最近）": "同向卫星：从最近到再次最近相对转角 $2\\pi$ 所需时间。",
        "反向（最近到最远）": "反向卫星：从最近到最远相对转角 $\\pi$ 所需时间。",
        "反向（最近到最近）": "反向卫星：从最近到再次最近相对转角 $2\\pi$ 所需时间。",
        "质量半径关系": "双星：两星到质心的距离与质量成反比。",
        "质量角速度关系": "双星：角速度与间距、总质量的关系式。",
        "两极重力加速度": "自转影响：极点视重与万有引力关系（无向心加速度）。",
        "赤道重力加速度": "自转影响：赤道视重（万有引力减自转向心力）。",
        "滑动摩擦力": "写滑动摩擦定律（正压力与动摩擦因数）。",
        "最大静摩擦力": "写出最大静摩擦与正压力关系（静摩擦因数）。",
        "弹簧弹力": "胡克定律（伸长或压缩时的弹力）。",
        "共点力平衡": "共点力平衡的矢量条件（合力为零）。",
        "空气阻力": "题给阻力模型（如与速度成正比或平方）时的表达式。",
        "弹力做功": "弹簧：弹力做功与初末形变量的关系（弹性势能变化）。",
        "重力做功与重力势能": "重力做功等于重力势能增量的负值。",
        "弹力做功与弹性势能": "弹力做功等于弹性势能增量的负值。",
        "非保守力做功": "功能关系：非保守力做功与机械能变化。",
        "合力做功": "合力做功等于动能增量（动能定理）。",
        "动能": "动能定义式 $\\frac12 mv^2$。",
        "重力做功": "重力做功与初末高度差的关系（或下落高度）。",
        "弹力做功": "弹簧弹力做功与形变量的关系；若表中为“弹力与速度垂直”特例请按该条件书写。",
        "恒力冲量": "冲量：力与作用时间的乘积（矢量）。",
        "平均力冲量": "用平均力表示的冲量（动量变化）。",
        "动量定理": "合外力冲量等于动量变化（矢量式）。",
        "系统动量定理": "系统所受合外力的冲量等于系统总动量变化。",
        "动量守恒": "系统所受合外力为零时总动量守恒的表达式。",
        "恢复系数": "碰撞恢复系数定义（分离与接近的相对速度大小之比）。",
        "一维恢复系数": "对心碰撞：分离相对速度与接近相对速度之比。",
        "约化质量": "两体相对运动：约化质量 $\\mu$ 与两质量关系。",
        "碰撞损失机械能": "完全非弹性或一般碰撞：损失的动能表达式。",
        "回复力": "简谐振动：回复力与位移的比例关系（指向平衡位置）。",
        "简谐振动方程": "位移随时间的余弦（或正弦）形式。",
        "速度与加速度": "简谐振动：速度、加速度与位移或相位的关系。",
        "周期频率关系": "周期、频率与角频率之间的关系。",
        "弹簧振子周期": "理想弹簧振子振动周期公式。",
        "单摆回复力": "小角度下单摆沿弧切向的回复力与角位移关系。",
        "单摆周期": "小角度单摆周期公式。",
        "水平弹簧振子能量": "弹簧振子：动能与弹性势能之和（守恒式）。",
        "波动通式": "沿 $x$ 轴传播的平面简谐波位移表达式。",
        "任意点振动方程": "已知波动方程写某点的振动方程（令 $x$ 为常数）。",
        "波速波长频率关系": "$v、\\lambda、f、\\omega、k$ 之间的关系。",
        "相位差": "两点在同一时刻的相位之差（与波程差联系）。",
        "相干加强条件": "双缝干涉：光程差为波长的整数倍（对应加强）。",
        "相干减弱条件": "双缝干涉：光程差为半波长奇数倍（对应减弱）。",
        "衍射条件": "明显衍射条件（障碍物或缝宽与波长量级相比）。",
        "驻波条件": "弦上形成驻波：长度与半波长的整数倍关系。",
        "多普勒效应": "波源或观察者运动时观测频率变化公式（写明约定符号）。",
        "电场强度定义": "试探电荷所受电场力与电荷量的比值（矢量）。",
        "点电荷场强": "真空点电荷电场强度大小（库仑定律导出）。",
        "电场叠加": "多个电荷产生的电场强度矢量叠加原理。",
        "匀强电场": "匀强电场强度与沿场强方向电势差、距离关系。",
        "电势定义": "电场中某点电势（相对零势点）的定义式。",
        "电势差定义": "两点间电势差与电场力移送电荷做功关系。",
        "电场力做功": "电场力做功与初末电势差、电荷量关系。",
        "电势能变化": "电场力做功与电势能变化的关系。",
        "匀强电场电势差": "匀强场：沿任意方向的电势差与场强投影、距离关系。",
        "电容定义": "电容器电容：电荷量与两极板电势差之比。",
        "平行板电容器": "真空平行板电容与面积、间距关系。",
        "电容器能量": "电容器储能公式（用电容与电压表示）。",
        "加速电场": "带电粒子经加速电场获得的动能（初速为零时常用形式）。",
        "偏转电场加速度": "偏转板内垂直初速方向的加速度（不计重力）。",
        "偏转位移": "类平抛：穿出偏转板时在偏转方向的位移公式。",
        "电流定义式": "电流：单位时间通过截面的电荷量。",
        "电流微观表达式": "金属导体：电流与载流子数密度、电荷、漂移速率、截面积。",
        "电阻定义式": "欧姆定律：电阻与电压、电流关系。",
        "电阻决定式": "电阻定律：与电阻率、长度、截面积关系。",
        "串联电阻": "串联总电阻。",
        "并联电阻": "并联总电阻（两电阻倒数之和形式亦可）。",
        "电动势": "电源电动势定义（非静电力移送电荷所做功与电荷量之比）。",
        "闭合电路欧姆定律": "全电路电流与电动势、内外阻关系。",
        "路端电压": "路端电压与电流、电动势、内阻关系。",
        "纯电阻功率": "纯电阻电路功率（任选一种常用形式）。",
        "电源总功率": "电源消耗化学能等的功率 $EI$。",
        "电源输出功率": "电源输出到外电路的功率。",
        "电源效率": "输出功率与总功率之比。",
        "电流表改装分流电阻": "扩大量程：并联分流电阻与满偏电流、量程关系。",
        "电压表改装串联电阻": "扩大量程：串联分压电阻关系。",
        "欧姆表回路": "欧姆表：闭合回路欧姆定律形式（含调零电阻模型）。",
        "欧姆表中值电阻": "指针半偏时待测电阻与中值电阻关系。",
        "电桥平衡条件": "惠斯通电桥平衡时四个电阻的比例关系。",
        "磁感应强度": "电流元受力定义式或运动电荷受力给出的 $B$（写出一种）。",
        "安培力": "通电导线在磁场中所受安培力大小（电流与磁场垂直时）。",
        "通电导线受力方向": "左手定则判定安培力方向的表述（文字即可）。",
        "直导线磁场方向": "直线电流磁场方向判定（安培定则）。",
        "螺线管磁场方向": "通电螺线管内部磁场方向判定（安培定则）。",
        "洛伦兹力": "运动电荷在磁场中所受洛伦兹力大小（$v\\perp B$）。",
        "向心力关系": "带电粒子匀速圆周：洛伦兹力提供向心力。",
        "半径": "匀强磁场中圆轨道半径与 $mv、qB$ 关系。",
        "周期": "带电粒子在匀强磁场中圆周运动周期。",
        "运动时间": "转过圆心角 $\\theta$ 时在磁场中运动时间与周期关系。",
        "速度选择器": "电场与磁场平衡时能以直线穿过的速度条件。",
        "选择速度": "速度选择器中选出的速度大小（$E$ 与 $B$ 表示）。",
        "质谱仪半径": "经速度选择后粒子在磁场中的偏转半径公式。",
        "霍尔电压": "霍尔效应：横向电势差与 $I、B、nq、d$ 等关系（模型依题）。",
        "回旋加速器最大速度": "由磁场与 $D$ 形盒半径限制的最大回旋速度。",
        "回旋加速器最大动能": "与最大速度对应的动能。",
        "磁通量": "匀强磁场穿过平面的磁通量定义（面积与法线夹角）。",
        "法拉第电磁感应定律": "感应电动势大小与磁通量变化率关系。",
        "感应电流": "闭合回路欧姆定律：感应电流与感应电动势、电阻。",
        "回路电荷量": "感应过程中通过回路截面的电荷量与磁通变化、电阻关系。",
        "导体棒切割": "棒长 $l$、速度 $v$、磁场 $B$ 互相垂直时的动生电动势。",
        "动生电动势": "同上（单棒模型）。",
        "回路电流": "棒电阻与负载构成回路时的电流。",
        "安培力冲量": "安培力对棒的冲量与电荷量、杆长、磁场关系（常见积分结论）。",
        "感应电流功率": "电路中电功率（或力的功率）与感应电流关系。",
        "恒力最终速度": "棒受恒外力与安培力平衡时的收尾速度。",
        "线圈转动电动势": "线圈在匀强磁场中转动产生的瞬时电动势（从中性面计时）。",
        "最大电动势": "交流发电机峰值电动势。",
        "从中性面计时": "写出从中性面开始计时的电动势瞬时值（正弦形式）。",
        "周期与角速度": "交流电周期与角频率关系。",
        "双棒动量关系": "光滑导轨双棒：安培力等大反向时常用的系统动量守恒式。",
        "双缝干涉条纹间距": "相邻亮纹（或暗纹）间距与波长、缝屏距、缝距关系。",
        "相干加强条件": "光程差为波长的整数倍（写明暗纹则另条件）。",
        "相干减弱条件": "光程差为半波长奇数倍。",
        "光程": "几何路程与折射率乘积。",
        "洛埃德镜条纹间距": "与双缝类似间距公式（注意半波损失对明暗互换）。",
        "薄膜干涉光程差": "近似垂直入射：薄膜反射相干的两束光光程差表达式。",
        "半波损失": "何时附加 $\\lambda/2$ 光程（疏到密反射等表述）。",
        "劈尖厚度": "小劈尖角：膜厚与水平距离、夹角关系。",
        "劈尖条纹间距": "相邻条纹对应的膜厚差与条纹间距公式。",
        "反射定律": "入射角等于反射角（在同一平面内）。",
        "折射定律": "斯涅尔定律：入射角与折射角正弦之比。",
        "折射率定义": "真空光速与介质光速之比。",
        "相对折射率": "两种介质间相对折射率与各自折射率关系。",
        "全反射临界角": "光密到光疏：临界角与折射率关系。",
        "透镜成像公式": "薄透镜成像公式（含符号约定依教材）。",
        "放大率": "像高与物高之比（或像距物距之比依符号约定）。",
        "热力学温度": "摄氏温标与热力学温标换算。",
        "微粒数": "物质的量与阿伏伽德罗常数、微粒数关系。",
        "物质的量": "质量与摩尔质量关系。",
        "单个分子平均占有体积": "固体或液体：摩尔体积与阿伏伽德罗常数。",
        "固体、液体分子直径估算": "球模型：分子直径与摩尔体积关系（数量级估算）。",
        "气体分子平均间距估算": "立方体模型：平均间距与摩尔体积关系。",
        "分子平均动能": "温度与分子平均动能（理想气体）。",
        "分子平均速率": "三种特征速率之一（写明题目常用哪一种）。",
        "等温变化": "玻意耳定律：压强与体积乘积（理想气体）。",
        "等容变化": "查理定律：压强与热力学温度成正比。",
        "等容变化比值形式": "查理定律：初末态压强与温度比值形式。",
        "等压变化": "盖—吕萨克定律：体积与热力学温度成正比。",
        "等压变化比值形式": "盖—吕萨克定律：初末态体积与温度比值形式。",
        "理想气体状态方程": "$pV=nRT$ 或质量形式。",
        "液体上下压强": "静止液体内部压强（深度、密度）。",
        "有质量活塞上下压强": "活塞受力平衡：上下气体压强与活塞重力关系。",
        "水平液柱与活塞压强": "水平柱塞两侧压强传递关系。",
        "竖直液柱加速度": "液柱整体加速：上下压强差与液柱动力学方程。",
        "竖直活塞加速度": "活塞与气体：牛顿第二定律列式后的加速度表达式。",
        "热力学第一定律": "$\\Delta U=Q+W$（注明符号约定：外界对气体做功为正等）。",
        "等容过程": "体积不变：热力学第一定律简化形式。",
        "等压过程气体对外做功": "等压膨胀（或压缩）功与压强、体积变化。",
        "压强线性变化做功": "$p$ 随 $V$ 线性变化时气体做功（平均压强或图像面积）。",
        "等温过程": "理想气体等温：内能变化为零时的吸放热与做功关系。",
        "绝热过程": "$Q=0$：内能变化仅由做功引起（理想气体）。",
        "能量守恒": "封闭系统能量守恒表述（与本节模型对应的式子）。",
        "第一类永动机": "不可能制成的原因（违背能量守恒）。",
        "第二类永动机": "不可能制成的原因（违背热力学第二定律）。",
        "能量子关系": "谐振子能量量子化：相邻能级间隔与频率。",
        "光子频率与波长": "真空中波长与频率关系。",
        "光子能量表达式": "光子能量与频率（普朗克常量）。",
        "振子能量量子化": "普朗克假设：最小能量单元与频率。",
        "峰值波长规律": "黑体辐射：维恩位移定律形式。",
        "黑体辐射规律（定性）": "温度升高：峰值波长向短波移动、总辐射增强等。",
        "光子能量": "光子能量与频率。",
        "光子动量": "光子动量与波长或频率关系。",
        "德布罗意波长": "实物粒子德布罗意波长与动量。",
        "德布罗意关系（非相对论）": "动量与波长的德布罗意关系。",
        "爱因斯坦光电方程": "光子能量、逸出功与最大初动能关系。",
        "最大初动能（电压表示）": "遏止电压与最大初动能关系。",
        "截止频率": "光电效应：截止频率与逸出功。",
        "逸出功（波长表示）": "用极限波长表示逸出功。",
        "最大初动能--频率图像": "$E_k-\\nu$ 图斜率与截距的物理意义对应的公式。",
        "遏止电压--频率图像": "$U_c-\\nu$ 图斜率与截距对应的公式。",
        "卢瑟福散射角判定": "大角度散射说明原子有一小而重的带正电核。",
        "玻尔能级公式（氢原子）": "氢原子能级与量子数 $n$ 的关系。",
        "轨道半径（氢原子）": "玻尔模型：第 $n$ 轨道半径与玻尔半径。",
        "类氢离子轨道半径": "核电荷数为 $Z$ 时轨道半径与氢原子半径关系。",
        "频率条件": "跃迁：辐射或吸收光子频率与两能级差关系。",
        "最大谱线数（从第 $n$ 能级向下）": "一群氢原子从 $n$ 向下跃迁最多发射谱线条数。",
        "衰变规律": "剩余核数随时间指数衰减规律。",
        "半衰期定义": "半数原子核衰变所需时间（统计规律）。",
        "质量亏损": "反应前后质量之差。",
        "质能关系": "质量亏损与释放核能关系。",
        "原子质量单位换算": "$1\\ \\mathrm{u}$ 对应的能量（MeV）。",
        "结合能法放能": "用生成物与反应物结合能之差表示释放核能。",
        "比结合能": "平均每个核子的结合能定义。",
        "反应类型": "表格左栏：反应类型名称（非公式，照抄即可）。",
        "发现质子": "历史上人工转变：发现质子的核反应方程。",
        "发现中子": "查德威克实验：发现中子的核反应方程。",
        "发现正电子": "人工放射性：发现正电子的核反应方程。",
        "$\\alpha$ 衰变": "写出 $\\alpha$ 衰变方程通式或示例。",
        "$\\beta^-$ 衰变本质": "写出中子转化为质子并放出电子的本质方程。",
        "核裂变": "重核裂变典型方程（题给元素）。",
        "核聚变": "轻核聚变典型方程（如氘氚）。",
    }
)

# --- 同条目多处公式：按章节内出现次序（从 0 开始）---
LEFT_HINTS_TRIPLE.update(
    {
        ("section_1.tex", "位移", 0): "匀变速直线运动：位移与时间、初速度、加速度的关系式。",
        ("section_1.tex", "位移", 1): "同一过程：用平均速度表示的位移公式。",
        ("section_3.tex", "向心力", 0): "用线速度写向心力大小（圆周运动）。",
        ("section_3.tex", "向心力", 1): "用向心加速度写向心力（$F=ma_{\\text{向}}$）。",
        ("section_4.tex", "向心力简化式", 0): "圆轨道：由线速度写 $GM=v^2 r$。",
        ("section_4.tex", "向心力简化式", 1): "圆轨道：由角速度写 $GM=\\omega^2 r^3$。",
        ("section_4.tex", "向心力简化式", 2): "圆轨道：由向心加速度写 $GM=a r^2$。",
        ("section_4.tex", "向心力简化式", 3): "圆轨道：由周期写 $GM=4\\pi^2 r^3/T^2$。",
        ("section_5.tex", "重力", 0): "地表附近重力大小（质量与 $g$）。",
        ("section_6.tex", "重力", 0): "动力学中重力大小（与静力学表述一致即可）。",
        ("section_7.tex", "动能定理", 0): "合外力做功等于动能增量（动能定理）。",
        ("section_8.tex", "功", 0): "恒力做功：力、位移及夹角余弦。",
        ("section_25.tex", "干涉加强条件", 0): "两波源起振方向相同：振动加强的波程差条件。",
        ("section_25.tex", "干涉加强条件", 1): "两波源起振方向相反：振动加强的波程差条件。",
        ("section_25.tex", "干涉减弱条件", 0): "两波源起振方向相同：振动减弱条件。",
        ("section_25.tex", "干涉减弱条件", 1): "两波源起振方向相反：振动减弱条件。",
    }
)


def split_tabular_rows(inner: str) -> list[str]:
    rows: list[str] = []
    i = 0
    n = len(inner)
    row_start = 0
    brace = 0
    env_depth = 0
    math_dollar = False

    while i < n:
        if inner.startswith(r"\\", i) and brace == 0 and env_depth == 0 and not math_dollar:
            chunk = inner[row_start:i].strip()
            if chunk:
                rows.append(chunk)
            i += 2
            row_start = i
            continue
        ch = inner[i]
        if ch == "{" and not (i > 0 and inner[i - 1] == "\\"):
            brace += 1
        elif ch == "}" and brace > 0:
            brace -= 1
        elif ch == "$" and not (i > 0 and inner[i - 1] == "\\"):
            math_dollar = not math_dollar
        elif inner.startswith(r"\begin{", i):
            env_depth += 1
            i += len(r"\begin{")
            continue
        elif inner.startswith(r"\end{", i) and env_depth > 0:
            env_depth -= 1
            i += len(r"\end{")
            continue
        i += 1
    tail = inner[row_start:n].strip()
    if tail:
        rows.append(tail)
    return rows


def split_amp(row: str) -> list[str]:
    parts: list[str] = []
    cur: list[str] = []
    brace = 0
    env_depth = 0
    i = 0
    n = len(row)
    while i < n:
        if row.startswith(r"\begin{", i):
            env_depth += 1
            j = row.find("}", i)
            cur.append(row[i : j + 1])
            i = j + 1
            continue
        if row.startswith(r"\end{", i) and env_depth > 0:
            env_depth -= 1
            j = row.find("}", i)
            cur.append(row[i : j + 1])
            i = j + 1
            continue
        ch = row[i]
        if ch == "{":
            brace += 1
        elif ch == "}":
            brace -= 1
        elif ch == "&" and brace == 0 and env_depth == 0:
            parts.append("".join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    parts.append("".join(cur).strip())
    return parts


def looks_like_formula(rhs: str) -> bool:
    if not rhs.strip():
        return False
    if "$" in rhs or r"\(" in rhs or r"\[" in rhs:
        return True
    if re.search(
        r"\\(?:frac|sqrt|sum|int|mathrm|text|ce|Delta|alpha|beta|gamma|omega|mu|pi|cdot|times|pm|mp|infty)\b",
        rhs,
    ):
        return True
    if re.search(r"[=][^，。\s]", rhs) and len(rhs) < 160:
        return True
    return False


def clean_label(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def fix_answer_cell(formula: str) -> str:
    f = formula.strip()
    if "\\begin{aligned}{ll}" in f:
        f = f.replace("\\begin{aligned}{ll}", "\\begin{cases}").replace(
            "\\end{aligned}", "\\end{cases}"
        )
    return f


def strip_leading_hlines(row: str) -> tuple[list[str], str]:
    """返回前置的 \\hline 列表与剩余行内容。"""
    hl: list[str] = []
    r = row.strip()
    while r.startswith(r"\hline"):
        hl.append(r"\hline")
        r = r[len(r"\hline") :].strip()
    return hl, r


def escape_hint_tex(s: str) -> str:
    return s.replace("%", r"\%")


def lookup_left_hint(sec_fn: str, eff_label: str, row_idx: int) -> str | None:
    k3 = (sec_fn, eff_label, row_idx)
    if k3 in LEFT_HINTS_TRIPLE:
        return LEFT_HINTS_TRIPLE[k3]
    k2 = (sec_fn, eff_label)
    if k2 in LEFT_HINTS_PAIR:
        return LEFT_HINTS_PAIR[k2]
    return LEFT_HINTS_SINGLE.get(eff_label)


def format_question_left_cell(left_raw: str, hint: str | None) -> str:
    """仅在填空卷使用：条目 + 小号说明。"""
    if not hint:
        return left_raw
    h = escape_hint_tex(hint)
    base = left_raw.strip()
    if base:
        return f"{base}\\newline {{\\footnotesize {h}}}"
    return f"{{\\footnotesize {h}}}"


def main() -> None:
    sections = section_inputs()
    lines_q: list[str] = []
    lines_a: list[str] = []

    for sec in sections:
        path = ROOT / f"{sec}.tex"
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        search = 0
        while True:
            idx = content.find(r"\begin{tabularx}", search)
            if idx < 0:
                break
            got = extract_tabularx_at(content, idx)
            if not got:
                break
            block, end = got
            search = end

            meta = tabularx_meta(block)
            if meta is None:
                continue
            colspec, inner = meta
            if colspec not in ALLOWED_COLSPECS:
                continue

            lines_q.append(f"% --- {path.name} ---\n")
            lines_a.append(f"% --- {path.name} ---\n")
            lines_q.append(f"\\begin{{tabularx}}{{\\columnwidth}}{{{colspec}}}\n")
            lines_a.append(f"\\begin{{tabularx}}{{\\columnwidth}}{{{colspec}}}\n")

            prev_label = ""
            occ = defaultdict(int)

            for raw_row in split_tabular_rows(inner):
                hlines, row = strip_leading_hlines(raw_row.strip())
                for h in hlines:
                    lines_q.append(f"  {h}\n")
                    lines_a.append(f"  {h}\n")
                if not row:
                    continue

                if "\\multicolumn" in row:
                    lines_q.append(f"  {row} \\\\\n")
                    lines_a.append(f"  {row} \\\\\n")
                    continue

                cells = split_amp(row)
                if len(cells) != 2:
                    lines_q.append(f"  {row} \\\\\n")
                    lines_a.append(f"  {row} \\\\\n")
                    continue

                left_raw, right_raw = cells[0], cells[1]
                left_key = clean_label(left_raw)
                eff_label = left_key if left_key else prev_label
                if left_key:
                    prev_label = left_key

                if looks_like_formula(right_raw):
                    if eff_label in SKIP_LABELS:
                        continue
                    sec_fn = path.name
                    ri = occ[(sec_fn, eff_label)]
                    occ[(sec_fn, eff_label)] = ri + 1
                    hint = lookup_left_hint(sec_fn, eff_label, ri)
                    left_q = format_question_left_cell(left_raw, hint)
                    lines_q.append(f"  {left_q} & \\\\\n")
                    lines_a.append(
                        f"  {left_raw} & {fix_answer_cell(right_raw)} \\\\\n"
                    )
                else:
                    lines_q.append(f"  {left_raw} & {right_raw} \\\\\n")
                    lines_a.append(f"  {left_raw} & {right_raw} \\\\\n")

            lines_q.append("\\end{tabularx}\n\\medskip\n\n")
            lines_a.append("\\end{tabularx}\n\\medskip\n\n")

    OUT_Q.write_text("".join(lines_q), encoding="utf-8")
    OUT_A.write_text("".join(lines_a), encoding="utf-8")
    print(f"Wrote {OUT_Q.name} and {OUT_A.name}")


if __name__ == "__main__":
    main()
