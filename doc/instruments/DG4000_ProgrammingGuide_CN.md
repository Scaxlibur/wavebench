**RIGOL**

**编程手册**


**DG4000系列函数/任意波形发生器** 


本手册用于指导用户使用SCPI命令通过远程接口（USB或LAN）编程控制**RIGOL** DG4000系列函数/任意波形发生器。


**本手册主要内容：**


SCPI简介

命令系统

编程实例

命令速查


**软件版本：**

00\.01.12

软件升级可能更改或增加产品功能，请关注**RIGOL**网站获取最新版本手册或联系**RIGOL**升级软件。


**声明：**


本公司产品受中国及其它国家和地区的专利（包括已取得的和正在申请的专利）保护。

本公司保留改变规格及价格的权利。

本手册提供的信息取代以往出版的所有资料。

本手册提供的信息如有变更，恕不另行通知。

对于本手册可能包含的错误，或因手册所提供的信息及演绎的功能，以及因使用本手册而导致的任何偶然或继发的损失，**RIGOL**概不负责。

未经**RIGOL**事先书面许可，不得影印、复制或改编本手册的任何部分。


如您在使用此产品或本手册的过程中有任何问题或需求，可与**RIGOL**联系：

电子邮箱：service@rigol.com

网址：[www.rigol.com](http://www.rigol.com/)


©2011 北京普源精电科技有限公司版权所有。


2015年08月       文档编号：PGB04008-1110
## **SCPI简介**


SCPI (Standard Commands for Programmable Instrument) 是IEEE 488.2上的可程控仪器标准指令集。


本章内容包括：


命令格式

符号说明

参数类型

命令缩写
### **命令格式**


SCPI命令为树状层次结构，包括多个子系统，每个子系统由一个根关键字和一个或数个层次关键字构成。命令行通常以冒号“**:**”开始；关键字之间用冒号“**:**”分隔，关键字后面跟随可选的参数设置；命令行后面添加问号“**?**”，表示查询；命令和参数以“空格”分开。


例如：

```
:COUPling:AMPL:DEViation <deviation>
:COUPling:AMPL:DEViation?
```


COUPling是命令的根关键字，AMPL和DEViation分别是第二级和第 三级关键字。命令行以冒号“**:**”开始，同时将各级关键字分开，<deviation>表示可设置的参数；问号“**?**”表示查询；命令:COUPling:AMPL:DEViation和参数<deviation>之间用“空格”分开。


在一些带参数的命令中，通常用逗号“**,**”分隔多个参数，例如：

```
:MMEMory:COPY <directory_name>,<file_name>
```
### **符号说明**


下面四种符号不是SCPI命令中的内容，不随命令发送，但是通常用于辅助说明命令中的参数。


**大括号 { }**

大括号中的参数是可选项，可以不设置，也可以设置一次或多次。例如：

[:TRACe]:DATA[:DATA] VOLATILE,<value>{,<value>}命令中，{,<value>}中的浮点电压值可以省略，也可以设置一个或多个电压值。


**竖线 |**

竖线用于分隔多个参数选项，发送命令时必须选择其中一个参数。例如：

:DISPlay:SAVer[:STATe] ON|OFF命令中，可选择的命令参数为“ON”或“OFF”。


**三角括号 < >**

三角括号中的参数必须用一个有效值来替换。例如：

以:DISPlay:BRIGhtness 10的形式发送:DISPlay:BRIGhtness <brightness>|MINimum|MAXimum命令 。


**方括号 [ ]**

方括号中的内容（参数或关键字）是可省略的。如果省略参数，仪器将该参数设置为默认值。例如：

对于[:SOURce<n>]:MOD[:STATe]?命令，

发送下面四条命令的效果是一样的：

```
:MOD?
```

```
:MOD:STATe?
```

```
:SOURce1:MOD?
```

```
:SOURce1:MOD:STATe?
```


### **参数类型**


本手册介绍的命令中所含的参数可以分为以下6种类型：布尔、关键字、整型、连续实型、离散、ASCII字符串。


**布尔**

参数取值为“ON”或“OFF”。例如：

```
:DISPlay:SAVer[:STATe] ON|OFF
```


**关键字**

参数取值为所列举的值。例如：

[:SOURce<n>]:BURSt:GATE:POLarity NORMal|INVerted 

参数为“NORMal”或“INVerted”。


**整型**

除非另有说明，参数在有效值范围内可以取任意整数值。注意，此时请不要设置参数为小数格式，否则将出现异常。例如：

```
:OUTPut[<n>]:LOAD <ohms>|INFinity|MINimum|MAXimum
```

参数<ohms>可取1到10000范围内的任一整数。

**连续实型**

参数在有效值范围内按精度要求（通常默认精度为小数点以后取六位有效值），可以任意进行取值。例如：

[:SOURce<n>]:MOD:AM[:DEPTh] <depth>|MINimum|MAXimum 

参数<depth>可设置为0至120之间的任意实数。

**离散**

参数只能取指定的数值，并且这些数值不是连续的。例如：

[:SOURce<n>]:MOD[:STATe] ON|OFF 

参数<n>只能取1或2。

**ASCII字符串**

参数取值为ASCII字符的组合。例如：

```
:MMEMory:MDIRectory <dir_name>
```

参数<dir\_name>为字符串形式。


**说明：**在DG4000命令系统中，部分命令带有MAXimum和MINimum参数。例如：

[:SOURce<n>]:MOD:ASKey:AMPLitude <amplitude>|MINimum|MAXimum 
[:SOURce<n>]:MOD:ASKey:AMPLitude? [MINimum|MAXimum
1\. 设置命令以MAXimum为参数表示以最大值设置指定的信号源参数；

2\. 设置命令以MINimum为参数表示以最小值设置指定的信号源参数；

3\. 查询命令以MAXimum为参数表示查询指定的信号源参数的最大值；

4\. 查询命令以MINimum为参数表示查询指定的信号源参数的最小值。
## **命令缩写**


所有命令对大小写不敏感，你可以全部采用大写或小写。但是如果要缩写，必须输完命令格式中的所有大写字母，例如：


```
:SYSTem:COMMunicate:USB:INFormation?
```


可缩写成：


```
:SYST:COMM:USB:INF?
```

**命令系统**


本章按照字母A-Z顺序分别介绍DG4000系列命令系统。

COUNter命令子系统

COUPling命令子系统

DISPlay命令子系统

```
:HCOPy:SDUMp:DATA?
```

IEEE 488.2公用命令

MEMory命令子系统

MMEMory命令子系统

OUTPut命令子系统

PA命令子系统

SOURce命令子系统

SYSTem命令子系统

TRACe命令子系统


**说明：**本命令集中，涉及频率、幅度等参数设置的命令，允许带单位发送命令。各参数支持的单位及缺省单位如下表所示：


|**参数**|**支持单位**|**缺省单位**|
| :-: | :-: | :-: |
|频率|MHZ/KHZ/HZ/UHZ|HZ|
|幅度|VPP/MVPP/VRMS/MVRMS/DBM|VPP/VRMS/DBM（取决于当前被设置参数）|
|偏移/高电平/低电平|V/MV|V|
|时间|MS/KS/S/US/NS|S|
|相位|°|°|
|占空比/调制深度等|%|%|


● MHZ等同于mHz。

● MVPP等同于mVpp、MVRMS等同于mVrms、MV等同于mV。

● MS等同于ms。

**注意：**对于命令中参数范围的说明，本手册以DG4162型号为例。
## **COUNter命令子系统**


```
:COUNter:ATTenuation 1X|10X
:COUNter:ATTenuation?
```

```
:COUNter:AUTO
```

```
:COUNter:COUPing AC|DC
:COUNter:COUPing?
```

```
:COUNter:GATEtime AUTO|USER1|USER2|USER3|USER4|USER5|USER6
:COUNter:GATEtime?
```

```
:COUNter:HF ON|OFF
```

```
:COUNter:HF?
```

```
:COUNter:IMPedance 50|1M
:COUNter:IMPedance?
```

```
:COUNter:LEVE <value>|MINimum|MAXimum
:COUNter:LEVE? [MINimum|MAXimum]
:COUNter:MEASure?
:COUNter:SENSitive <value>|MINimum|MAXimum
:COUNter:SENSitive? [MINimum|MAXimum]
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
:COUNter:STATIstics:CLEAr
:COUNter:STATIstics:DISPlay DIGITAL|CURVE
:COUNter:STATIstics:DISPlay?
```

```
:COUNter:STATIstics[:STATe] ON|OFF
:COUNter:STATIstics[:STATe]?
```

**:COUNter:ATTenuation**


**命令格式**


```
:COUNter:ATTenuation 1X|10X
:COUNter:ATTenuation?
```


**功能描述**


设置频率计的衰减系数为X1或X10。

查询频率计的衰减系数。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|1X|10X |1X|


**返回格式**


返回1X或10X。


**举例**


下面的命令设置衰减系数为X10：

```
:COUNter:ATTenuation 10X
```


下面的查询返回10X。

```
:COUNter:ATTenuation?
```


**相关命令**


```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```


**:COUNter:AUTO**


**命令格式**


```
:COUNter:AUTO
```


**功能描述**


发送该命令，仪器自动设置频率计的闸门时间。


**说明**


该命令仅当频率计功能打开时可用。

该命令与命令:COUNter:GATEtime AUTO功能相同。


**举例**


下面的命令自动设置频率计的闸门时间：

```
:COUNter:AUTO
```


**相关命令**


```
:COUNter:GATEtime AUTO|USER1|USER2|USER3|USER4|USER5|USER6
:COUNter:GATEtime?
```

```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```

**:COUNter:COUPing**


**命令格式**


```
:COUNter:COUPing AC|DC
:COUNter:COUPing?
```


**功能描述**


设置频率计的耦合类型为AC或DC。

查询频率计的耦合类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|AC|DC  |AC|


**返回格式**


返回AC或DC。


**举例**


下面的命令设置耦合类型为DC：

```
:COUNter:COUPing DC
```


下面的查询返回DC。

```
:COUNter:COUPing?
```


**相关命令**


```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```


**:COUNter:GATEtime**


**命令格式**


```
:COUNter:GATEtime AUTO|USER1|USER2|USER3|USER4|USER5|USER6
:COUNter:GATEtime?
```


**功能描述**


设置频率计的闸门时间。

查询频率计的闸门时间。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|AUTO|USER1|USER2|USER3|USER4|USER5|USER6|USER1|


**说明**


各参数对应的闸门时间值如下表所示：

|AUTO|AUTO|
| :-: | :-: |
|USER1|1 ms|
|USER2|10 ms|
|USER3|100 ms|
|USER4|1 s|
|USER5|10 s|
|USER6|>10 s|


**返回格式**


查询返回AUTO、USER1、USER2、USER3、USER4、USER5或USER6。


**举例**


下面的命令设置频率计的闸门时间为10 ms：

```
:COUNter:GATEtime USER2
```


下面的查询返回USER2。

```
:COUNter:GATEtime?
```


**相关命令**


```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```

```
:COUNter:AUTO
```


**:COUNter:HF**


**命令格式**


```
:COUNter:HF ON|OFF
```

```
:COUNter:HF?
```


**功能描述**


打开或关闭频率计的高频抑制功能。

查询频率计的高频抑制是否打开。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**返回格式**


查询返回ON或OFF。


**举例**


下面的命令打开频率计的高频抑制功能：

```
:COUNter:HF ON
```


下面的查询返回ON。

```
:COUNter:HF?
```


**相关命令**


```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```

**:COUNter:IMPedance** 


**命令格式**


```
:COUNter:IMPedance 50|1M
:COUNter:IMPedance?
```


**功能描述**


设置频率计的输入阻抗为50 Ω或1 MΩ。

查询频率计的输入阻抗。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|离散型|50 Ω|1 MΩ |1 MΩ|


**返回格式**


返回50或1M。


**举例**


下面的命令设置输入阻抗为50 Ω：

```
:COUNter:IMPedance 50
```


下面的查询返回50。

```
:COUNter:IMPedance?
```


**相关命令**


```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```


**:COUNter:LEVE** 


**命令格式**


```
:COUNter:LEVE <value>|MINimum|MAXimum
:COUNter:LEVE? [MINimum|MAXimum]
```
**功能描述**


设置频率计的触发电平。

查询频率计的触发电平。


**参数**

|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<value>|连续实型|-2.5 V至2.5 V|0 V|


**返回格式**


查询以科学计数形式返回触发电平。


**举例**


下面的命令设置触发电平为2 V：

```
:COUNter:LEVE 2
```


下面的查询返回2.000000E+00。

```
:COUNter:LEVE?
```


**相关命令**


```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```


**:COUNter:MEASure**


**命令格式**


```
:COUNter:MEASure?
```


**功能描述**


查询频率计当前的测量结果。


**返回格式**


以“频率,周期,占空比,正脉宽,负脉宽”形式返回各参数的测量结果，其中，每个参数以科学计数形式表示。


**举例**


下面的查询返回1.000099993E+03,9.999000134E-04,1.422600068E+01,1.422537019E-04,8.576463115E-04：

```
:COUNter:MEASure?
```


**相关命令**


```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```

**:COUNter:SENSitive**


**命令格式**


```
:COUNter:SENSitive <value>|MINimum|MAXimum
:COUNter:SENSitive? [MINimum|MAXimum]
```
**功能描述**


设置频率计的触发灵敏度。

查询频率计的触发灵敏度。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<value>|连续实型|0%至100%|50%|


**返回格式**


查询以科学计数形式返回触发灵敏度。


**举例**


下面的命令设置触发灵敏度为60%：

```
:COUNter:SENSitive 60
```


下面的查询返回6.000000E+01。

```
:COUNter:SENSitive?
```


**相关命令**


```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```


**:COUNter[:STATe]**


**命令格式**


```
:COUNter[:STATe] ON|OFF
```

```
:COUNter[:STATe]?
```


**功能描述**


打开或关闭频率计功能。

查询频率计功能的状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**返回格式**


返回ON（频率计开启时）或OFF（频率计关闭时）。


**举例**


下面的命令开启频率计功能：

```
:COUNter:STATe ON
```


下面的查询返回ON。

```
:COUNter:STATe?
```


**:COUNter:STATIstics:CLEAr** 


**命令格式**


```
:COUNter:STATIstics:CLEAr
```


**功能描述**


清除当前的统计结果。


**说明**


该命令仅在统计功能打开时可用（请使用:COUNter:STATIstics[:STATe] ON|OFF打开统计功能）。


**相关命令**


```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```

```
:COUNter:STATIstics[:STATe] ON|OFF
:COUNter:STATIstics[:STATe]?
```

**:COUNter:STATIstics:DISPlay**


**命令格式**


```
:COUNter:STATIstics:DISPlay DIGITAL|CURVE
:COUNter:STATIstics:DISPlay?
```


**功能描述**


选择频率计测量结果统计功能的显示类型为数字（DIGITAL）或动态曲线 （CURVE）。

查询频率计测量结果统计功能的显示类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|DIGITAL|CURVE|DIGITAL|


**返回格式**


查询返回DIGITAL或CURVE。


**举例**


下面的命令选择统计功能的显示形式为动态曲线：

```
:COUNter:STATIstics:DISPlay CURVE
```


下面的查询返回CURVE。

```
:COUNter:STATIstics:DISPlay?
```


**相关命令**


```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```

```
:COUNter:STATIstics[:STATe] ON|OFF
:COUNter:STATIstics[:STATe]?
```


**:COUNter:STATIstics[:STATe]**


**命令格式**


```
:COUNter:STATIstics[:STATe] ON|OFF
:COUNter:STATIstics[:STATe]?
```


**功能描述**


打开或关闭频率计的测量结果统计功能。

查询频率计测量结果统计功能的开关状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**返回格式**


查询返回ON或OFF。


**举例**


下面的命令打开频率计的测量结果统计功能：

```
:COUNter:STATIstics:STATe ON
```


下面的查询返回ON。

```
:COUNter:STATIstics:STATe?
```


**相关命令**


```
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
```
## **COUPling命令子系统**


```
:COUPling:AMPL:DEViation <deviation>
:COUPling:AMPL:DEViation?
```

```
:COUPling:AMPL[:STATe] ON|OFF
:COUPling:AMPL[:STATe]?
```

```
:COUPling:CHannel:BASE CH1|CH2
:COUPling:CHannel:BASE?
```

```
:COUPling:FREQuency:DEViation <deviation>
:COUPling:FREQuency:DEViation?
:COUPling:FREQuency[:STATe] ON|OFF
:COUPling:FREQuency[:STATe]?
```

```
:COUPling:PHASe:DEViation <deviation>
:COUPling:PHASe:DEViation?
:COUPling:PHASe[:STATe] ON|OFF
:COUPling:PHASe[:STATe]?
```

```
:COUPling[:STATe] ON|OFF
:COUPling[:STATe]?
```


**:COUPling:AMPL:DEViation**


**命令格式**


```
:COUPling:AMPL:DEViation <deviation>
:COUPling:AMPL:DEViation?
```


**功能描述**


设置幅度耦合的幅度差。

查询幅度差值。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<deviation>|连续实型|0 Vpp至20 Vpp|0 Vpp|


**返回格式**


查询以科学计数形式返回当前的幅度差。


**举例**


下面的命令将 幅度差设置为500 mVpp：

:COUPling:AMPL:DEViation 0.5


下面的查询返回5.000000E-01。

```
:COUPling:AMPL:DEViation?
```


**相关命令**


```
:COUPling[:STATe] ON|OFF
:COUPling[:STATe]?
```

```
:COUPling:AMPL[:STATe] ON|OFF
:COUPling:AMPL[:STATe]?
```


**:COUPling:AMPL[:STATe]**


**命令格式**


```
:COUPling:AMPL[:STATe] ON|OFF
:COUPling:AMPL[:STATe]?
```


**功能描述**


打开或关闭幅度耦合功能。

查询幅度耦合功能的开关状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**说明**


您也可以使用:COUPling[:STATe] ON|OFF 命令同时打开或关闭频率耦合、相位耦合和幅度耦合功能 。


**返回格式**


查询返回ON或OFF。


**举例**


下面的命令打开幅度耦合：

```
:COUPling:AMPL:STATe ON
```


下面的查询返回ON。

```
:COUPling:AMPL:STATe?
```


**相关命令**


```
:COUPling[:STATe] ON|OFF
:COUPling[:STATe]?
```

```
:COUPling:AMPL:DEViation <deviation>
:COUPling:AMPL:DEViation?
```

**:COUPling:CHannel:BASE**


**命令格式**


```
:COUPling:CHannel:BASE CH1|CH2
```

```
:COUPling:CHannel:BASE?
```


**功能描述**


设置耦合基准通道为CH1或CH2。

查询当前的耦合基准通道。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|CH1|CH2|CH1|


**说明**


1\. 该命令仅在耦合功能关闭时有效(请使用:COUPling[:STATe] ON|OFF** 命令关闭耦合功能)。

2\. 当频率、相位或幅度耦合功能打开时，在耦合基准通道的频率、相位和幅度左侧会对应显示一个绿色“\*”标记。


**返回格式**


查询返回CH1或CH2。


**举例**


下面的命令将耦合基准通道设置为CH2：

```
:COUPling:CHannel:BASE CH2
```


下面的查询返回CH2。

```
:COUPling:CHannel:BASE?
```


**相关命令**


```
:COUPling[:STATe] ON|OFF
:COUPling[:STATe]?
```

**:COUPling:FREQuency:DEViation**


**命令格式**


```
:COUPling:FREQuency:DEViation <deviation>
```

```
:COUPling:FREQuency:DEViation?
```


**功能描述**


设置频率耦合的频率差。

查询频率差值。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<deviation>|连续实型|0 μHz至160 MHz|0 μHz|


**返回格式**


查询以科学计数形式返回当前的频率差。


**举例**


下面的命令将频率差设置为100 Hz：

```
:COUPling:FREQuency:DEViation 100
```


下面的查询返回1.000000E+02。

```
:COUPling:FREQuency:DEViation?
```


**相关命令**


```
:COUPling[:STATe] ON|OFF
:COUPling[:STATe]?
```

```
:COUPling:FREQuency[:STATe] ON|OFF
:COUPling:FREQuency[:STATe]?
```


**:COUPling:FREQuency[:STATe]**


**命令格式**


```
:COUPling:FREQuency[:STATe] ON|OFF
:COUPling:FREQuency[:STATe]?
```


**功能描述**


打开或关闭频率耦合功能。

查询频率耦合功能的开关状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**说明**


您也可以使用:COUPling[:STATe] ON|OFF 命令同时打开或关闭频率耦合、相位耦合和幅度耦合功能 。


**返回格式**


查询返回ON或OFF。


**举例**


下面的命令打开 频率耦合：

```
:COUPling:FREQuency:STATe ON
```


下面的查询返回ON。

```
:COUPling:FREQuency:STATe?
```


**相关命令**


```
:COUPling[:STATe] ON|OFF
:COUPling[:STATe]?
```

```
:COUPling:FREQuency:DEViation <deviation>
:COUPling:FREQuency:DEViation?
```

**:COUPling:PHASe:DEViation**


**命令格式**


```
:COUPling:PHASe:DEViation <deviation>
```

```
:COUPling:PHASe:DEViation?
```


**功能描述**


设置相位耦合的相位差。

查询相位差值。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<deviation>|连续实型|0°至360°|0°|


**返回格式**


查询以科学计数形式返回当前的相位差。


**举例**


下面的命令将相位差设置为10°：

```
:COUPling:PHASe:DEViation 10
```


下面的查询返回1.000000E+01。

```
:COUPling:PHASe:DEViation?
```


**相关命令**


```
:COUPling[:STATe] ON|OFF
:COUPling[:STATe]?
```

```
:COUPling:PHASe[:STATe] ON|OFF
:COUPling:PHASe[:STATe]?
```


**:COUPling:PHASe[:STATe]**


**命令格式**


```
:COUPling:PHASe[:STATe] ON|OFF
:COUPling:PHASe[:STATe]?
```


**功能描述**


打开或关闭相位耦合功能。

查询相位耦合功能的开关状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**说明**


您也可以使用:COUPling[:STATe] ON|OFF 命令同时打开或关闭频率耦合、相位耦合和幅度耦合功能 。


**返回格式**


查询返回ON或OFF。


**举例**


下面的命令打开相位耦合：

```
:COUPling:PHASe:STATe ON
```


下面的查询返回ON。

```
:COUPling:PHASe:STATe?
```


**相关命令**


```
:COUPling[:STATe] ON|OFF
:COUPling[:STATe]?
```

```
:COUPling:PHASe:DEViation <deviation>
:COUPling:PHASe:DEViation?
```

     **:COUPling[:STATe]**


`    `**命令格式**


```
:COUPling[:STATe] ON|OFF
```

```
:COUPling[:STATe]?
```


**功能描述**


打开或关闭通道的频率耦合、相位耦合和幅度耦合功能。

查询返回三种耦合功能的开关状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**说明**


您也可以使用对应的命令分别打开或关闭频率耦合 、相位耦合和幅度耦合功能（见本页相关命令）。


**返回格式**


查询返回三种耦合功能的开关状态，格式为FREQ:OFF,PHASE:OFF,AMPL:OFF。


**举例**


下面的命令开启三种耦合功能：

```
:COUPling:STATe ON
```


下面的查询返回FREQ:ON,PHASE:ON,AMPL:ON。

```
:COUPling:STATe?
```


**相关命令**


```
:COUPling:AMPL[:STATe] ON|OFF
:COUPling:AMPL[:STATe]?
```

```
:COUPling:FREQuency[:STATe] ON|OFF
:COUPling:FREQuency[:STATe]?
```

```
:COUPling:PHASe[:STATe] ON|OFF
:COUPling:PHASe[:STATe]?
```


## **DISPlay命令子系统**


```
:DISPlay:BRIGhtness <brightness>|MINimum|MAXimum
:DISPlay:BRIGhtness? [MINimum|MAXimum]
:DISPlay:SAVer:IMMediate
:DISPlay:SAVer[:STATe] ON|OFF
:DISPlay:SAVer[:STATe]?
```


**:DISPlay:BRIGhtness**

**命令格式**


```
:DISPlay:BRIGhtness <brightness>|MINimum|MAXimum
```

```
:DISPlay:BRIGhtness? [MINimum|MAXimum]
```
**功能描述**


设置屏幕亮度。

查询亮度设置。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<brightness>|离散型|1%至100%|50%|


**说明**


该设置保存在非易失性存储器中，不受恢复出厂值（\*RST）的影响。


**返回格式**


以百分比的形式返回当前亮度设置。


**举例**


下面的命令设置亮度为80%：

```
:DISPlay:BRIGhtness 80
```


下面的查询返回80%。

```
:DISPlay:BRIGhtness?
```

**:DISPlay:SAVer:IMMediate**


**命令格式**


```
:DISPlay:SAVer:IMMediate
```


**功能描述**


立即进入屏幕保护状态。


**举例**


发送下面的命令，仪器立即进入屏幕保护状态：

```
:DISPlay:SAVer:IMMediate
```


**相关命令**


```
:DISPlay:SAVer[:STATe] ON|OFF
:DISPlay:SAVer[:STATe]?
```

**:DISPlay:SAVer[:STATe]**


**命令格式**


```
:DISPlay:SAVer[:STATe] ON|OFF
```

```
:DISPlay:SAVer[:STATe]?
```


**功能描述**


启用或禁用屏幕保护模式。

查询屏幕保护的状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|ON|


**说明**


启用屏幕保护功能时，若停止操作仪器满15分钟，仪器自动进入屏幕保护状态。


**返回格式**


查询返回ON或OFF。


**举例**


下面的命令打开屏幕保护功能：

```
:DISPlay:SAVer:STATe ON
```


下面的查询返回ON。

```
:DISPlay:SAVer:STATe?
```


**相关命令**


```
:DISPlay:SAVer:IMMediate
```

**:HCOPy:SDUMp:DATA?** 


**命令格式**


```
:HCOPy:SDUMp:DATA?
```


**功能描述**


查询前面板显示屏图像（屏幕截图）。


**返回格式**


返回一个确定长度的二进制数据块，该数据块包含图像，且以#开头，如#9001152054BM6......，其中，“#”后的“9”表示“9”后面的9个字符（001152054）用来表示数据长度。


## **IEEE 488.2公用命令**


*IDN?

*RCL USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10 

*RST

*SAV USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10

*TRG


*IDN?**


**命令格式**


\*IDN?


**功能描述**


查询仪器的ID字符串。


**返回格式**


以字符串形式返回厂商、型号、序列号和版本号，各信息以逗号分隔。


**举例**


下面的命令查询仪器的ID，返回Rigol Technologies,DG4162,DG41620000,00.01.02。

\*IDN? 


*RCL**


**命令格式** 


\*RCL USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10


**功能描述**


调用非易失存储器中指定存储位置的状态文件。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10|USER1|


**说明**


该命令仅在指定的存储位置已经存在数据时有效。

该命令仅将指定存储位置的文件读取至仪器。


**举例**


下面的命令读取USER2中的状态文件：

\*RCL USER2 


**相关命令**


*SAV USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10

*RST**


**命令格式** 


\*RST


**功能描述**


将仪器恢复到出厂默认状态。

*SAV**


**命令格式** 


\*SAV USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10


**功能描述**


将当前的仪器状态保存到非易失存储器的指定存储位置。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10|USER1|


**说明**


若指定的存储位置已经存在数据，当前的仪器状态直接覆盖原数据，仪器不会给出提示信息。


**举例**


下面的命令将当前的仪器状态保存至USER2：

\*SAV USER2 


**相关命令**


*RCL USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10

*TRG**


**命令格式** 


\*TRG


**功能描述**


触发仪器产生一次输出。


**说明**


该命令仅在Sweep或Burst打开（参考[:SOURce<n>]:SWEep:STATe ON|OFF 或[:SOURce<n>]:BURSt[:STATe] ON|OFF 命令）且触发源为手动时有效（参考[:SOURce<n>]:SWEep:TRIGger:SOURce INTernal|EXTernal|MANual 或[:SOURce<n>]:BURSt:TRIGger:SOURce INTernal|EXTernal|MANual 命令）。


**相关命令**


[:SOURce<n>]:SWEep:STATe ON|OFF 
[:SOURce<n>]:SWEep:TRIGger:SOURce INTernal|EXTernal|MANual 
[:SOURce<n>]:BURSt[:STATe] ON|OFF 
[:SOURce<n>]:BURSt:TRIGger:SOURce INTernal|EXTernal|MANual 

**MEMory命令子系统**


```
:MEMory:STATe:DELete USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```

```
:MEMory:STATe:LOCK USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10,ON|OFF
:MEMory:STATe:LOCK? USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```

```
:MEMory:STATe:VALid? USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```


**:MEMory:STATe:DELete**


**命令格式**


```
:MEMory:STATe:DELete USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```


**功能描述**


删除指定存储位置的状态文件。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10|USER1|


**说明**


该命令仅当指定存储位置已存储有效的状态文件时有效。


**相关命令**


```
:MEMory:STATe:VALid? USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```

**:MEMory:STATe:LOCK** 


**命令格式**


```
:MEMory:STATe:LOCK USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10,ON|OFF
:MEMory:STATe:LOCK? USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```


**功能描述**


锁定或解锁指定存储位置的文件。

查询指定存储位置的文件是否锁定。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10|USER1|
|——|布尔型|ON|OFF|OFF|


**说明**


指定位置的文件被锁定，表示该文件为只读文件。用户不可修改、重命名该文件，也不可重新在指定存储位置保存其它文件。


**返回格式**


返回ON或OFF。


**举例**


下面的命令将USER2的存储文件锁定：

```
:MEMory:STATe:LOCK USER2,ON
```


下面的查询返回ON。

```
:MEMory:STATe:LOCK? USER2
```

**:MEMory:STATe:VALid?**


**命令格式**


```
:MEMory:STATe:VALid? USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```


**功能描述**


查询指定的存储位置是否已存储有效的状态文件。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10|USER1|


**返回格式**


返回1（有效）或0（无效）。


**举例**


下面的查询返回1。

```
:MEMory:STATe:VALid? USER1
```
## **MMEMory命令子系统**


```
:MMEMory:CATalog?
:MMEMory:CDIRectory <directory_name>
:MMEMory:CDIRectory?
:MMEMory:COPY <directory_name>,<file_name>
```

```
:MMEMory:DELete <file_name>
:MMEMory:LOAD <file_name>
:MMEMory:MDIRectory <dir_name>
```

```
:MMEMory:RDIRectory?
:MMEMory:STORe <file_name>
```

"

**注意：**MMEMory命令子系统仅适用于外部存储器。若DG4000当前未连接U盘，发送MMEMory命令子系统任一命令时，仪器将提示“远程命令错误”。

**:MMEMory:CATalog?**


**命令格式**


```
:MMEMory:CATalog?
```


**功能描述**


查询当前路径下所有文件和文件夹。


**说明**


该命令仅适用于外部存储器。


**返回格式**


格式：{已用空间,剩余空间,"大小,属性,名称"…}。其中，已用空间和剩余空间单位为“Byte”。文件属性显示为空，文件夹属性显示为DIR。例如：

196608,1073004544,"4000,,000.RAF","1364,,3333.RSF","1364,,2222.RSF","1365,DIR,ABCD" 


**:MMEMory:CDIRectory**


**命令格式**


:MMEMory:CDIRectory <directory\_name>

```
:MMEMory:CDIRectory?
```


**功能描述**


将当前路径修改为<directory\_name>指定的路径。

查询以字符串形式返回当前路径。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<directory\_name>|ASCII字符|带双引号的字符串，长度限制在300个字符内|——|


**说明**


该命令 仅适用于外部存储器。若所设置的路径不存在，则提示“远程命令错误”。


**返回格式**


以带双引号的字符串返回当前路径。


**举例**


下面的命令设置当前路径为D:\rigol：

:MMEMory:CDIRectory "D:\rigol" 


下面的查询返回"D:\rigol"。

```
:MMEMory:CDIRectory?
```

**:MMEMory:COPY**


**命令格式**


:MMEMory:COPY <directory\_name>,<file\_name>


**功能描述**


将当前路径下由<file\_name>指定的文件复制到<directory\_name>指定的路径（非当前路径）下。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<directory\_name>|ASCII字符|带双引号的字符串，长度限制在300个字符内|——|
|<file\_name>|ASCII字符|带双引号的字符串（包含后缀），长度限制在40字符内|——|


**说明**


该命令仅适用于外部存储器。

<file\_name>指定的文件必须为当前路径下的文件（可使用:MMEMory:CDIRectory <directory_name> 命令修改当前路径）。

若<file\_name>指定的文件或<directory\_name>指定的路径不存在，则提示“远程命令错误”。


**举例**


下面的命令将当前路径下的rigol1.RAF文件复制到路径D:\rigol之下。

:MMEMory:COPY "D:\rigol","rigol1.RAF" 

**:MMEMory:DELete**


**命令格式**


:MMEMory:DELete <file\_name>


**功能描述**


删除当前路径下由<file\_name>指定的文件或文件夹。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<file\_name>|ASCII字符|带双引号的字符串（包含后缀），长度限制在40字符内|——|


**说明**


该命令仅适用于外部存储器。若<file\_name>指定的文件不存在，则提示“远程命令错误”。


**举例**


下面的命令删除当前路径下文件名为rigol1.RAF的文件。

:MMEMory:DELete "rigol1.RAF"

**:MMEMory:LOAD**


**命令格式**


:MMEMory:LOAD <file\_name>


**功能描述**


加载当前路径下由<file\_name>指定的文件。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<file\_name>|ASCII字符|带双引号的字符串（包含后缀），长度限制在40字符内|——|


**说明**


该命令仅适用于外部存储器。

若<file\_name>指定的文件不存在，则提示“远程命令错误”。

可加载文件类型：状态文件（.RSF） 和任意波文件（.RAF）。

任意波文件被加载到当前通道。


**举例**


下面的命令加载当前路径下文件名为rigol1.RAF的文件。

:MMEMory:LOAD "rigol1.RAF"

**:MMEMory:MDIRectory**


**命令格式**


:MMEMory:MDIRectory <dir\_name>


**功能描述**


在当前路径下以<dir\_name>指定的文件名创建一个文件夹。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<dir\_name>|ASCII字符|带双引号的字符串，长度限制在40个字符内|——|


**说明**


该命令仅适用于外部存储器。若指定文件名已存在，提示“远程命令错误”。


**举例**


下面的命令在当前路径下创建一个以rigol1命名的文件夹：

:MMEMory:MDIRectory "rigol1" 


**:MMEMory:RDIRectory?**


**命令格式**


```
:MMEMory:RDIRectory?
```


**功能描述**


查询当前可用盘符（不适用于C盘）。


**说明**


该命令仅适用于外部存储器。


**返回格式**


格式："1,"D:""（当前已插入U盘）。

**:MMEMory:STORe**


**命令格式**


:MMEMory:STORe <file\_name>


**功能描述**


以<file\_name>指定的文件名将文件存储到当前路径下。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<file\_name>|ASCII字符|带双引号的字符串（包含后缀），长度限制在40字符内|——|


**说明**


该命令仅适用于外部存储器。若<file\_name>指定的文件不存在，则提示“远程命令错误”。

可 存储的文件类型：状态文件（.RSF）、任意波文件（.RAF）。

存储任意波文件时，仪器只存储当前通道的数据。


**举例**


下面的命令将counter.RSF文件存储到当前路径下。

:MMEMory:STORe "counter.RSF"
## **OUTPut命令子系统**


:OUTPut[<n>]命令，用于设置与控制通道的输出参数与状态。<n>表示通道的标号，取值为1或2，若该参数缺省，则默认对通道1进行操作。


```
:OUTPut[<n>]:IMPedance <ohms>|INFinity|MINimum|MAXimum
```

```
:OUTPut[<n>]:IMPedance? [MINimum|MAXimum
:OUTPut[<n>]:LOAD <ohms>|INFinity|MINimum|MAXimum
```

```
:OUTPut[<n>]:LOAD? [MINimum|MAXimum
:OUTPut[<n>]:NOISe:SCALe <percent>|MINimum|MAXimum
:OUTPut[<n>]:NOISe:SCALe? [MINimum|MAXimum
:OUTPut[<n>]:NOISe[:STATe] ON|OFF
:OUTPut[<n>]:NOISe[:STATe]?
```

```
:OUTPut[<n>]:POLarity NORMal|INVerted
:OUTPut[<n>]:POLarity?
```

```
:OUTPut[<n>][:STATe] ON|OFF
:OUTPut[<n>][:STATe]?
```

```
:OUTPut[<n>]:SYNC:POLarity POSitive|NEGative
:OUTPut[<n>]:SYNC:POLarity?
```

```
:OUTPut[<n>]:SYNC[:STATe] ON|OFF
:OUTPut[<n>]:SYNC[:STATe]?
```

**:OUTPut[<n>]:IMPedance**


**命令格式**


```
:OUTPut[<n>]:IMPedance <ohms>|INFinity|MINimum|MAXimum
```

```
:OUTPut[<n>]:IMPedance? [MINimum|MAXimum
```
**功能描述**


设置前面板[Output1]或[Output2]连接器的输出阻抗 ，单位默认为Ω。

查询[Output1]或[Output2]连接器的输出阻抗。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<ohms>|整型|1 Ω至10000 Ω|50 Ω|


**说明**


默认设置：INFinity（高阻）

该命令与如下命令完全兼容：

```
:OUTPut[<n>]:LOAD <ohms>|INFinity|MINimum|MAXimum
```

```
:OUTPut[<n>]:LOAD? [MINimum|MAXimum
```
**返回格式**


查询返回具体阻抗值或者INFINITY（高阻）。


**举例**


下面的命令将[Output2]连接器的输出阻抗设置为100 Ω。

```
:OUTPut2:IMPedance 100
```


下面的查询返回100。

```
:OUTPut2:IMPedance?
```


**相关命令**


```
:OUTPut[<n>]:LOAD <ohms>|INFinity|MINimum|MAXimum
```

```
:OUTPut[<n>]:LOAD? [MINimum|MAXimum
```
**:OUTPut[<n>]:LOAD**


**命令格式**


```
:OUTPut[<n>]:LOAD <ohms>|INFinity|MINimum|MAXimum
```

```
:OUTPut[<n>]:LOAD? [MINimum|MAXimum
```
**功能描述**


设置前面板[Output1]或[Output2]连接器的输出阻抗，单位默认为Ω。

查询[Output1]或[Output2]连接器的输出阻抗。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<ohms>|整型|1 Ω至10000 Ω|50 Ω|


**说明**


默认设置：INFinity（高阻）

该命令与如下命令完全兼容：

```
:OUTPut[<n>]:IMPedance <ohms>|INFinity|MINimum|MAXimum
```

```
:OUTPut[<n>]:IMPedance? [MINimum|MAXimum
```
**返回格式**


查询返回具体阻抗值或者INFINITY（高阻）。


**举例**


下面的命令将[Output2]连接器的输出阻抗设置为100 Ω。

```
:OUTPut2:LOAD 100
```


下面的查询返回100。

```
:OUTPut2:LOAD?
```


**相关命令**


```
:OUTPut[<n>]:IMPedance <ohms>|INFinity|MINimum|MAXimum
```

```
:OUTPut[<n>]:IMPedance? [MINimum|MAXimum
```
**:OUTPut[<n>]:NOISe:SCALe**


**命令格式**


```
:OUTPut[<n>]:NOISe:SCALe <percent>|MINimum|MAXimum
:OUTPut[<n>]:NOISe:SCALe? [MINimum|MAXimum
```
**功能描述**


设置在[Output1]或[Output2]连接器上叠加的噪声的比例。

查询在[Output1]或[Output2]连接器上叠加的噪声的比例。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<percent>|连续实型|0%至50%|10%|


**返回格式**


以科学计数形式返回当前的噪声比例。


**举例**


下面的命令将[Output2]连接器的噪声比例设置为15%：

```
:OUTPut2:NOISe:SCALe 15
```


下面的查询返回1.500000E+01。

```
:OUTPut2:NOISe:SCALe?
```

**:OUTPut[<n>]:NOISe[:STATe]**


**命令格式**


```
:OUTPut[<n>]:NOISe[:STATe] ON|OFF
:OUTPut[<n>]:NOISe[:STATe]?
```


**功能描述**


启用或禁用[Output1]或[Output2]连接器上的 噪声叠加功能。

查询[Output1]或[Output2]连接器上的 噪声叠加状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|ON|


**返回格式**


查询返回ON或OFF。


**举例**


下面的命令启用[Output1]连接器上的 噪声叠加：

```
:OUTPut:NOISe ON
```


下面的查询返回ON:

```
:OUTPut:NOISe?
```


**:OUTPut[<n>]:POLarity**


**命令格式**


```
:OUTPut[<n>]:POLarity NORMal|INVerted
```

```
:OUTPut[<n>]:POLarity?
```


**功能描述**


设置[Output1]或[Output2]连接器的输出极性。

查询[Output1]或[Output2]连接器的输出极性。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|NORMal|INVerted|NORMal（常规）|


**说明**


输出极性为反相 （INVerted）时，波形相对于偏移电压进行反相。

波形反相后：任何偏移电压都不变；在用户界面中观察到的波形不反相；与波形相关的同步信号也不反相。


**返回格式**


返回NORMAL或INVERTED。


**举例**


下面的命令将[Output1]连接器的输出极性设置为反相。

```
:OUTPut1:POLarity INVerted
```


查询返回INVERTED。

```
:OUTPut1:POLarity?
```


**:OUTPut[<n>][:STATe]**


**命令格式**


```
:OUTPut[<n>][:STATe] ON|OFF
```

```
:OUTPut[<n>][:STATe]?
```


**功能描述**


启用或禁用前面板[Output1]或[Output2]连接器的输出。

查询[Output1]或[Output2]连接器的状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**返回格式**


查询返回ON或OFF。


**举例**


下面的命令启用[Output1]连接器：

```
:OUTPut ON
```


下面的查询返回ON。

```
:OUTPut?
```

**:OUTPut[<n>]:SYNC:POLarity**


**命令格式**


```
:OUTPut[<n>]:SYNC:POLarity POSitive|NEGative
```

```
:OUTPut[<n>]:SYNC:POLarity?
```


**功能描述**


设置[Sync1]或[Sync2]连接器的输出极性。

查询[Sync1]或[Sync2]连接器的输出极性。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|POSitive|NEGative|POSitive|


**返回格式**


返回POS或NEG。


**举例**


下面的命令将[Sync2]连接器的输出极性设置为负极性 ：

```
:OUTPut2:SYNC:POLarity NEGative
```


下面的查询返回NEG。

```
:OUTPut2:SYNC:POLarity?
```


**:OUTPut[<n>]:SYNC[:STATe]**


**命令格式**


```
:OUTPut[<n>]:SYNC[:STATe] ON|OFF
```

```
:OUTPut[<n>]:SYNC[:STATe]?
```


**功能描述**


启用或禁用[Sync1]或[Sync2]连接器上的同步信号。

查询返回ON或OFF。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|ON|


**说明**


在禁用同步信号时，[Sync1]或[Sync2]连接器上的输出电平是逻辑低电平。


**返回格式**


查询返回ON或OFF。


**举例**


下面的命令禁用[Sync1]连接器上的同步信号：

```
:OUTPut:SYNC OFF
```


下面的查询返回OFF:

```
:OUTPut:SYNC?
```


## **PA命令子系统**


:PA命令用来设置和查询使用外部功放（PA）时的相关信息。包括设置和查询PA开关状态，增益，输出极性和偏置以及保存PA的工作状态到仪器内部存储器中。


```
:PA:GAIN 1X|10X
```

```
:PA:GAIN?
```

```
:PA:OFFSet[:STATe] ON|OFF
```

```
:PA:OFFSet[:STATe]?
```

```
:PA:OFFSet:VALUe <value>|MINimum|MAXimum
```

```
:PA:OFFSet:VALUe? [MINimum|MAXimum
:PA:OUTPut:POLarity NORMal|INVerted
```

```
:PA:OUTPut:POLarity?
```

```
:PA:SAVE
```

```
:PA[:STATe] ON|OFF
```

```
:PA[:STATe]?
```


**:PA:GAIN**

**命令格式**


```
:PA:GAIN 1X|10X
```

```
:PA:GAIN?
```


**功能描述**


选择在功放输出端信号放大的增益为1X或10X。

查询功放输出端信号放大的增益。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|1X|10X|离散型|1X|10X|1X|


**说明**


1X表示无增益输出，10X表示将信号放大10倍后输出。


**返回格式**


返回1X或10X。


**举例**


下面的命令选择在功放输出端信号放大的增益为10X。

```
:PA:GAIN 10X
```


下面的命令查询返回10X。

```
:PA:GAIN?
```

**:PA:OFFSet[:STATe]**

**命令格式**


```
:PA:OFFSet[:STATe] ON|OFF
```

```
:PA:OFFSet[:STATe]?
```


**功能描述**


打开或关闭在功放输出端的输出偏置。

查询在功放输出端输出偏置的开关状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|ON|OFF|布尔型|ON|OFF|OFF |


**说明**


您可以发送:PA:OFFSet:VALUe命令设置在功放输出端的输出偏移量。


**返回格式**


返回ON或OFF。


**举例**


下面的命令打开在功放输出端的输出偏置。

```
:PA:OFFSet:STATe ON
```


下面的命令查询返回ON。

```
:PA:OFFSet:STATe?
```

**:PA:OFFSet:VALUe**

**命令格式**


```
:PA:OFFSet:VALUe <value>|MINimum|MAXimum
```

```
:PA:OFFSet:VALUe? [MINimum|MAXimum
```
**功能描述**


设置功放输出端的输出偏移量。

查询功放输出端的输出偏移量。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<value>|实型|-12V至12V|0V|


**说明**


您可以发送:PA:OFFSet:[STATe]命令打开或关闭在功放输出端的输出偏置。


**返回格式**


以科学计数形式返回输出偏移量，有效位数为7位，如1.234500E+00，表示输出偏移量为1.2345V。


**举例**


下面的命令设置在功放输出端的输出偏移量为1.2345V。

:PA:OFFSet:VALUe 1.2345 


下面的命令查询返回1.234500E+00。

```
:PA:OFFSet:VALUe?
```

**:PA:OUTPut:POLarity**

**命令格式**


```
:PA:OUTPut:POLarity NORMal|INVerted
```

```
:PA:OUTPut:POLarity?
```


**功能描述**


选择功放输出端信号的输出极性为常规（NORMal）或反相（INVerted）。

查询功放输出端信号的输出极性。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|NORMal|INVerted|离散型|NORMal|INVerted|NORMal |


**说明**


功放输出端信号的输出极性是指在功放的输出端信号为常规（NORMal）输出或反相（INVerted）输出。常规模式下，输出正常信号；反相模式下，将信号反相后输出。


**返回格式**


返回NORMAL或INVERTED。


**举例**


下面的命令选择功放输出端信号的输出极性为常规。

```
:PA:OUTPut:POLarity NORMal
```


下面的命令查询返回NORMAL。

```
:PA:OUTPut:POLarity?
```

**:PA:SAVE**

**命令格式**


```
:PA:SAVE
```


**功能描述**


保存PA当前的工作状态到仪器内部存储器中。


**说明**


下次打开PA时，将自动调用上次保存的工作状态。


**:PA[:STATe]**

**命令格式**


```
:PA[:STATe] ON|OFF
```

```
:PA[:STATe]?
```


**功能描述**


打开或关闭外部功放。

查询外部功放的开关状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|ON|OFF|布尔型|ON|OFF|OFF|


**说明**


打开外部功放时，PA将输入信号（即信号发生器的输出信号）进行功率放大并输出，关闭外部功放时，PA无输出。


**返回格式**


返回ON或OFF。


**举例**


下面的命令打开外部功放。

```
:PA:STATe ON
```


下面的命令查询返回ON。

```
:PA:STATe?
```
## **SOURce命令子系统** 


[:SOURce<n>]命令，用于设置基本波、任意波、谐波、调制（Mod）、扫频（Sweep）以及脉冲串（Burst）输出信号的相关参数。<n>的取值为1或2，表示相应的通道，缺省时默认对通道1进行操作。


包括如下类别：


[:SOURce<n>]:APPLy

[:SOURce<n>]:BURSt

[:SOURce<n>]:FREQuency

[:SOURce<n>]:FUNCtion

[:SOURce<n>]:HARMonic

[:SOURce<n>]:MARKer

[:SOURce<n>]:MOD

[:SOURce<n>]:PERiod

[:SOURce<n>]:PHASe

[:SOURce<n>]:PULSe

[:SOURce<n>]:SWEep

[:SOURce<n>]:VOLTage

**[:SOURce<n>]:APPLy**


[:SOURce<n>]:APPLy:CUSTom[<freq>[,<amp>[,<offset>[,<phase>]]]]
[:SOURce<n>]:APPLy:HARMonic [<freq>[,<amp>[,<offset>[,<phase>]]]
[:SOURce<n>]:APPLy:NOISe [<amp>[,<offset>]
[:SOURce<n>]:APPLy:PULSe [<freq>[,<amp>[,<offset>[,<delay>]]]
[:SOURce<n>]:APPLy:RAMP [<freq>[,<amp>[,<offset>[,<phase>]]]
[:SOURce<n>]:APPLy:SINusoid [<freq>[,<amp>[,<offset>[,<phase>]]]]
[:SOURce<n>]:APPLy:SQUare [<freq>[,<amp>[,<offset>[,<phase>]]]] 
[:SOURce<n>]:APPLy:USER [<freq>[,<amp>[,<offset>[,<phase>]]]]
[:SOURce<n>]:APPLy?

**[:SOURce<n>]:APPLy:CUSTom**


**命令格式**


[:SOURce<n>]:APPLy:CUSTom [<freq>[,<amp>[,<offset>[,<phase>]]]
**功能描述**


以指定参数（频率、幅度、DC偏移和起始相位 ）输出用户自定义波形。


**参数**


|名称|类型|范围 <sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<freq>|连续实型|1 μHz至40 MHz|1 kHz|
|<amp>|连续实型|——|5 Vpp|
|<offset>|连续实型|——|0 V<sub>DC</sub>|
|<phase>|连续实型|0°至360°|0°|

注 <sup>1</sup>：对于不同的型号，各参数的取值范围不同。此外，<amp>受阻抗和频率/周期设置的限制，<offset>受阻抗和幅度/高电平设置的限制，详见本产品用户手册。 此处指DG4162在阻抗为“高阻”时的范围。


**举例**


下面的命令输出自定义波形，自定义波形的频率为100 Hz、幅度为2.5 Vpp、DC偏移为0.5 V<sub>DC</sub>、起始相位为90°：

:APPLy:CUSTom 100,2.5,0.5,90

**[:SOURce<n>]:APPLy:HARMonic**


**命令格式**


[:SOURce<n>]:APPLy:HARMonic [<freq>[,<amp>[,<offset>[,<phase>]]]
**功能描述**


输出一个具有指定频率、振幅、DC偏移和起始相位的谐波。


**参数**


|名称|类型|范围 <sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<freq>|连续实型|1 μHz至80 MHz|1 kHz|
|<amp>|连续实型|——|5 Vpp|
|<offset>|连续实型|——|0 V<sub>DC</sub>|
|<phase>|连续实型|0°至360°|0°|

注<sup>1</sup> ：对于不同的型号，各参数的取值范围不同。此外，<amp>受阻抗和频率/周期设置的限制，<offset>受阻抗和幅度/高电平设置的限制，详见本产品用户手册。

此处指DG4162在阻抗为“高阻”，谐波次数为“2”时的范围 。


**举例**


下面的命令设置谐波的频率为100 Hz、幅度为2.5Vpp、DC偏移为0.5 V<sub>DC</sub>、起始相位为90°：

:APPLy:HARMonic 100,2.5,0.5,90

**[:SOURce<n>]:APPLy:NOISe**


**命令格式**


[:SOURce<n>]:APPLy:NOISe [<amp>[,<offset>]
**功能描述**


输出一个具有指定的幅度和DC偏移的噪声波。


**参数**


|名称|类型|范围 <sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<amp>|连续实型|0 Vpp至10 Vpp（50 Ω）|5 Vpp|
|<offset>|连续实型|——|0 V<sub>DC</sub>|

注 <sup>1</sup>：<offset>受阻抗和幅度/高电平设置的限制，详见本产品用户手册。


**举例**


下面的命令设置噪声的幅度为2.5 Vpp、DC偏移为0.5 V<sub>DC</sub>：

:APPLy:NOISe 2.5,0.5

**[:SOURce<n>]:APPLy:PULSe**


**命令格式**


[:SOURce<n>]:APPLy:PULSe [<freq>[,<amp>[,<offset>[,<delay>]]]
**功能描述**


输出一个具有指定频率、振幅、DC偏移和延时的脉冲波。


**参数**


|名称|类型|范围 <sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<freq>|连续实型|1 μHz 至 40 MHz|1 kHz|
|<amp>|连续实型|——|5 Vpp|
|<offset>|连续实型|——|0 V<sub>DC</sub>|
|<delay>|连续实型|0 ns 至 脉冲周期|0 ns|

注 <sup>1</sup>：对于不同的型号，各参数的取值范围不同。此外，<amp>受阻抗和频率/周期设置的限制，<offset>受阻抗和幅度/高电平设置的限制，详见本产品用户手册。

此处指DG4162在阻抗为“高阻”时的范围。


**举例**


下面的命令设置脉冲波的频率为100 Hz、幅度为2.5Vpp、DC偏移为0.5 V<sub>DC</sub>、延时为5 ms：

:APPLy:PULSe 100,2.5,0.5,0.005

**[:SOURce<n>]:APPLy:RAMP**


**命令格式**


[:SOURce<n>]:APPLy:RAMP [<freq>[,<amp>[,<offset>[,<phase>]]]
**功能描述**


输出一个具有指定频率、振幅、DC偏移和起始相位的锯齿波。


**参数**


|名称|类型|范围 <sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<freq>|连续实型|1 μHz至4 MHz|1 kHz|
|<amp>|连续实型|——|5 Vpp|
|<offset>|连续实型|——|0 V<sub>DC</sub>|
|<phase>|连续实型|0°至360°|0°|

注 <sup>1</sup>：对于不同的型号，各参数的取值范围不同。此外，<amp>受阻抗和频率/周期设置的限制，<offset>受阻抗和幅度/高电平设置的限制，详见本产品用户手册。 此处指DG4162在阻抗为“高阻”时的范围。


**举例**


下面的命令设置锯齿波的频率为100 Hz、幅度为2.5Vpp、DC偏移为0.5 V<sub>DC</sub>、起始相位为90°：

:APPLy:RAMP 100,2.5,0.5,90

**[:SOURce<n>]:APPLy:SINusoid**


**命令格式**


[:SOURce<n>]:APPLy:SINusoid [<freq>[,<amp>[,<offset>[,<phase>]]]
**功能描述**


输出一个具有指定频率、振幅、DC偏移和起始相位的正弦波。


**参数**


|名称|类型|范围 <sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<freq>|连续实型|1 μHz至160 MHz|1 kHz|
|<amp>|连续实型|——|5 Vpp|
|<offset>|连续实型|——|0 V<sub>DC</sub>|
|<phase>|连续实型|0°至360°|0°|

注 <sup>1</sup>：对于不同的型号，各参数的取值范围不同。此外，<amp>受阻抗和频率/周期设置的限制，<offset>受阻抗和幅度/高电平设置的限制，详见本产品用户手册。 此处指DG4162在阻抗为“高阻”时的范围。


**举例**


下面的命令设置正弦波的频率为100 Hz、幅度为2.5Vpp、DC偏移为0.5 V<sub>DC</sub>、起始相位为90°：

:APPLy:SINusoid 100,2.5,0.5,90

**[:SOURce<n>]:APPLy:SQUare**


**命令格式**


[:SOURce<n>]:APPLy:SQUare [<freq>[,<amp>[,<offset>[,<phase>]]]
**功能描述**


输出一个具有指定频率、振幅、DC偏移和起始相位的方波。


**参数**


|名称|类型|范围 <sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<freq>|连续实型|1 μHz至50 MHz|1 kHz|
|<amp>|连续实型|——|5 Vpp|
|<offset>|连续实型|——|0 V<sub>DC</sub>|
|<phase>|连续实型|0°至360°|0°|

注 <sup>1</sup>：对于不同的型号，各参数的取值范围不同。此外，<amp>受阻抗和频率/周期设置的限制，<offset>受阻抗和幅度/高电平设置的限制，详见本产品用户手册。 此处指DG4162在阻抗为“高阻”时的范围。


**举例**


下面的命令设置方波的频率为100 Hz、幅度为2.5 Vpp、DC偏移为0.5 V<sub>DC</sub>、起始相位为90°：

:APPLy:SQUare 100,2.5,0.5,90

**[:SOURce<n>]:APPLy:USER**


**命令格式**


[:SOURce<n>]:APPLy:USER [<freq>[,<amp>[,<offset>[,<phase>]]]
**功能描述**


输出一个具有指定频率、振幅、DC偏移和起始相位的任意波。


**参数**


|名称|类型|范围 <sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<freq>|连续实型|1 μHz至40 MHz|1 kHz|
|<amp>|连续实型|——|5 Vpp|
|<offset>|连续实型|——|0 V<sub>DC</sub>|
|<phase>|连续实型|0°至360°|0°|

注 <sup>1</sup>：对于不同的型号，各参数的取值范围不同。此外，<amp>受阻抗和频率/周期设置的限制，<offset>受阻抗和幅度/高电平设置的限制，详见本产品用户手册。 此处指DG4162在阻抗为“高阻”时的范围。


**说明**


若当前任意波为DC，直接提取偏移参数修改DC偏移，频率、幅度和相位参数丢弃。


**举例**


下面的命令设置任意波的频率为100 Hz、幅度为2.5 Vpp、DC偏移为0.5 V<sub>DC</sub>、起始相位为90°：

:APPLy:USER 100,2.5,0.5,90

**[:SOURce<n>]:APPLy?**


**命令格式**


[:SOURce<n>]:APPLy?


**功能描述**


查询函数发生器的当前配置。


**返回格式**


返回一个带引号的字符串，返回格式 为"波形名称，频率，幅度，偏移，起始相位/延时" 。

对应没有的项用“DEF”代替，例如："NOISE,DEF,5.000000E+00,0.000000E+00,DEF"。

**[:SOURce<n>]:BURSt**


[:SOURce<n>]:BURSt:GATE:POLarity NORMal|INVerted 
[:SOURce<n>]:BURSt:GATE:POLarity? 

[:SOURce<n>]:BURSt:INTernal:PERiod <period>|MINimum|MAXimum 
[:SOURce<n>]:BURSt:INTernal:PERiod? [MINimum|MAXimum
[:SOURce<n>]:BURSt:MODE TRIGgered|GATed|INFinity 
[:SOURce<n>]:BURSt:MODE? 
[:SOURce<n>]:BURSt:NCYCles <cycles>|MINimum|MAXimum 
[:SOURce<n>]:BURSt:NCYCles? [MINimum|MAXimum
[:SOURce<n>]:BURSt:PHASe <phase>|MINimum|MAXimum 
[:SOURce<n>]:BURSt:PHASe? [MINimum|MAXimum
[:SOURce<n>]:BURSt[:STATe] ON|OFF 
[:SOURce<n>]:BURSt[:STATe]? 
[:SOURce<n>]:BURSt:TDELay <delay>|MINimum|MAXimum 
[:SOURce<n>]:BURSt:TDELay? [MINimum|MAXimum
[:SOURce<n>]:BURSt:TRIGger[:IMMediate]
[:SOURce<n>]:BURSt:TRIGger:SLOPe POSitive|NEGative 
[:SOURce<n>]:BURSt:TRIGger:SLOPe? 

[:SOURce<n>]:BURSt:TRIGger:SOURce INTernal|EXTernal|MANual 
[:SOURce<n>]:BURSt:TRIGger:SOURce?

[:SOURce<n>]:BURSt:TRIGger:TRIGOut OFF|POSitive|NEGative 
[:SOURce<n>]:BURSt:TRIGger:TRIGOut? 


**[:SOURce<n>]:BURSt:GATE:POLarity**


**命令格式**


[:SOURce<n>]:BURSt:GATE:POLarity NORMal|INVerted

[:SOURce<n>]:BURSt:GATE:POLarity?


**功能描述**


选择当后面板**[Mod/FSK/Trig]**连接器上的门控信号为高电平或低电平时输出脉冲串。

查询极性设置。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|NORMal|INVerted|NORMal|


**说明**


该命令仅在门控Burst模式下有效。


**返回格式**


返回NORM或INV。


**举例**


下面的命令设置极性为负极性，即当后面板**[Mod/FSK/Trig]**连接器上的门控信号为低电平时，仪器输出脉冲串：

```
:BURSt:GATE:POLarity INVerted
```


下面的查询返回INV。

```
:BURSt:GATE:POLarity?
```


**相关命令**


[:SOURce<n>]:BURSt:MODE TRIGgered|GATed|INFinity 
[:SOURce<n>]:BURSt:MODE?

**[:SOURce<n>]:BURSt:INTernal:PERiod**


**命令格式**


[:SOURce<n>]:BURSt:INTernal:PERiod <period>|MINimum|MAXimum

[:SOURce<n>]:BURSt:INTernal:PERiod? [MINimum|MAXimum
**功能描述**


设置Burst脉冲串周期（从一个N循环脉冲串开始到下一个脉冲串开始的时间），单位默认为“s”。

查询Burst脉冲串周期。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<period>|连续实型|≥ 1 μs + 波形周期<sup>1</sup> × 脉冲串个数|10 ms|

注<sup>1</sup> ：波形周期为脉冲串函数（正弦波、方波等）的周期。


**说明**


该命令仅适用于内部触发N循环脉冲串模式。

若设置的脉冲串周期过小，信号发生器将自动增加该周期以允许指定数量的循环输出。


**返回格式**


以科学计数形式返回周期值。


**举例**


下面的命令设置脉冲串周期为0.5 s：

:BURSt:INTernal:PERiod 0.5


下面的查询返回5.000000E-01。

```
:BURSt:INTernal:PERiod?
```


**相关命令**


[:SOURce<n>]:BURSt:MODE TRIGgered|GATed|INFinity 
[:SOURce<n>]:BURSt:MODE?


**[:SOURce<n>]:BURSt:MODE**


**命令格式**


[:SOURce<n>]:BURSt:MODE TRIGgered|GATed|INFinity

[:SOURce<n>]:BURSt:MODE?


**功能描述**


选择脉冲串类型 为N循环、门控或无限。

查询脉冲串类型 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|TRIGgered|GATed|INFinity |TRIGgered |


**返回格式**


返回TRIG、GAT或INF。


**举例**


下面的命令将脉冲串类型设置为门控：

```
:SOURce:BURSt:MODE GATed
```


下面的查询返回：GAT。

```
:SOURce:BURSt:MODE?
```

**[:SOURce<n>]:BURSt:NCYCles**


**命令格式**


[:SOURce<n>]:BURSt:NCYCles <cycles>|MINimum|MAXimum

[:SOURce<n>]:BURSt:NCYCles? [MINimum|MAXimum
**功能描述**


设置脉冲串循环数。

查询脉冲串循环数。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<cycles>|整型|1至1 000 000（外部或手动触发）1至500 000（内部触发）|1|


**说明**


该命令仅在N循环模式下有效。


**返回格式**


返回一个整数。


**举例**


下面的命令设置脉冲串的循环数为100：

```
:BURSt:NCYCles 100
```


下面的查询返回：100。

```
:BURSt:NCYCles?
```


**相关命令**


[:SOURce<n>]:BURSt:MODE TRIGgered|GATed|INFinity 
[:SOURce<n>]:BURSt:MODE? 


**[:SOURce<n>]:BURSt:PHASe**


**命令格式**


[:SOURce<n>]:BURSt:PHASe <phase>|MINimum|MAXimum

[:SOURce<n>]:BURSt:PHASe? [MINimum|MAXimum
**功能描述**


设置脉冲串起始相位，单位默认为 “°”。

查询脉冲串的起始相位。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<phase>|连续实型|0°至360°|0°|


**说明**


对于正弦波、方波、锯齿波，0°是波形正向通过0 V（或DC偏移值）的点。

对于任意波形，0°是第一个波形点。

对于脉冲波和噪声波无效。


**返回格式**


以科学计数形式返回相位值。


**举例**


下面的命令设置起始相位为10°：

```
:BURSt:PHASe 10
```


下面查询返回1.000000E+01。

```
:BURSt:PHASe?
```

**[:SOURce<n>]:BURSt[:STATe]**


**命令格式**


[:SOURce<n>]:BURSt[:STATe] ON|OFF

[:SOURce<n>]:BURSt[:STATe]?


**功能描述**


打开或关闭Burst功能。

查询Burst功能状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF |OFF |


**说明**


启用Burst时，Sweep或Mod功能将自动关闭（如果当前已打开） 。


**返回格式**


返回ON或OFF。


**举例**


下面的命令打开Burst功能：

```
:BURSt ON
```


下面的查询返回ON。

```
:BURSt?
```


**[:SOURce<n>]:BURSt:TDELay**


**命令格式**


[:SOURce<n>]:BURSt:TDELay <delay>|MINimum|MAXimum

[:SOURce<n>]:BURSt:TDELay? [MINimum|MAXimum
**功能描述**


设置信号发生器从接收到触发信号到开始输出N循环（或无限）脉冲串之间的时间，单位默认为“s”。

查询脉冲串延时。


**参数**


|名称|类型|范围<sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<delay>|连续实型|0 s至85 s|0 s|

注<sup>1</sup>：使用内部触发源时，N循环脉冲串的延时还受载波周期、脉冲周期和循环数的限制。


**说明**


该命令在N循环和无限脉冲串模式下有效。


**返回格式**


以科学计数形式返回时间值。


**举例**


下面的命令设置延时为2.5 s:

:BURSt:TDELay 2.5


下面的查询返回2.500000E+00。

```
:BURSt:TDELay?
```


**相关命令**


[:SOURce<n>]:BURSt:MODE TRIGgered|GATed|INFinity 
[:SOURce<n>]:BURSt:MODE? 

**[:SOURce<n>]:BURSt:TRIGger[:IMMediate]**


**命令格式**


[:SOURce<n>]:BURSt:TRIGger[:IMMediate
**功能描述**


使仪器立即触发。


**说明**


该命令仅在触发源为手动模式时有效。

**[:SOURce<n>]:BURSt:TRIGger:SLOPe**


**命令格式**


[:SOURce<n>]:BURSt:TRIGger:SLOPe POSitive|NEGative

[:SOURce<n>]:BURSt:TRIGger:SLOPe?


**功能描述**


选择信号发生器在外部触发信号的上升沿或下降沿时启动脉冲串输出。

查询外部触发信号的边沿类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|POSitive|NEGative |POSitive|


**说明**


该命令仅在外部触发源时有效。


**返回格式**


返回POS或NEG。　


**举例**


下面的查询返回NEG。

```
:BURS:TRIG:SLOP NEG
```


**相关命令**


[:SOURce<n>]:BURSt:MODE TRIGgered|GATed|INFinity 
[:SOURce<n>]:BURSt:MODE?

**[:SOURce<n>]:BURSt:TRIGger:SOURce**


**命令格式**


[:SOURce<n>]:BURSt:TRIGger:SOURce INTernal|EXTernal|MANual

[:SOURce<n>]:BURSt:TRIGger:SOURce?


**功能描述**


设置Burst触发源类型 为内部、外部或手动。

查询Burst触发源类型 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|INTernal|EXTernal|MANual|INTernal|


**返回格式**


返回INT、EXT或MAN。


**举例**


下面的命令选择手动触发源：

```
:BURSt:TRIGger:SOURce MANual
```


下面的查询返回MAN。

```
:BURSt:TRIGger:SOURce?
```

**[:SOURce<n>]:BURSt:TRIGger:TRIGOut**


**命令格式**


[:SOURce<n>]:BURSt:TRIGger:TRIGOut OFF|POSitive|NEGative

[:SOURce<n>]:BURSt:TRIGger:TRIGOut?


**功能描述**


指定触发输出信号的边沿类型。

查询触发输出信号的边沿类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|OFF|POSitive|NEGative |OFF|


**说明**


触发源为内部或手动模式时有效。


**返回格式**


返回OFF、POS或NEG。


**举例**


下面的命令设置触发输出信号的边沿类型为上升沿：

```
:BURSt:TRIGger:TRIGout POSitive
```


下面的查询返回POS。

```
:BURSt:TRIGger:TRIGout POSitive
```


**相关命令**


[:SOURce<n>]:BURSt:TRIGger:SOURce INTernal|EXTernal|MANual 
[:SOURce<n>]:BURSt:TRIGger:SOURce?

**[:SOURce<n>]:FREQuency**


[:SOURce<n>]:FREQuency:CENTer <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:CENTer? [MINimum|MAXimum
[:SOURce<n>]:FREQuency[:FIXed] <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency[:FIXed]? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:SPAN <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:SPAN? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:STARt <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:STARt? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:STOP <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:STOP? [MINimum|MAXimum
**[:SOURce<n>]:FREQuency:CENTer**


**命令格式**


[:SOURce<n>]:FREQuency:CENTer <frequency>|MINimum|MAXimum

[:SOURce<n>]:FREQuency:CENTer? [MINimum|MAXimum
**功能描述**


设置扫频的中心频率，单位默认为“Hz”。

查询扫频的中心频率。


**参数**


|名称|类型|范围<sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|见如下注释|550 Hz|

注<sup>1</sup> ：不同扫频波形对应的中心频率范围不同 ：

正弦波：1 μHz至160 MHz

方波：1 μHz至50 MHz

锯齿波：1 μHz至4 MHz

任意波：1 μHz至40 MHz（内置波形DC除外）


**说明**


扫频模式下，起始频率、终止频率、中心频率和频率跨度相互关联，满足如下关系：


`        `中心频率=（︱起始频率 + 终止频率︱）/2
`        `频率跨度= 终止频率 - 起始频率


**返回格式**


以科学计数形式返回中心频率值。


**举例**


下面的命令设置中心频率为600 Hz。

```
:FREQuency:CENTer 600
```


下面的查询返回6.000000E+02。

```
:FREQuency:CENTer?
```


**相关命令**


[:SOURce<n>]:FREQuency:SPAN <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:SPAN? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:STARt <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:STARt? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:STOP <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:STOP? [MINimum|MAXimum
**[:SOURce<n>]:FREQuency[:FIXed]**


**命令格式**


[:SOURce<n>]:FREQuency[:FIXed] <frequency>|MINimum|MAXimum

[:SOURce<n>]:FREQuency[:FIXed]? [MINimum|MAXimum
**功能描述**


设置基本波的频率，单位默认为“Hz”。

查询基本波的频率。


**参数**


|名称|类型|范围<sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|见如下注释|1 kHz|

注<sup>1</sup> ：不同波形对应的频率范围不同 ：

正弦波：1 μHz至160 MHz

方波：1 μHz至50 MHz

锯齿波：1 μHz至4 MHz

脉冲：1 μHz至40 MHz

任意波：1 μHz至40 MHz 

谐波：1 μHz至80 MHz 


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令设置频率为1.5kHz。

```
:FREQuency 1500
```


下面的查询返回1.500000E+03。

```
:FREQuency?
```

**[:SOURce<n>]:FREQuency:SPAN**


**命令格式**


[:SOURce<n>]:FREQuency:SPAN <frequency>|MINimum|MAXimum

[:SOURce<n>]:FREQuency:SPAN? [MINimum|MAXimum
**功能描述**


设置扫频的频率跨度，单位默认为“Hz”。

查询频率跨度。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|请参考用户手册的说明|900 Hz|


**说明**


扫频模式下，起始频率、终止频率、中心频率和频率跨度相互关联，满足如下关系：


`        `中心频率=（︱起始频率 + 终止频率︱）/2
`        `频率跨度= 终止频率 - 起始频率


**返回格式**


以科学计数形式返回频率跨度值。


**举例**


下面的命令设置频率跨度为1100 Hz。

```
:FREQuency:SPAN 1100
```


下面的查询返回1.100000E+03。

```
:FREQuency:SPAN?
```


**相关命令**


[:SOURce<n>]:FREQuency:CENTer <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:CENTer? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:STARt <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:STARt? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:STOP <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:STOP? [MINimum|MAXimum
**[:SOURce<n>]:FREQuency:STARt**


**命令格式**


[:SOURce<n>]:FREQuency:STARt <frequency>|MINimum|MAXimum

[:SOURce<n>]:FREQuency:STARt? [MINimum|MAXimum
**功能描述**


设置扫频的起始频率，单位默认为“Hz”。

查询扫频的起始频率值。


**参数**


|名称|类型|范围<sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|见如下注释|100 Hz|

注<sup>1</sup> ：不同扫频波形对应的起始频率范围不同 ：

正弦波：1 μHz至160 MHz

方波：1 μHz至50 MHz

锯齿波：1 μHz至4 MHz

任意波：1 μHz至40 MHz（内置波形DC除外）


**说明**


扫频模式下，起始频率、终止频率、中心频率和频率跨度相互关联，满足如下关系：


`        `中心频率=（︱起始频率 + 终止频率︱）/2
`        `频率跨度= 终止频率 - 起始频率


**返回格式**


以科学计数形式返回起始频率值。


**举例**


下面的命令设置起始频率为500 Hz。

```
:FREQuency:STARt 500
```


下面的查询返回5.000000E+02。

```
:FREQuency:STARt?
```


**相关命令**


[:SOURce<n>]:FREQuency:CENTer <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:CENTer? [MINimum|MAXimum
[:SOURce<n>]:FREQuency:SPAN <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:SPAN? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:STOP <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:STOP? [MINimum|MAXimum
**[:SOURce<n>]:FREQuency:STOP**


**命令格式**


[:SOURce<n>]:FREQuency:STOP <frequency>|MINimum|MAXimum

[:SOURce<n>]:FREQuency:STOP? [MINimum|MAXimum
**功能描述**


设置扫频的终止频率，单位默认为“Hz”。

查询扫频的终止频率值。


**参数**


|名称|类型|范围<sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|见如下注释|1 kHz|

注<sup>1</sup> ：不同扫频波形对应的终止频率范围不同 ：

正弦波：1 μHz至160 MHz

方波：1 μHz至50 MHz

锯齿波：1 μHz至4 MHz

任意波：1 μHz至40 MHz（内置波形DC除外）


**说明**


扫频模式下，起始频率、终止频率、中心频率和频率跨度相互关联，满足如下关系：


`        `中心频率=（︱起始频率 + 终止频率︱）/2
`        `频率跨度= 终止频率 - 起始频率


**返回格式**


以科学计数形式返回终止频率值。


**举例**


下面的命令设置终止频率为5 kHz。

```
:FREQuency:STOP 5000
```


下面的查询返回5.000000E+03。

```
:FREQuency:STOP?
```


**相关命令**


[:SOURce<n>]:FREQuency:CENTer <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:CENTer? [MINimum|MAXimum
[:SOURce<n>]:FREQuency:SPAN <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:SPAN? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:STARt <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:STARt? [MINimum|MAXimum
### **[:SOURce<n>]:FUNCtion**


[:SOURce<n>]:FUNCtion:ARB:STEP

[:SOURce<n>]:FUNCtion:RAMP:SYMMetry <symmetry>|MINimum|MAXimum 
[:SOURce<n>]:FUNCtion:RAMP:SYMMetry? [MINimum|MAXimum
[:SOURce<n>]:FUNCtion[:SHAPe] <wave> 
[:SOURce<n>]:FUNCtion[:SHAPe]? 

[:SOURce<n>]:FUNCtion:SQUare:DCYCle <percent>|MINimum|MAXimum 
[:SOURce<n>]:FUNCtion:SQUare:DCYCle? [MINimum|MAXimum
**[:SOURce<n>]:FUNCtion:ARB:STEP**


**命令格式**


[:SOURce<n>]:FUNCtion:ARB:STEP


**功能描述**


打开任意波的逐点输出模式。


**说明**


逐点输出模式下，信号发生器自动根据波形长度（16,384）和采样率计算输出信号的频率（30.517578125 kHz）。信号发生器固定以该频率逐个输出波形点。逐点输出模式可以防止重要的波形点丢失。

该命令仅在任意波功能打开时有效。

**[:SOURce<n>]:FUNCtion:RAMP:SYMMetry**


**命令格式**


[:SOURce<n>]:FUNCtion:RAMP:SYMMetry <symmetry>|MINimum|MAXimum

[:SOURce<n>]:FUNCtion:RAMP:SYMMetry? [MINimum|MAXimum
**功能描述**


设置锯齿波的对称性，以%表示。

查询锯齿波的对称性。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<symmetry>|连续实型|0%至100%|50%|


**返回格式**


以科学计数形式返回对称性。


**举例**


下面的命令将锯齿波的对称性设置为80%。

```
:FUNCtion:RAMP:SYMMetry 80
```


下面的查询返回8.000000E+01。

```
:FUNCtion:RAMP:SYMMetry?
```

**[:SOURce<n>]:FUNCtion[:SHAPe]**


**命令格式**


[:SOURce<n>]:FUNCtion[:SHAPe] <wave>

[:SOURce<n>]:FUNCtion[:SHAPe]?


**功能描述**


选择波形。

查询当前选择的波形。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<wave>|关键字|SINusoid|SQUare|RAMP|PULSe|NOISe|USER|HARMonic|CUSTom|DC|ABSSINE|ABSSINEHALF|AMPALT|ATTALT|GAUSSPULSE|NEGRAMP|NPULSE|PPULSE|SINETRA|SINEVER|STAIRDN|STAIRUD|STAIRUP|TRAPEZIA|BANDLIMITED|BUTTERWORTH|CHEBYSHEV1|CHEBYSHEV2|COMBIN|CPULSE|CWPULSE|DAMPEDOSC|DUALTONE|GAMMA|GATEVIBR|LFMPULSE|MCNOSIE|NIMHDISCHARGE|PAHCUR|QUAKE|RADAR|RIPPLE|ROUNDHALF|ROUNDPM|STEPRESP|SWINGOSC|TV|VOICE|THREEAM|THREEFM|THREEPM|THREEPWM|THREEPFM|CARDIAC|EOG|EEG|EMG|PULSILOGRAM|RESSPEED|LFPULSE|TENS1|TENS2|TENS3|IGNITION|ISO167502SP|ISO167502VR|ISO76372TP1|ISO76372TP2A|ISO76372TP2B|ISO76372TP3A|ISO76372TP3B|ISO76372TP4|ISO76372TP5A|ISO76372TP5B|SCR|SURGE|AIRY|BESSELJ|BESSELY|CAUCHY|CUBIC|DIRICHLET|ERF|ERFC|ERFCINV|ERFINV|EXPFALL|EXPRISE|GAUSS|HAVERSINE|LAGUERRE|LAPLACE|LEGEND|LOG|LOGNORMAL|LORENTZ|MAXWELL|RAYLEIGH|VERSIERA|WEIBULL|X2DATA|COSH|COSINT|COT|COTHCON|COTHPRO|CSCCON|CSCPRO|CSCHCON|CSCHPRO|RECIPCON|RECIPPRO|SECCON|SECPRO|SECH|SINC|SINH|SININT|SQRT|TAN|TANH|ACOS|ACOSH|ACOTCON|ACOTPRO|ACOTHCON|ACOTHPRO|ACSCCON|ACSCPRO|ACSCHCON|ACSCHPRO|ASECCON|ASECPRO|ASECH|ASIN|ASINH|ATAN|ATANH|BARLETT|BARTHANN|BLACKMAN|BLACKMANH|BOHMANWIN|BOXCAR|CHEBWIN|FLATTOPWIN|HAMMING|HANNING|KAISER|NUTTALLWIN|PARZENWIN|TAYLORWIN|TRIANG|TUKEYWIN|SINusoid|


**说明**


若仪器当前没有打开调制、扫频和脉冲串模式，该命令选择仪器输出的波形。

若仪器当前打开调制、扫频或脉冲串模式，该命令选择对应功能的载波波形。

若发送:FUNCtion DC命令,仪器将自动关闭调制、扫频或脉冲串（当前已打开）。


**返回格式**


返回SIN、SQU、RAMP、PULSE、NOISE、HARMONIC、CUSTOM；

选中除SINusoid|SQUare|RAMP|PULSe|NOISe|USER|HARMonic|CUSTom|之外的波形时，返回值与上表中对应的参数一致；

**注意：**若当前选中USER（ 任意波）时，查询返回任意波当前选中的内置波形对应的返回值。


**举例**


下面的命令选中方波：

```
:FUNCtion SQUare
```


下面的查询返回SQU。

```
:FUNCtion?
```

**[:SOURce<n>]:FUNCtion:SQUare:DCYCle**


**命令格式**


[:SOURce<n>]:FUNCtion:SQUare:DCYCle <percent>|MINimum|MAXimum

[:SOURce<n>]:FUNCtion:SQUare:DCYCle? [MINimum|MAXimum
**功能描述**


设置方波占空比，以%表示。

查询方波的占空比。


**参数**


|名称|类型|范围<sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<percent>|连续实型|见下面注释|50%|

注<sup>1</sup>：占空比的范围受“频率/周期”设置的限制。

`     `频率 ≤ 10 MHz：20％至80％

`         `10 MHz < 频率 ≤ 40 MHz：40％至60％

`     `频率 > 40 MHz：50％（固定）


**返回格式**


以科学计数形式返回占空比。


**举例**


下面的命令将方波的占空比设置为80%。

:FUNCtion:SQUare:DCYCle 80%  或  :FUNCtion:SQUare:DCYCle 80


下面的查询返回8.000000E+01。

```
:FUNCtion:SQUare:DCYCle?
```

**[:SOURce<n>]:HARMonic**


[:SOURce<n>]:HARMonic:AMPL <sn>,<value>|MINimum|MAXimum 
[:SOURce<n>]:HARMonic:AMPL? <sn>[,MINimum|MAXimum
[:SOURce<n>]:HARMonic:ORDEr <value>|MINimum|MAXimum 
[:SOURce<n>]:HARMonic:ORDEr? [MINimum|MAXimum
[:SOURce<n>]:HARMonic:PHASe <sn>,<value>|MINimum|MAXimum 
[:SOURce<n>]:HARMonic:PHASe? <sn>[,MINimum|MAXimum
[:SOURce<n>]:HARMonic:TYPe EVEN|ODD|ALL|USER 
[:SOURce<n>]:HARMonic:TYPe? 

[:SOURce<n>]:HARMonic:USER <user> 
[:SOURce<n>]:HARMonic:USER?


**[:SOURce<n>]:HARMonic:AMPL**


**命令格式**


[:SOURce<n>]:HARMonic:AMPL <sn>,<value>|MINimum|MAXimum 
[:SOURce<n>]:HARMonic:AMPL? <sn>[,MINimum|MAXimum
**功能描述**


设置指定次谐波的幅度。

查询指定次谐波的幅度。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<sn>|整型|2至16|2|
|<value>|整型|受阻抗与频率设置的限制，请参考用户手册|1\.2647 Vpp|


**返回格式**


以科学计数形式返回 指定次谐波的幅度值。


**举例**


下面的命令设置第2次谐波的幅度为2.5 Vpp。

:HARMonic:AMPL 2,2.5


下面的查询返回2.500000E+00。

```
:HARMonic:AMPL? 2
```

**[:SOURce<n>]:HARMonic:ORDEr**


**命令格式**


[:SOURce<n>]:HARMonic:ORDEr <value>|MINimum|MAXimum 
[:SOURce<n>]:HARMonic:ORDEr? [MINimum|MAXimum
**功能描述**


设置谐波次数。

查询谐波次数。


**参数**


|名称|类型|范围<sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<value>|整型|见下面的注释|2|

注<sup>1</sup>：2 至 仪器最大输出频率÷基波频率，且为整数，最大值为16。


**返回格式**


以科学计数形式返回谐波次数。


**举例**


下面的命令设置谐波次数为7：

```
:HARMonic:ORDEr 7
```


下面的查询返回7.000000E+00。

```
:HARMonic:ORDEr?
```

**[:SOURce<n>]:HARMonic:PHASe**


**命令格式**


[:SOURce<n>]:HARMonic:PHASe <sn>,<value>|MINimum|MAXimum 
[:SOURce<n>]:HARMonic:PHASe? <sn>[,MINimum|MAXimum
**功能描述**


设置指定次谐波的相位。

查询指定次谐波的相位。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<sn>|整型|2至16|2|
|<value>|整型|0°至360°|0°|


**返回格式**


以科学计数形式返回 指定次谐波的相位值。


**举例**


下面的命令设置第2次谐波的相位为90°。

```
:HARMonic:PHASe 2,90
```


下面的查询返回9.000000E+01。

```
:HARMonic:PHASe? 2
```

**[:SOURce<n>]:HARMonic:TYPe**


**命令格式**


[:SOURce<n>]:HARMonic:TYPe EVEN|ODD|ALL|USER 
[:SOURce<n>]:HARMonic:TYPe? 


**功能描述**


选择谐波类型为偶次、奇次、全部或自定义。

查询谐波类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|EVEN|ODD|ALL|USER |EVEN|


**返回格式**


返回EVEN、ODD、ALL或USER。


**举例**


下面的命令设置谐波类型为奇次：

```
:HARMonic:TYPe ODD
```


下面的查询返回ODD。

```
:HARMonic:TYPe?
```

**[:SOURce<n>]:HARMonic:USER**


**命令格式**


[:SOURce<n>]:HARMonic:USER <user> 
[:SOURce<n>]:HARMonic:USER? 


**功能描述**


设置指定通道的自定义谐波输出。

查询指定通道的自定义谐波输出。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<n>|离散型|1|2|1|
|<user>|ASCII字符串|X000000000000000至X111111111111111|X000000000000000|


**说明**


在自定义谐波（[:SOURce<n>]:HARMonic:TYPe）中，用户可自定义输出谐波的次数，最高次数为16。使用16位二进制数据分别代表16次谐波的输出状态，最左侧的位表示基波，固定为X，不允许修改，后面的15位从左到右依次对应2次谐波到16次谐波。1表示打开相应次谐波的输出，0表示关闭相应次谐波的输出。例如：将16位数据设置为X001000000000001，表示输出基波和4次、16次谐波。

省略[:SOURce<n>]时，默认设置CH1的相关参数。

**返回格式**


返回X000000000000000至X111111111111111之间的一个字符串，如X001000000000001。


**举例**


下面的命令设置CH1的自定义谐波输出基波和4次、16次谐波。

```
:HARMonic:USER X001000000000001
```


下面的命令查询返回X001000000000001。

```
:HARMonic:USER?
```
### **[:SOURce<n>]:MARKer**


[:SOURce<n>]:MARKer:FREQuency <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MARKer:FREQuency? [MINimum|MAXimum
[:SOURce<n>]:MARKer[:STATE] ON|OFF 
[:SOURce<n>]:MARKer[:STATe]?


**[:SOURce<n>]:MARKer:FREQuency**


**命令格式**


[:SOURce<n>]:MARKer:FREQuency <frequency>|MINimum|MAXimum

[:SOURce<n>]:MARKer:FREQuency? [MINimum|MAXimum
**功能描述**


设置标记频率，单位默认为“Hz”。

查询标记频率值。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|受“起始频率”和“终止频率”限制|550 Hz|


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令将标记的频率设置为800 Hz：

```
:MARKer:FREQuency 800
```


下面的查询返回8.000000E+02。

```
:MARKer:FREQuency?
```

**[:SOURce<n>]:MARKer[:STATe]**


**命令格式**


[:SOURce<n>]:MARKer[:STATe] ON|OFF

[:SOURce<n>]:MARKer[:STATe]?


**功能描述**


打开或关闭扫频的频率 标记功能。

查询频率标记功能的状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**说明**


步进扫频方式时，频率标记功能不可用。


**返回格式**


返回ON或OFF。


**举例**


下面的命令打开扫频的频率标记功能：

```
:MARKer ON
```


下面的查询返回ON。

```
:MARKer?
```
### **[:SOURce<n>]:MOD**


[:SOURce<n>]:MOD[:STATe] ON|OFF 
[:SOURce<n>]:MOD[:STATe]?

[:SOURce<n>]:MOD:TYPe AM|FM|PM|ASK|FSK|PSK|PWM|BPSK|QPSK|3FSK|4FSK|OSK 
[:SOURce<n>]:MOD:TYPe?

AM

[:SOURce<n>]:MOD:AM[:DEPTh] <depth>|MINimum|MAXimum 
[:SOURce<n>]:MOD:AM[:DEPTh]? [MINimum|MAXimum
[:SOURce<n>]:MOD:AM:INTernal:FREQuency <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:AM:INTernal:FREQuency? [MINimum|MAXimum
[:SOURce<n>]:MOD:AM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:AM:INTernal:FUNCtion? 

[:SOURce<n>]:MOD:AM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:AM:SOURce?

FM

[:SOURce<n>]:MOD:FM[:DEViation] <deviation>|MINimum|MAXimum 
[:SOURce<n>]:MOD:FM[:DEViation]? [MINimum|MAXimum
[:SOURce<n>]:MOD:FM:INTernal:FREQuency <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:FM:INTernal:FREQuency? [MINimum|MAXimum
[:SOURce<n>]:MOD:FM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:FM:INTernal:FUNCtion? 

[:SOURce<n>]:MOD:FM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:FM:SOURce?

PM

[:SOURce<n>]:MOD:PM[:DEViation] <deviation>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PM[:DEViation]? [MINimum|MAXimum
[:SOURce<n>]:MOD:PM:INTernal:FREQuency <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PM:INTernal:FREQuency? [MINimum|MAXimum
[:SOURce<n>]:MOD:PM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:PM:INTernal:FUNCtion? 

[:SOURce<n>]:MOD:PM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:PM:SOURce?

ASK

[:SOURce<n>]:MOD:ASKey:AMPLitude <amplitude>|MINimum|MAXimum 
[:SOURce<n>]:MOD:ASKey:AMPLitude? [MINimum|MAXimum
[:SOURce<n>]:MOD:ASKey:INTernal[:RATE] <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:ASKey:INTernal[:RATE]? [MINimum|MAXimum
[:SOURce<n>]:MOD:ASKey:POLarity POSitive|NEGative 
[:SOURce<n>]:MOD:ASKey:POLarity?

[:SOURce<n>]:MOD:ASKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:ASKey:SOURce? 

FSK

[:SOURce<n>]:MOD:FSKey[:FREQuency] <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:FSKey[:FREQuency]? [MINimum|MAXimum
[:SOURce<n>]:MOD:FSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:FSKey:INTernal:RATE? [MINimum|MAXimum
[:SOURce<n>]:MOD:FSKey:POLarity POSitive|NEGative 
[:SOURce<n>]:MOD:FSKey:POLarity?

[:SOURce<n>]:MOD:FSKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:FSKey:SOURce? 

PSK

[:SOURce<n>]:MOD:PSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PSKey:INTernal:RATE? [MINimum|MAXimum
[:SOURce<n>]:MOD:PSKey:PHASe <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PSKey:PHASe? [MINimum|MAXimum
[:SOURce<n>]:MOD:PSKey:POLarity POSitive|NEGative 
[:SOURce<n>]:MOD:PSKey:POLarity?

[:SOURce<n>]:MOD:PSKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:PSKey:SOURce?

BPSK

[:SOURce<n>]:MOD:BPSKey:DATA 01|10|PN15|PN21 
[:SOURce<n>]:MOD:BPSKey:DATA?

[:SOURce<n>]:MOD:BPSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:BPSKey:INTernal:RATE? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:BPSKey:PHASe <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:BPSKey:PHASe? [MINimum|MAXimum
QPSK

[:SOURce<n>]:MOD:QPSKey:DATA PN15|PN21 
[:SOURce<n>]:MOD:QPSKey:DATA?

[:SOURce<n>]:MOD:QPSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:INTernal:RATE? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:QPSKey:PHASe1 <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:PHASe1? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:QPSKey:PHASe2 <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:PHASe2? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:QPSKey:PHASe3 <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:PHASe3? [MINimum|MAXimum
3FSK

[:SOURce<n>]:MOD:3FSKey[:FREQuency] <n>,<frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:3FSKey[:FREQuency]? <n>[,MINimum|MAXimum
[:SOURce<n>]:MOD:3FSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:3FSKey:INTernal:RATE? [MINimum|MAXimum
4FSK

[:SOURce<n>]:MOD:4FSKey[:FREQuency] <n>,<frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:4FSKey[:FREQuency]? <n>[,MINimum|MAXimum
[:SOURce<n>]:MOD:4FSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:4FSKey:INTernal:RATE? [MINimum|MAXimum
OSK

[:SOURce<n>]:MOD:OSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:OSKey:INTernal:RATE? [MINimum|MAXimum
[:SOURce<n>]:MOD:OSKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:OSKey:SOURce? 
[:SOURce<n>]:MOD:OSKey:TIME <time>|MINimum|MAXimum 
[:SOURce<n>]:MOD:OSKey:TIME? [MINimum|MAXimum
PWM

[:SOURce<n>]:MOD:PWM[:DEViation]:DCYCle <percent>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PWM[:DEViation]:DCYCle? [MINimum|MAXimum
[:SOURce<n>]:MOD:PWM[:DEViation][:WIDTh] <deviation>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PWM[:DEViation][:WIDTh]? [MINimum|MAXimum
[:SOURce<n>]:MOD:PWM:INTernal:FREQuency <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PWM:INTernal:FREQuency? [MINimum|MAXimum
[:SOURce<n>]:MOD:PWM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:PWM:INTernal:FUNCtion?

[:SOURce<n>]:MOD:PWM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:PWM:SOURce?


**[:SOURce<n>]:MOD[:STATe]**


**命令格式**


[:SOURce<n>]:MOD[:STATe] ON|OFF

[:SOURce<n>]:MOD[:STATe]?


**功能描述**


打开或关闭调制功能。

查询调制功能的开关状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**说明**


启用Mod时，Sweep或Burst功能将自动关闭（如果当前已打开）。


**返回格式**


返回ON或OFF。


**举例**


下面的命令打开调制功能：

```
:MOD ON
```


下面的查询返回ON。

```
:MOD?
```

**[:SOURce<n>]:MOD:TYPe**


**命令格式**


[:SOURce<n>]:MOD:TYPe AM|FM|PM|ASK|FSK|PSK|PWM|BPSK|QPSK|3FSK|4FSK|OSK

[:SOURce<n>]:MOD:TYPe?


**功能描述**


选择调制方式。

查询调制方式。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|AM|FM|PM|ASK|FSK|PSK|PWM|BPSK|QPSK|3FSK|4FSK|OSK|AM|


**说明**


PWM调制只在Pulse已打开时有效。

OSK调制只在Sine已打开时有效。


**返回格式**


返回AM、FM、PM、ASK、FSK、PSK、PWM、BPSK、QPSK、3FSK、4FSK或OSK。


**举例**


下面的命令选择FSK调制：

```
:MOD:TYPe FSK
```


下面的查询返回FSK。

```
:MOD:TYPe?
```

**[:SOURce<n>]:MOD:AM[:DEPTh]**


**命令格式**


[:SOURce<n>]:MOD:AM[:DEPTh] <depth>|MINimum|MAXimum

[:SOURce<n>]:MOD:AM[:DEPTh]? [MINimum|MAXimum
**功能描述**


以百分比形式设置AM调制深度 。

查询AM调制深度 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<depth>|连续实型|0%至120%|100%|


**说明**


<depth>可设置范围为0%至120%，支持不带%设置。

0%时，输出振幅是指定值的一半。

100%时，输出振幅等于指定的值。

大于100%时，仪器的输出不会超过10 Vpp（负载为50 Ω）。


**返回格式**


以科学计数形式返回调制深度值。


**举例**


下面的命令设置调制深度为80%：

```
:MOD:AM 80
```


下面的查询返回8.000000E+01。

```
:MOD:AM?
```


**[:SOURce<n>]:MOD:AM:INTernal:FREQuency**


**命令格式**


[:SOURce<n>]:MOD:AM:INTernal:FREQuency <frequency>|MINimum|MAXimum

[:SOURce<n>]:MOD:AM:INTernal:FREQuency? [MINimum|MAXimum
**功能描述**


设置AM调制波的频率，单位默认为“Hz”。

查询AM调制波的频率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|2 mHz至50 kHz|100 Hz|


**说明**


该命令仅在选择内部调制源时可用。


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令设置调制波的频率为25 Hz。

```
:MOD:AM:INTernal:FREQuency 25
```


下面的查询返回2.500000E+01。

```
:MOD:AM:INTernal:FREQuency?
```


**相关命令**


[:SOURce<n>]:MOD:AM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:AM:SOURce?


**[:SOURce<n>]:MOD:AM:INTernal:FUNCtion**


**命令格式**


[:SOURce<n>]:MOD:AM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:AM:INTernal:FUNCtion?


**功能描述**


选择AM调制波形。

查询AM调制波形。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER|SINusoid|


**说明**


该命令仅在选择内部调制源时可用。


**返回格式**


返回SIN、SQU、TRI、RAMP、NRAM、NOIS或USER。


**举例**


下面的命令选择方波为调制波形：

```
:MOD:AM:INTernal:FUNCtion SQUare
```


下面的查询返回SQU。

```
:MOD:AM:INTernal:FUNCtion?
```


**相关命令**


[:SOURce<n>]:MOD:AM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:AM:SOURce?

**[:SOURce<n>]:MOD:AM:SOURce**


**命令格式**


[:SOURce<n>]:MOD:AM:SOURce INTernal|EXTernal

[:SOURce<n>]:MOD:AM:SOURce?


**功能描述**


选择AM调制源类型 为内部（INTernal）或外部 （EXTernal）。

查询AM调制源类型 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|INTernal|EXTernal|INTernal|


**返回格式**


返回INT或EXT。


**举例**


下面的命令设置调制源类型为外部：

```
:MOD:AM:SOURce EXTernal
```


下面的查询返回EXT。

```
:MOD:AM:SOURce?
```

**[:SOURce<n>]:MOD:FM[:DEViation]**


**命令格式**


[:SOURce<n>]:MOD:FM[:DEViation] <deviation>|MINimum|MAXimum

[:SOURce<n>]:MOD:FM[:DEViation]? [MINimum|MAXimum
**功能描述**


设置FM调制 的频率偏差，单位默认为“Hz”。

查询FM调制 的频率偏差。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<deviation>|连续实型|见本页的“说明”|1 kHz|


**说明**


频率偏差<deviation>应满足以下条件：

● 小于或等于载波频率。

● 频率偏差 + 载波频率 ≤ 当前载波频率上限 + 1 kHz。


**返回格式**


查询以科学计数形式返回偏差数值。


**举例**


下面的命令设置频率偏差为800 Hz：

```
:MOD:FM 800
```


下面的查询返回8.000000E+02。

```
:MOD:FM?
```


**[:SOURce<n>]:MOD:FM:INTernal:FREQuency**


**命令格式**


[:SOURce<n>]:MOD:FM:INTernal:FREQuency <frequency>|MINimum|MAXimum

[:SOURce<n>]:MOD:FM:INTernal:FREQuency? [MINimum|MAXimum
**功能描述**


设置FM调制波的频率，单位默认为“Hz”。

查询FM调制波的频率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|2 mHz至50 kHz|100 Hz|


**说明**


该命令仅在选择内部调制源时可用。


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令设置调制波的频率为25 Hz。

```
:MOD:FM:INTernal:FREQuency 25
```


下面的查询返回2.500000E+01。

```
:MOD:FM:INTernal:FREQuency?
```


**相关命令**


[:SOURce<n>]:MOD:FM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:FM:SOURce?

**[:SOURce<n>]:MOD:FM:INTernal:FUNCtion**


**命令格式**


[:SOURce<n>]:MOD:FM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:FM:INTernal:FUNCtion?


**功能描述**


选择FM调制波形。

查询FM调制波形。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER|SINusoid|


**说明**


该命令仅在选择内部调制源时可用。


**返回格式**


返回SIN、SQU、TRI、RAMP、NRAM、NOIS或USER。


**举例**


下面的命令选择方波为调制波形：

```
:MOD:FM:INTernal:FUNCtion SQUare
```


下面的查询返回SQU。

```
:MOD:FM:INTernal:FUNCtion?
```


**相关命令**


[:SOURce<n>]:MOD:FM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:FM:SOURce?

**[:SOURce<n>]:MOD:FM:SOURce**


**命令格式**


[:SOURce<n>]:MOD:FM:SOURce INTernal|EXTernal

[:SOURce<n>]:MOD:FM:SOURce?


**功能描述**


选择FM调制源类型为内部（INTernal）或外部 （EXTernal）。

查询FM调制源类型 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|INTernal|EXTernal|INTernal|


**返回格式**


返回INT或EXT。


**举例**


下面的命令设置调制源类型为外部：

```
:MOD:FM:SOURce EXTernal
```


下面的查询返回EXT。

```
:MOD:FM:SOURce?
```


**[:SOURce<n>]:MOD:PM[:DEViation]**


**命令格式**


[:SOURce<n>]:MOD:PM[:DEViation] <deviation>|MINimum|MAXimum

[:SOURce<n>]:MOD:PM[:DEViation]? [MINimum|MAXimum
**功能描述**


设置PM调制的 相位偏差，单位默认为“°”。

查询PM调制的 相位偏差。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<deviation>|连续实型|0°至360°|90°|


**返回格式**


查询以科学计数形式返回相位偏差值。


**举例**


下面的命令设置相位偏差为180°：

```
:MOD:PM 180
```


下面的查询返回1.800000E+02。

```
:MOD:PM?
```


**[:SOURce<n>]:MOD:PM:INTernal:FREQuency**


**命令格式**


[:SOURce<n>]:MOD:PM:INTernal:FREQuency <frequency>|MINimum|MAXimum

[:SOURce<n>]:MOD:PM:INTernal:FREQuency?


**功能描述**


设置PM调制波的频率，单位默认为“Hz”。

查询PM调制波的频率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|2 mHz至50 kHz|100 Hz|


**说明**


该命令仅在选择内部调制源时可用。


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令设置调制波的频率为25 Hz。

```
:MOD:PM:INTernal:FREQuency 25
```


下面的查询返回2.500000E+01。

```
:MOD:PM:INTernal:FREQuency?
```


**相关命令**


[:SOURce<n>]:MOD:PM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:PM:SOURce?

**[:SOURce<n>]:MOD:PM:INTernal:FUNCtion**


**命令格式**


[:SOURce<n>]:MOD:PM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:PM:INTernal:FUNCtion?


**功能描述**


选择PM调制波形。

查询PM调制波形。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER|SINusoid|


**说明**


该命令仅在选择内部调制源时可用。


**返回格式**


返回SIN、SQU、TRI、RAMP、NRAM、NOIS或USER。


**举例**


下面的命令选择方波为调制波形：

```
:MOD:PM:INTernal:FUNCtion SQUare
```


下面的查询返回SQU。

```
:MOD:PM:INTernal:FUNCtion?
```


**相关命令**


[:SOURce<n>]:MOD:PM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:PM:SOURce?

**[:SOURce<n>]:MOD:PM:SOURce**


**命令格式**


[:SOURce<n>]:MOD:PM:SOURce INTernal|EXTernal

[:SOURce<n>]:MOD:PM:SOURce?


**功能描述**


选择PM调制源类型为内部（INTernal）或外部 （EXTernal）。

查询PM调制源类型 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|INTernal|EXTernal|INTernal|


**返回格式**


返回INT或EXT。


**举例**


下面的命令设置调制源类型为外部：

```
:MOD:PM:SOURce EXTernal
```


下面的查询返回EXT。

```
:MOD:PM:SOURce?
```

**[:SOURce<n>]:MOD:ASKey:AMPLitude**


**命令格式**


[:SOURce<n>]:MOD:ASKey:AMPLitude <amplitude>|MINimum|MAXimum

[:SOURce<n>]:MOD:ASKey:AMPLitude? [MINimum|MAXimum
**功能描述**


设置ASK调制波的幅度，单位默认为“Vpp”。

查询ASK调制波的幅度。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<amplitude>|连续实型|0 Vpp至10 Vpp（高阻）|2 Vpp|


**返回格式**


以科学计数形式返回幅度值。


**举例**


下面的命令设置调制波的幅度为2.5 Vpp：

:MOD:ASKey:AMPLitude 2.5


下面的查询返回2.500000E+00。

```
:MOD:ASKey:AMPLitude?
```

**[:SOURce<n>]:MOD:ASKey:INTernal[:RATE]**


**命令格式**


[:SOURce<n>]:MOD:ASKey:INTernal[:RATE] <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:ASKey:INTernal[:RATE]? [MINimum|MAXimum
**功能描述**


设置ASK速率，单位默认为“Hz”。

查询ASK速率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|2 mHz至1 MHz|100 Hz|


**说明**


该命令仅在选择内部调制源时可用。


**返回格式**


以科学计数形式返回速率值。


**举例**


下面的命令设置ASK速率为500 Hz。

```
:MOD:ASKey:INTernal 500
```


下面的查询返回5.000000E+02。

```
:MOD:ASKey:INTernal?
```


**相关命令**


[:SOURce<n>]:MOD:ASKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:ASKey:SOURce? 


**[:SOURce<n>]:MOD:ASKey:POLarity**


**命令格式**


[:SOURce<n>]:MOD:ASKey:POLarity POSitive|NEGative

[:SOURce<n>]:MOD:ASKey:POLarity?


**功能描述**


选择由调制波的正极性或负极性控制幅度输出。

查询ASK调制极性。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|POSitive|NEGative|POSitive|


**返回格式**


返回POS或NEG。


**举例**


下面的命令设置由调制波的负极性控制幅度输出：

```
:MOD:ASKey:POLarity NEGative
```


下面的查询返回NEG。

```
:MOD:ASKey:POLarity?
```

**[:SOURce<n>]:MOD:ASKey:SOURce**


**命令格式**


[:SOURce<n>]:MOD:ASKey:SOURce INTernal|EXTernal

[:SOURce<n>]:MOD:ASKey:SOURce?


**功能描述**


选择ASK调制源类型为内部（INTernal）或外部 （EXTernal）。

查询ASK调制源类型 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|INTernal|EXTernal|INTernal|


**返回格式**


返回INT或EXT。


**举例**


下面的命令设置调制源类型为外部：

```
:MOD:ASKey:SOURce EXTernal
```


下面的查询返回EXT。

```
:MOD:ASKey:SOURce?
```

**[:SOURce<n>]:MOD:FSKey[:FREQuency]**


**命令格式**


[:SOURce<n>]:MOD:FSKey[:FREQuency] <frequency>|MINimum|MAXimum

[:SOURce<n>]:MOD:FSKey[:FREQuency]? [MINimum|MAXimum
**功能描述**


设置FSK跳跃频率。

查询FSK跳跃频率 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|见本页“说明”|100 Hz|


**说明**


载波波形不同，可设置的频率范围<frequency>不同：

正弦波：1 μHz至160 MHz

方波：1 μHz至50 MHz

锯齿波：1 μHz至4 MHz

任意波：1 μHz至40 MHz（内置波形DC除外）


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令设置FSK跳跃频率为300 Hz：

```
:MOD:FSKey 300
```


下面的查询返回3.000000E+02。

```
:MOD:FSKey?
```

**[:SOURce<n>]:MOD:FSKey:INTernal:RATE**


**命令格式**


[:SOURce<n>]:MOD:FSKey:INTernal:RATE <rate>|MINimum|MAXimum

[:SOURce<n>]:MOD:FSKey:INTernal:RATE? [MINimum|MAXimum
**功能描述**


设置FSK速率，单位默认为“Hz”。

查询FSK速率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|2 mHz至1 MHz|100 Hz|


**说明**


该命令仅在选择内部调制源时可用。


**返回格式**


以科学计数形式返回速率值。


**举例**


下面的命令设置FSK速率为150 Hz。

```
:MOD:FSKey:INTernal:RATE 150
```


下面的查询返回1.500000E+02。

```
:MOD:FSKey:INTernal:RATE?
```


**相关命令**


[:SOURce<n>]:MOD:FSKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:FSKey:SOURce?  


**[:SOURce<n>]:MOD:FSKey:POLarity**


**命令格式**


[:SOURce<n>]:MOD:FSKey:POLarity POSitive|NEGative

[:SOURce<n>]:MOD:FSKey:POLarity?


**功能描述**


选择由调制波的正极性或负极性控制频率输出。

查询FSK调制极性。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|POSitive|NEGative|POSitive|


**返回格式**


返回POS或NEG。


**举例**


下面的命令设置由调制波的负极性控制相位输出：

```
:MOD:FSKey:POLarity NEGative
```


下面的查询返回NEG。

```
:MOD:FSKey:POLarity?
```

**[:SOURce<n>]:MOD:FSKey:SOURce**


**命令格式**


[:SOURce<n>]:MOD:FSKey:SOURce INTernal|EXTernal

[:SOURce<n>]:MOD:FSKey:SOURce?


**功能描述**


选择FSK调制源类型为内部（INTernal）或外部 （EXTernal）。

查询FSK调制源类型 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|INTernal|EXTernal|INTernal|


**返回格式**


返回INT或EXT。


**举例**


下面的命令设置调制源类型为外部：

```
:MOD:FSKey:SOURce EXTernal
```


下面的查询返回EXT。

```
:MOD:FSKey:SOURce?
```

**[:SOURce<n>]:MOD:PSKey:INTernal:RATE**


**命令格式**


[:SOURce<n>]:MOD:PSKey:INTernal:RATE <rate>|MINimum|MAXimum

[:SOURce<n>]:MOD:PSKey:INTernal:RATE? [MINimum|MAXimum
**功能描述**


设置PSK速率，单位默认为“Hz”。

查询PSK速率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<rate>|连续实型|2 mHz至1 MHz|100 Hz|


**说明**


该命令仅在选择内部调制源时可用。


**返回格式**


以科学计数形式返回速率值。


**举例**


下面的命令设置PSK速率为150 Hz。

```
:MOD:PSKey:INTernal:RATE 150
```


下面的查询返回1.500000E+02。

```
:MOD:PSKey:INTernal:RATE?
```


**相关命令**


[:SOURce<n>]:MOD:PSKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:PSKey:SOURce?

**[:SOURce<n>]:MOD:PSKey:PHASe**


**命令格式**


[:SOURce<n>]:MOD:PSKey:PHASe <phase>|MINimum|MAXimum

[:SOURce<n>]:MOD:PSKey:PHASe [MINimum|MAXimum
**功能描述**


设置PSK调制波的相位。

查询PSK调制波的相位。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<phase>|连续实型|0°至360°|180°|


**返回格式**


以科学计数形式返回相位值。


**举例**


下面的命令设置PSK调制波的相位为90°：

```
:MOD:PSKey:PHASe 90
```


下面的查询返回9.000000E+01。

```
:MOD:PSKey:PHASe?
```

**[:SOURce<n>]:MOD:PSKey:POLarity**


**命令格式**


[:SOURce<n>]:MOD:PSKey:POLarity POSitive|NEGative

[:SOURce<n>]:MOD:PSKey:POLarity?


**功能描述**


选择由调制波的正极性或负极性控制相位输出。

查询PSK调制极性。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|POSitive|NEGative|POSitive|


**返回格式**


返回POS或NEG。


**举例**


下面的命令设置由调制波的负极性控制相位输出：

```
:MOD:PSKey:POLarity NEGative
```


下面的查询返回NEG。

```
:MOD:PSKey:POLarity?
```

**[:SOURce<n>]:MOD:PSKey:SOURce**


**命令格式**


[:SOURce<n>]:MOD:PSKey:SOURce INTernal|EXTernal

[:SOURce<n>]:MOD:PSKey:SOURce?


**功能描述**


选择PSK调制源类型为内部（INTernal）或外部 （EXTernal）。

查询PSK调制源类型 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|INTernal|EXTernal|INTernal|


**返回格式**


返回INT或EXT。


**举例**


下面的命令设置调制源类型为外部：

```
:MOD:PSKey:SOURce EXTernal
```


下面的查询返回EXT。

```
:MOD:PSKey:SOURce?
```

**[:SOURce<n>]:MOD:BPSKey:DATA**


**命令格式**


[:SOURce<n>]:MOD:BPSKey:DATA 01|10|PN15|PN21
[:SOURce<n>]:MOD:BPSKey:DATA?


**功能描述**


设置BPSK调制的调制源。

查询BPSK调制的调制源。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|01|10|PN15|PN21|PN15|


**返回格式**


返回01、10、PN15或PN21。


**举例**


下面的命令设置调制源为PN21：

```
:MOD:BPSKey:DATA PN21
```


下面的查询返回PN21。

```
:MOD:BPSKey:DATA?
```


**[:SOURce<n>]:MOD:BPSKey:INTernal:RATE**


**命令格式**


[:SOURce<n>]:MOD:BPSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:BPSKey:INTernal:RATE? [MINimum|MAXimum
**功能描述**


设置BPSK速率。

查询BPSK速率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<rate>|连续实型|2 mHz至1 MHz|100 Hz|


**返回格式**


以科学计数形式返回速率值。


**举例**


下面的命令设置BPSK速率为150 Hz。

```
:MOD:BPSKey:INTernal:RATE 150
```


下面的查询返回1.500000E+02。

```
:MOD:BPSKey:INTernal:RATE?
```


**[:SOURce<n>]:MOD:BPSKey:PHASe**


**命令格式**


[:SOURce<n>]:MOD:BPSKey:PHASe <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:BPSKey:PHASe? [MINimum|MAXimum
**功能描述**


设置BPSK相位。

查询BPSK相位。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<phase>|连续实型|0°至360°|180°|


**返回格式**


以科学计数形式返回相位值。


**举例**


下面的命令设置BPSK相位为90°：

```
:MOD:BPSKey:PHASe 90
```


下面的查询返回9.000000E+01。

```
:MOD:BPSKey:PHASe?
```

**[:SOURce<n>]:MOD:QPSKey:DATA**


**命令格式**


[:SOURce<n>]:MOD:QPSKey:DATA PN15|PN21
[:SOURce<n>]:MOD:QPSKey:DATA?


**功能描述**


设置QPSK调制的调制源。

查询QPSK调制的调制源。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|PN15|PN21|PN15|


**返回格式**


返回PN15或PN21。


**举例**


下面的命令设置调制源为PN21：

```
:MOD:QPSKey:DATA PN21
```


下面的查询返回PN21。

```
:MOD:QPSKey:DATA?
```


**[:SOURce<n>]:MOD:QPSKey:INTernal:RATE**


**命令格式**


[:SOURce<n>]:MOD:QPSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:INTernal:RATE? [MINimum|MAXimum
**功能描述**


设置QPSK速率。

查询QPSK速率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<rate>|连续实型|2 mHz至1 MHz|100 Hz|


**返回格式**


以科学计数形式返回速率值。


**举例**


下面的命令设置QPSK速率为150 Hz。

```
:MOD:QPSKey:INTernal:RATE 150
```


下面的查询返回1.500000E+02。

```
:MOD:QPSKey:INTernal:RATE?
```

**[:SOURce<n>]:MOD:QPSKey:PHASe1**


**命令格式**


[:SOURce<n>]:MOD:QPSKey:PHASe1 <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:PHASe1? [MINimum|MAXimum
**功能描述**


设置QPSK调制 相位1。

查询QPSK调制 相位1。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<phase>|连续实型|0°至360°|45°|


**返回格式**


以科学计数形式返回相位值。


**举例**


下面的命令设置QPSK调制相位1为90°：

```
:MOD:QPSKey:PHASe1 90
```


下面的查询返回9.000000E+01。

```
:MOD:QPSKey:PHASe1?
```


**[:SOURce<n>]:MOD:QPSKey:PHASe2**


**命令格式**


[:SOURce<n>]:MOD:QPSKey:PHASe2 <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:PHASe2? [MINimum|MAXimum
**功能描述**


设置QPSK调制 相位2。

查询QPSK调制 相位2。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<phase>|连续实型|0°至360°|135°|


**返回格式**


以科学计数形式返回相位值。


**举例**


下面的命令设置QPSK调制相位2为180°：

```
:MOD:QPSKey:PHASe2 180
```


下面的查询返回1.800000E+02。

```
:MOD:QPSKey:PHASe2?
```

**[:SOURce<n>]:MOD:QPSKey:PHASe3**


**命令格式**


[:SOURce<n>]:MOD:QPSKey:PHASe3 <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:PHASe3? [MINimum|MAXimum
**功能描述**


设置QPSK调制 相位3。

查询QPSK调制 相位3。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<phase>|连续实型|0°至360°|225°|


**返回格式**


以科学计数形式返回相位值。


**举例**


下面的命令设置QPSK调制相位3为280°：

```
:MOD:QPSKey:PHASe3 280
```


下面的查询返回2.800000E+02。

```
:MOD:QPSKey:PHASe3?
```

**[:SOURce<n>]:MOD:3FSKey[:FREQuency]** 


**命令格式**


[:SOURce<n>]:MOD:3FSKey[:FREQuency] <n>,<frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:3FSKey[:FREQuency]? <n>[,MINimum|MAXimum
**功能描述**


设置3FSK调制 的跳跃频率。

查询3FSK调制 的跳跃频率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<n>|整型|1至2|1|
|<frequency>|连续实型|见本页“说明”|100 Hz|


**说明**


载波波形不同，可设置的频率范围<frequency>不同：

正弦波：1 μHz至160 MHz

方波：1 μHz至50 MHz

锯齿波：1 μHz至4 MHz

任意波：1 μHz至40 MHz（内置波形DC除外）


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令设置3FSK跳跃频率1为300 Hz：

```
:MOD:3FSKey 1, 300
```


下面的查询返回3.000000E+02。

```
:MOD:3FSKey? 1
```

**[:SOURce<n>]:MOD:3FSKey:INTernal:RATE**


**命令格式**


[:SOURce<n>]:MOD:3FSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:3FSKey:INTernal:RATE? [MINimum|MAXimum
**功能描述**


设置3FSK键控频率。

查询3FSK键控频率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<rate>|连续实型|2 mHz至1 MHz|100 Hz|


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令设置3FSK键控频率为150 Hz。

```
:MOD:3FSKey:INTernal:RATE 150
```


下面的查询返回1.500000E+02。

```
:MOD:3FSKey:INTernal:RATE?
```

**[:SOURce<n>]:MOD:4FSKey[:FREQuency]** 


**命令格式**


[:SOURce<n>]:MOD:4FSKey[:FREQuency] <n>,<frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:4FSKey[:FREQuency]? <n>[,MINimum|MAXimum
**功能描述**


设置4FSK调制 的跳跃频率。

查询4FSK调制 的跳跃频率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<n>|整型|1至3|1|
|<frequency>|连续实型|见本页“说明”|100 Hz|


**说明**


载波波形不同，可设置的频率范围<frequency>不同：

正弦波：1 μHz至160 MHz

方波：1 μHz至50 MHz

锯齿波：1 μHz至4 MHz

任意波：1 μHz至40 MHz（内置波形DC除外）


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令设置4FSK跳跃频率1为300 Hz：

```
:MOD:4FSKey 1, 300
```


下面的查询返回3.000000E+02。

```
:MOD:4FSKey? 1
```

**[:SOURce<n>]:MOD:4FSKey:INTernal:RATE**


**命令格式**


[:SOURce<n>]:MOD:4FSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:4FSKey:INTernal:RATE? [MINimum|MAXimum
**功能描述**


设置4FSK键控频率。

查询4FSK键控频率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<rate>|连续实型|2 mHz至1 MHz|100 Hz|


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令设置4FSK键控频率为150 Hz。

```
:MOD:4FSKey:INTernal:RATE 150
```


下面的查询返回1.500000E+02。

```
:MOD:4FSKey:INTernal:RATE?
```

**[:SOURce<n>]:MOD:OSKey:INTernal:RATE**


**命令格式**


[:SOURce<n>]:MOD:OSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:OSKey:INTernal:RATE? [MINimum|MAXimum
**功能描述**


设置OSK键控频率，单位默认为“Hz”。

查询OSK键控频率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<rate>|连续实型|2 mHz至1 MHz|1 kHz|


**说明**


该命令仅在选择内部调制源时可用。


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令设置OSK键控频率为500 Hz。

```
:MOD:OSKey:INTernal:RATE 500
```


下面的查询返回5.000000E+02。

```
:MOD:OSKey:INTernal:RATE?
```


**相关命令**


[:SOURce<n>]:MOD:OSKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:OSKey:SOURce? 

**[:SOURce<n>]:MOD:OSKey:SOURce**


**命令格式**


[:SOURce<n>]:MOD:OSKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:OSKey:SOURce? 


**功能描述**


选择OSK调制源类型为内部（INTernal）或外部 （EXTernal）。

查询OSK调制源类型 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|INTernal|EXTernal|INTernal|


**返回格式**


返回INT或EXT。


**举例**


下面的命令设置调制源类型为外部：

```
:MOD:OSKey:SOURce EXTernal
```


下面的查询返回EXT。

```
:MOD:OSKey:SOURce?
```

**[:SOURce<n>]:MOD:OSKey:TIME**


**命令格式**


[:SOURce<n>]:MOD:OSKey:TIME <time>|MINimum|MAXimum 
[:SOURce<n>]:MOD:OSKey:TIME? [MINimum|MAXimum
**功能描述**


设置OSK调制 的震荡周期。

查询OSK调制 的震荡周期。


**参数**


|名称|类型|范围<sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<time>|连续实型|8 ns至200 s|100 μs|

注<sup>1</sup>：震荡周期的可设置范围受当前的键控频率限制。


**返回格式**


以科学计数形式返回周期值。


**举例**


下面的命令设置OSK震荡周期为150 μs：

:MOD:OSKey:TIME 0.00015


下面的查询返回1.500000E-04。

```
:MOD:OSKey:TIME?
```

**[:SOURce<n>]:MOD:PWM[:DEViation]:DCYCle**


**命令格式**


[:SOURce<n>]:MOD:PWM[:DEViation]:DCYCle <percent>|MINimum|MAXimum

[:SOURce<n>]:MOD:PWM[:DEViation]:DCYCle? [MINimum|MAXimum
**功能描述**


设置PWM调制的占空比偏差。

查询PWM调制的占空比偏差。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<percent>|连续实型|0%至50%|20%|


**说明**


占空比偏差<percent>满足下列条件：

不能超过当前脉冲的占空比。

受到最小占空比和当前边沿时间的限制。


**返回格式**


以科学计数形式返回占空比偏差值。


**举例**


下面的命令设置占空比偏差为45%：

:MOD:PWM:DCYCle 45%


下面的查询返回4.500000E+01。

```
:MOD:PWM:DCYCle?
```


**[:SOURce<n>]:MOD:PWM[:DEViation][:WIDTh]**


**命令格式**


[:SOURce<n>]:MOD:PWM[:DEViation][:WIDTh] <deviation>|MINimum|MAXimum

[:SOURce<n>]:MOD:PWM[:DEViation][:WIDTh]? [MINimum|MAXimum
**功能描述**


设置PWM调制的脉宽偏差 。

查询PWM调制的脉宽偏差 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<deviation>|连续实型|0 ns至500 ks|200 μs|


**说明**


脉宽偏差<deviation>满足下列条件：

脉宽偏差不能超过当前的脉冲宽度。

脉宽偏差受到最小脉冲宽度和当前边沿时间设置的限制。


**返回格式**


以科学计数形式返回当前脉宽偏差。


**举例**


下面的命令设置脉宽偏差为10 μs：

:MOD:PWM 0.00001


下面的查询返回1.000000E-05。

```
:MOD:PWM?
```

**[:SOURce<n>]:MOD:PWM:INTernal:FREQuency**


**命令格式**


[:SOURce<n>]:MOD:PWM:INTernal:FREQuency <frequency>|MINimum|MAXimum

[:SOURce<n>]:MOD:PWM:INTernal:FREQuency?


**功能描述**


设置PWM调制波的频率。

查询PWM调制波的频率。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<frequency>|连续实型|2 mHz至50 kHz|100 Hz|


**返回格式**


以科学计数形式返回频率值。


**举例**


下面的命令设置PWM调制波的频率为300 Hz：

```
:MOD:PWM:INTernal:FREQuency 300
```


下面的查询返回3.000000E+02。

```
:MOD:PWM:INTernal:FREQuency?
```


**[:SOURce<n>]:MOD:PWM:INTernal:FUNCtion**


**命令格式**


[:SOURce<n>]:MOD:PWM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:PWM:INTernal:FUNCtion?


**功能描述**


选择PWM调制波形。

查询PWM调制波形。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER|SINusoid|


**说明**


该命令仅在选择内部调制源时可用。


**返回格式**


返回SIN、SQU、TRI、RAMP、NRAM、NOIS或USER。


**举例**


下面的命令选择方波为调制波形：

```
:MOD:PWM:INTernal:FUNCtion SQUare
```


下面的查询返回SQU。

```
:MOD:PWM:INTernal:FUNCtion?
```


**相关命令**


[:SOURce<n>]:MOD:PWM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:PWM:SOURce?

**[:SOURce<n>]:MOD:PWM:SOURce**


**命令格式**


[:SOURce<n>]:MOD:PWM:SOURce INTernal|EXTernal

[:SOURce<n>]:MOD:PWM:SOURce?


**功能描述**


选择PWM调制源类型为内部（INTernal）或外部 （EXTernal）。

查询PWM调制源类型 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|INTernal|EXTernal|INTernal|


**返回格式**


返回INT或EXT。


**举例**


下面的命令设置调制源类型为外部：

```
:MOD:PWM:SOURce EXTernal
```


下面的查询返回EXT。

```
:MOD:PWM:SOURce?
```
### **[:SOURce<n>]:PERiod**


[:SOURce<n>]:PERiod[:FIXed] <period> 
[:SOURce<n>]:PERiod[:FIXed]?


**[:SOURce<n>]:PERiod[:FIXed]**


**命令格式**


[:SOURce<n>]:PERiod[:FIXed] <period>

[:SOURce<n>]:PERiod[:FIXed]?


**功能描述**


设置基本波的周期，单位默认为“s”。

查询基本波的周期。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<period>|连续实型|见本页“说明”|1 ms|


**说明**


不同波形对应的周期范围不同。

正弦波：6.2 ns至1.0000 Ms

方波：20.0 ns至1.0000 Ms

锯齿波：250.0 ns至1.0000 Ms

脉冲波：25.0 ns至1.0000 Ms

任意波：25.0 ns至1.0000 Ms

谐波：12.5 ns至1.0000 Ms


**返回格式**


以科学计数形式返回周期值。


**举例**


下面的命令设置周期为100 ms。

:PERiod 0.1


下面的查询返回1.000000E-01。

```
:PERiod?
```
### **[:SOURce<n>]:PHASe**
### **　

[:SOURce<n>]:PHASe[:ADJust] <phase>|MINimum|MAXimum 
[:SOURce<n>]:PHASe[:ADJust]? [MINimum|MAXimum
-------------------------------------------------------------------
### [:SOURce<n>]:PHASE:INITiate
**[:SOURce<n>]:PHASe[:ADJust]**


**命令格式**


[:SOURce<n>]:PHASe[:ADJust] <phase>|MINimum|MAXimum

[:SOURce<n>]:PHASe[:ADJust]? [MINimum|MAXimum
**功能描述**


设置基本波的起始相位。

查询起始相位。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<phase>|连续实型|0° 至 360°|0° |


**返回格式**


以科学计数形式返回相位值。


**举例**


下面的命令设置起始相位为90°：

```
:PHASe 90
```


下面的查询返回9.000000E+01。

```
:PHASe?
```

**[:SOURce<n>]:PHASe:INITiate**


**命令格式**


[:SOURce<n>]:PHASe:INITiate


**功能描述**


执行同相位操作。


**说明**


在两个通道中，任一通道处于调制模式时，此设置无效。
### **[:SOURce<n>]:PULSe**
### **　
[:SOURce<n>]:PULSe:DCYCle <percent>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:DCYCle? [MINimum|MAXimum
---------------------------------------------------------------
[:SOURce<n>]:PULSe:DELay <delay>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:DELay? [MINimum|MAXimum
--------------------------------------------------------------
[:SOURce<n>]:PULSe:HOLD WIDTh|DUTY 
[:SOURce<n>]:PULSe:HOLD?
-----------------------------------------
[:SOURce<n>]:PULSe:TRANsition[:LEADing] <seconds>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:TRANsition[:LEADing]? [MINimum|MAXimum
-------------------------------------------------------------------------------
[:SOURce<n>]:PULSe:TRANsition:TRAiling <seconds>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:TRANsition:TRAiling? [MINimum|MAXimum
----------------------------------------------------------------------------
[:SOURce<n>]:PULSe:WIDTh <seconds>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:WIDTh? [MINimum|MAXimum
--------------------------------------------------------------
**[:SOURce<n>]:PULSe:DCYCle**


**命令格式**


[:SOURce<n>]:PULSe:DCYCle <percent>|MINimum|MAXimum

[:SOURce<n>]:PULSe:DCYCle? [MINimum|MAXimum
**功能描述**


设置脉冲占空比，以%表示。

查询脉冲占空比。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<percent>|连续实型|见本页的“说明”|50%|


**说明**


与脉宽相关联，修改其中一个参数将自动修改另一个参数。

脉冲占空比受“最小脉冲宽度（4 ns）”和“脉冲周期”限制：

`    `脉冲占空比 ≥ 100 × 最小脉冲宽度 ÷ 脉冲周期

`    `脉冲占空比 ≤ 100 ×（1 - 2 × 最小脉冲宽度 ÷ 脉冲周期）


**返回格式**


以科学计数形式返回占空比数值。


**举例**


下面的命令将脉冲的占空比设置为60%：

```
:PULSe:DCYCle 60
```


下面的查询返回6.000000E+01。

```
:PULSe:DCYCle?
```


**相关命令**


[:SOURce<n>]:PULSe:HOLD WIDTh|DUTY 
[:SOURce<n>]:PULSe:HOLD?

[:SOURce<n>]:PULSe:WIDTh <seconds>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:WIDTh? [MINimum|MAXimum
**[:SOURce<n>]:PULSe:DELay**


**命令格式**


[:SOURce<n>]:PULSe:DELay <delay>|MINimum|MAXimum

[:SOURce<n>]:PULSe:DELay? [MINimum|MAXimum
**功能描述**


设置脉冲延时时间，单位默认为“s”。

查询脉冲的延时时间


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<delay>|连续实型|0 ns 至 脉冲周期|0 ns|


**返回格式**


以科学计数形式返回脉冲延时。


**举例**


下面的命令将脉冲的延时时间设置为8 ms：

:PULSe:DELay 0.008


下面的查询返回8.000000E-03。

```
:PULSe:DELay?
```

**[:SOURce<n>]:PULSe:HOLD**


**命令格式**


[:SOURce<n>]:PULSe:HOLD WIDTh|DUTY

[:SOURce<n>]:PULSe:HOLD?


**功能描述**


选中脉冲波的脉宽或占空比 。

查询当前选中的脉冲波参数。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|离散型|WIDTh|DUTY|DUTY|


**说明**


脉冲占空比与脉宽相关联，修改其中一个参数将自动修改另一个参数。 


**返回格式**


返回WIDT或DUTY。


**举例**


下面的命令选中脉宽：

```
:PULSe:HOLD WIDTh
```


下面的查询返回WIDT。

```
:PULSe:HOLD?
```


**相关命令**


[:SOURce<n>]:PULSe:DCYCle <percent>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:DCYCle? [MINimum|MAXimum
[:SOURce<n>]:PULSe:WIDTh <seconds>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:WIDTh? [MINimum|MAXimum
**[:SOURce<n>]:PULSe:TRANsition[:LEADing]**


**命令格式**


[:SOURce<n>]:PULSe:TRANsition[:LEADing] <seconds>|MINimum|MAXimum

[:SOURce<n>]:PULSe:TRANsition[:LEADing]? [MINimum|MAXimum
**功能描述**


设置脉冲上升沿时间，单位默认为“s”。

查询脉冲的上升沿时间。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<seconds>|连续实型|见本页“说明”|1\.9531 μs|


**说明**


可设置范围受当前指定的脉宽限制，限制关系为满足不等式：上升/下降沿时间 ≤ 0.625 × 脉宽

当所设置的数值超出限定值，DG4000自动调整边沿时间以适应指定的脉宽。


**返回格式**


以科学计数形式返回时间值，单位默认为“s”。


**举例**


下面的命令设置上升沿时间为10 μs：

:PULSe:TRANsition 0.00001


下面的查询返回1.000000E-05。

```
:PULSe:TRANsition?
```


**[:SOURce<n>]:PULSe:TRANsition:TRAiling**


**命令格式**


[:SOURce<n>]:PULSe:TRANsition:TRAiling <seconds>|MINimum|MAXimum

[:SOURce<n>]:PULSe:TRANsition:TRAiling? [MINimum|MAXimum
**功能描述**


设置脉冲下降沿时间，单位默认为“s”。

查询脉冲的下降沿时间。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<seconds>|连续实型|见本页“说明”|1\.9531 μs|


**说明**


可设置范围受当前指定的脉宽限制，限制关系为满足不等式：上升/下降沿时间 ≤ 0.625 × 脉宽

当所设置的数值超出限定值，DG4000自动调整边沿时间以适应指定的脉宽。


**返回格式**


以科学计数形式返回时间值，单位默认为“s”。


**举例**


下面的命令设置下降沿时间为10 μs：

:PULSe:TRANsition:TRAiling 0.00001


下面的查询返回1.000000E-05。

```
:PULSe:TRANsition:TRAiling?
```


**[:SOURce<n>]:PULSe:WIDTh**


**命令格式**


[:SOURce<n>]:PULSe:WIDTh <seconds>|MINimum|MAXimum

[:SOURce<n>]:PULSe:WIDTh? [MINimum|MAXimum
**功能描述**


设置脉冲的脉宽，单位默认为“s”。

查询脉冲的脉宽。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<seconds>|连续实型|见本页“说明”|500 μs|


**说明**


与占空比相关联，修改其中一个参数将自动修改另一个参数。

受“最小脉冲宽度（4 ns）”和“脉冲周期”的限制。

`    `脉冲宽度 ≥ 最小脉冲宽度

`    `脉冲宽度 ≤ 脉冲周期 - 2 × 最小脉冲宽度


**返回格式**


以科学计数形式返回脉宽值。


**举例**


下面的命令将脉冲的脉宽设置为600 μs：

:PULSe:WIDTh 0.0006


下面的查询返回6.000000E-04。

```
:PULSe:WIDTh?
```


**相关命令**


[:SOURce<n>]:PULSe:HOLD WIDTh|DUTY 
[:SOURce<n>]:PULSe:HOLD?

[:SOURce<n>]:PULSe:DCYCle <percent>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:DCYCle? [MINimum|MAXimum
### **[:SOURce<n>]:SWEep**
### **　
[:SOURce<n>]:SWEep:HTIMe:STARt <seconds>|MINimum|MAXimum 
[:SOURce<n>]:SWEep:HTIMe:STARt? [MINimum|MAXimum
--------------------------------------------------------------------
[:SOURce<n>]:SWEep:HTIMe:STOP <seconds>|MINimum|MAXimum 
[:SOURce<n>]:SWEep:HTIMe:STOP? [MINimum|MAXimum
-------------------------------------------------------------------
[:SOURce<n>]:SWEep:RTIMe <seconds>|MINimum|MAXimum 
[:SOURce<n>]:SWEep:RTIMe? [MINimum|MAXimum
--------------------------------------------------------------
[:SOURce<n>]:SWEep:SPACing LINear|LOGarithmic|STEp 
[:SOURce<n>]:SWEep:SPACing?
------------------------------------------------------
[:SOURce<n>]:SWEep:STATe ON|OFF 
[:SOURce<n>]:SWEep:STATe?
------------------------------------------
[:SOURce<n>]:SWEep:STEP <steps>|MINimum|MAXimum

[:SOURce<n>]:SWEep:STEP? [MINimum|MAXimum
[:SOURce<n>]:SWEep:TIME <seconds>|MINimum|MAXimum 
[:SOURce<n>]:SWEep:TIME? [MINimum|MAXimum
-------------------------------------------------------------
### [:SOURce<n>]:SWEep:TRIGger[:IMMediate
[:SOURce<n>]:SWEep:TRIGger:SLOPe POSitive|NEGative 
[:SOURce<n>]:SWEep:TRIGger:SLOPe?             
---------------------------------------------------------------
[:SOURce<n>]:SWEep:TRIGger:SOURce INTernal|EXTernal|MANual 
[:SOURce<n>]:SWEep:TRIGger:SOURce?
--------------------------------------------------------------
[:SOURce<n>]:SWEep:TRIGger:TRIGOut OFF|POSitive|NEGative 
[:SOURce<n>]:SWEep:TRIGger:TRIGOut?
------------------------------------------------------------
### **　
**[:SOURce<n>]:SWEep:HTIMe:STARt**


**命令格式**


[:SOURce<n>]:SWEep:HTIMe:STARt <seconds>|MINimum|MAXimum

[:SOURce<n>]:SWEep:HTIMe:STARt? [MINimum|MAXimum
**功能描述**


设置扫频的起始保持时间，单位默认为“s”。

查询扫频的起始保持时间。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<seconds>|连续实型|0 s 至 300 s|0 s|


**返回格式**


以科学计数形式返回时间值。


**举例**


下面的命令设置起始保持时间为1 s：

```
:SWEep:HTIMe:STARt 1
```


查询返回1.000000E+00。

```
:SWEep:HTIMe:STARt?
```

**[:SOURce<n>]:SWEep:HTIMe:STOP**


**命令格式**


[:SOURce<n>]:SWEep:HTIMe:STOP <seconds>|MINimum|MAXimum

[:SOURce<n>]:SWEep:HTIMe:STOP? [MINimum|MAXimum
**功能描述**


设置扫频的终止保持时间，单位默认为“s”。

查询扫频的终止保持时间。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<seconds>|连续实型|0 s 至 300 s|0 s|


**返回格式**


以科学计数形式返回时间值。


**举例**


下面的命令设置终止保持时间为1 s：

```
:SWEep:HTIMe:STOP 1
```


查询返回1.000000E+00。

```
:SWEep:HTIMe:STOP?
```

**[:SOURce<n>]:SWEep:RTIMe**


**命令格式**


[:SOURce<n>]:SWEep:RTIMe <seconds>|MINimum|MAXimum

[:SOURce<n>]:SWEep:RTIMe? [MINimum|MAXimum
**功能描述**


设置扫频的返回时间，单位默认为“s”。

查询扫频的返回时间。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<seconds>|连续实型|0 s 至 300 s|0 s|


**返回格式**


以科学计数形式返回时间值。


**举例**


下面的命令设置返回时间为5 s：

```
:SWEep:RTIMe 5
```


查询返回5.000000E+00。

```
:SWEep:RTIMe?
```

**[:SOURce<n>]:SWEep:SPACing**


**命令格式**


[:SOURce<n>]:SWEep:SPACing LINear|LOGarithmic|STEp

[:SOURce<n>]:SWEep:SPACing?


**功能描述**


选择扫频类型为线性（LINear）、对数 （LOGarithmic）或步进 （STEp）。

查询扫频类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|LINear|LOGarithmic|STEp|LINear|


**返回格式**


返回LIN、LOG或STE。


**举例**


下面的命令选择对数扫频：

```
:SWEep:SPACing LOGarithmic
```


查询返回LOG。

```
:SWEep:SPACing?
```

**[:SOURce<n>]:SWEep:STATe**


**命令格式**


[:SOURce<n>]:SWEep:STATe ON|OFF

[:SOURce<n>]:SWEep:STATe?


**功能描述**


打开或关闭扫频功能。

查询扫频功能的状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**说明**


启用Sweep后，Mod和Burst功能将自动关闭（如果当前已打开）。


**返回格式**


返回OFF或ON。


**举例**


下面的命令打开扫频功能：

```
:SWEep:STATe ON
```


下面的查询返回ON。

```
:SWEep:STATe?
```

**[:SOURce<n>]:SWEep:STEP**


**命令格式**


[:SOURce<n>]:SWEep:STEP <steps>|MINimum|MAXimum

[:SOURce<n>]:SWEep:STEP? [MINimum|MAXimum
**功能描述**


设置步进扫频的步进数。

查询步进扫频的步进数。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<steps>|整型|2 至 2048|2|


**返回格式**


以科学计数形式返回步进数。


**举例**


下面的命令设置步进数为5：

```
:SWEep:STEP 5
```


查询返回5.000000E+00。

```
:SWEep:STEP?
```

**[:SOURce<n>]:SWEep:TIME**


**命令格式**


[:SOURce<n>]:SWEep:TIME <seconds>|MINimum|MAXimum

[:SOURce<n>]:SWEep:TIME? [MINimum|MAXimum
**功能描述**


设置扫频时间，单位默认为“s”。

查询扫频时间。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<seconds>|连续实型|1 ms至300 s|1 s|


**返回格式**


以科学计数形式返回时间值。


**举例**


下面的命令设置扫频时间为5 s：

```
:SWEep:TIME 5
```


下面的查询返回5.000000E+00。

```
:SWEep:TIME?
```

**[:SOURce<n>]:SWEep:TRIGger[:IMMediate]**


**命令格式**


[:SOURce<n>]:SWEep:TRIGger[:IMMediate
**功能描述**


使仪器立即触发。


**说明**


该命令仅在触发源为手动模式时有效。


**相关命令**


[:SOURce<n>]:SWEep:TRIGger:SOURce INTernal|EXTernal|MANual 
[:SOURce<n>]:SWEep:TRIGger:SOURce?

**[:SOURce<n>]:SWEep:TRIGger:SLOPe**


**命令格式**


[:SOURce<n>]:SWEep:TRIGger:SLOPe POSitive|NEGative

[:SOURce<n>]:SWEep:TRIGger:SLOPe?


**功能描述**


选择信号发生器在外部触发信号的上升沿（POSitive）或下降沿 （NEGative）时启动扫频输出。

查询扫频输出的外部触发信号的边沿类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|POSitive|NEGative|POSitive|


**说明**


该命令仅在外部触发源时有效。


**返回格式**


返回POS或NEG。


**举例**


下面的命令设置边沿类型为下降沿 ：

```
:SWEep:TRIGger:SLOPe NEGative
```


下面的查询返回NEG。

```
:SWEep:TRIGger:SLOPe?
```


**相关命令**


[:SOURce<n>]:SWEep:TRIGger:SOURce INTernal|EXTernal|MANual 
[:SOURce<n>]:SWEep:TRIGger:SOURce?

**[:SOURce<n>]:SWEep:TRIGger:SOURce**


**命令格式**


[:SOURce<n>]:SWEep:TRIGger:SOURce INTernal|EXTernal|MANual

[:SOURce<n>]:SWEep:TRIGger:SOURce?


**功能描述**


选择扫频触发源的类型为内部（INTernal）、外部（EXTernal）或手动（MANual）。

查询扫频触发源的类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|` `INTernal|EXTernal|MANual|INTernal|


**返回格式**


返回INT、EXT或MAN。


**举例**


下面的命令设置触发源类型为手动 ：

```
:SWEep:TRIGger:SOURce MANual
```


下面的查询返回MAN。

```
:SWEep:TRIGger:SOURce?
```


**[:SOURce<n>]:SWEep:TRIGger:TRIGOut**


**命令格式**


[:SOURce<n>]:SWEep:TRIGger:TRIGOut OFF|POSitive|NEGative

[:SOURce<n>]:SWEep:TRIGger:TRIGOut?


**功能描述**


设置扫频触发输出的边沿类型为上升沿（POSitive）或下降沿（NEGative），或关闭触发输出信号（OFF）。

查询扫频触发输出的边沿类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|OFF|POSitive|NEGative|OFF|


**说明**


触发源为内部或手动模式时有效。


**返回格式**


返回OFF，POS或NEG。


**举例**


下面的命令设置输出下降沿 ：

```
:SWEep:TRIGger:TRIGout NEGative
```


下面的查询返回NEG。

```
:SWEep:TRIGger:TRIGout?
```


**相关命令**


[:SOURce<n>]:SWEep:TRIGger:SOURce INTernal|EXTernal|MANual 
[:SOURce<n>]:SWEep:TRIGger:SOURce?


### **[:SOURce<n>]:VOLTage**


[:SOURce<n>]:VOLTage[:LEVel][:IMMediate][:AMPLitude] <amplitude>|MINimum|MAXimum 
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate][:AMPLitude]? [MINimum|MAXimum
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:HIGH <voltage>|MINimum|MAXimum 
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:HIGH? [MINimum|MAXimum
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:LOW <voltage>|MINimum|MAXimum 
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:LOW? [MINimum|MAXimum
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:OFFSet <voltage>|MINimum|MAXimum 
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:OFFSet? [MINimum|MAXimum
[:SOURce<n>]:VOLTage:UNIT VPP|VRMS|DBM 
[:SOURce<n>]:VOLTage:UNIT?   


**[:SOURce<n>]:VOLTage[:LEVel][:IMMediate][:AMPLitude]**


**命令格式**


[:SOURce<n>]:VOLTage[:LEVel][:IMMediate][:AMPLitude] <amplitude>|MINimum|MAXimum

[:SOURce<n>]:VOLTage[:LEVel][:IMMediate][:AMPLitude]? [MINimum|MAXimum
**功能描述**


设置基本波的幅度，单位默认为“Vpp”。

查询基本波的幅度值。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<amplitude>|连续实型|见本页“说明”|5 Vpp|


**说明**


幅度范围受“阻抗”和“频率/周期”设置的限制，请参见本产品用户手册。


**返回格式**


以科学计数形式返回幅度值。


**举例**


下面的命令设置幅度为2.5 Vpp：

:VOLTage 2.5


下面的查询返回2.500000E+00。

```
:VOLTage?
```


**[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:HIGH**


**命令格式**


[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:HIGH <voltage>|MINimum|MAXimum

[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:HIGH? [MINimum|MAXimum
**功能描述**


设置基本波的高电平，单位默认为“V”。

查询基本波的高电平。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<voltage>|连续实型|当前的低电平 至 10 V（高阻）/5 V（50 Ω）|2\.5 V|


**返回格式**


以科学计数形式返回高电平值。


**举例**


下面的命令将高电平设置为5 V：

```
:VOLTage:HIGH 5
```


下面的查询返回5.000000E+00。

```
:VOLTage:HIGH?
```


**相关命令**


[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:LOW <voltage>|MINimum|MAXimum 
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:LOW? [MINimum|MAXimum
**[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:LOW**


**命令格式**

[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:LOW <voltage>|MINimum|MAXimum

[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:LOW? [MINimum|MAXimum
**功能描述**


设置基本波的低电平，单位默认为“V”。

查询基本波的低电平。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<voltage>|连续实型|-10 V（高阻）/-5 V（50 Ω）至 当前的高电平 |-2.5 V|


**返回格式**


以科学计数形式返回低电平值。


**举例**


下面的命令将低电平设置为-5 V：

:VOLTage:LOW -5


下面的查询返回-5.000000E+00。

```
:VOLTage:LOW?
```


**相关命令**


[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:HIGH <voltage>|MINimum|MAXimum 
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:HIGH? [MINimum|MAXimum
**[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:OFFSet**


**命令格式**


[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:OFFSet <voltage>|MINimum|MAXimum

[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:OFFSet? [MINimum|MAXimum
**功能描述**


设置直流偏移电压，单位默认为“V<sub>DC</sub>”。

查询直流偏移电压值。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<voltage>|连续实型|见本页“说明”|0 V<sub>DC</sub>|


**说明**


偏移范围受“阻抗”和“幅度/高电平”设置的限制，请参见本产品用户手册。


**返回格式**


以科学计数形式返回偏移电压值。


**举例**


下面的命令设置偏移电压为100 mV<sub>DC</sub>：

:VOLTage:OFFSet 0.1


下面的查询返回1.000000E-01。

```
:VOLTage:OFFSet?
```


**[:SOURce<n>]:VOLTage:UNIT**


**命令格式**


[:SOURce<n>]:VOLTage:UNIT VPP|VRMS|DBM

[:SOURce<n>]:VOLTage:UNIT?


**功能描述**


设置幅度的单位为VPP、VRMS或DBM。

查询幅度的单位。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|VPP|VRMS|DBM|VPP|


**说明**


当阻抗为“高阻”时，DBM不可用。


**返回格式**


返回VPP、VRMS或DBM。


**举例**


下面的命令设置幅度的单位为VRMS：

```
:VOLTage:UNIT VRMS
```


下面的查询返回VRMS。

```
:VOLTage:UNIT?
```


## **SYSTem命令子系统**


```
:SYSTem:BEEPer[:IMMediate
:SYSTem:BEEPer:STATe ON|OFF
:SYSTem:BEEPer:STATe?
```

```
:SYSTem:COMMunicate:LAN:AUTOip[:STATe] ON|OFF
:SYSTem:COMMunicate:LAN:AUTOip[:STATe]?
```

```
:SYSTem:COMMunicate:LAN:DHCP[:STATe] ON|OFF
:SYSTem:COMMunicate:LAN:DHCP[:STATe]?
```

```
:SYSTem:COMMunicate:LAN:DNS <address>
:SYSTem:COMMunicate:LAN:DNS?
```

```
:SYSTem:COMMunicate:LAN:GATEway <address>
:SYSTem:COMMunicate:LAN:GATEway?
```

```
:SYSTem:COMMunicate:LAN:IPADdress <ip_addr>
:SYSTem:COMMunicate:LAN:IPADdress?
```

```
:SYSTem:COMMunicate:LAN:MAC?
```

```
:SYSTem:COMMunicate:LAN:SMASk <mask>
:SYSTem:COMMunicate:LAN:SMASk?
```

```
:SYSTem:COMMunicate:LAN:STATic[:STATe] ON|OFF
:SYSTem:COMMunicate:LAN:STATic[:STATe]?
```

```
:SYSTem:COMMunicate:USB:INFormation?
```

```
:SYSTem:COMMunicate:USB[:SELF]:CLASs COMPuter|PRINter
:SYSTem:COMMunicate:USB[:SELF]:CLASs?
```

```
:SYSTem:CSCopy CH1|CH2,CH2|CH1
```

```
:SYSTem:CWCopy CH1|CH2,CH2|CH1
```

```
:SYSTem:ERRor?
```

```
:SYSTem:KLOCk[:STATe] ON|OFF
:SYSTem:KLOCk[:STATe]?
```

```
:SYSTem:LANGuage ENGLish|SCHinese
:SYSTem:LANGuage?
```

```
:SYSTem:POWeron DEFault|LAST
:SYSTem:POWeron?
```

```
:SYSTem:POWSet AUTO|USER
:SYSTem:POWSet?
```

```
:SYSTem:PRESet DEFault|USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```

```
:SYSTem:RESTART
```

```
:SYSTem:ROSCillator:SOURce INTernal|EXTernal
:SYSTem:ROSCillator:SOURce?
```

```
:SYSTem:SHUTDOWN
```

```
:SYSTem:VERSion?
```

**:SYSTem:BEEPer[:IMMediate]**


**命令格式**


```
:SYSTem:BEEPer[:IMMediate
```
**功能描述**


蜂鸣器立即产生一次蜂鸣。


**说明**


该命令仅在蜂鸣器已打开时（参考:SYSTem:BEEPer:STATe ON|OFF 命令）有效。


**相关命令**


```
:SYSTem:BEEPer:STATe ON|OFF
:SYSTem:BEEPer:STATe?
```

**:SYSTem:BEEPer:STATe**


**命令格式**


```
:SYSTem:BEEPer:STATe ON|OFF
```

```
:SYSTem:BEEPer:STATe?
```


**功能描述**


打开或关闭蜂鸣器。

查询蜂鸣器的状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|ON|


**返回格式**


返回ON或OFF。


**举例**


下面的命令打开蜂鸣器：

```
:SYSTem:BEEPer:STATe ON
```


下面的查询返回ON。

```
:SYSTem:BEEPer:STATe?
```

**:SYSTem:COMMunicate:LAN:AUTOip[:STATe]**


**命令格式**


```
:SYSTem:COMMunicate:LAN:AUTOip[:STATe] ON|OFF
```

```
:SYSTem:COMMunicate:LAN:AUTOip[:STATe]?
```


**功能描述**


打开或关闭自动IP模式（AUTOIP）。

查询AUTOIP模式的状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|ON|


**返回格式**


返回ON或OFF。


**举例**


下面的命令打开AUTOIP模式 ：

```
:SYSTem:COMMunicate:LAN:AUTOip ON
```


下面的查询返回ON。

```
:SYSTem:COMMunicate:LAN:AUTOip?
```

**:SYSTem:COMMunicate:LAN:DHCP[:STATe]**


**命令格式**


```
:SYSTem:COMMunicate:LAN:DHCP[:STATe] ON|OFF
```

```
:SYSTem:COMMunicate:LAN:DHCP[:STATe]?
```


**功能描述**


打开或关闭动态IP模式（DHCP）。

查询动态IP模式（DHCP）状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|ON|


**说明**


该模式下，由当前网络中的DHCP服务器向信号发生器分配IP地址等网络参数。


**返回格式**


返回ON或OFF。


**举例**


下面的命令打开DHCP模式 ：

```
:SYSTem:COMMunicate:LAN:DHCP ON
```


下面的查询返回ON。

```
:SYSTem:COMMunicate:LAN:DHCP?
```

**:SYSTem:COMMunicate:LAN:DNS**


**命令格式**


```
:SYSTem:COMMunicate:LAN:DNS <address>
```

```
:SYSTem:COMMunicate:LAN:DNS?
```


**功能描述**


为信号发生器设置DNS地址。

查询DNS地址。


**参数**


|名称|类型|范围<sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<address>|ASCII字符串|0\.0.0.0至255.255.255.255|——|

注<sup>1</sup>：根据TCP/IP协议，DNS的有效范围为0.0.0.0至223.255.255.255且第一段数值不能为127。


**说明**


该命令仅在手动IP模式打开（参考:SYSTem:COMMunicate:LAN:STATic[:STATe] ON|OFF 命令）时可用。

该设置仅在仪器已正确连接至LAN时有效。

一般说来，用户不需要设置网络中的域名服务器地址，因此该参数设置可以忽略。


**返回格式**


查询命令返回当前域名服务器地址，格式为nnn.nnn.nnn.nnn。


**举例**


下面的命令将DNS地址设置为202.106.46.151。

:SYSTem:COMMunicate:LAN:DNS 202.106.46.151


下面的查询返回202.106.46.151。

```
:SYSTem:COMMunicate:LAN:DNS?
```


**相关命令**


```
:SYSTem:COMMunicate:LAN:STATic[:STATe] ON|OFF
:SYSTem:COMMunicate:LAN:STATic[:STATe]?
```

**:SYSTem:COMMunicate:LAN:GATEway**


**命令格式**


```
:SYSTem:COMMunicate:LAN:GATEway <address>
```

```
:SYSTem:COMMunicate:LAN:GATEway?
```


**功能描述**


为信号发生器设置默认网关。

查询默认网关。


**参数**


|名称|类型|范围<sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<address>|ASCII字符串|0\.0.0.0至255.255.255.255|——|

注<sup>1</sup>：根据TCP/IP协议， 默认网关的有效范围为0.0.0.0至223.255.255.255且第一段数值不能为127。


**说明**


该命令仅在手动IP模式打开（参考:SYSTem:COMMunicate:LAN:STATic[:STATe] ON|OFF 命令）时可用。

该设置仅在仪器已正确连接至LAN时有效。


**返回格式**


查询命令返回当前默认网关，格式为nnn.nnn.nnn.nnn。


**举例**


下面的命令将默认网关设置为172.16.3.1。

:SYSTem:COMMunicate:LAN:GATEway 172.16.3.1


下面的查询返回172.16.3.1。

```
:SYSTem:COMMunicate:LAN:GATEway?
```

**:SYSTem:COMMunicate:LAN:IPADdress**


**命令格式**


:SYSTem:COMMunicate:LAN:IPADdress <ip\_addr>

```
:SYSTem:COMMunicate:LAN:IPADdress?
```


**功能描述**


为信号发生器设置IP地址。

查询IP地址。


**参数**


|名称|类型|范围<sup>1</sup>|默认值|
| :-: | :-: | :-: | :-: |
|<ip\_addr>|ASCII字符串|0\.0.0.0至255.255.255.255|——|

注<sup>1</sup>：根据TCP/IP协议，DNS的有效范围为0.0.0.0至223.255.255.255且第一段数值不能为127。


**说明**


该命令仅在手动IP模式打开（参考:SYSTem:COMMunicate:LAN:STATic[:STATe] ON|OFF 命令）时可用。

该设置仅在仪器已正确连接至LAN时有效。


**返回格式**


查询命令返回当前IP地址，格式为nnn.nnn.nnn.nnn。


**举例**


下面的命令将IP地址设置为172.16.3.145。

:SYSTem:COMMunicate:LAN:IPADdress 172.16.3.145


下面的查询返回172.16.3.145。

```
:SYSTem:COMMunicate:LAN:IPADdress?
```


**相关命令**


```
:SYSTem:COMMunicate:LAN:STATic[:STATe] ON|OFF
:SYSTem:COMMunicate:LAN:STATic[:STATe]?
```

**:SYSTem:COMMunicate:LAN:MAC?**


**命令格式**


```
:SYSTem:COMMunicate:LAN:MAC?
```


**功能描述**


查询MAC地址。


**返回格式**


返回MAC地址，如：00-14-0E-42-12-CF。

**:SYSTem:COMMunicate:LAN:SMASk**


**命令格式**


```
:SYSTem:COMMunicate:LAN:SMASk <mask>
```

```
:SYSTem:COMMunicate:LAN:SMASk?
```


**功能描述**


为信号发生器设置子网掩码。

查询子网掩码。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<mask>|ASCII字符串|0\.0.0.0至255.255.255.255|——|


**说明**


该命令仅在手动IP模式打开（参考:SYSTem:COMMunicate:LAN:STATic[:STATe] ON|OFF 命令）时可用。

该设置仅在仪器已正确连接至LAN时有效。


**返回格式**


查询命令返回当前子网掩码，格式为nnn.nnn.nnn.nnn。


**举例**


下面的命令将子网掩码设置为255.255.255.0。

:SYSTem:COMMunicate:LAN:SMASk 255.255.255.0


下面的查询返回255.255.255.0。

```
:SYSTem:COMMunicate:LAN:SMASk?
```


**相关命令**


```
:SYSTem:COMMunicate:LAN:STATic[:STATe] ON|OFF
:SYSTem:COMMunicate:LAN:STATic[:STATe]?
```

**:SYSTem:COMMunicate:LAN:STATic[:STATe]**


**命令格式**


```
:SYSTem:COMMunicate:LAN:STATic[:STATe] ON|OFF
```

```
:SYSTem:COMMunicate:LAN:STATic[:STATe]?
```


**功能描述**


打开或关闭手动IP模式（ManualIP）。

查询返ManualIP模式 的状态。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**说明**


该模式下，由用户自定义信号发生器的IP地址等网络参数。


**返回格式**


返回ON或OFF。


**举例**


下面的命令打开ManualIP模式。

```
:SYSTem:COMMunicate:LAN:STATic ON
```


下面的查询返回ON。

```
:SYSTem:COMMunicate:LAN:STATic?
```

**:SYSTem:COMMunicate:USB:INFormation?**


**命令格式**


```
:SYSTem:COMMunicate:USB:INFormation?
```


**功能描述**


查询USB信息。


**返回格式**


以字符串形式返回USB信息，如：:USB0::0X1AB1::0X0640::DG41620000::INSTR。

**:SYSTem:COMMunicate:USB[:SELF]:CLASs**


**命令格式**


```
:SYSTem:COMMunicate:USB[:SELF]:CLASs COMPuter|PRINter
```

```
:SYSTem:COMMunicate:USB[:SELF]:CLASs?
```


**功能描述**


设置USB Device接口连接的仪器类型为计算机（COMPuter）或打印机（PRINter）。

查询USB Device接口连接的仪器类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|COMPuter|PRINter|COMPuter|


**说明**


DG4000在其后面板提供一个USB Device接口。该接口可以连接计算机（COMPuter）以实现远程控制，或连接打印机（PRINter）以打印屏幕 内容。


**返回格式**


返回COMP或PRIN。


**举例**


下面的命令将仪器类型设置为计算机（COMPuter）。

```
:SYSTem:COMMunicate:USB:CLASs COMPuter
```


下面的查询返回COMP。

```
:SYSTem:COMMunicate:USB:CLASs?
```

**:SYSTem:CSCopy**


**命令格式**


```
:SYSTem:CSCopy CH1,CH2|CH2,CH1
```


**功能描述**


将CH1（CH2）的配置 状态复制到CH2（CH1） 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|CH1,CH2|CH2,CH1|CH1,CH2|


**说明**


DG4000支持两个通道间的状态或波形复制功能，即将其中一个通道的状态（参数和输出配置）或任意波形参数复制到另一个通道，或交换两个通道的状态。

状态包括通道的波形（易失波形除外）和波形参数（频率、幅度等）、功能（调制、扫频、脉冲串等）、输出配置（同步、阻抗、极性等）。

耦合状态下不能复制。


**举例**


下面的命令将CH1的配置 状态复制到CH2。

```
:SYSTem:CSCopy CH1,CH2
```

**:SYSTem:CWCopy**


**命令格式**


```
:SYSTem:CWCopy CH1|CH2,CH2|CH1
```


**功能描述**


将CH1（CH2）的 任意波数据（不包括波形的参数）复制到CH2（CH1） 。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|CH1,CH2|CH2,CH1|CH1,CH2|


**说明**


DG4000支持两个通道间的状态或波形复制功能，即将其中一个通道的状态（参数和输出配置）或任意波形参数复制到另一个通道，或交换两个通道的状态。

波形复制仅在两个通道都选择任意波时有效。

耦合状态下不能复制。


**举例**


下面的命令将CH1的波形复制到CH2。

```
:SYSTem:CWCopy CH1,CH2
```

**:SYSTem:ERRor?**


**命令格式**


```
:SYSTem:ERRor?
```


**功能描述**


查询错误事件队列。


**返回格式**


返回错误事件信息，例如：-113, "Undefined header; keyword cannot be found"。

如果没有错误，则返回：0, "No Error"。 

**:SYSTem:KLOCk**


**命令格式**


```
:SYSTem:KLOCk[:STATe] ON|OFF
```

```
:SYSTem:KLOCk[:STATe]?
```


**功能描述**


远程锁定或解锁前面板。

查询前面板是否处于远程锁定模式。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|布尔型|ON|OFF|OFF|


**说明**


前面板的远程锁定模式默认为关闭（OFF），屏幕右上角显示“!(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAARCAIAAABbzbuTAAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAmklEQVR42sWRUQ3EIBBE6wAcgAQccE6QgATqAAlIQQISkICE7aSbklyuQC+55N7XBmaWybBtv0VrLaX8wmCtLaU88rxOvPdEtPDgrtZK7+SchwbeGkJAnv6CEGJhcM5hVkrN1MYYFrXWoOPDmRo6npGHUw1jsBqivrWeLNRgv+Ci7g0pJbojxjiM1D2oyF4svpY9s74/4e7/zQH/Jo7hDZjVKAAAAABJRU5ErkJggg==)”图标 ，按 **Burst** 键返回本地操作模式。

前面板远程锁定模式打开时，屏幕右上角显示“!(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAARCAIAAABbzbuTAAAAAXNSR0IArs4c6QAAAANzQklUCAgI2+FP4AAAAAlwSFlzAAALEgAACxIB0t1+/AAAAXZJREFUKJFtkiGQ2zAQRV+nAQIGAgcOGhwo6izIdAIDDwYaFBgGHjQoMCgwPCgQYNDpGBwwNDggGCgYGGhwQHBBQIFqN3WiWbLa/1baL2GggdMUPXxhuaof1b+khABnaKGDI+xvAL2oO7i/yTCJLLyAh+YeMDMrCx4SHgEwICLdW5fn+TVWliWwMpBDARZKeITTiuF9sNaGEGKMwHa7TYz3nh6O4CFAhAjeWo2jXnTuPX6MetHiewF8PkMEndQZGNQ+PPBVfv3u0gnrb+uqqvq3fjmciJTgIT7l+to0P+u0bzJzYwSIyPgxmmR0ZnQtenAikqrPsId8oZ7vXcL4lOtGQvViYQ8euvlNZ/UMGKgzoyK62Tg4Tm9lYCUiycQk7fs+hABYY7gozhVwhlfoQIHhfUi970QcT2sZ4QTFdPlPJjNt2+52u5TXdT0PFmP0B1cqzzBCDce55g7ueobrZSdpt/jIibnjN1hooAVZFP779zfMIxj4A1smxqumAZf2AAAAAElFTkSuQmCC)”图标，按 **Burst** 键无法返回本地操作模式。


**返回格式**


返回ON或OFF。


**举例**


下面的命令打开远程锁定模式。

```
:SYSTem:KLOCk ON
```


下面的查询返回ON。

```
:SYSTem:KLOCk?
```


**:SYSTem:LANGuage**


**命令格式**


```
:SYSTem:LANGuage ENGLish|SCHinese
```

```
:SYSTem:LANGuage?
```


**功能描述**


设置系统语言为英文（ENGLish）或简体中文 （SCHinese）。

查询系统语言的类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|ENGLish|SCHinese|ENGLish|


**返回格式**


返回ENG或SCH。


**举例**


下面的命令将系统语言设置为英文。

```
:SYSTem:LANGuage ENGLish
```


下面的查询返回ENGL。

```
:SYSTem:LANGuage?
```

**:SYSTem:POWeron**


**命令格式**


```
:SYSTem:POWeron DEFault|LASt
```

```
:SYSTem:POWeron?
```


**功能描述**


选择在开机时仪器将要使用的配置为默认值（DEFault）或上次值 （LASt）。

查询仪器开机使用的配置类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|DEFault|LASt|DEFault（默认值）|


**返回格式**


返回DEFAULT或LAST。


**举例**


下面的命令将开机使用的配置类型设置为上次值（LASt） 。

```
:SYSTem:POWeron LASt
```


下面的查询返回LAST。

```
:SYSTem:POWeron?
```


**:SYSTem:POWSet**


**命令格式**


```
:SYSTem:POWSet AUTO|USER
:SYSTem:POWSet?
```


**功能描述**


选择通电时的开机方式为自动(AUTO)或手动(USER)。

查询通电时的开机方式。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|AUTO|USER|AUTO|


**说明**


自动（AUTO）：上电后，仪器自动开机。

手动（USER）：上电后，按下前面板电源开关，仪器开机。


**返回格式**


返回AUTO或USER。


**举例**


下面的命令将开机方式设置为手动(USER)。

```
:SYSTem:POWSet USER
```


下面的查询返回USER。

```
:SYSTem:POWSet?
```

**:SYSTem:PRESet**


**命令格式**


```
:SYSTem:PRESet DEFault|USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```


**功能描述**


将系统恢复到出厂默认状态（DEFault）或用户预设状态（USER1、USER2、USER3、USER4、USER5、USER6、USER7、USER8、USER9或USER10）。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|DEFault|USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10|DEFault|


**说明**


若恢复系统至用户预设状态，该命令仅当指定的存储位置已存储有效的状态文件时有效。


**举例**


下面的命令将系统恢复到出厂默认状态。

```
:SYSTem:PRESet DEFault
```

**:SYSTem:RESTART**


**命令格式**


```
:SYSTem:RESTART
```


**功能描述**


重新启动仪器。

**:SYSTem:ROSCillator:SOURce**


**命令格式**


```
:SYSTem:ROSCillator:SOURce INTernal|EXTernal
```

```
:SYSTem:ROSCillator:SOURce?
```


**功能描述**


设置参考时钟源的类型为内部（INTernal）或外部 （EXTernal） 。

查询参考时钟源的类型。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|INTernal|EXTernal|INTernal|


**说明**


DG4000提供内部10MHz的时钟源，也接受从后面板 **[10MHz In/Out]** 输入的外部时钟源，还可以从 **[10MHz In/Out]** 连接器输出时钟源，供其他设备使用。


**返回格式**


返回INT或EXT。


**举例**


下面的命令设置参考时钟源类型为外部(该设置在系统检测到外部时钟源时生效)。

```
:SYSTem:ROSCillator:SOURce EXTernal
```


下面的查询返回EXT。

```
:SYSTem:ROSCillator:SOURce?
```

**:SYSTem:SHUTDOWN**


**命令格式**


```
:SYSTem:SHUTDOWN
```


**功能描述**


关机。

**:SYSTem:VERSion?**


**命令格式**


```
:SYSTem:VERSion?
```


**功能描述**


查询并返回SCPI版本信息。


**返回格式**


返回SCPI版本信息，如：1999.0。
## **TRACe命令子系统**


[:TRACe]:DATA:DAC16 VOLATILE,<flag>,<binary_block_data>

[:TRACe]:DATA:DAC VOLATILE,[<binary_block_data>|<value>,<value>,<value>...
[:TRACe]:DATA[:DATA] VOLATILE,<value>{,<value>} 

[:TRACe]:DATA:POINts:INTerpolate LINear|OFF 
[:TRACe]:DATA:POINts:INTerpolate?

[:TRACe]:DATA:POINts VOLATILE,<value>|MINimum|MAXimum

[:TRACe]:DATA:POINts? VOLATILE[,MINimum|MAXimum
[:TRACe]:DATA:VALue? VOLATILE,<point>

[:TRACe]:DATA:VALue VOLATILE,<point>,<data>

[:TRACe]:DATA:LOAD? VOLATILE

[:TRACe]:DATA:LOAD? <num>


**[:TRACe]:DATA:DAC16**


**命令格式**


[:TRACe]:DATA:DAC16 VOLATILE,<flag>,<binary\_block\_data>


**功能描述**


下载大波表到DDRII中。


**说明**


该命令由两部分构成，一部分为命令字符串，包括“[:TRACe]:DATA:DAC16 VOLATILE,<flag>,”，另一部分为二进制数据，包括“<binary\_block\_data>”。

<flag>表示数据传输的状态，可设置为CON或END——CON表示本数据包后还有数据包；END表示本数据包为最后一个数据包，数据发送结束。

<binary\_block\_data>表示要 下载的二进制数据，其范围为0000至3FFF，数据长度必须为16 kpts（32 kBytes）。

二进制数据块之前用#号开头。

例如：发送命令**:DATA:DAC16 VOLATILE,CON,#532768二进制数**

**#**号之后的**5**表示数据长度信息**32768**共占5个字符；**32768**表示后续**二进制数**的字节数 。每个波形点占两个字节，所以字节数必须为偶数。

若收到的命令<flag>为END时,仪器自动切换到任意波输出。

若需要下载的波表总长度为16 kpts，且一次性下载至仪器时，用户可以在仪器本地编辑数据。否则不支持本地编辑。

**[:TRACe]:DATA:DAC**


**命令格式**


[:TRACe]:DATA:DAC VOLATILE,[<binary\_block\_data>|<value>,<value>,<value>...
**功能描述**


将二进制数据块或十进制DAC值下载到易失性存储器中。


**说明**


<binary\_block\_data>为要下载的二进制数据，其范围为0000至3FFF，数据长度为4 Bytes（2 pts）至32768 Bytes（16 kpts）。二进制数据块以#号开头。

例如：发送命令**:DATA:DAC VOLATILE,#516384二进制数**

**#**号之后的**5**表示数据长度信息**16384**共占5个字符；**16384**表示后续**二进制数**的字节数。每个波形点占两个字节，所以字节数必须为偶数。

<value>,<value>,<value>...表示要下载的十进制DAC值。当不以#开头时，则可以用字符串的形式发送十进制DAC值。

例如：发送命令**:DATA:DAC VOLATILE,0,16383,8192,0,16383**

共发送了5个数据点。

对于点数不足16384的数据，仪器会自动用均匀插值的方式扩展为16384个点。

发送该命令后，仪器自动切换当前通道输出易失波形，同时修改插值方式和可编辑点数。使用该命令下发的数据允许在仪器本地进行编辑。

**[:TRACe]:DATA[:DATA]**


**命令格式**


[:TRACe]:DATA[:DATA] VOLATILE,<value>{,<value>}


**功能描述**


将浮点电压值下载到易失性存储器中，浮点数范围-1到+1，数据长度不超过512 kpts。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<value>|连续实型|-1~1 |——|


**说明**


每次可以下载1到16384（16k）个点。

-1和1分别与波形的最大值和最小值对应（假设偏移为0）。例如：若幅度设置为5 Vpp，则1对应于2.5 V，-1对应于-2.5 V。

该命令会覆盖易失性存储器中的上一个波形（不生成错误）。

发送该命令后，仪器自动切换当前通道输出易失波形，同时修改插值方式和可编辑点数。使用该命令下发的数据允许在仪器本地进行编辑。 


**举例**


下面的命令下载4个点（-0.5，-0.25，0.25，0.5）到易失性存储器：

:DATA VOLATILE,-0.5,-0.25,0.25,0.5

**[:TRACe]:DATA:POINts:INTerpolate**


**命令格式**


[:TRACe]:DATA:POINts:INTerpolate LINear|OFF 
[:TRACe]:DATA:POINts:INTerpolate?


**功能描述**


设置在波形的定义点之间的插值方式。

查询插值方式。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|——|关键字|LINear|OFF |OFF |


**说明**


LINear：线性插值，波形编辑器会用一条直线将两个定义的点连接起来；

OFF：关闭插值方式，波形编辑器将在两点之间保持恒定的电压电平并建立一个阶梯状的波形。

仅当当前输出为易失波形时才可以修改插值类型。


**返回格式**


返回LINEAR或OFF。


**举例**


下面的命令选择线性插值方式。

```
:DATA:POINts:INTerpolate LINear
```


下面的查询返回LINEAR。

```
:DATA:POINts:INTerpolate?
```


**[:TRACe]:DATA:POINts**


**命令格式**


[:TRACe]:DATA:POINts VOLATILE,<value>|MINimum|MAXimum

[:TRACe]:DATA:POINts? VOLATILE[,MINimum|MAXimum
**功能描述**


设置编辑波形的初始化点数。

查询编辑波形的初始化点数。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<value>|整型|2至16384|——|


**说明**


该命令自动将当前输出更改为易失波形，并将易失波形初始化为0。

发送该命令后，您可以使用[:TRACe]:DATA:VALue VOLATILE,<point>,<data>命令修改指定点的电压。


**返回格式**


返回2至16384之间的一个整数 。

**[:TRACe]:DATA:VALue?**


**命令格式**


[:TRACe]:DATA:VALue? VOLATILE,<point>


**功能描述**


查询易失空间中某个点的十进制整数值。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<point>|整型|1至16384|——|


**说明**


该命令仅当当前输出为易失波形时有效。


**返回格式**


返回一个十进制数值。


**举例**


下面的命令查询点1的十进制整数值，返回0。

```
:DATA:VALue? VOLATILE,1
```


**[:TRACe]:DATA:VALue**


**命令格式**


[:TRACe]:DATA:VALue VOLATILE,<point>,<data>


**功能描述**


修改易失空间中某个点的十进制整数值。


**参数**


|名称|类型|范围|默认值|
| :-: | :-: | :-: | :-: |
|<point>|整型|1至16384|——|
|<data>|整型|0至16383|——|


**说明**


该命令仅当当前输出为易失波形时有效。


**举例**


下面的命令将点1修改成10：

```
:DATA:VALue VOLATILE,1,10
```


下面的查询返回10。

```
:DATA:VALue? VOLATILE,1
```


**相关命令**


[:TRACe]:DATA:VALue? VOLATILE,<points> 

**[:TRACe]:DATA:LOAD?**


**命令格式**


[:TRACe]:DATA:LOAD? VOLATILE

[:TRACe]:DATA:LOAD? <num>


**功能描述**


查询易失性存储器中任意波数据包的个数。

读取易失性存储器中的指定的数据包。


**说明**


首先发送[:TRACe]:DATA:LOAD? VOLATILE命令，来获取总数据包的个数，返回一个十进制数值。

然后发送[:TRACe]:DATA:LOAD? <num>命令读取第num个数据包的数据，其中，num的范围为1至数据包个数值。

**编程实例** 


本章列举了在Visual C++ 6.0、Visual Basic 6.0和LabVIEW 8.6开发环境中如何使用命令实现信号发生器常用功能的编程实例。这些实例都是基于NI（National Instrument）-VISA（Virtual Instrument Software Architecture）库编程实现的。


NI-VISA是美国国家仪器有限公司根据VISA标准编写的应用程序接口。您可以使用NI-VISA通过USB等仪器总线实现信号发生器与PC的通信。VISA定义了一套软件命令，用户无需了解接口总线如何工作，就可以对仪器进行控制。具体细节可参考NI-VISA的帮助。


本章内容包括：


编程准备

Visual C++ 6.0 编程实例

Visual Basic 6.0 编程实例

LabVIEW 8.6 编程实例


**编程准备**


首先确认您的电脑上是否已经安装NI的VISA库（可到NI网站下载<http://www.ni.com/visa/>）。本文中默认安装路径为：C:\Program Files\IVI Foundation\VISA。


本文应用信号发生器的USB Device接口与PC通信。请使用USB数据线将信号发生器后面板的USB Device接口与PC的USB 接口相连。


信号发生器首次与PC正确连接后，接通仪器电源，此时PC上将弹出“**硬件更新向导**”对话框，请按照向导的提示安装“USB Test and Measurement Device (IVI)”（安装步骤如下）。


1\. 选择“从列表或指定位置安装（高级）”；

2\. 点击“下一步”；

` `![image003.jpg](data:image/jpeg;base64,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)

3\. 选择“不要搜索。我要自己选择要安装的驱动程序”；

4\. 点击“下一步”；

` `![image004.jpg](data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAoHBwgHBgoICAgLCgoLDhgQDg0NDh0VFhEYIx8lJCIfIiEmKzcvJik0KSEiMEExNDk7Pj4+JS5ESUM8SDc9Pjv/2wBDAQoLCw4NDhwQEBw7KCIoOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozv/wAARCADvAUYDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDE043etSyTbod4Qyt5rAAKOTjPYVo3Wl6rZzWkEkEQkvDiFQo+bt6cY756VD4N1pdBeWcw+aZrfylBxhWJBDHPYYzgda25PFPna3pd9JPP5NkGVkMChju+++Qf4iBxxgD619pVliIVeSEPdS/T/M+fUKEouU5a37mJeWOrWLQi5tYo/PLBCQmDjHfpzkEc80TWGrW8QkuLeCEMqsnmNGC4Y4G3nmpZtUa6s9KikZVmtXklmkMWQHLhhjnJ6c1f1/xGmthQjSW0QkRjH5WXYoWwwbdgZ3ng9MDmj2mJvFOC630fcXs8Pq1L01M680zV9OgM97BbQQg48x3jxu/uccluDx7H0qM2esCCOX7D/rc7UEQLkAA524yBg9e9b+reKbK60O80+1F4ZZ4YUWWQn5Cm0EAlieRvyf55qBfEdiuopINPQIgG66MYMzYiVQFHbkEZJ6HpWcK+Kcbun+H9f10LlRwyduf8TLtdO1S7tre4jW0WO53eUZGRd2Dg9enI71ljUJCAQsZB/wBgVs6Tq8FlbW8VzYxSfZY5NhKmT5inygAn5Tv+YkHHtWK8bSO0j43OSxxnqfrXZS9q6klOOnQ5qioqCcXr1Hfb5f7sf/fAo+3y/wB2P/vgUzyKPIrq5DC8R/2+X+7H/wB8Cj7fL/dj/wC+BTPIo8ijkC8R/wBvl/ux/wDfAo+3y/3Y/wDvgUzyKPIo5AvEf9vl/ux/98D/AAo+3y/3Y/8Avgf4UzyKPIo5EF4j/t8v92P/AL4H+FH2+X+7H/3wP8KZ5FHkUciC8R/2+X+7H/3wP8KPt8v92P8A74H+FM8ijyKORBeI/wC3y/3Y/wDvgf4Ufb5f7sf/AHwP8KZ5FHkUciC8R/2+X+7H/wB8D/Cj7fL/AHY/++B/hTPIo8ijkQXiP+3y/wB2P/vgf4Ufb5f7sf8A3wP8KZ5FHkUciC8R39oS/wB2P/vgf4Uf2hL/AHY/++B/hTPINHkGjkC8R/8AaEv92P8A74H+FH9oS/3Y/wDvgf4UzyDR5Bo5AvEf/aEv92P/AL4H+FH9oS/3Y/8Avgf4UzyDR5Bo5AvEf/aEv92P/vgf4Uf2hL/dj/74H+FM8g0eQaOQLxH/ANoS/wB2P/vgf4Uf2hL/AHY/++B/hTPINHkGjkC8R/8AaEv92P8A74H+FH9oS/3Y/wDvgf4UzyDR5Bo5AvEV9Rlx92P/AL4H+FQNqU392P8A74H+FPeCoWt6fIaRcS5pfjnWPDUryWbIySjDRP8Acz/ewO/GM+9FYeoxBUUn1orzMThacql5RTZ6tCpaCSPXPCPgLQ9U8MWV9crc+dKh3bZiBwxHT8K2v+FaeHvS7/8AAg1a8Af8iRpv+43/AKG1dEc446187icZiI1ppTdrvr5nXToUnCLcVscl/wAKz8O/3bv/AMCDR/wrPw7/AHbv/wACDXER6/q934k0nyJb62jM+yWFZZfKLSTNHxu/hG3d3HOBjFN0/wARaynie1uoNUuJtPjM0bwjLiMeY2wbXIL7gqkNn5VcDPHOH17E/wDPx/eafV6X8qO5/wCFZ+Hf7t3/AOBBo/4Vn4d/u3f/AIEGuGnn1yfxnLMk+pT2zar5CCOd3jIEayEfJgcbei84LA+66jq2sf8ACV6gF8SSxxrdlcoJQioXChVCj5mOxR8qsB8xzmj69if+fj+8Pq9L+VHcf8Kz8O/3bv8A8CDR/wAKz8O/3bv/AMCDXEXmt6/PrF3Omp3kcdsbiV1EqquYpHSEKGUZXpuXkv19qz9f1nxPJ4hkMWr3sIItQ0UUvCuQCxIGAuPmyp/E0fXsT/z8f3h9Xpfyo9H/AOFZ+Hf7t3/4EGj/AIVn4d/u3f8A4EGuI8Saxr+n65p1uus3d4YYwZnsgdn+qGScPg8BmJOMZBwB1v69c+IU8aaXAl3qk1ttia5a3RkVgWRXaNVLEjB5PbJwTjNH17E/8/H94fV6X8qOo/4Vn4d/u3f/AIEGj/hWfh3+7d/+BBrkJtY163tNHuL24uryWSBWmtkunilicJgb0RcrksWLNlcADjINU/F+p69p1zYQWuuXlzFNaNG8lvI0hbIG6VSFAJA7DGAM+po+vYn/AJ+P7w+r0v5Ud3/wrPw7/du//Ag0f8Kz8O/3bv8A8CDXD+KNc1ucRpp+pXEN3JZQSvEswBlfe5K7lOxSFGTg8jaOSOb/AIr1DXb7RLK+0+W/kxBIJyr+QkjiRVTb83LFfMxtyc7TjpR9exP/AD8f3h9Xpfyo6n/hWfh3+7d/+BBo/wCFZ+Hf7t3/AOBBqLwXrkkOh6LYahbXsl9eCUSyCNnWFlZsrIx+62ABg967Oj69if8An4/vD6vS/lRyP/Cs/Dv927/8CDR/wrPw7/du/wDwINddRR9exP8Az8f3h9Xpfyo5H/hWfh3+7d/+BBo/4Vn4d/u3f/gQa66ij69if+fj+8Pq9L+VHI/8Kz8O/wB27/8AAg0f8Kz8O/3bv/wINddRR9exP/Px/eH1el/Kjkf+FZ+Hf7t3/wCBBo/4Vn4d/u3f/gQa66ij69if+fj+8Pq9L+VHI/8ACs/Dv927/wDAg0f8Kz8O/wB27/8AAg111FH17E/8/H94fV6X8qOR/wCFZ+Hf7t3/AOBBo/4Vn4d/u3f/AIEGuuoo+vYn/n4/vD6vS/lRyP8AwrPw7/du/wDwINH/AArPw7/du/8AwINddRR9exP/AD8f3h9Xpfyo5H/hWfh3+7d/+BBo/wCFZ+Hf7t3/AOBBrrqKPr2J/wCfj+8Pq9L+VHI/8Kz8O/3bv/wINH/Cs/Dv927/APAg111FH17E/wDPx/eH1el/Kjkf+FZ+Hf7t3/4EGj/hWfh3+7d/+BBrrqKPr2J/5+P7w+r0v5UeS6v/AMK10PVJ9Nv7nUEuYCA6gyMBkA9QPQ1S/tb4Vf8AP5qX/kT/AArO8SW5uPiP4qWPT4L+dYIzHDMm4H5ogxGCCMKTyOQM1l6X4T8O3+qA6jqH9kQw3P2e4tTOkpL44CSDop9SCPc13fWaiSvOWy6kewp/yr7jpTqnwpPW81H/AMif4Un9p/Cj/n71H/yJ/hXAXGgWV3cyw6RdGO5jcq1hesqSAg4IV/uv+h9jWLcWtxZXLW91BJBMh+ZJFKsPwNaRr1Jfbl9//AD2NP8AlR6Z8SNC0fSdI0a/0XzvK1ANJmVycrtUrwen3qKsfEr/AJEXwb/16D/0XHRXoYWcp0k5O71/NmUoxUmkj0rwB/yJGm/7jf8AobV0dc54A/5EjTf9xv8A0Nq6OvmsV/vE/V/mdVH+HH0QUhAPUA0tFc5oJRgelLRQAmM0YHpS0UAIAB0FLRRQAmBnOOaOlLRQAmBjGBj0owB2FLRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAHg+taZYaj8ZtVk1TUX0+ytCk00yEq2NqKAGH3clhz2rU+Ilv4Nk16xEen3k97dAMJ7F1WOXsoLN8rH1I9Peua8c6nFp3xM15bm1+02t0qwzRh9jbdqNlW7EFQehFJ4atbOa48jT9akudMlBMunTwK8qHsfKY4kA7mMhsdAK9CpF6S8l+RCKF9dRa54gnsdU0O4jvJ7hhFJbRCO4GScB4/uuenofeuu8ZeDT4Y+GIGoXp1C9F1GIpJB/qE5+RM8gY6jNdB4Tl0DQdAufFGpNIn2SWW1hEzs/lhTjbCHG5d2B8p5HTpmvKPGnjXUPGerfaLgmK0iJFvbA8Rj1Pqx7mpp805pJWSG9jtfiX/AMiL4N/69B/6Ljoo+Jf/ACIvg3/r0H/ouOivdwf8FfP82cs/iZ6P4CnhTwVpqtKikI3BYf3zXQ/aYP8AnvH/AN9iuT8Ef8ifp/8AuN/6Ea3q+Zxc/wDaKnq/zOmiv3cfRF77TB/z3j/77FH2mD/nvH/32Ko0Vzc5pYvfaYP+e8f/AH2KPtMH/PeP/vsVS6dRSUc4WL32mD/nvH/32KPtMH/PeP8A77FUaKOcLF77TB/z3j/77FH2mD/nvH/32Ko0vTtRzhYu/aYP+e8f/fYo+0wf894/++xVGijnCxe+0wf894/++xR9pg/57x/99iqX4UfhRzhYu/aYP+e8f/fYo+0wf894/wDvsVS/Cj8KOcLF37TB/wA94/8AvsUfaYP+e8f/AH2KpfhSUc4WL32mD/nvH/32KPtMH/PeP/vsVRoo5wsXvtMH/PeP/vsUfaYP+e8f/fYqjRRzhYvfaYP+e8f/AH2KPtMH/PeP/vsVRoo5wsXvtMH/AD3j/wC+xR9pg/57x/8AfYqjRRzhYvfaYP8AnvH/AN9ij7TB/wA94/8AvsVRoo5wsXvtMH/PeP8A77FH2mD/AJ7x/wDfYqjRRzhYvfaYP+e8f/fYo+0wf894/wDvsVRoo5wsXvtMH/PeP/vsUfaYP+e8f/fYqjRRzhYvfaYP+e8f/fYo+0wf894/++xVGijnCx5h4x+Fep+I/FV9q1tqumxw3LKVWSVgwwoHOFPpWKPglrakMutaSCDkETPx/wCO17TRXUsbNJKyFyI8l1D4W+L9Wt4LfUPFFhcxWwIiWW4c7c/8B5Puaof8KR1rP/IZ0n/v6/8A8TXtNFCxs1skHIjyv4sWxsfC3hexaWOWS1iMLtGcqWVEBx+VFT/Gr/jz0j/rpL/JaK+iwD5sNF+v5s5Knxs6/wAEf8ifp/8AuN/6Ea3qwfBH/In6f/uN/wChGt6vmcX/ALxU9X+Z00f4cfRBVTUmK26AyNHE0irM6nBVO/PYZwCewNW6CMjB5BrnTs7mjV0URBb294kNkzEPExmjifOOPlYejE9PX8K5fSdVmkuLjfd3Dv5BmWKbUFYB/nHllAdx+4BxznJ7iuxxb2cDviOCJAWcgBQB3JrDj8ZaK8koSOXzIYDcH90oyACeDnrhTVN3YkrGfDqd2txdumrSYW0by4JWRSJAuQrblDArk/N/Fx3BzRtNZ1Bopki1EzstmdxMnCkF8kAqCWwygY9MknArorHxNYalcTRRWUzyxhiwRY5GbawU42sT/EPwzUg8QaetvcXQsbxILYN50v2XAQqcMp75H8qkZiTalINP1qJdbLNaxM2JLhBlgx+4ygNgqq/i5GKj8CXzRXN6dQ1YPGip/wAfVzk/MxII3HAxjGfpW4vifRzbpMIpPnDlUEG5yVIyMLnnBDemOTjFEvijQ4rSW4yXVGAVVgOZQW2hkyMMpPfOOKAMmfVLyfwkfs2r2ouWlVY5Iph5igykfPnOe3Ax+VZNtqevS6TqFydVlRg6rHCW3SM2D8y8ghT1PXofrXWw+JtIlhluViljt4nKNM8AUFgu7A7n06dSB3pjeLtF+w297GXlW4ysapD824KDtOenB+nX3pgczJqGsjwcjte3Mkxmj+SVWExULuOGVj8pBXkgZ5PcVb03U9R/4R20kbUFjH21gXZtzkFGdQSzYwD0zjOB267LeMrOJGZrG9AAfcAi5wnB4zzyCOOmDmnN4t0hI7f7Sk0L3MjRiF4csCpK/MBnAyOP/rGgDmI9U1OTRNOuXv2mlAlBIcq7/L0G3Kkrkt8xB49qtQanqKW0SxSygMrBnRpJY1LDCchiCT1ILfKTjoK6GXxRotvBJMZCQjMFCQkmTGMlcDHelbxNpcAjUpcIZYzIkf2VwSd23bjH3ieBQByuoajq2xJ5Lt5IYLR/nWXyo5ijpyCG+YnBUkH1xU13daw2n2n2S/mHlR26FkulKtI7sME7gWbBU4yeBz61ual4x0nTZkgnhmO6JZVzGF4OcDDYIPynjFMk8b6Pb3klpcQXFuYUWQs8SgfMFIAGc5+f0/hbHSgCXUr67srWzDXElkGiJZrlg7GTcoCMwDDOCx6EDGeQKcmsmzha6uHubm3Szjll2wgyLIWwBtXoSOSPbNXnv7G6gw8XnwvJEg3IGVi+Np59M89xWfceLNE0e4nsdssTWhG9IrcgKD3HTI57UgN5TuUMM4IzzS1gv400NL8Whnfcf+WoUeX1x97P1/I+lb+KQCUVkweJ9Mub5rSF5ZGWXyvMRNyE9Oo7ZyPqKS38T2F3NHFCs5Z95+dNmFVtpOCQTz2AJ9qLAa9FZcPiTTZ7qa3ja4Z4SA+LWTA+Xdz8vHHr1NVl8YaZJA88cd0Y0h81maHYoHycZYgZ/eL7e9FgN2isi08TWF7C8saXAVIRLkx8EccAg4zk49znHAzQ3iW0ijupbiCeKK1VWd/kcEN0xtYk+/pRYDXorEj8XaZJa/adtyI8E7vKypwQpwQcHll/OkfxdpqW73Biu1iUxqHaIKrM4yoBJx0xz05osBuUVlReI7OVHcQXYVJPL3NDgE+oJPI/UcZqGbxfo0NuJ/tDSKXkjxEu8hk3cHHTO04z1osBt0VkWvifTru0FzGLgRmfyAGi+ZjtDEgDJIA5P0q7puo2+q2Md5alzFIARvQqeme/8xxQBaoqrfalbaciG4fBc/KgI3HHU89gP85qGbXLSN4lhSe883aVNrH5g5zjnOM4BOOuB0oA0KKxLrxfpFnGHuGnjzG0m1oSGABA5HbJPH0+lPuvFOl2knlu8pJWNlPlMqtvJC4LYHb/ADzRYDYopsUqTwpNG25JFDKfUGnUAeZfGn/j00j/AH5f5LRR8af+PTSP9+X+S0V9dl3+6w+f5s46nxs6/wAEf8ifp/8AuN/6Ea3qwfBH/In6f/uN/wChGt6vmsX/ALxU9X+Z0Uf4cfRBRRRXMaEF7KkFjPNIFKJGzNvYKMAdyeBXn+mrpz2ZeV18yUC3lWItK0eVYAoquQGcbxjk5fIwK9DuI2mt5IkfYzrgNzx+RB/IiucPgpPssVsNSlKIwJMke48FiAMnpl2656j8WgKemX2m6dfXeoh5khSKdgsyyZLkh3j3OSu5dgUjgknvSWuq6XdaVqQeGOCRX82TzQGMqvIzABQRuZScZPAOK1V8KRrai1F4UjEciFkhG5i+4EnJI+6xHA981FY+Do9Otb63gvSVu0dAWiGY8sWB4OD15/DGKegHO3z6bL9pksrpkisX2FCG3ktGqk7iwzzj3JyTVmcxS2lzZq0cUCKLTG5eQrnJ+ZhsJdcgDtyB3ra/4RWVor1JNQVjdyCTLQs4U4APyu7A8D2PPXHFIngyBY3iN7KsRYlREMMeWK7ySd23dxgL0ouBhNPawaXHaW95FcFL2REP2fczMwZCWycbSobGM9B6VBFFatoizyxnMMki20cUIcR5QSHuOASMkknjGa6mXwpFcMHuLnznjlWWPfH8pILH51z8xJdjnjrgCo7TwhFb2QtpJoZQjSvH+5YfO/GW+ck4BIAyOtFwMzSfDUeraVJcecUSZZPJ/dCNGZjncQp+ZQcjFaEvgm3ltrWAXRjFq7sjKh43DrjPUHp+vJOdG00CGwjso7W5ngW1YNIkbnbcHaF+cHPHGcCtWlcDlpfBKTeWWu1QxSs0YSM/IrHkZJOTj9fyq3D4addTtLqe5jlSzBEZERV/v7l77R0AJAy3Oa3qKLgc5rfg+LXNTa9nmQExhAChOAMbehHfdn2bHvSJ4QBupJ5bwoJYUicQ793yYK/MzE8EA+vHWukopXAx5NClmknaW/YCZln2xRhNs4ULvz1I+UHHrWdf+DDqN+97NPbh2m87asTYcgKMNk5I4P54rqaKLgc6fCjPrv8Aa7XxSTj91ECqYDD5ev3do6ep9ODsx2bJqlxetcyus0SRrAT+7jCkkkD+8c8n0AFWaKLgYDeHJkvjcW81uo88yhnEhYAvuK43bfXGAMcHrVe38GCC7gulu445YWVg0cR3D52dsMW75A5B6c109FFwMO28MJb3F3L/AGjdYuRtO3YrFSoB3MFyx75P8+apx+D7i2sY7Wz1JLfMTRzMsJOQdmNoJ4/1Yzn3rqKKLgczB4NEUlz5l6Zo57Q2+X37j8qqpYbiCF2kgf7Rqa38OXCm7E9xCqXERjH2cSKY8j5tuWIAY8nGD710FFO7AwbbwnbwKifbbny4+Ujjwgjbcj5U4yOYx1J4Pamt4VV9Pls2uiYzPFJFwTxGBjf/AHjxnPHOK6CilcDmU8GJ9kMb38nmGQynag8vfj5TtbOCCc5GCePSnT+EWuifNvyh35BiXGVyTyDkZyzHpgcAcZz0lFO4HN2fg6K0sYLQ3sjCG4aZZdo34ZSCmTxjkduQMGrmm6DLplvp8EWq3Hl2m4yRhVCT5GMEfwgHkAdya2KKVwMnWtHudSmhe2uUgCqVkDKcv/d6emSfxqleeE/7SgtY7ua33wJh7hISZJGIIbqcYOfqD0Iro6KLgcxf+DE1CWCSSeGHyVI2QRMq5GNpA3e3I9/xqYeFi0u9540xDFGrIHZ18sk8MzHAJIzjHA9Tmuhop3AitUlitYo55FklRAHdF2qx9h2HtUtFFIDzL40/8emkf78v8loo+NP/AB6aR/vy/wAlor67Lv8AdYfP82cdT42df4I/5E/T/wDcb/0I1vVg+CP+RP0//cb/ANCNb1fNYv8A3ip6v8zoo/w4+iCiiiuY0CiiigBQkhRX2qA2MZfrmq8t7BCwV2IYruAA7VOhVWVzDudVAHz8ZxjOMdap3NgbkjLKuEC5703boA9tQtl2/OTu6YFOa9gQkZYkDPyqTkVC+nmQxneI/LGBs+nX86kls9+WVyGOOD93pikApvYVZlO/KnBAXkfhT2uolIDsUy235hjn8fpUMtj5k7SCTAdgx65H0oNicsRIDuOTuUe47exoAcdQtw+zLFs4wFPXOKkN1CJfKLHcSR0PUVWOm5lEnnHKtuANSCy2zrIJCoV2YKB0z2FAEr3McbhGLZPcDIHGeTUbahbIiOZPvnAGOfypJrLzXDBwMPvGVz9abNZzOqLHMqhMgEjkigC1HIksYkjYMrdCKa88URw8gUgZpIIniRVZwQoxgDjrx+lJJAz+Ztk2iQcjbnnGKAJDKixeaWAT+9TDdQL96ZR+NMa0RoSnG5hgvjrzk1G2nh0CNLkKSR8v+fQUAW1ZXUMpBVhkEdxQzBBljgZxmmxoY41QEYUADjsKJIzJGUJwGPPHagBJLiGFtskiofenqwbOOxwfY1UvLNriTcuDk5IJx2xVpEKl2J5dsnHbjH9KAHUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAHmXxp/49NI/35f5LRR8af+PTSP8Afl/ktFfXZd/usPn+bOOp8bOv8Ef8ifp/+43/AKEa3qwfBH/In6f/ALjf+hGt6vmsX/vFT1f5nRR/hx9EFFFFcxoFFFFAE8dqrwK5kfJXPUf4Vmz3TxOoDpjaC2UJPPHargZ1UKJXAAwBmoZI4XID5yoxwxHv2ptroBUur+a3faFQrsB3YI5+lNk1G4jkjVo40LDJDH2+vFWzDbt94FuMckn/AD1pfKtyckZI7kk0gIZb2RJQvlgcH5TnJ4B7DHeiS8lW5eMIoVSAMjJPT+eatbkLBs8rnB5qN44JCS2fm64YgH8qAK7X0gmKEAJvI3KmcAd+akFzK0yKqqVfPU4PH9ePxp5gtm+8gPXrk0vlW+/cBg8fdJFAAs0nmMDHwADtBGRnP+FRw3E0jAbUJK5AGcjjP9RU+Y9xbPJGCajENurbhkEDHDN0oArWN5cXFyEkKlSCeFx/nmrEdy0jABAAxwCT3xkfyojt7aFw8a7SBgHJpfJg83zAWBIwQDgUASxv5kauAQGUGnU0NGOmBxjpRvX1oAdRTd6+tG9fWgB1FN3r60b19aAHUU3evrRvX1oAdRTd6+tLvX1/SgBaKTevr+lKSAMmgAopMn+6/wD3yaMn+6//AHyaAFopMn+4/wD3yaMn+6//AHyaAFopMn+6/wD3yaAcnGCD6EYoAWiiigAooooA8y+NP/HppH+/L/JaKPjT/wAemkf78v8AJaK+uy7/AHWHz/NnHU+NnX+CP+RP0/8A3G/9CNb1YPgj/kT9P/3G/wDQjW9XzWL/AN4qer/M6KP8OPogooormNAooooAKhkkkSSMRswy5yAODyOv4ZqakG4ZAIwTnlaAELyB0YMxU5UgZ/A/p+tP3N/eP5035/Vf++f/AK9Hz+q/98//AF6AHbm/vH86Nzf3j+dN+f1X/vn/AOvR8/qv/fP/ANegB25v7x/Ojc394/nTfn9V/wC+f/r0fP6r/wB8/wD16AHbm/vH86Nzf3j+dN+f1X/vn/69Hz+q/wDfP/16AHbm/vH86Nzf3j+dN+f1X/vn/wCvR8/qv/fP/wBegB25v7x/Ojc394/nTfn9V/75/wDr0fP6r/3z/wDXoAdub+8fzo3N/eP5035/Vf8Avn/69Hz+q/8AfP8A9egB25v7x/Ojc394/nTfn9V/75/+vR8/qv8A3z/9egB25v7x/Ojc394/nTfn9V/75/8Ar0fP6r/3z/8AXoAdub+8fzqTe4gO3lsnGTUPz+q/98//AF6Xc+MZXHX7v/16aYDfMeSNyyFBjgE80rdv94fzoYMwIJHPt/8AXpSAwwaGwLNZISUyRSkSqrMu5cHGc88e1Xfm/wCej/nRl/8Anq/507isVLVSl3Fvibb/AAEbvU9f/r0/zWS+VZHcA5Drk85Jxj8MdKsZf/nq/wCdGX/56P8AnSuFiWDf5CeZnfjnNNm/1qf7p/pTPm/56P8AnSY5yWZj05NDYxaKKKQBRRRQB5l8af8Aj00j/fl/ktFHxp/49NI/35f5LRX12Xf7rD5/mzjqfGzr/BH/ACJ+n/7jf+hGt6sHwR/yJ+n/AO43/oRrer5rF/7xU9X+Z0Uf4cfRBUc88dtEZJCcZAAAyWJ6ADuakqC7heVI2iK+ZE4kUN0J5GD9QTz2rnVr6mj2I21JI4pGlgnR40MgjKgs4H93BwTnAxnvVFPEYeWSL+xtVVol3SbrdQEGCeTu9BQNLkjspIoo3hC72RTKJXLtjJz0wAOB+dRJppinvplgvGe4wQ28K0nybWDnJ6nHQcYGKHYmLk1qQ2XjrSr+eWGCG73QgtIXRVVQBkknd7VNB4z0i5IEUjndGZAeMFRnPfqNp49qxtI8LXWmGeVreV5JY3VfLl2FS2epHUEHHGMY75pun+EprGeSX7Asu6DyokONsLf3wCCDyWP49zzT0KOi07xLY6tI8dissrxkhlwFIwcHqRmrF9q8Wm2jXV7BLDCn3nJUgfka57R/Dt9o0F0Ld3W4kVhBMbaNvJJbr2JyvUZwPfrWzq0V1qGhy2SQTGeSLYXZUVWbGCf4sdzwM+hFICGTxfp8dpLdeTcPFC21ygQkckdN3qCPy9aSw8YafqNnJeW9vd+RGVBdoxyWOAAASSSe2KyJPDN4ul3Gnw2w8ucZ3qNjI+c992VGSeeST2wKlt/Dk9podxYR2zmSSaJwcjYyo4bGDnGBxk7s9TRoBtx+IbaWBpltrvajBHUwnehIyAV6jj2pg8T2X2d7gw3CQxs6s7ptAKY3Dk5zz+NZNvol7DG2/TY5wboTGByoRh5RTkqoGc8/d/Gi80nUbyMR/wBk2sNugZY7ZeQA2N53YGDn5gcHBAo0A0rjxbp1tawXLLK8dypaIR7WZwBk8BuwqG88b6bYWsF1dWl9HFOCUJiXnBweN3r36cj1rMi8NXzWdtZyxvDFA7svk44ym1crwGPuT07VHdeEbu406ws2DyNbAmSZ1A3Mevy555wc5GcAEcU7IDeXxVZNDFKLa8/fcoixb2IztzhScDIP5Gkm8X6XbxiSVnRSrMN2ASF4PBIPXis248P3E1tZ28NvPam3GTMLhmOfmHCgqP4iQ2QQT37wal4XudRkt3ED26xoVdFdnzjkZLH5gSOQeme+OVoBtz+K9Mt2KyScqgc7ZEOASAOjdckcenNI/iq0SUxraXcrfJs8pUcSb/u7SGwc1l2+hajDexXMiTSLAd8cZl+YOI0QHd0/hPO3ocVVn8KXUjD/AEbcNqB9pKGUd1JywGP4SBn6UaAdH/wkdpsR2hnRXZFDOoVSW+78xOD+BqvL4x06K4khMF0zROY3KIpCsNued3ONy9PWsuTw3dszztAlzJIASkkCqAwwF5BPGM5wBn9RFP4VuVuFeCGeVRcrKxeQRFlCBduACB06ijQDefxTp6XxsmSfz1YoVVM/MDgjI75/lVmXWIIbtbSVdk742xtLGC2ew+br7ViroMratBfSJeRuhmkZ4ZBkM75CqD0UDIJznk0usWOoz3we10+WW3mlMsoyiupKopAy2OiA/iaNAN+K+M6b4rWV1yRkMnBHBH3uDUkVwZJWjaF4mVQ2GIPBJHYn0rMji1GO5SaPzYkkupJ7qIQq3mBgAFDE5GMda0YS8l5JKYXjXy1UF8ZJyT2J9RSAsUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAeZfGr/AI89I/35f5LRR8af+PTSP9+X+S0V9dl3+6w+f5s46nxs6/wR/wAidp/+43/oRrerB8Ef8idp/wDuN/6Ea3q+axf+8VPV/mdFH+HH0QUUUVzGhW1OZ7fSrueMlXihZ1IIBBAz34rl4fEOtG71OOdrfZ5TPaGJC5OFJyoGNwG059/yPS6vKkGj3cshAVIixyM/TjB7+xrhpJ3FndPDZ2h8y2ZNqwBpFkAkZv4VU8hQflxhlOaaAtaT4lvC96Ly8nkaKBWZSyL5ZZgMqMHJHJxnp69a3dJvdYuri8VprSdQwEOEKqcnBdWBO5Bjp1ySMgAE4FhqWqxvfktOJI7WLZkq2WYpsCgkgkDcB/vVY0P7Zarq0ptLhriMSxQPDbR8txjJTJByRx0AFNgah1PUYtIgumkiYST7FmkkCfxsuHGMbeM5HQeuOc7Ttf1i501o7y4SG9W4RdsUO6RkZ+flwcfKcgj+76VEb/UZLOS3vY4YooUiLLdQoijczB+OuSAc56gnjmqP9ozaVYT+Vdwx+d8rBY4g4URs4DD5fvY7kkDjGaLAaeja1qQtm+13sjyPd/ZwZIgxU+U7bQo64YD6gdqsahq+oNYutpcK0nnz4kiZRlUUFVGf4TknPt1rL1C61G3hhim8qQF08yFY9gAbzcRfL95BtBXOOOvWotGOu3VjbC7hWaW4m3RtIEkchAx27ScbfYkHigDW0fWNSh8OWV3q0s/nzXZLbkBZoB1IAHA5H5j1p1/qWuHTdNexmdZXXy7oGJM+aOo5BIOQ2eMADtkVg32oXtl4asbsxw200lw8jGJVildQpPQE5GQPmyOg471et5rq7i0zN06Xc0cwaeGQK0yrIuSzf7vHXniiwC6n4i14GMWMwV5ZclPLjIRQFZhzyBgt1/DPNX59X16O005zHIvntFvk+yCQsWdgV+VgANu0juc9RXNzX76fqOnxRC4ihgjVmtpDsaSVlcGQHGVIIODXaaNNZweXo8lxFPdB5Z0WPMiqBIf4yBkqePXNDAyNV17X7ZE8lIo51EElxC+CVBXLgDqF4OcnjI554q674k1OC4EiXckNsYYmUwRgKzMWBwzZLDI4OAOPz7O40ywun8y4sreZ+u54wT2HX8B+Qp0VhZwBxDawx79u7agG7b93P07elK6A5nVNb1FZvKtjMhjET7o5I3Vy6/IpyAcEq34nj2ZqHiq4tPFi2LSzxxrJGj2yWofzMkfcJOeSwz04xjJzXVTWdrcSGSa2ilcoULOgJ2nqOe1RtpenvcJcPY27TJjbIYgWXGMYPtgflRdAclca3qq6pNapLcFPPdkCOrkRjI5Kg4C43FTg479Kmj8UX8kvmQSQ3EMMrmQMwy0eMKRtQYGemec4FdRLplhMxaWyt3Zn8wlowSWxjd9cd6kktLaaRJJLeJ3jYMjMgJUjoR6YycUXA4zS9Z1ufV7GO4muXjmnkyfLVUZEkYN24G0r6Yx71Y0bWdbuNWhS9kuPsssCTHFmABnPX5flXg/NnsK6WTSdNmn8+WwtnlyTvaIE88nmp47aCKV5Y4Y0kdQruqgFgOgJ9BRcCr/acV3ocmp6ZLHcR+U8kTnIVtuc+/Y1m2fictpqXl7EqM1pJd+XGV+4rhcct1/T3rfVEVdioqr/AHQAB+VNMMTdYYzxjlB09PpSAxJfFVut1bKg/dMshnDbdylQ2FX5uTlGzjIx3FPXxXZuZ1S2umaCATuNqj5MgcHOD1/zxWx5EOQfJjyM4+QcZ60piiZSpiQqRggqMY9PpQBUmuEutMhnjkuUE4Vo/spDO2RwM4Ix79PeuZuNY1HTvC66k1zdNO7IT5oWRCpJ4UgLggjBzzge+a7NQFACgKB0A4xUT2ttJbi3e3iaEdIygKj8PxNMDkItd1q4047biImR2WKZExIPllYHaRgjKAEjjg4pNN8Q3slh9plubhUe4ljRnClgFXphlHOVY9OM9+3VppWnRbvLsLZd5BbESjJGcHp7n8zSzabYXCss1lbyKx3EPEpyeefryfzNF0BzT6prMWnQSSXZBnllBldIweCEXy1XqOpwRncB2qKfXddis7dxIJpiZWlSNU+Qgoqq20cYLEEHGSMV066NpaQmFdOtRGTkoIVxnr0x7D8qlisbOAIIbSGMJjbtjA24yRj8SfzouByd/rWuQ2MiWrf6ZsfKyujksshRtgCj06egJ7cw6x4m1NbW2uYrnyITbvJK1vHldysOAx68HBAHHr3rsJtMsLj/AF9jbyc7vniB555/8eP5mli06xg3eVZwJuQxttjAyhOSv09qLgclH4g1a6nt7O1ufmdFQsYhI4ygdpDgjcwwRtAA5PNR3PiHVmu8LJIfO2Isds6nLiQBgq/MybhkAnIya7OSytJnZ5bWF3cYZmjBJGMYJ+nH0pj6Zp8q7ZLG3ddgTBiB+UHIH0B5ouAabI82mWssjl3eJSzHqTjnNWabGiRRrHGoREGFVRgAelOpAeZfGn/j00j/AH5f5LRR8af+PTSP9+X+S0V9dl3+6w+f5s46nxs6/wAEf8idp/8AuN/6Ea3qwfBH/Inaf/uN/wChGt6vmsX/ALxU9X+Z0Uf4cfRBRRRXMaBTPIh80y+TH5hBUvsG4g8kZ9DT6KAIEsbKKXzY7O3STOd6wqG/PGaljijhXbFGkakk4RQoyep4p1FAEf2a3O/NvF+8OX+QfMcYyfXjikSztYk2R2sCJknasSgZIweMenFS0UAR/ZrfbIn2eLbKcyLsGHPqfX8aVYYUkMiQxq7HcWCAEnpkn1p9FADTFEYzGYkMZGChUYx6YqKSwspRiWytpBkn54VPJ6nkew/Kp6KAIUs7WJNkdrAi/wB1YlA/LHufzp8UMUEYjhiSJB0VFCgfgKfRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB5l8af+PTSP9+X+S0UfGn/j00j/AH5f5LRX12Xf7rD5/mzjqfGzr/BH/In6f/uN/wChGt6sHwR/yJ+n/wC43/oRrer5rF/7xU9X+Z0Uf4cfRBRRRXMaBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAHmXxq/489I/35f5LRR8av+PTSP8Afl/ktFfXZd/usPn+bOOp8bOt8Exg+ENPO5x8jdGwPvGt3yh/fk/77NYngj/kT9P/ANxv/QjW9XzWL/3ip6v8zoo/w4+iGeUP78n/AH2aPKH9+T/vs0+iuY0GeUP78n/fZo8of35P++zT6KAGeUP78n/fZo8of35P++zT6KAGeUP78n/fZo8of35P++zT6KAGeUP78n/fZo8of35P++zT6KAGeUP78n/fZo8of35P++zT6KAGeUP78n/fZo8of35P++zT6KAGeUP78n/fZo8of35P++zT6KAGeUP78n/fZo8of35P++zT6KAGeUP78n/fZo8of35P++zT+9ZsMlxdCNxfvE88rqkEUCNtVWKliT24yT74FVFNibsX/KH9+T/vs0eUP78n/fZqlqIl0uCOe51h1jeVYi5gjAXccZJI6U8qFUM3iSNQVDAlIhwRkH6YquR9xc3kWvKH9+T/AL7NHlD+/J/32awb7Xbeyu47Ya49w8m0gxpABhlZgcsQDwvr/EPWrV9eDT1jaXWLh1dVfdFaRsFDHCk4Hcg4+lHI+4c3kanlD+/J/wB9mjyh/fk/77NZ0k08UM80epPMbYI7RyW6KHRuhBHODz+VUJ9Wv4rVb15Zo7eSXyw0cUJRSWKgEuwPbqeKapve4ufpY6Dyh/fk/wC+zR5Q/vyf99ms6MXnko13rkNnKVy8MqQ7k+pBxWdf64LK6jtl1xbh5NpHlxwgYZWYEFiAeF9f4h60ez81/XyDm8jovKH9+T/vs0eUP78n/fZrHvryTT1jefXHKOqtvS0RlUMcJk/7R4HvVixW8vwTFrEikIj7ZLRFJVxlTj3wffg0ez81/XyDm8jQ8of35P8Avs0eUP78n/fZrLnmvLIs0moGVopURoXt1TcrMBuBHbnr6jBq/qM72tjNNHjegG3PTJIH9alwat5jUkyXyh/fk/77NHlD+/J/32ab/Zl6ODq75/694/8ACqerLd6Vpk182pSSrCASohjXgkDOcds5p8j7hzeRe8of35P++zR5Q/vyf99mucsvEH2uya6e+ubdEUNmSGHawLBeG/EdQKt6JqI1/wA4WmrXKtCAWElrGOCSFPTvto5H3Dm8jY8of35P++zR5Q/vyf8AfZpv9m3n/QYk/wDAeP8AwqIrc2moQQS3ZuUnRz80aoVK49Ouc0uR9w5jzv40KFs9JALH95L9457LRS/Gr/jz0j/fl/ktFfV5d/usPn+bOWp8bOv8Ef8AIn6f/uN/6Ea3q808OfEvw/pGgWlhci7MsKkNsiBHJJ9fetP/AIW74Z/uX3/fkf8AxVeJicHiJV5yjHRt/ma0qkVTin2R3FFcP/wt3wz/AHL7/vyP/iqP+Fu+Gf7l9/35H/xVYfUcT/Iy/aw7ncUVw/8Awt3wz/cvv+/I/wDiqP8Ahbvhn+5ff9+R/wDFUfUcT/Iw9rDudxRXD/8AC3fDP9y+/wC/I/8AiqP+Fu+Gf7l9/wB+R/8AFUfUcT/Iw9rDudxRXD/8Ld8M/wBy+/78j/4qj/hbvhn+5ff9+R/8VR9RxP8AIw9rDudxRXD/APC3fDP9y+/78j/4qj/hbvhn+5ff9+R/8VR9RxP8jD2sO53FFcP/AMLd8M/3L7/vyP8A4qj/AIW74Z/uX3/fkf8AxVH1HE/yMPaw7ncUVw//AAt3wz/cvv8AvyP/AIqj/hbvhn+5ff8Afkf/ABVH1HE/yMPaw7ncUVw//C3fDP8Acvv+/I/+Ko/4W74Z/uX3/fkf/FUfUcT/ACMPaw7ncUVw/wDwt3wz/cvv+/I/+Ko/4W74Z/uX3/fkf/FUfUcT/Iw9rDudwOtZNvItskaTWl6s9vLIVkhgZgys5bGQCCpBHH8iK53/AIW74Z/uX3/fkf8AxVH/AAt3wz/cvv8AvyP/AIqqjgsSvsMTqQfU39RuLi+kiMUl5bxxSLKqf2Y7ncvvkcVYF1ayKGu9NmuZsfNK2mkFvwIP865j/hbvhn+5ff8Afkf/ABVH/C3fDP8Acvv+/I/+Kp/U8R/Ixe0j3N24WC5vVmeG/WFAAsKWTrgYIIDdlIJyAB161Frkf9qKpt47yB8Irh7F2V1QllGMcYJNY/8Awt3wz/cvv+/I/wDiqP8Ahbvhn+5ff9+R/wDFUfU8R/Iw9pHubnL2c0CW129zcpFFlrd1RVToMt2GWOScnNQQzS21pHZXOmai7W94Zw0MG9XAYkDPoQayv+Fu+Gf7l9/35H/xVH/C3fDP9y+/78j/AOKq44bEJW9mJyi3e5vnUrQgA+Gbw7QAM2AOAOg6VVuJ1ub1Zn0zVlhQALDHZlcDBBAbPCkE5AA69ayv+Fu+Gf7l9/35H/xVH/C3fDP9y+/78j/4qn9Wrf8APr8Q51/N+Be19m1mLbHpepRblVJUe0JSRFJYD1HJPSrmm6i1imW0nVHlMUcRItSFCoMKB+ZOT61i/wDC3fDP9y+/78j/AOKo/wCFu+Gf7l9/35H/AMVR9Wrf8+vxDnX834GxdTSaiwjh0zUVmluI2aW4h2qqKwO3PYD09fU1rarFJPptxHEhdyAVUdThgf6VyP8Awt3wz/cvv+/I/wDiqP8Ahbvhn+5ff9+R/wDFVEsLiHa1O1gUoa3Z2B1mMsT9jv8An/p1f/Cq99d2uo2b2lxZ6j5UmNwS3kUnBB649q5f/hbvhn+5ff8Afkf/ABVH/C3fDP8Acvv+/I/+KpfU8R/Ix+0j3NGx0qzsLQW0P9qhC6O/+hvhtjhlHTpgYI75zVjRLWz0KWVra2vyskMcRX7HIPuZ+YnnJJY+gFY3/C3fDP8Acvv+/I/+Ko/4W74Z/uX3/fkf/FUfU8R/Iw9pHudh/bCf8+d9/wCAr/4VCJ2vtUt5Ut7iOOCOQM00RTltuAM9ehrlf+Fu+Gf7l9/35H/xVH/C3fDP9y+/78j/AOKo+p4j+Rhzx7mV8af+PTSP9+X+S0Vg/EXxjpfiq3sE04Tg27OX81AvUDGOT6UV9DgYSp4eMZqz1/NnPNpybR//2Q==)

5\. 选择“USB Test and Measurement Device (IVI)”；

6\. 点击“下一步”；

` `![image005.jpg](data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAoHBwgHBgoICAgLCgoLDhgQDg0NDh0VFhEYIx8lJCIfIiEmKzcvJik0KSEiMEExNDk7Pj4+JS5ESUM8SDc9Pjv/2wBDAQoLCw4NDhwQEBw7KCIoOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozv/wAARCADsAUMDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDLgu9R8UXs97PNG0pUyt5zcIvouc4A9P61butJ1WzuLS2khhEt5/qVCjn1J44x3z071B4O1v8AsBpZ1i8xprfylzjCtkEMfXGM471syeKTLren37TXPlWkbx+WYk3HI+Zsg8ljjjsBX2lR4inU5KcFypfpt958+o0JJynLW/cxryw1eweFLm2ijM+7ZkJg4Pr057c80sun6vbqpngt4i+zYrvGC+77u3nmpH1VpotIDsElsS0kknkqcyGTeMYwT79Ku654iTWmjIM1vAsySeQqAuSoKht+7jIY8Y49TT58TeKcV1vo+/6i9nhrNqXpqUL7TdW0yHzr2K2gi5CszId7DqoA5Le3sajkstXijV3sgCysxjEal1VeSWXqBjnnsM1ua54otNQ0W7061juw9wYj5sjf3Qqsv3icEKT756dahufElpNd3TJp6JHIkwE/lgzyFkZQPYfNzyeFFZwrYtxu6euvT0/r5FypYZOyn+JmR6fqT2sVz/oaJNEZk3sqkqM5PT/ZNZg1CUjO2P8A79ituw1tLS1CvZxGWC2kSBtpfDn7mNx+XBLHIPfgCsMwZPb8K7KPtXOSqKy6HNVVFRi4PXqO+3y/3Y/++BR9vl/ux/8AfApn2ej7PXTyI57xH/b5f7sf/fAo+3y/3Y/++BTPs9H2ejkQXiP+3y/3Y/8AvgUfb5f7sf8A3wKZ9no+z0ciC8R/2+X+7H/3wKPt8v8Adj/74FM8j3FHke4o5EO8R/2+X+7H/wB8Cj7fL/dj/wC+BTPI9xR5HuKORBeI/wC3y/3Y/wDvgUfb5f7sf/fApnke4o8j3FHIgvEf9vl/ux/98Cj7fL/dj/74FM8j3FHke4o5EF4j/t8v92P/AL4FH2+X+7H/AN8CmeR7ijyPcUciC8R/2+X+7H/3wKPt8v8Adj/74H+FM8j3FHke9HIgvEd/aEv91P8Avgf4Uf2hL/dT/vgf4UzyDR5Bo5EF4j/7Ql/up/3wP8KP7Ql/up/3wP8ACmeQaPINHIgvEf8A2hL/AHU/74H+FH9oS/3U/wC+B/hTPINHkGjkQXiP/tCX+6n/AHwP8KP7Ql/up/3wP8KZ5Bo8g0ciC8R/9oS/3U/74H+FH9oS/wB1P++B/hTPINHkGjkQXiP/ALQl/up/3wP8KP7Ql/ux/wDfA/wpnkGgwHFHIgvEa+ozdhH/AN8D/CoX1Gcjon/fAp7wVC1vT5DWLgbNp8WPEemWqWS+TOsIwJJgWcjOeTnnHT8KK466QLcuPeivHqYSlzv3UexGo+VantXhDwLoGp+F7G9ureVppUJYrO6g4YjoD7Vtf8K48N/8+0//AIEv/jU/gH/kSNN/3G/9Dat+UgROW6BTnjP6V4OJxeIjWmlN7vq+50U6NNwi3FbHMf8ACt/DX/PtP/4EP/jR/wAK38Nf8+s//gQ/+NcF4b1DXIfEljdvc37WhgEDQOrDyyXG1AsjAldu07+vJHOKTSLXWn8aQXTxahNBLqU5WTzHeMojZB/hyMnjoCAOD0rD65if+fj+9l+wpfyr7jvv+Fb+Gv8An1n/APAh/wDGj/hW/hr/AJ9Z/wDwIf8AxrgLLTdRl8fE/aLk2n2hQh3H7Ow3btpO3AJxsHAPBPoa2tWuNbj8VSahpN9qUtvdXENnEcKyj94jSlEK/wCrC/LuHOc9smj65if+fj+9h7Cl/KvuOl/4Vv4a/wCfWf8A8CH/AMaP+Fb+Gv8An1n/APAh/wDGuJuNU1x/El7f3c2o22nrrRWOe3tWYGGOKVRs6g54H3TkkHqMVj6xp3iyXxhd2sbPZ2P22aSO5kVggDZ2ljydmcYHQ0fXMT/z8f3sPYUv5V9x6d/wrfw1/wA+s/8A4EP/AI0f8K38Nf8APrP/AOBD/wCNche2Pia41yW8jvb1FfW47ZRDIY0CpHw4UqwAxgbuh7jnixrcurR+JJEWee5iYMrXUM8/+gljgk7PlXaqjA2kMSTxij65if8An4/vYewpfyr7jp/+Fb+Gv+fWf/wIf/Gj/hW/hr/n1n/8CH/xrgPEcviK28XEWs+qT2pWF8x+btQI+VO5hgqWIyenPpVm7uNdu/Eckj3d+lrHNIZG81kV44zGYgrbMcM5bjl8YOOKPrmJ/wCfj+9h7Cl/KvuO2/4Vv4a/59Z//Ah/8aP+Fb+Gv+fWf/wIf/GuH8QN4guY7FbuG4d5NOt7iYwrLFNJM0bq2duVyh+Y4UYznnaAZvHOs61aa5aSQ/2hMFsUkSWymdUmJySpCqMAlOe/K4x0o+uYn/n4/vYewpfyr7jsv+Fb+Gv+faf/AMCH/wAaP+Fb+Gv+faf/AMCH/wAa4jx2NbXxVFPaiQeekIlt1V/JhG+Ml3cYDgkbSCBxn3pdRuvED6RFYpBfwRTW0cRugHx5pAZsYfYI8Bhu25H15o+u4n/n4/vYewpfyr7jtv8AhW/hr/n2n/8AAh/8aP8AhW/hr/n2n/8AAh/8a891u78RXl5aanfRXbBNONyqEmNLhhJ8qqgBAJXblSATk8cVe1o61HZW8enXlzJHYWFqi/vZGVpzK3oPncKASQcDH4UfXcT/AM/H97D2FL+Vfcdp/wAK38Nf8+0//gQ/+NH/AArfw1/z7T/+BD/41uaNHcxaVAl3E8U4X51eczHOepbvnr7dKvUfXcT/AM/H97D2FL+Vfccr/wAK38Nf8+0//gQ/+NH/AArfw1/z7T/+BD/411VFH13E/wDPx/ew9hS/lX3HK/8ACt/DX/PtP/4EP/jR/wAK38Nf8+0//gQ/+NdVRR9dxP8Az8f3sPYUv5V9xyv/AArfw1/z7T/+BD/40f8ACt/DX/PtP/4Ev/jXVUUfXcT/AM/H97D2FL+Vfccr/wAK38M/8+s//gS/+NH/AArfwz/z6z/+BL/411VFH13E/wDPx/ew9hS/lX3HK/8ACt/DP/PrP/4Ev/jR/wAK38M/8+s//gS/+NdVRR9dxP8Az8f3sPYUv5V9xyv/AArfwz/z6z/+BL/40f8ACt/DP/PrP/4Ev/jXVUUfXcT/AM/H97D2FL+Vfccr/wAK38M/8+s//gS/+NH/AArfwz/z6z/+BL/411VFH13E/wDPx/ew9hS/lX3HK/8ACt/DP/PrP/4Ev/jUF94C8KafYXF7PbXHlW0TSvtuHJ2qCTgZ9BXY1leKf+RS1j/rwn/9ANVHGYlyS9o/vYewpfyr7jyr/hIvhV/zw1P/AL6f/wCKo/4SH4Vf88NT/wC+n/8Aiq5e2tFm8IWdw+l2t3ZW8MrXMgYRzI/mtgBxzu2kEKwIIHFSy6B4PstCu5/t8+pXatG+yCRVMELcbh1VyGIBHHXoK7XiZp25pfeyfY0/5V9x0f8AwkHwpP8Ay76n+b//ABVX9Ck+GniPV4dKsLbUDcT7tm93C8KWOTu9Aa8tl8OvcRNcaLcrqcIG5kjXbPGP9qPr+K5HvW18Ixj4kaaDwQJf/RbVTrVHFtTlon1Yexp/yr7il4qt49P8VanZ24KwwXLxoCckAHA5NFP8cf8AI8a1/wBfkn/oVFexBtxTZhyo978Af8iRpv8AuN/6G1dFXO+AP+RI0z/rm3/obV0VfKYr+PP1f5nXR/hx9EFFFFc5oFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFZXin/kUtY/68J//QDWrWV4p/5FLWP+vCf/ANANXD4kDPJvhTb+GNNgF7rF4ov9Sjkjhhm4jMYO1h6Fj6H8Kybq5tob7WD4Z8NXlhebShjklVj5ZZT/AKhhkg7TnGQMjtXL2eq6dNp8WmazZyPDAW8i6tmxLDuOSCp+VxnnBwfeut0yC3l0IJHdS695Mq+TtGTGhYDGOJYGHJyCyGu2pFxm5MhEPg3wqnjrUGlis59Ge0cNNdWhxETn7qqTlH78Egegrp1t7W0+P9jbWpUrFbbWIOWLeS2Sx7se5PNX/HPjmx8CaX/wjvh3adRKne+d3k55LsT96Q9efqffz74UTSXHxNsJpnaSSQzM7scliY2ySaVPmkpTe1n+QMpeOP8AkeNa/wCvyT/0Kijxx/yPGtf9fkn/AKFRX0lP4F6HKe7eA7mGPwXpqvIAQjZH/AjXQfbLf/nqPyNct4IJ/wCEO07k/cb/ANCNb2T6n86+Qxc/9oqer/M6qK/dx9EW/tlv/wA9R+Ro+2W//PUfkaqZPqfzoyfU/nXPzmli39st/wDnqPyNH2y3/wCeo/I1RlnEMfmPvKgjO0E49+O1Ztt4n0m7SR4bxmSJykjmNgFIBPOR/smjnCx0H2y3/wCeo/I0fbLf/nqPyNYKeI9Mls4rqG5eaObIjWKJ3diBkjaoJzj+dNl8TadCVDvcDKuTuhZNu1Qxzux2Io5mFjoPtlv/AM9R+Ro+2W//AD1H5Guct/FekXFnFeC6aOGViqtKu3kAHn0+8MZ9ae/inRY4o5DqUTLJEZl2Nu+UAk9O/BGOpIPpT5mFjoPtlv8A89R+Ro+2W/8Az1H5GsMa7bSOFtUubwbA5a2j3qASQMnPXKtx7VDeeK9I06WOG+upLWWTGI5YnDD64BHp+dLmYWOi+2W//PUfkaPtlv8A89R+Rrnn8UaTHdfZmu383GSgickcEjjGegPQdjnFRt4v0ZbqS2N22+NVbO3IbcARt9Tg9PrT5mFjpftlv/z1H5Gj7Zb/APPUfkaxG12zTU/7OJm84TCDO35d5AIHXPQjnGK0Mn1P50ucLFv7Zb/89R+Ro+2W/wDz1H5GsOLxFpU13HaJfxmeWRoljLc71OCMds5yPUUWmv2N9dC3t5WckkB+ApI6gZOex7UczCxufbLf/nqPyNH2y3/56j8jWFZeJNJ1CWWK1v0d4lLOM4wB1+uBzx2I9amsdXsdSeRLO6WZomKuBnjHB/DmjnYWNf7Zb/8APUfkaPtlv/z1H5Gsj+2LEtKiXPmvCcSJErSMpyV6KCeoI/A0thqttqZP2RpnULu3tC6KeSOCwGSCKOdhY1vtlv8A89R+Ro+2W/8Az1H5GqFzcx2kXmXEnlqWCgnPJPQVQk8R6XDYR38108NvLwjyQyLn5S/QjP3QT+FHOFje+2W//PUfkaPtlv8A89R+RqoGJAIYkEZHNU7zWLDT7iG3vLxIJJwxQO2AQoyeaOcLGv8AbLf/AJ6j8jR9st/+eo/I1zt94r0nT4oJJLl5UuGZY2gXeCQQCD6csPzobxXpCw28jXTg3KK8KFCGcHpjPHY9+1PmYWOi+2W//PUfkaPtlv8A89R+RrIbVrRJYIWmIln2bEwSfmOFzjgVDd+I9NsL1LK5uJI53ztXyZDnHoQOeoHGeaXOwsbv2y3/AOeo/I0fbLf/AJ6j8jWFP4i0y3u2tZbsrMiqzKEZtoPTOBx2znGMirR1C3W++xGfE/8Ad7Z9M9M98Uc7Cxp/bLf/AJ6j8jR9st/+eo/I1y8XjTSJtUGmI9z9qLbNpjwAc465x1q2viHT3bAlnwSFV/s0uxiegB24/wD1inzMLG79st/+eo/I1U1YQalo97YLcLGbq3khDlSdu5SM4/GsqLxTossxhXUogyq7Hc2AApwTn8Pyoj8UaTMD5V55jeX5gRR8xHPAB7jaSR1AGaFNp3Cx5v8A8KO/6mWH/wABW/8Aiqkt/gvPZzpPbeLFglQ5WSO3ZWU+xDV6LD4jsJ2whucbVbPkseqhgMDJzgg4xVu21O1vJpYYJw0sW0vGflYZAI+U89CO1dDxlXrb7kLlR5bL8E5Z5nmm8UxySSMWd3t2JYnqSd1bHg/4Xr4W8TWusNrsVwtvvzGLcqW3KV65969DyfU/nRk+p/Ok8ZUat+iDkR86eNznxvrJHe8k/nRTfGf/ACOer/8AX3J/OivrqfwL0OI9v8Ec+D9OH+w3/oRqPVvFlvawbbICSd5fKR5wUhHOCxc8YB461J4I48H6cf8AYb/0I06Xwhokq3Qa1JNyG5Zt3lFsksgPCnJzXx+Kt9YqX7v8zrpfw4+iKela3Kl/KdV8Q6PLblMJ5M6DLZHQcEcZzknPHStrTtY0/VVJsrlZCBkoQVbGeuDzg+vSuNk8O6zpsCW0Xh7R9QWLIW6EKtJJ1271ZhjsCef611+l6HpujIfsNqsbMMM5JZsZzjJ7D06VzuxoV/E00VvYW00r7Nl7DtOzdyTgjqMZBPJOK43T7O3tNIuZvMjfEyf66AuGJifIwCexYknkEDIrvNY0tNXsRavIUCypLjJwxVgQDjnHHr6VkWPhNrVXSWaFla4a4AjMinO1gq7t2Qo3HgdaEwMK1jszoH2d7qG2tJ5CYmNoXCjBB3HaMhTJyxPGBikvI9Ou9ItEnm8r7OZThLds7Cq7s4Rdpxhhxzkc1uN4MT7Ba20d4yeVGUl3b3WTJUnAL/KPlPHIOelM1jwUdWAY3cUTo+UzGzYUBQq7t24fd6g/pTugMdB4d0zT4vNleJZFltVWMSecz5Vd7BgCANvK+/1rTsfD0eow2V7Y6gs1kIoiFLvlnRHGc5wCGYEZBIxT7jwjqTxBLXVYbYieSUssbn75BwAWOMYHPsK17bSLmPTbC0lv2T7HOJCbcFRKik7Yzn+HkA+uKLgUTdQ+GFvL3VJGfzME+QhcAlnfHrnLnrjIA96xvFP9l3N0biXUVt31CBfLWSFmBQDb82Pu8qTnngH0Fb+t+Gf7amkY3YhSQRblEIYkoX5JzzkPjFVrrwRbXqWAuLyUm0iWI7UXDKEIPbPJYtyT1NICrfWVmms2Up1KSO5a3VIpI7RpFACNngDBBDg55PHaqep6PJpd5CbnUNNijmURqJUIklCFAPmC8dhx/exk1r33hSW4ufMilssKpCPNbkuuYwnYgcEbhx1NdF5ELKivEjhBhdyg4+menSi4HN3WjWMniqOSMSJKZ1E6tIxUt5ZfC9xkA5ORg9qlh8Q2Z1eYteXLrdBIobdrZhHCwZlJJ9WbI5x93HNW/wCw5Gvnv2vW+0+YJI8ZCAg9xnn5fk+hJ6msiDwM9reyzwXkG2SdJtpiddu192PlbB4wM4oAqaRqGipqa29pc2v2uB8JOyMqsVGWCnkYOG4/2RjtiTTUezvUkE93HAjsA0li+BmLPQnAw2WwQD71cs/C2qW2pC7k1WCaMMx8lomI2tncuc5Oc9TzxUtr4QjtriacNa5n3hoxAdsYbqUO7Oc+vbgYFPQDntItNGt5NQkstXkklFtLJEptmAVNu3OV54MeeOoxjrXQ+F7Rmmlv4jELd5ZhhXmLbyy9Q4HAwee+aXRfCS6Pfi6Fwsxbf5gO8Zz0wNxHTGQePSt27t5Liymt4Lh7SSRSFmiA3Rn1A6ZpNgLBaWttcNPDbQxSSHLukYVn5zyR15JP1NUbLQ7aDTxazpvJYu+x2RWbcxzwRzg4PritGJGjhjR5DIyqFLt1YgdT9etOpAY9/wCHLOW0eK2tIC0jqX892bIAPQncQee3vU+maLa6dZC38qFzxuIiCrwMDA+n1PJ9a0aKAK9zDdS3Nq8F35EUTkzx+WG85ccDP8P1FZ+u6HJrTRr9oEMcaMOhbLEjHHtgc5z1HetiigDl9R8ITat/x9XwU/aPPLw7hyWBICkkAYA5zknHQCrM3hkTw6fGzlBbSKZAlw+Aq5wEGOpz36e9b9FO4GDe+G5LycMt9NbpEF8plndmcjpu5GAPY575FQaj4UmvLiO4hvfJcRRJIrMz+YUfccsecY6e9dLRSuBz2p+HJbnUbq7tRbgzneN8rIFbbtOVVSGz1J4PPbrSSeG5pddjvnFkYUm37RGoyhA3KV2cktk5LcZroqKLgcpaeDpIdbfUpZIm3y7/AC1kfI9PmwM4OTjHO489KmtvC0sN5JdFoMSk5g82VlTKgbg2RuwBwCOASM10tFO4HGR+BrqEzsl+heZZEzvcBQc4OOfXlcjkZzV4eF7j7O8LzwyebLJNIzFyJHO8LlTns4BOSflFdLRRdgcjB4KnXeklzAqSoEdlBfC/LuQKw6ZXg5yBitLR/D76bfC4keBisRTdEm0uSFHIAAAwg6dSSa3KKLgFFFFIZ85+M/8Akc9X/wCvuT+dFHjP/kc9X/6+5P50V9zT+Beh557f4J/5E/T/APcb/wBCNbtYXgj/AJE/T/8Acb/0I1u18fi/94qer/M66P8ADj6IKKKK5jQKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooGfOfjP/kc9X/6+5P50UeM/+Rz1f/r7k/nRX3NL4I+h557f4I58H6d/uN/6Ea0k1KGTmOG6kGSNyW7EHBxwcetZvgfjwhp3+4f/AEI0+3tZVkh+0R6gYYmLNbxoux3Dkq2c5xznHcgV8hil/tFT/E/zZ0QbVONl0RcuNb0y0hhlubxIUuFLx7wcsBjPGO2R+dPm1bTbdFee/t4leMSKXkA3IRkEA9RXPa3o+qXtlYJb6VHcvBDhhNMsYGeq5znsM9fbvm2+i39x9gDLLAsexJRFcsu1FBHQNj0AA9Mk1zNK5utjTm1zSbd1SbU7WNmUMFaUAkHGP5j86JNc0iGVYpdUs0dhkK06gngH19CPzrktf8Favq99aTRzLGLcBWYykk4x8yknI4B6859q0NT0HV573zrRVKzJGW8wKSjAjdv+YbvlHUdT2B5o0A2pfEGjwjMmoRqPM8oHDYL4zgHHJx6VbF7atMYRcRmUP5ZTPIbG7GPoM1x+qeB7q+1OedyXt2mMqpDIFZgy7SBvyAe/pjA5q83g/wA68triQ/6u6kkcMqSHZ85TlgSTlhx2/CjQDpjLEr+W0iBzj5SwB56cfgaVHWRA6MGVuQynINYF7YXEWutdNpv2+GZs/dDeV/q+cHuNhx/vdeDnX0+2lt4pvNUK01w82wHOwMemf89aQFmilwfQ0YPoaBiUUuD6GjB9DQAlFLg+howfQ0AJRS4PoaMH0NACUUuD6GjB9DQAlFLg+howfQ0AJRS4PoaMH0NACUUuD6GjB9DQAlFLg+howfQ0AJRS4PoaMH0NACUUuD6GjB9DQAlFLg+howfQ0AJRS4PoaMH0NACUUuD6GjB9DQAlFLgjtSUAfOfjP/kc9X/6+5P50UeM/wDkc9X/AOvuT+dFfc0vgj6Hnnt/gj/kT9O/3G/9CNa0EELQK7xgk5JJySeTWT4I/wCRP07/AHG/9CNaf2lLe0j80MquCobHBOTXyOKv7epb+Z/mzqpfw4+hiaZ4osNRuxbtprwEztDvfO0bRksSQMfTr1qbStes9UvxaiyjiLKzA+duIIIGCMAZOc8E9DVOy0y2sNQFw2tXEywr5zW8sY2BFGwtjPHDYz9KfbXfhez1V7+3ureJmVv3aDAyxBZvrke2Mn1rFKT2uW7Lc6X7NB/zxWj7NB/zxWsz/hKdF/5/ovzo/wCEp0b/AJ/ovzo5anZivE0/s0H/ADxWj7NB/wA8VrM/4SnRv+f6L86P+Ep0b/n+i/OjlqdmF4mn9mg/54rR9mg/54rWZ/wlOjf8/wBF+dH/AAlOjf8AP9F+dHLU7MLxNP7NB/zxWj7NB/zxWsz/AISnRv8An+i/Oj/hKdG/5/ovzo5anZheJp/ZoP8AnitH2aD/AJ4rWZ/wlOjf8/0X50f8JTo3/P8ARfnRy1OzC8TT+zQf88Vo+zQf88VrM/4SnRv+f6L86P8AhKdG/wCf6L86OWp2YXiaf2aD/nitH2aD/nitZn/CU6N/z/RfnR/wlOjf8/0X50ctTswvE0/s0H/PFaPs0H/PFazP+Ep0X/n+i/Oj/hKtF/5/ovzo5anZheJp/ZoP+eK0fZoP+eK1nJ4m0iR1RL2NmYgKAepNaf77/n2l/KpfOtxqz2G/ZoP+eK0fZoP+eK0799/z7S/lR++/59pfypXkOyG/ZoP+eK0fZoP+eK0799/z7S/lR++/59pfyovILIb9mg/54rR9mg/54rTv33/PtL+VH77/AJ9pfyovILIb9mg/54rR9mg/54rTv33/AD7S/lR++/59pfyovILIb9mg/wCeK0fZoP8AnitO/ff8+0v5Ufvv+faX8qLyCyG/ZoP+eK0fZoP+eK0799/z7S/lR++/59pfyovILIb9mg/54rR9mg/54rTv33/PtL+VH77/AJ9pfyovILIb9mg/54rR9mg/54rTv33/AD7S/lR++/59pfyovILIiVES4GxQuUYEDvgj/GpqjwwuF3IyHYxw31WpKJAj5z8Z/wDI56v/ANfcn86KPGf/ACOer/8AX3J/Oivt6XwR9DhPb/BH/In6d/uN/wChGtG+tJLzRreOO3achmOFbGDzgn5h396zvBH/ACJ+nf7jf+hGum07/jwj/H+Zr5LEf7xU9X+bOml/Dj6Hnd5aX+sPeXeoWNxAml2cq+Y8jjzJuMDBPIA54yKzJbywaJvJe1QnLZMI3ZOcDG3GOnpjtmvXpoY7iJoZkWSNxhlYZBFUP+Ee0X/oFWn/AH5X/CrwtZUYtO7/AK9DKVBtLX7/AOkeSarcWzar51l5OwYIwnyZyccYGRjHb257y3J0y5uLqV5lDCZREsShEaPI56dcZ7du9erf8I9ov/QKtP8Avyv+FH/CPaL/ANAq0/78r/hXZ9fjp7r+/wD4Bn9Vfc8iu109YZUtmVnWcFH3E7oyvQcdj1p9jBpUlp5l1c7ZlZsxliu4YOMEA98fma9a/wCEe0X/AKBVp/35X/Cj/hHtF/6BVp/35X/Cn/aCtaz+/wD4Avqrve55JdrYR6a0VtOksguM5IwxXDDjjp93v1zxxV+afQ7uCzhcpB5afvHiTBZtijk49QT9TXpn/CPaL/0CrT/vyv8AhR/wj2i/9Aq0/wC/K/4Unjovo/v/AOAP6s+/4Hk8dvpJgiZrr940Tb1ZiNrjGOg5B5H4Uk8WkLYtNDIzTEDZEZDkE+vy44+vavWf+Ee0X/oFWn/flf8ACj/hHtF/6BVp/wB+V/wo+vrs/v8A+AH1V919x5VLBoS20pju5ml2gx59cc5GP68Uk8GjLHKYLlmKnKbmOWAAOMY78jrXq3/CPaL/ANAq0/78r/hR/wAI9ov/AECrT/vyv+FH19dn9/8AwA+qvuvuPI43tI9dWRGiW087cNwLKqHsQR6cdKmZdGkfzJJmDNKFcINqhdoBYcdN2TXq3/CPaL/0CrT/AL8r/hR/wj2i/wDQKtP+/K/4UPHrs/v/AOAH1V9zyMrprtBiQrGXkDKzc442knbxn8cVFdJYLaxNbSu0xdhIjHIUZOMcc8Y5r2H/AIR7Rf8AoFWn/flf8KP+Ee0X/oFWn/flf8Kf9oLs/vF9Vfc8osZoEsivnW8TeXKGEqZJc/cI4PT1qQ3trJBIsbW0W61yweIZMpwCAdp7KfTljXqf/CPaL/0CrT/vyv8AhR/wj2i/9Aq0/wC/K/4Unjot35fx/wCAP6s+55JC8baxp+1lZg0IkZe77ufrxj8q9trPXQNHRw66XaBlIIIhXg1oVyYmuqzTStY3o0vZp6hRRRXMbBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBQvP8Aj+j/AOuTfzFR1Jef8f0f/XJv5io6ynuNHzn4z/5HPV/+vuT+dFHjP/kc9X/6+5P50V9vS+CPocJ7f4I/5E/Tv9xv/QjXTad/x4R/j/M1zPgj/kT9O/3G/wDQjXTad/x4R/j/ADNfJYj/AHip/if5s6aX8OPoWqKKKyNAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAKF5/x/R/8AXJv5io6kvP8Aj+j/AOuTfzFR1lPcaPnPxn/yOer/APX3J/Oijxn/AMjnq/8A19yfzor7en8C9DhPb/BH/In6d/uN/wChGum07/jwj/H+ZrmfBH/In6d/uN/6Ea2fs8PZMd+GIr5HEtLEVPV/mzqpL93H0Rr0VkfZ4v7p/wC+j/jR9ni/un/vo/41jzouzNeisj7PF/dP/fR/xo+zxf3T/wB9H/GjnQWZr0VkfZ4v7p/76P8AjR9ni/un/vo/40c6CzNeisj7PF/dP/fR/wAaPs8X90/99H/GjnQWZr0VkfZ4v7p/76P+NH2eL+6f++j/AI0c6CzNeisj7PF/dP8A30f8aPs8X90/99H/ABo50Fma9FZH2eL+6f8Avo/40fZ4v7p/76P+NHOgszXorI+zxf3T/wB9H/Gj7PF/dP8A30f8aOdBZmvRWR9ni/un/vo/40fZ4v7p/wC+j/jRzoLM16KyPs8X90/99H/Gj7PF/dP/AH0f8aOdBZmvRWR9ni/un/vo/wCNH2eL+6f++j/jRzoLM16KyPs8X90/99H/ABo+zxf3T/30f8aOdBZmvRWR9ni/un/vo/40fZ4v7p/76P8AjRzoLM16KyPs8X90/wDfR/xo+zxf3T/30f8AGjnQWZr0VgXElvbyCPyJpZCpfbFliF9TzwKYJkOcaZfnHXCdP/Hqa16CudFRXO/aI8bv7NvsAZJ2cY9fvUGZFBJ0y/AHUlOB/wCPU9ewXOiornTMo66ZqHP+x/8AZUCZSMjS9QIPQhP/ALKjXsFzoqK57zh/0CtQ/wC/f/2VHnL/ANArUP8Av3/9lRr2C5pXn/H7H/1yb+YqOq1rLDJK6rBLDKgG5ZlIbB6HqeOD+VWaynuVE+c/Gf8AyOer/wDX3J/Oijxn/wAjnq//AF9yfzor7en8C9DhPb/BH/In6d/uN/6EavrqqO8iLGMxnBDTKp646GqHgj/kT9O/3G/9CNJqWma1tD6dcwbwzAKxZQFYnk5yMjPYZNfH4tpYio33f5nRBuNGLSvojS0nVbTWbBLy0cMh4dQclGwCVPuM1Rh8SJNfwWq2crrMhkE0ZBTaOd2CQSuOvGQeMZIq/pNgNK0q2sVcMYU2tIo2726lsdsnJqpbaHawXcc1reTAQEYi3q4Uc5GSCQCd2QD1z6ccy8zZXtqKddQfaSYHjWJNyPICAflLDcMZTIGRnt1weKzbTxkLsoVtotphMjbZWJ43bsfLjA2jOeRuHFbZSzWWdzcqGvwo/wBaBuwuBt79Oay4vDGktO4N5JO7gecDKpdyM/MWA3D73OCB0p2GMm8ZW8VrczLZyuYrcToBnZJwxI3lccBc578+lJbeL/NN1vtEIgUECObliXCAcgAfeB/+vVo+GNMlWRGaSSEh0MZcMEY55z1yATgE45PHNJbeHLAXE8y3BnW4aN5Ytse1wuCgO1c44B96NAIbTxaLmwmunsDF5Uoh2mbJZywGMbc9+uPannxMy2clzLYNCouFhiLMdr5UMSTtGMZx7mpf7H0uzsiy3MdszXAl+2ARIxcOWC5xtwDnjFMm0mw1KdjeavJeSw4UDzY18pgTjhQOck9fSnYBkPigC3866gRf3rJtikJONu5W+YAYbB6np+IEV54umtYY5RotwwkuXg/1ifLtYDecE8Yz+Ix3zVqPR7OztPLbUmSPz2lRj5SASknJ4UAkEng59Krf8I9pFzZRM+ptPDbSPJHMJY/kckEksBzzzg+vPFFgCbxeY9NS9TS5XHzB8zIFQjGemSRzwcdqfdeKjawQSyadsEu7O+5QbOMrn24Of7uOaszaLpktgtnJKhjMm4M/lsx53MoJHQnk49ewqPVfD+m6o1vcG4S1SI/ujAkIG4+hKnr6UgMzWfHEukRWsrabEVnjVmBugdhJIxkAg9AfxrqLOZ7mxguJIxG0sasyBtwUkcjPfHSuf1HwnoU1vB9ruhC0MRjE+6NCyHjB4x6cgdeuTWjFDo2n3iXa3cMUj2yQoGuAEMY5BC5xzjqKdr7AatFVpNSsIpPLlvrZHH8LTKD+WasKwZQykFSMgg5BFJpoBaKKKQBRRRQAUUUUAFFFFABRRRQAUUUUAZWpCV7m6ggjMkk9h5QAGcBnILfgCT+lZOrafrUuiTRR2Ya5e4iuoxEiuAduwqdxxkbVJ9ckCukubG2u2Vp4tzKMKwZlIHpkEHFQ/wBj2H/PKT/wIk/+KrRSVibM4k6PqK6NcWp0q+ZZvs7PDGkiGRgDuySWzzjOR/8AWtWukXreHmtRp95FMs5aOCeEzJhguQN4AQgblyeM8nrXWf2PYf8APKT/AMCJP/iqP7HsP+eUn/gRJ/8AFU+aIWZyuoaFq0lhCtramK6M+6URW4jjRsAKRtflRgcjI7npWla2N3ZeDorWW3nYW0j+bCpbeyBGC4yecNsORxxkdK2P7HsP+eUn/gRJ/wDFUf2RY/8APKT/AMCJP/iqOaIWZm+HvtrPFO7TzvG8vnzMCvmqUXaoB9+3HQnvz0rXDDdiN22gEYx83sOazTpFiesUn/gRL/8AFUn9j2H/ADyk/wDAiT/4qjmiFmSFt2u3POcW0X/oUlWahtrO3tAwgi2byCxLFicdOSSamrOTuxpWPnPxn/yOer/9fcn86KPGf/I56v8A9fcn86K+4p/AvQ4T2/wR/wAifp/+43/oRrdrn/BUsa+ENPDOAQjcZ/2jW758X/PRfzr4/F/7xU9X+Z10f4cfRD64DT7FYPEIu3t9UVDLLmZreTOBv2tkDOWzzwPvGu88+L/nov50faIv+ei/nWdOo4JruW1c4e0iuGu7e8uobpC9uYZ4DbzlSFQKCxVQSWOT3H41HoW7S5fPuNP1Z4pN6+XHbzbox8+Pl5wCCMc5ye2Oe8+0Rf8APRfzo+0Rf89F/OtXiLpqwuU4iGA2wuYYI9ThBtJiCkVwy+Y4GEXcCDgDG7H9K0LR/sjXzRzasd6RiNTbP8+EAIB2DacjaD2rp/tEX/PRfzo+0Rf89F/Opde+6HY4y7vZ7nQriyfTNShIdHRYYGIIIwVUbTgAjnPXOc5Jqmn29opUa1u2kErOxezkVR8zthMowYMSD0BGa7/7RF/z0X86PtEX/PRfzqliElblFY4CaCaYJiHUliiujIyyWs0jfN5hbYMYIO9QTxkr0wajiimudFWG5tL8TR+dI2/TZiSxCqgXoScKOScACvQ/tEX/AD0X86PtEX/PRfzp/WX2DlOA1FJYdL0+3jsbi6eNgz+TpMxKjHJyWxv9T347Cp3mZ9IsLc6deRohbzBHpkv7snOf3ONpz03Z4zwBiu4+0Rf89F/Oj7RF/wA9F/Ol9Y02/r7g5Thb5rm5tLVoLW8t3EMSiKGxlQQssnHHYbecZ456mszXLe5mfT0s9M1Bvs0CI8n2GXlgrDJ+XnA2j354r037RF/z0X86PtEX/PRfzqo4rl6Bynm+s2K6nraXUVhqcdukSjH2CYGPgAhRxkgDtjJzxxXpEDB7eNgSQUHVCp6eh5H0NH2iL/nov50efF/z0X86xq1XUSXYaVh9FM8+L/nov50efF/z0X86xGPopnnxf89F/Ojz4v8Anov50APopnnxf89F/Ojz4v8Anov50APopnnxf89F/Ojz4v8Anov50APopnnxf89F/Ojz4v8Anov50APopnnxf89F/Ojz4v8Anov50APopnnxf89F/Ojz4v8Anov50APopnnxf89F/Ojz4v8Anov50APopnnxf89F/Ojz4v8Anov50APopnnxf89F/Ojz4v8Anov50APopnnxf89F/Ojz4v8Anov50AfO3jP/AJHPV/8Ar7k/nRR4z/5HLV/+vuT+dFfc0vgXocB7h4IJHg7TsE/cbv8A7Rrd3N/eP51g+CP+RP0//cb/ANCNbtfH4v8A3ip6v8zro/w4+iF3N/eP50bm/vH86SiuY0F3N/eP50bm/vH86SigBdzf3j+dG5v7x/OkooAXc394/nRub+8fzpKKAF3N/eP50bm/vH86SigBdzf3j+dG5v7x/OkooAXc394/nRub+8fzpKKAF3N/eP50bm/vH86SigBdzf3j+dG5v7x/OkooAXc394/nUZu4QcG5jBHYyD/GotQYrpl2ykgiByCOx2morSC0a8W3eytYkSBWRTCpM2QMtnHQdMdecntVximrsTepa+2Qf8/UX/f0f40n2yD/AJ+ov+/o/wAap3SwR65a29vY2DxPBI0quFTGGQAj5TkgE8cdaewPmBV8LxEbwNxeADGeT69OcU+RdxXZZ+2Qf8/cX/f0f40fbIP+fuL/AL+j/Guds5LufxB5UtlY/Z8/LHEqEMu98tzFnAAUZyASB61I94B4gis1s7DypZpImi+zrvjCuqhh3OQ27oRx6c0ci7hdnQJcJJnZOr467XBxSfa4f+fqL/v6P8a57UJI/wCybW5jhhikbzkd4UCeYqkgHjscA/jUs+luNchtY3D27wiZ9ltAGT5wO6cr685xScdbIE2bn2uD/n6i/wC/o/xo+2Qf8/UX/f0f41T8kGRVHhWIAsAWaSHAHc8En8KwLS6Mer7tSt7GO0LIoCKuzDMwD8x7gOVGSQCQPU0uVjudV9sg/wCfqL/v6P8AGj7ZB/z9Rf8Af0f41zMl7nX7awjsbERXMro5FsrNbhXdRnn+ILnJGAeOcituyt7C70RLua0tLd3jJaTyVwuCRuwe3GaOVhcvJMsmTHKr467WzSvKIxueQIPVmwKyrEr/AGnDttUtS9ozOiJtDfOoDY6jI5APIzVqSKKbWbaOeJJUEErbXXcM5QZwfqfzpRV2D0LH2yD/AJ+ov+/o/wAaPtkH/P1F/wB/R/jUv2HT/wDnwtf+/K/4VyHjSZ9O1CxXT4kiWRD5gSBCoO4BSQVOc8ir5V3FdnU/bIP+fqL/AL+j/Gj7ZB/z9xf9/R/jXHahqN3Hb2iWFvZzzSqGLC2RmKs77MoF6lUOcHjByK6nQ0tNQ0KyvLjT7QTTwh3AgXAPftRyLuF2WPtkH/P3F/39H+NSq5YAq+QehBzml+w6f/z4Wv8A35X/AAqlpoVY7hEUKiXUqqoGAo3dB7UnFJXQJu58/eM/+Rz1f/r7k/nRR4z/AORz1f8A6+5P50V9tS+CPocR7f4I/wCRP0//AHG/9CNbteBWPxF8SaZZRWVpdRJDCMIphU989TU//C1PFn/P7D/4Dp/hXh18qrVKspprVt9e/oaU68YwUX0PdqK8J/4Wp4s/5/Yv/AdP8KP+FqeLP+f2L/wHT/Csv7Hr91+P+RX1mHY92orwn/haniz/AJ/Yv/AdP8KP+FqeLP8An9i/8B0/wo/sev3X4/5B9Zh2PdqK8J/4Wp4s/wCf2L/wHT/Cj/haniz/AJ/Yv/AdP8KP7Hr91+P+QfWYdj3aivCf+FqeLP8An9i/8B0/wo/4Wp4s/wCf2L/wHT/Cj+x6/dfj/kH1mHY92orwn/haniz/AJ/Yv/AdP8KP+FqeLP8An9i/8B0/wo/sev3X4/5B9Zh2PdqK8J/4Wp4s/wCf2L/wHT/Cj/haniz/AJ/Yv/AdP8KP7Hr91+P+QfWYdj3aivCf+FqeLP8An9i/8B0/wo/4Wp4s/wCf2L/wHT/Cj+x6/dfj/kH1mHY92orwn/haniz/AJ/Yv/AdP8KP+FqeLP8An9i/8B0/wo/sev3X4/5B9Zh2PdqK8J/4Wp4s/wCf2L/wHT/Cj/haniz/AJ/Yv/AdP8KP7Hr91+P+QfWYdj3OaJZ7eSF8hZUKHHXBGKqpBqaIqDUICEGATanP/odeLf8AC1PFn/P7F/4Dp/hR/wALU8Wf8/sX/gOn+FNZRiF1X4/5A8RB9GewNojPIZHXTGdjksdNUkn1zuq35eq/9BCD/wABT/8AF14p/wALU8Wf8/sX/gOn+FH/AAtTxZ/z+xf+A6f4U/7JxPeP9fIXt4eZ7PDZXtuXMFzZxGQ7n2WW3cfU4fmoZ9Hmurlbmea0edMASG1YHjp0k5/GvHv+FqeLP+f2L/wHT/Cj/haniz/n9i/8B0/wo/snE94/18g9vDzPZLjSZb6Py7y7VkVGWNYYdgXIxnqegHTigWWrhgw1eLcBtB+xjOPTO6vG/wDhaniz/n9i/wDAdP8ACj/haniz/n9i/wDAdP8AColk1eWra+9/5FLEwWyPZfsus/8AQZj/APAMf/FVQu7O406K3kmvrZbX7bC0qJaLEG+cckg15T/wtTxZ/wA/sX/gOn+FNf4oeKZAFkuoHAIYBrZCAQcg9OoNJZLXTvzL72P61Ht+CPTxZR6jrfmaYNlqkQbzZoATGecLtLBivBGCOCpHQYGx9k1jGP7Yix0x9jH/AMVXicfxJ8SxXDzR3MKyvkswhX5t2MjHTqufqT61P/wtTxZ/z+xf+A6f4Ulk9abbuvvYfWYrp+R7TaWNxHeNd3d59pmMflqRFsAXIJ7nPQVJc20sk8Vxb3AhljVky0e9SrYzxkf3R3rxL/haniz/AJ/Yv/AdP8KP+FqeLP8An9i/8B0/wq45PXjs1+P+RLxMHvc9r8vVf+ghb/8AgKf/AIumyW2ozJslvLWRchtr2eRkcg4L9RXi3/C1PFn/AD+xf+A6f4Uf8LU8Wf8AP7F/4Dp/hVf2Tie8f6+Qvbw8z2drK9bJa5szuznNlnOc5/j9z+Zp0dvqMUaxxXtrGiDCqtngKPQAPxXi3/C1PFn/AD+xf+A6f4Uf8LU8Wf8AP7F/4Dp/hR/ZOJ7x/r5B7eHme1+Xqn/QQg/8BT/8XUtnbG1hKNIZHd2kd9uMsxycDsK8P/4Wp4s/5/Yv/AdP8KP+FqeLP+f2L/wHT/Ch5TiH1X4/5AsRBdGZPjP/AJHPV/8Ar7k/nRWffXk2pX019dMGnncvIwGMk9eKK+gguWKT6GFz/9k=)

` `![image006.jpg](data:image/jpeg;base64,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)

7\. 安装过程结束后，点击“完成”。

` `![image007.jpg](data:image/jpeg;base64,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)


至此，编程准备工作结束。下面将详细介绍在Visual C++ 6.0，Visual Basic 6.0和LabVIEW 8.6开发环境中的编程实例。

**Visual C++ 6.0 编程实例**


进入Visual C++6.0编程环境，按照下列步骤操作：


**1.**     建立一个基于对话框的MFC的工程。


**2.**     打开Project→Settings 中的Link选项卡，在Object/library modules中手动添加visa32.lib。

`    `!(data:image/png;base64,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)


**3.**     打开Tools→Options 中的Directories选项卡。

在Show directories for中选择Include files，双击Directories选框中 红色箭头处，添加Include的路径：C:\Program Files\IVI Foundation\VISA\WinNT\include。

在Show directories for中选择Library files，双击Directories选框中 红色箭头处，添加Lib的路径：C:\Program Files\IVI Foundation\VISA\WinNT\lib\msc。

!(data:image/png;base64,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)

**注：至此，VISA库添加完毕。**


**4.**     添加Text、Edit和Button控件。布局如下所示：

!(data:image/png;base64,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)


**5.**     添加控件变量。

打开View→ClassWizard的Member Variables选项卡，添加下述三个变量：

仪器地址CString m\_strInstrAddr

命令CString m\_strCommand

返回值CString m\_strResult


**6.**     封装VISA的读和写操作。

\1)     对VISA的写操作进行封装便于操作。

bool CDemoForDGDlg::InstrWrite(CString strAddr, CString strContent)  //Write //operation

{

`       `ViSession defaultRM,instr;

`       `ViStatus status;

`       `ViUInt32 retCount;

`       `char \* SendBuf = NULL;

`       `char \* SendAddr = NULL;

`       `bool bWriteOK = false;

`       `CString str;


`       `// Change the address's data style from CString to char\*

`       `SendAddr = strAddr.GetBuffer(strAddr.GetLength());

`       `strcpy(SendAddr,strAddr);

`       `strAddr.ReleaseBuffer();


`       `// Change the command's data style from CString to char\*

`       `SendBuf = strContent.GetBuffer(strContent.GetLength());

`       `strcpy(SendBuf,strContent);

`       `strContent.ReleaseBuffer();


`       `//open a VISA resource

`       `status = viOpenDefaultRM(&defaultRM);

`       `if (status < VI\_SUCCESS)

`       `{ 

AfxMessageBox("No VISA resource was opened!");

return false;

`       `}


`       `status = viOpen(defaultRM, SendAddr, VI\_NULL, VI\_NULL, &instr);


`       `//Write command to the instrument

`       `status = viWrite(instr, (unsigned char \*)SendBuf, strlen(SendBuf), &retCount);


`       `//Close the system

`       `status = viClose(instr);

`       `status = viClose(defaultRM);


`       `return bWriteOK;

}


\2)     对VISA的读操作进行封装便于操作。

bool CDemoForDGDlg::InstrRead(CString strAddr, CString \*pstrResult)  //Read //operation

{

`       `ViSession defaultRM,instr;

`       `ViStatus status;

`       `ViUInt32 retCount;

`       `char \* SendAddr = NULL;

`       `unsigned char RecBuf[MAX\_REC\_SIZE];

`       `bool bReadOK = false;

`       `CString str;


`       `// Change the address's data style from CString to char\*

`       `SendAddr = strAddr.GetBuffer(strAddr.GetLength());

`       `strcpy(SendAddr,strAddr);

`       `strAddr.ReleaseBuffer();


`       `memset(RecBuf,0,MAX\_REC\_SIZE);


`       `//Open a VISA resource

`       `status = viOpenDefaultRM(&defaultRM);

`       `if (status < VI\_SUCCESS)

`       `{ 

// Error Initializing VISA...exiting 

AfxMessageBox("No VISA resource was opened!");

return false;

`       `}


`       `//Open the instrument

`       `status = viOpen(defaultRM, SendAddr, VI\_NULL, VI\_NULL, &instr);


`       `//Read from the instrument

`       `status = viRead(instr, RecBuf, MAX\_REC\_SIZE, &retCount);


`       `//close the system

`       `status = viClose(instr);

`       `status = viClose(defaultRM);


`       `(\*pstrResult).Format("%s",RecBuf);


`       `return bReadOK;

}


**7.**     增加控件消息响应代码。

\1)     连接仪器

void CDemoForDGDlg::OnBtConnectInstr()         // Connect to the instrument

{

`       `// TODO: Add your control notification handler code here

`       `ViStatus status;

`       `ViSession defaultRM;

`       `ViString expr = "?\*";

`       `ViPFindList findList = new unsigned long;

`       `ViPUInt32 retcnt = new unsigned long;

`       `ViChar instrDesc[1000];

`       `CString strSrc = "";

`       `CString strInstr = "";

`       `unsigned long i = 0;

`       `bool bFindDG = false;


`       `status = viOpenDefaultRM(&defaultRM);

`       `if (status < VI\_SUCCESS)

`       `{ 

// Error Initializing VISA...exiting 

MessageBox("No VISA instrument was opened ! ");

return ;

`       `}     


`       `memset(instrDesc,0,1000);


`       `// Find resource

`       `status = viFindRsrc(defaultRM,expr,findList, retcnt, instrDesc);   


`       `for (i = 0;i < (\*retcnt);i++)

`       `{

// Get instrument name

strSrc.Format("%s",instrDesc);

InstrWrite(strSrc,"\*IDN?");

::Sleep(200);

InstrRead(strSrc,&strInstr);


// If the instrument(resource) belongs to the DG series then jump out //from the loop

strInstr.MakeUpper();

if (strInstr.Find("DG") >= 0)

{

bFindDG = true;

m\_strInstrAddr = strSrc;

break;

}


//Find next instrument

status =  viFindNext(\*findList,instrDesc);             

`       `}


`       `if (bFindDG == false)

`       `{

MessageBox("Didn’t find any DG!");

`       `}

`       `UpdateData(false);      

}


\2)     写操作

void CDemoForDGDlg::OnBtWrite()                     //Write operation

{

`       `// TODO: Add your control notification handler code here

`       `UpdateData(true);

`       `if (m\_strInstrAddr.IsEmpty())

`       `{

MessageBox("Please connect to the instrument first!");

`       `}

`       `InstrWrite(m\_strInstrAddr,m\_strCommand);

`       `m\_strResult.Empty();

`       `UpdateData(false);      

} 

\3)     读操作

void CDemoForDGDlg::OnBtRead()                            //Read operation

{

`       `// TODO: Add your control notification handler code here

`       `UpdateData(true);

`       `InstrRead(m\_strInstrAddr,&m\_strResult);

`       `UpdateData(false);      

}


**8.**     运行结果。

\1)     点击“Connect”寻找信号发生器；

\2)     在“Command”编辑框中输入“\*IDN?”；

\3)     点击“Write”将命令写入信号发生器中；

\4)     点击“Read”读取返回值。


运行结果如下图所示。


`   `!(data:image/png;base64,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)

**Visual Basic 6.0 编程实例**


进入Visual Basic 6.0编程环境，按照下列步骤操作：


**1.**     建立一个标准应用程序工程（Standard EXE）。


**2.**     打开Project→Add File…，添加visa32.bas到工程中，visa32.bas模块包含了所有VISA库中的函数和常数声明。

!(data:image/png;base64,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)

随后增加Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)声明语句到visa32.bas中，也可以新建模块来声明Sleep函数。


**3.**     添加Text、Edit和Button控件。布局如下所示

!(data:image/png;base64,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)


**4.**     封装VISA的读和写操作

\1)     对VISA的写操作进行封装便于操作。

'-----------------------------------------------------------

'Function Name：InstrWrite

'Function：  Send command to the instrument

'Input：  rsrcName,instrument(resource) name   

` `strCmd,Command

'-----------------------------------------------------------

Public Sub InstrWrite(rsrcName As String, strCmd As String)

`    `Dim status As Long

`    `Dim dfltRM As Long

`    `Dim sesn As Long

`    `Dim rSize As Long


'Initialize the system

status = viOpenDefaultRM(dfltRM)

`    `'Failed to initialize the system

`    `If (status < VI\_SUCCESS) Then

`        `MsgBox " No VISA resource was opened！"

`        `Exit Sub

`    `End If

`    `‘Open the VISA instrument

`    `status = viOpen(dfltRM, rsrcName, VI\_NULL, VI\_NULL, sesn)

`    `'Failed to open the instrument

`    `If (status < VI\_SUCCESS) Then

`        `MsgBox "Failed to open the instrument！"

`        `Exit Sub

`    `End If


`    `'Write command to the instrument

`    `status = viWrite(sesn, strCmd, Len(strCmd), rSize)

'Failed to write to the instrument

If (status < VI\_SUCCESS) Then

`        `MsgBox " Faild to write to the instrument！"

`        `Exit Sub

`    `End If


`    `'Close the system

`    `status = viClose(sesn)

`    `status = viClose(dfltRM)


End Sub


\2)     对VISA的读操作进行封装便于操作。

'-----------------------------------------------------------

'Function Name：InstrRead

'Function：  Read the return value from the instrument

'Input：  rsrcName,Resource name

'Return：The string gotten from the instrument

'-----------------------------------------------------------

Public Function InstrRead(rsrcName As String) As String

`    `Dim status As Long

`    `Dim dfltRM As Long

`    `Dim sesn As Long

`    `Dim strTemp0 As String \* 256

`    `Dim strTemp1 As String

`    `Dim rSize As Long


`    `'Begin by initializing the system

`    `status = viOpenDefaultRM(dfltRM)

`    `'Initial failed

`    `If (status < VI\_SUCCESS) Then

`        `MsgBox " Failed to open the instrument! "

`        `Exit Function

`    `End If

`    `'Open the instrument

`    `status = viOpen(dfltRM, rsrcName, VI\_NULL, VI\_NULL, sesn)

`    `'Open instrument failed

`    `If (status < VI\_SUCCESS) Then

`        `MsgBox " Failed to open the instrument! "

`        `Exit Function

`    `End If


`    `' Read from the instrument

`    `stasus = viRead(sesn, strTemp0, 256, rSize)

`    `' Read failed

`    `If (status < VI\_SUCCESS) Then

`        `MsgBox " Failed to read from the instrument! "

`        `Exit Function

`    `End If


`    `'Close the system

`    `status = viClose(sesn)

`    `status = viClose(dfltRM)


`    `' Remove the space at the end of the string

`    `strTemp1 = Left(strTemp0, rSize)

`    `InstrRead = strTemp1

End Function


**5.**     增加控件事件代码

\1)     连接仪器

' Connect to the instrument

Private Sub CmdConnect\_Click()

`    `Const MAX\_CNT = 200

`    `Dim status As Long

`    `Dim dfltRM As Long

`    `Dim sesn As Long

`    `Dim fList As Long

`    `Dim buffer As String \* MAX\_CNT, Desc As String \* 256

`    `Dim nList As Long, retCount As Long

`    `Dim rsrcName(19) As String \* VI\_FIND\_BUFLEN, instrDesc As String \* VI\_FIND\_BUFLEN

`    `Dim i, j As Long

Dim strRet As String

`    `Dim bFindDG As Boolean


`    `‘Initialize the system

`    `status = viOpenDefaultRM(dfltRM)

`    `' Initialize failed

`    `If (status < VI\_SUCCESS) Then

`        `MsgBox " No VISA resource was opened ！"

`        `Exit Sub

`    `End If


`    `' Find instrument resource

`    `Call viFindRsrc(dfltRM, "USB?\*INSTR", fList, nList, rsrcName(0))

`    `' Get the list of the instrument(resource)

`    `strRet = ""

`    `bFindDG = False

`    `For i = 0 To nList - 1

`        `' Get the instrument name

`        `InstrWrite rsrcName(i), "\*IDN?"

`        `Sleep 200

`        `strRet = InstrRead(rsrcName(i))

`        `' Continue to switch the resource until find a DG instrument

`        `strRet = UCase(strRet)

`        `j = InStr(strRet, "DG")

`        `If (j >= 0) Then

bFindDG = True

Exit For

`        `End If


`        `Call viFindNext(fList + i - 1, rsrcName(i))

`    `Next i

`    `'Dispaly

`    `If (bFindDG = True) Then

`        `TxtInsAddr.Text = rsrcName(i)

`    `Else

`        `TxtInsAddr.Text = ""

`    `End If

`    `End Sub


\2)     写操作

'Write the command to the instrument

Private Sub CmdWrite\_Click()

`    `If (TxtInsAddr.Text = "") Then

`        `MsgBox ("Please write the instrument address！")

`    `End If


`    `InstrWrite TxtInsAddr.Text, TxtCommand.Text

End Sub


\3)     读操作

'Read the return value from the instrument

Private Sub CmdRead\_Click()

`    `Dim strTemp As String

`    `strTemp = InstrRead(TxtInsAddr.Text)

`    `TxtReturn.Text = strTemp

End Sub


**6.**     运行结果

\1)     点击“Connect”寻找信号发生器；

\2)     在“Command”编辑框中输入“\*IDN?”；

\3)     点击“Write”将命令写入信号发生器中；

\4)     点击“Read”读取返回值。


运行结果如下图所示：


!(data:image/png;base64,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)

**LabVIEW 8.6 编程实例**


进入Labview 8.6编程环境，按照下列步骤操作：


**1.**    创建事件结构

!(data:image/png;base64,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)


**2.**    添加事件（包括读操作，写操作，连接仪器和退出）

!(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAYEAAAEvCAIAAAAsLertAAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAgAElEQVR42uxdBXwbV9LfpNwr3LW9MnMKl2t7uWLapkmTNOiQKTHFFDNDDDHGEDPFzMwsMzOzLVtmsWXZli3JsiRrv1nJcR1Or+317j7Nb6qud+fNmzfvzf/N7GoVBJWSlKQkpT+OEPjv27j2z0M6XzLuv19+5lEVyhNqtKc1qc/pMV4wWXzRfOllK9ZL5qyXLDB+0Wz5RZMVKf9ebMp+Scq/G79oypLy78YrL2HMhmX8ArDhyvP6y8/rAS9hnzrsZ7SWnlFffEZz6c+aKw+fZT9+JPX5n86/dOTkBgZ9GdT20Bk8co75oBn/SRvhX51EL7ujr19B376CvuONvu+Dfb7thb7tjb7jJT6Q8u/E3lL+3dgLfctTynfiNz3uxBsytxTzRF/3QN+4gr7pjeHGqy7o6y6iV5yFLzusv3xpHT5fclp//pLwWTvBs3bCpyz4j5nxkfOi7fsHHjuksYFBL2h2IAdHkLPTyNkZRJWKaDIR3WVEdwXR4yL6XESPgzH8qcVGNNmI+gqivixlKf+X8fllRI0l5VvzeRaizELOLSEqS4jqFt68qsJClMTHIKN8g4xY7PwSxnDp/AJydh45w0RkF5GTC4gME5GZR2QYiAwdOU5DjtKQfdPIniHkEB75cgT5u/cGBiF/q0EOdCMn8YjcOKLEQFRZ2JxpAOhwEE0OogG4w0RUaYgSHVGkIvIURE7Kvx+TpSzlfzefJj2pSrZLZQXjuIHF3IAirn8h16+Q61vA9SngeuRwvPJYb+hTkWPEA65zYWUbMlvFvPM4vvkr5/wYyLGZJ8+R/BMnSnK6cNkduMw2XEZbcXpLcXpzcWpTUUJNTELfS8cHkJ1NyN8qkRcSr2HQm3nb9nRhGKRAfk8pa/+FkD1a4T9oXf1B++perbC96n5/VaxHFBfE6IOZ+1/Pp4jIcTGfJv6H2Qb2zP5GTEROzSLHxHxq9jfV/F/LJ6elfGv+acoqYSG7XuiRumYaxtP25533XlW+sqrgxj3uyP3SiHPIfNo2lvyWLrmgZS0wl28Ty9Py46lcWT3rvirrsnrMgbvXanWnJsM5evpjE7pD5AxaHCgMs+a5qq7ay3NtznCtTnBMflrR3s2S/4B+4Qv/0E7k793IezXIM1euYdDrhcgPA8jJSURxeb9uaKCnkZODua6RnrWJgd0lYwdLrQ/UChEFFoZBh0nIQSJyCKKFjJy5B5YlI8dJyAEicpiMNTwhPnMHsZ9IiAwJ+/MECTuGJqdvJXaMjKUMp8QCP12TPCU2Dzo6KtYAVw+RbtHpafL9cuQXtOgfWLKQ07SNTo+Tbm3YzXyavNEpKIfuZCl3EjtIQo6QNs5griMhx0g3GLOh7QwFO3+EiByYxSTh8zgZcwX0coiIjUWWhBwlip1PFGsg3ZZliMhRTPNDiqQdpoznNGnb5GkYwG0KwPFPsxvzeFyMwqDzgMTVt1d7VGzbzTI/ayNu9HJa7Jk7a/tD+DRRyrfmwzPuOSsBuXy/3DWLKN6FwFXAF3k37gknzkFbztdm3LfkRhzjiV87zCdXC1xTeO4Za7axGFrpBa9q+a+qeHGPOKy+fpau5Ta0z3npatwwGmu3mOjHDLKj252nWilRTeXIFw5RjE6Slb7u3/9CRnQF8vkY8m4r8qzvZh5UgewdRk4S/3p68sBP9tEGf21uf07J8unHX34a+fzBHV+88Il2HSK3tE2eoh2xaJO8ZBiziMhAkItDSPJ5Rnwg4TNb/jxG+taBYZe2bBY955m3vMOYDuncz2Knr4kdJX1tz7BJYTlnLL2uR0f2EZ9Sp1/OWfEqZD+tRsHwSKLzOOkrW0zbcTcqcmj6mfM027Rly3imZRzDNoX1V+XpMz5Msyj67kvzWOV5gmwQy3LPW/nEcg7rdDPsj5I+tZ6nMrjG9rXfGgzYJLGc0pfeNaJjASlLvoVtp7f8KUN6UoVinbwMm4Zd8rxWxDJyfPYWTpAhPa5EsUxi2aYsKQYsSABLMQgz5qjnAnJkdsOSk6THxGIXkxb/cnYaDDvtswD5sGkU3T6N9YM95S09innM/IUwxkNQIB8gfWnPdM5aNohdxlBmK4qd2sLHSDBeeU9Ageln1Oge8ZMUCusluT7kJHVzXh5WpBjHsayTFs2j6W8bzT+iNGcRy7BJXnxCCUzaMorr5/GYJxNse0COhGH6mZ+vPiBPNohh2aQsXQhfwLDvJPlBRap2yNzT56Y2lNys7dTtF8zW8/e4z907n5LybfgQ0SVjxT5+zTSCp+7Dk3VePXSR+60J5x8G7J267J163I+UR50SSF/aMcNxfCWv1bRawQ3P12PLBX+WoRt64/c4svyjRta9tRjeZgIacbkolajw1czRDxYi3PjkafK5rwZ/ejU1uhb55/j1GPR2I7JvHDlDO/tVRPAH+5tMnuDTn+uoe6Og7akj+vfv+PLxb9Vw2xSWkWMUj+K18YHJ8NThgDIetqUfIz2mNo8lIKfJDyiIFw2wjHgDl6U+DpcOEj8wZaCCtePKWaHpU1/LFSM/zj6szHjo3ByE3AMKlO2y5G1y1CeU5t8zZXLZqz7BzSV9/K9NGAVtK67u5eHxva/sxyGn6ZsY9LbBnEgoPKmag+wdeViG2k1EY6MbgxOHOprwBzSqxsbostpFRBr38cN9/qW8hPhmv4je7+SLAOZ/TlgA7xwW54g05P2MZ9VIK+w135Cm6sG1DwzoYO2DZ+kPKwFmkR45S9kYDqRIJ8kbIz1DhXyhjoAWZLUqmTW7B7YiX7Qgsownzs9LQBnCG5r8SYXx6BlG6YCotrw/o4yoHrqiGcEuLOh18W7RsqhAfhhC5GgS+HjgCKl4QNRe0/vQJyXIUZpcAIu3uHBMJVfIW/3uVEbL0LKBJa6pg6rtM/6ZEbWxneTsUe/o1bT9myZEniHR8KACeZss+U+qjPsVaPcr0h9RZryiy3j3VN22I3jkOPVppemlOeabB4uQU/RNzLrvEDGpWdjZNGLv3drQM3//j0MHrUdR7uJ7J2uQE1Dzk0DbfQo0bODHSdvlaY+pMgBc9l5moWvLrxytfUCBed9ZhjjlwbRtP0SMqOH3d4zGZhMu561uP056SpP5sXr/o/ubYUWBtkdVGGAYpg1WhRz1Pnnqg+fmtivSwHLQ8Ph50CZ2uPKG2HWe/21h6LSUb8OHic4ZKyahaxp+vHPuq8fsuD+Yc/5pyP5Qh/OOFuf9C9wPxBj0lT0zuGDt6KXVlGpB19g6rk1Q1CrIbhKUdgmjyoWPn6AbAAY5AAYNC5zP0S6qLMb7oyLRYqzPvI8V4MxCkO3sT28MHXk9NaYe2TWDvNOOPOtzDYPeaUEOTANqICro63KhUS5/aSt4/az839Hpt0YDnvV992HPr3TuP8tEjs5px/FqqobfV+xcmGc99kPT5TxeSMpocj3nY6uV4i7eEFHQM8XfZbP4ovpCSuV8SNKwRRL7YSXmFJmTVYgPzaMhf28/6ruchpvJKJ35xnH5XR1m06igb4Jj5t72lOwoaW71tQO4hrH1xPSe8ZFZ5O8FyDdTiMwMIj+PyNIxPkl/VIlBpnM+PV2KnIDAoP7j4iKRyiYy1r45nvrIfkJl/9oEedXlSs1Dn1eyRWhdPSEwafxFxUksAmWv8THal5eWqdO0h7+rQc6uzNJ57x8ubhoT6Tg2f2JMy6yk5FaTTwXy9GNWYDjAXgWch48zzBNXrqbgUyrnXlJe9MHxm5vGazqYr57qeOoMObqc5R835Jm7fN9Jhnsue4QsTMglvHusxb9M6BvSesJxqqN7tquHqGNVgfytD9k3tk1h/mdjDlCDKtfT0zqQL/sROeaDx+gZDSsDE+zIuPb73ixQi1ibobAHh+f+8n68ew6bu7KSkjFw3GF6G1Q9Z+aQM9hYdpox+2YF/vHDJa3MeBx1v+5ASgU9uGgROQCuo7+mv8igL71xqAw5xcTkJbyfapPO6+8nJ2TjQyJbkV3tT2mx5+aW3z1SihyeVw9bjskez6ig7DBjvWWwmFZJj84i5NUzX1OdoDFWS2tn6rrmnz/ehZyc29R2MYOfm9f7D61+Cmn+zz+1u6eQW4ZWXlWbQn6iqV5lRWURMqsoO61YbxssplbQ6/tY/qlTjx8aSWvm4ynrwQkDzx7tkvVnxeSMp5WTP7dfds/jSDxvmsBGZOawennTcin/TnyE5pTB1vRdVXRflXNdPWLP/d6Ks8uU874B5w0d7ps6q+8ojTkmkL92WPLNXttjwYkv5xtf5X2iy/5Ih/28KnuXJdcrX/Do6Tldr9EfnFYAg9asZWgW58gaBxh+1qJVrkjAZ3oZzOx+jHT0jZFDL6dG1yFfkpCPe5Hng65h0Pu9WAEP29G3/L9+0O5n9gNKe7Ku8A0bvedffPrBF95/4u/GLcg5IXJkUStWWF05tEO5j05bekumZg1FvX2riwt7PzhZG1+/JsnK3MP7FbyoPW2Ed45WLLO4L5/pJlAEUSmDYeH1yM62DipqYFlyMWyyoWUa+WxkeA51dy9BXs95TJFCYay+drC0aQpNiG3o75o4ot9UN46qeExgt3gUlxCFBUR24RGVJTKd+7FMCfLTEnKC9YLekrjPtWd/KP3CUdDeTVYyKm/tYz6nTJpbER1SzOweoJn4jiAHqYjCIqYB+ATzSycudZr68He1yDnuDI33/pGS5mlUybgiooLd3kII8Kt29W3+WHtMMhw+e+WFY81MDvrx/ozGQY6mS69DBqeqdryoaPiNvXk/eAmpE7PPfZvP4wn+fLjtdIiQMkH803vRyGd94fUin5CWU26U9vaJlsYRc5eGyFJ2btPSEydGobDdMOYnZkAVmpbajnw2gMiykcMLyY2YG/1CmpHPR8qHhMa2FWU1UzIOs675wmLcgIpJ5SxxEfmuH5FZQc4sYYOSYdbh162da+t7lgzNcpB3OozjlnuaBpFPWkHha4bLGAYdrkBkVxD5hQ3+ielSKEpMat+t0TJLWkK+6XtCa3WOznrxxzLk6DKVhf6kmJNQxrgSPXIxiVVb1nPfrrpdSm1vyPescIXMucXvjychX7YjZ5c3tB1iWmWu5+T2fq43wqAwkF2198nOrTAX3z2MQ46zD9lREuJaBvtm3MIHD9hSO7un+zonDsulIJ+NBlSjrbUD216LRw5MHLSlxsc393VPu0UM7bOekXiePE1HvmtDFNg/W/4rWU7Kt+HjTMcMACDuSSfuYUiCrLmfm3M+BAwyX33NePUlA97L5wiXEqjfOHHc03m7DNjRpdht6T3W3N023B1m3L1uvCtFwm2n5zU9R3+4zPePwq8a7qManiKr71uIcl/nLK+vcpbC7cl7HqUefgG//6nU6Abku3nkb8PIi1HXMGgHHjlCQc4xEWXR3gsJGb57mtKP2Tqdk1FROHv2nKGW7N906hBVdNsZjn8VOjVKSi6csnfAPbm/bZwu0rxY7x3WseNEdfPkRmWYUzRyxJUO26x2ALGrfeprpSqhCN2r2458h0eO0hPaRNHJfYnNwtDgqqcPDDPXUJ+wrmfUeDvshFyuIDp1MLdoeOe36Qm1nOjyJQp5YcfuBOyLBiqriDIHked8ZMNbFwovuHSltqH7HOYfkVlpmkZ7mwcf3FG43x8lDM+euYSfmqC/sqe0Z1akatcxQBbJns9GZBYQFS6mAViW8427kEmmIV81vmqNrqyKolP6SysIL+1M8ixZx5UMmVzuVDIoPetN3RiPkPuFZmfTOGrg1t0xg8qpZ5f0CWpqCchXfciP41+6rE+N085dJkxNzT/xeb5LOcqYJn2sMf6gClpFQJsbRvMqifJKafKOE3lNC90k1N+jAPmiHVETYJYocR6SY5ePoo31YwbBtLAqHnKQcdxfgAp538ukIQcovbOogVNr/SiqZlCkG8HClQ5fSl7A5Xe+fKy1gYCqBC4ix5aQk5x/2KyCmcPdY9vezXhVSxDbhpLHZz/RmERkhc8aCJaX2G8erUEU+MhZDsaKnPtPsjO70fbWCZt4ZkNl/4NfNpwOQ9H1NWX7ngcVhRWDIueArsphVM+sUNGb0dU+qexBMQih7nVcEAkFtGlKZMnCn9REGDSItd13kh3XjA73TafjZqyt8h/6tvNICIqK1rWceh5RFNjnCHCFPZA25pUQDtnPTZFYVtb5933bvF1uvQKPtjXi31ODNEdkly0ow/XV143hKsYdEugSx3Pm51+X60UUhRuW/3pWlPJt+BTHIYN/xI7zkx2nulfYPbHeOS4s7hF+ZMd70Xz1GcO1p+QJdvH0by8LHBN576uvRJXwzaN4n5tzd9lw3zDnfuOxdqVUCLm2itvoXg+Rf9QoR+OfJPV9S5kRMI+LYZeYnhfggJ3qRdv/xOi3D2EYtI+D7JpEXom7hkEfjiHH6IjyMnJ+/UvNRF1zx7P67mf1LmuYXr5gdUXL6OJr6g2IDrpNd13Rh6ZnU62mX4B8ikNUBDsd+HquHac1C18806Xjhde1qda1q9ezrX7i9MiRKywD26q3v0/5zHBc17F5v2bNNkXONg30ccN1Xd9xXYuShz/Les2CrePWq29b9a5869/suDqOrWYO1S9/nYwcoT9ihJqETO0+koDsH9x2Ad2mvrZNnb9NRfAPZ56uY6u+fd1F19oPjxQgcmtfXObtkcvBniJpiA55LhrY13z6Uwqyf+w9B5He5a7TajnbvqpCtNa3afAxDep85Bx/p/P6GJ5y8UrnF5cWNB3boNM3dicBCj9siKr7Tps61r66v+iIC1nXtkbXrg74C+X6lwzZeh59p9Ry/vxjrY7/tK5V6ZNnxhBtFFER7nNfNrhU9/nhlG2HRuX958A/cobVj6vQNf1mwAPHlTKRzxsRJfSoP0/fuuyRf+YiYIaGADNGjf8ng3Utn0ldmypTlwZlndztB/EPGaEqDj0P7q5E1NFXLNf1PPqVdPLv+xy37QJfxY9scLHiuS9S/qw9bxOC//5U+rYzzG2aQkRt/aTfwicHYAikT12Fes6tena1MrrVz6lSvXKWRjuGXz5QhmigkuFDpw/prp/3mQG369vVvPx1yqNqc7q+BD2bKgO7midPDDxltq53ZUjNoOChzwsQTZ6CD83EvnLHj+nfWs1o29ZrWlVbuDY8d7oflgqm7Tz/AZ11FR8iaDurnYd8UvGYsUjHd0Ki7emTfc9brau7DuherFI0qLIKm6SSFjIye6KquferLmv4TILYoQu1208xX7ZZV788CGL6l+qBYRWJufYTpZZt51Y33PWrGVEVSPnWrCC4lCX8zozzrTlngirirqGrfHRiTvThJd6zFmuP6fEfPkGwSWB854Vax/JeVFzxzFgrahdGVwqiagRBVcLIRqFj4TpyhCnvPLrXB/WLHmXLv0dS/X6NMMBK8ifL76SceoPlbyAc75mXeX70MyQ1pgE5JER2U5FXk69h0HsjiMz8NtWV7Zpr9+tw79dZeUCf+6AR90Fj+OQ8ZMh9wHh9uzG63RBCji+uI5a36aPbDVBEYx1RWEHOriB6KKLIxaoDWRYmoMFFVIXYgfoacgFF5JaRs6ztusLt+iiiI0LOrmKpDRzooog8GxNTXUE01zEx2SVES7jdSCwGCpU40Ol2PdEG64s2xORZmKQ6D7Ph/DqizAXN2/REmDflWIjqKqZBU7xXS0zV26JEV7TdQPSE4sTrp+qRk1OI4gqmSkOw0ek5Hmab9jqiLsLOw3CAAZ0h1GG7UGBhIz2LyWzTvNapmhCzR4WLaVDmY60Ul7Zp88ViS8g5NjYEGDiIgW262PGmMZgHMG8sYZcUV7brrYsHvrpNW4ANVguGwMGeSEKnwOfWMNs0BQhog/PKbMlwMBugXzWeeNQSN7IQhaUHDfmvaEw+sa/qgVPjMGRs4LpYp9t0RRu2YQPnI+DDs+K5g440OMgFETZSmBRdFOtXaW1DTBPd8AZIqnM2PCnp/ZxYm+LKNgOxnTAisTYQE2vjYlfPLN2vyzsfTDe0xH0nk4zdIVYSt8IWhuBnMfCDHGujI/hTGfPJhuW/mrddkPKtGTkvcsoT/k2T9b7mytcm7C/NOP+04HxkyX3ZZPVJvdXtajzkx+FLSfQfQ1CTMM6TJ1i7DNn7bTgHLnH3OHK/cFr90Hb1CV0e8tPcKbvBg1fRoDj80sGnp4/tmFX4YvbUxyS5nZQz71J/epp+8M+0r7cNfYBkx9chx1Hk2znk1aTNe9LDGAapsLdDVF8QPmCAPmCMPmiGPmiOPgBshj5git5nht5njN5nhN5nKGaDa7z5p+H1bHCrA4PrJe9wfHOrm5tvlTS4VavbaMAQAaIFUNXoJlW3G9GdNd/u0s1iBncaEQZPGEyIQVMSOfoSzLp2Xn+LzCaW3fCn/obYNl0xIhii2wwlTUQ3yt+gbfPPW3a6VUZ/i8IbZG6vHJEg2qk5DFkM0Tu12sp6ot+OUSnfkmGD0UkSqrlMvCPb+3fl/p3KfR+rDL6vOvy2Gv5VJfxfTw3vvtBun8F6ywl1S1vYea7/o3N9f1fu+5vywIcqQ2+rjLxyDv+sPP4lmW7HqLGdl1GDcCbN6Ie+PU8NHH514Mhrw0deHT38AuHAU2PfP4z//L5RxR0+iVPIESHyHQN5JXYTg4aQ4wxEgYmcXdymsgyb4f06vAd01+7XF9yvD8nL+nYDjCGhwFBTSyjl34mx3E0T/V9mLRQrYLX/KANEUr41q4se1RGaJHIupbEcM5YdM1hO2CfwikP6ikPaslUy53lTIXJOtNttzSNv2SEdxCSSmIwjJrPikrF8yJOLyPEfURfaxDKD4kaCE0aDE8eCk8ZCEvAh8fgQ+DMabx9GfUpxFflx+QYMGkb2zSJ7R5B9o8gBAnJoGvtCzdFZ7OvIx6jY9/2OUzGG4yM05LCUpfxfyIdoyAGKlG/NBynIjxTkByqyj47so137vMY/0pC9cCAW20sVH9Ov8TWZ/XRkLx3ZA3rIyD4y8i0d2T2PfDOP7GYg34o/JQdfMZB/UrG70bsIyFdk5LWEDQza9vbQI7IUtUs5hjZBWhZB2pbB1xiOsTNbWXJSyr8H3+BqKf+2rC3lO/K9OHDzWNM8UN8mTN82DA5+lrG8O2uYB1i6hHsmE7d9M4O8EL6BQdvfHvqLGsPR068sx6+rObutLv1GrpeylKUs5Z+5vz0vIvhSsK91f0fBL2rYXJNMHMWNkYUIYNBfg3/GoD+rzJk7+Q33lgnXaJzlaSlLWcpSvgOjKDMlKSwqwg9FF39xW/50xxgP+XoGeTbkOgyycPbvbS9cWZpi0EbYrKl1Pm2dT11iEhbnCcuLk/N0vHCNyuMQ4Soc34EFPMr6GnWNSwLJBcaYkEdhzo0uL04sMcclbeHPm1uJO50G/ayFcf4qGTpdWZq8a183dMpamLhlEzgJ4wKdt7wK9tzOJGgCo+auzNy7JbfTtlUteEPsXprE2zdchUmCS+C6O3QqGRF3eYa7MgtGSuZoq/yG8WLn39Vmcaczq+zZ5YUJcD78yaBhA7nHGZfy/0Pmc0kJccHRGAZxhWuUe+d1PmV9dbJ9dPVOGAQAVF2RE+B3OcDPdXigkYBvbW0qgRXp4+2UkxUL0HA7HIGwoZEHQ4OvBAe6J8aHgOTURGfYVa856kh7a9lAbx3gCzQEsZvbQqeV5Vmgf2igITY6cGyktbG+UIJ9W/tizt3c6Sjojwz38fNxhi6g060oIDmAmK+rzhsfbYOw3HJp4yrYc0uTQJg43evj5YQrSgFcuFmt5My141tou6WXwMNtLaVeng7eVxxrq/M4rOmtagGIcUWpvj7OM5PdEmtvqQTQtrkRV1meXYpLgwkaGWqCOQJ3bcoD4o+NtIDzqeRBsGeLkfhbOh86LSpI7uupiY0KgLaw91BJAzDj2ZkxK4uTdwVWKf8/xKDU5HBPd/vICF+IEV/v2zJc9fZy3GQ4Q55q7Z0S3AmDIN5KceknZA5raSpXVWTTyEOjw80LDEJsdMB5NUXYMCXJEYs5fkPowjKFbVn3gpr6+bOmxhdW2URYvnJyMp1tFZOEzqnxTthpa6pyITAgS7o5Mqsqsw0NNCHBMzfVBc0jg42L82MQbHAMn8AAJRBmN3cKe7WBgYa1laHtRWM6dWhz695su8gYG+yrJ073rIibAxQuzROA4VjAI6enRmZnxoK1N5gE6Y+bqy042sbaqLmhmMcmgjzEJyiETiXKIROhU4bE5zGfQDoGMJqeEgE2gLXiBHDyBrVwCdwre+bYyROHczJjUSFdom1J7E/oFD/UpCB/AvAFjuH8HHX45kwEOnJ2soYJUpA/mZcdP0cbgTkCd4EZEm2SreL0qWOD/Q3clWnQDGckDtxMSDcZcLCwINnMVDcqwtfxkgUqnMPmd2EiJipAVUUexigB1qWbZlzK/58xKDc77qzCSSsr64aGpsam5vqGxoYtXF/fUFcH3NjY1FJdU1tdvcHGxqYFWWGjNPROGATreHqi66svdimdkxWtL7g6X4SkS7BGnZ3usbI0hMAgE/vdL9sGB3lI0pCtlkFEhV298uGH79dU5iwypyGZ2v/j933dNRbmeo31RevCeXtb0293fwFLGVb5DTnUxFi7uakOdEclDkDDiDCfNR4NP9R80doIAhvCA8DL7bININoNgS3i00D4rOLpspKMoEB3nQuqTo6WYG1mepS1pSEkFDNTfXCSMNo2M9EFOAWwQqUQrgZ7ysnKQMCrKMspK8kCBt2w1cNIAQ2ZjFEYkYebnYqSnJ2tCXimq6MSwrW+tgDGYmKsDekMhHRggBscLC1OA/7KnTnOX6WCnWamOhWlmRI42Fr4iAR0GBFgOooud7SWGxtq11bnU8iDdramEPaoiHXF06GiLHNtlWxkqGVlaVBdmQMbww2ZC+RB//jH31WU5Rlz4y5O1lnp0YvMCTUVeU2Nc7VVuRTSMKRaBw/sgewPdIJteTnxVzwu+fm4AMqvca4DXP+8doIAACAASURBVIBjGJfM8Z+OHT1YVpLe2lxiaqLT01kN8Gpprg9T73bZFsAI8tPNlErKUgyCNawoL1NdVVVcXKyjq2NlZmVpaomRmaWFsYWlpZUF/M/CwNPNZesvDaWmphVkheKpd8Ogof4GSGR6u2sgYYFsHDIuFGVOT3YDBqHoSlZG9N4fdqufV4RsH3KK6+BAQAf4gPRsZLgZICAkyNPX23mS0A4nszNiUHQhJyvOxckKDm7YiiUpwyU7M9nTx6CvElyas6M1ivIvu9ickDkEOU5acviHH7x3QVsF8oIb8GudTw0J8shIi4KQhphXkDsBO/YkocPKwiAlMRTCD0XZAIIDfXXBgR7Hjx60tDAoyk8GsAPUA21gZFxMEGz+N5gEGAToMA9FqJczwJaL08W0lEjAo4tWRoB3gf5ucTGBpiYXeFzS+Fg7nDxwYA/AExShEWHeKCrQ0VZRVDgFI4Ls78b5WyVDrgS4CbW0lYU+JDKODpbRkf6g0OaiMZh0xcOhoa5QyKclJ4YBBkFKCFnJVg2Q0Qz01AF6gn4UXQTnQCmKojzHS+aZGdEuzhcT469GQH3q61yQl+jsbB0bEwg5sKzs8Z07P2ysK7wB0QCDhgcbXZytAegL85PUVBUAcQCjwY2AQeDV5MTQqAg/QLrmxuIbIFXK/58x6KzCifLysqCg4F2f7nrrs7fe/Nubb77x5psfvvnGp28oKarFxASGhFjraMmtr2/5tbPYuMLssLtgEMQe1CbycjKQhKMoC5a1vKwMBAZkEAf274E4IYx1GxloWVroU4gDkP9vzWWAtbWUzc10HezNpyZ6YVkDgiTEBWlpKtlYG/N5lOnJLmtLA8A1qOluyA4AejLTo8tw6Si6Bnv4sSMHmPOT7S1lUABCzgX5gramMsStiE/dChaQiAEOXtBS9sCAUgCQd+bUMeyOxsIEAJOxoVZPZxWct7czg3pqoLdOQ/2cp4fD7Eyfk4MllFpU0sDQQAOINdQWsFnTN5SHUDQ5O1kBgM7RR88qnIK8BnI6gDnIm9LTIqFyhBCFbIVGGYIU4/ChHwEIxgndkBzV1+EgeVE6dwaSnRsCnkHDKikoeYyNtAHQy0sz9HTO52bH40dawW+Q6xXmJ0I+AvkU5CbJiVdPnzoaFOAuXKNehxpMwuhwC5RjYiBbvmhlCGnaHG3s+LGDgLng7eLCZEheTpw4BJgYEuwJSDc10enpcQlsg6L4BhCHGYfkCHwOxjg7WsEeA1Ue1IkAOpDGwqX6mvwzp48B7FJJg9JyTMpbMaisrDQmKnbH33YgsghyBMFoH4KcRk4qnygtSc3K9rQwOX93DLrvegyCfTszLUpf9zwUQbD7QS0Dy51GHhzsqx8dbh4eaFxhTc9O9UA0zlFHtt7jhJVNnu2D7ANgCAJsoLceWo0MNkG6MTbSCqWQOLAnZ6a6R0dabljKEKhVFdm2NiawsUPMTI134Yeb6ZRBOA9toVPAHSp5kEYeYt50IxxKBgA4QATHS5a4olQIXTizyCQAbk4ROsFUN1cbh0uAiZ1QcEFtAgOBnIs009fdUQVBBV0Q8K0QmTeYBJAE9QtgAYwIov2Lzz8rL8kA+IAcZLC/XjKiMXzrPG0EkhTybD+UjaAcnAOfkIUBgkM6CQI3qAUPA7Aa6Gvo66kDcoHTxLdyCNAdAd+G2TzeOTLUBHAJtoETACIBKG+ogMDm/NwEmCDIm6DUgjkCe2jkAWgIzcHh4C7wAzgfZgRmAc5Av6AHjm++uwQzDnkZpIpQDELVCZAELoImYD/MFFS1MCkH9n8vmT7AUGkESnkrBkUHxXxs9DEGQHIIshdBFBFkN3IqUS4zOCAu3NbUVOM2GDSN/DXo1hgE8QALuqUJB6lBZ3sFhNy1u7Djklunkn1YcvKGegrWNyQs0BaSDggGCHXsljB2g3Nc0lDS9oZ9ePM5TmN9IVQKEKIgL7mnK761jLWF40XxXeSbn4XDJ9gJPcJ2DdG4+aQJhMEAQIe66nzIv2Boko4k9aPktuvmU6SbNYMAlG8wlqb6ovragu6OSohnybMqyaDEz4/GN4XFziFs1bZ55ga14Bkoaloacc2NOMmj+q1mSO7ES2yT+Plm2+A84AsY1lhfBAWgxM9bDVsQu0vSVnI7WdL11ieDW00CFG5qKALn93bVSBpKHjtILOnrqentqpY+HZPyrfOg0Nh3Tr2DZUDPIIgegryCHR5yOJbk7x171dHM/MKtMeibaeSZwBsxqLs1DxY3nQy77ggLVj+ABWMUkpFfxEvMMUlbBm0YVN1rQ/LAPP1ap/O/vNP5jU7n6Td2OkcdYmFPi0Z+gTHXTFqYw0vUbhnR4C+17Wa1oEeiEMz+l5Uwr9n2L8zRrbTd3vnkQegCpvXX9iLl/yHmsWeyMqIkGBQRGXn62Okfvtu7e/d338vu2bP3h2+//s7OzrmdUJSYckFJ6cx1v35/WwxSnbN0CajEJQ30Nfd1N/wm3Nvd0N/TiB9uHx3uwN+e73oVeKC3qbcLtEGF0gzHt+PBvpbROyqES8ODbWJVjfi7SY6AJDaQRvxQ+50lQQDEQHhk6NcOFlTdeYxwtV/sjaH+ljtr+19lyRT39TSCH0bv5tJbtoXZHx5oHf3l/UoWD+b8f6k5rCgwG3+3RXJtnbSDcO9vFIy/IGy7Ggbu5li4NEHoCQ/1O6d4srS0NDTsamys3dBQNn4kr7U9o6klZYhYgi8IxHvqRvk+mJDwSGtrIJ2+sIFB8QmFkudit8qD/AZ7qrgc+vIS+TfhFRZlcYHY1dHQ1FDe3Fh5K65obanp6W66zVWMmxorOzsaGPRJzgqVyZgmE0fJpFHKLZk8RpwZaW+rbWqsuF13LU1VhNFezgptkUns7Ki/g2HNTVUjw13sZQoMpLe7qfG2khgP9rcvL5HYy9TB/rbG+rLbSjZVgarW5urm21jY2FDR09VEJRMopDHKbYYJHqDTJmAIM1PDjfUVzbcd7P8sgwP7elqWFojzc1Nw3PRLPAALANbbInN2bLSn4Q4zdct+W2rGCX0wy+D8qYnBxvry651f0dZaA/rvYDZ+uIu1SOruvFNEtLc3QEdw3NfbAqsUgui3isd7ZBjgHH3yjo7F4giWaHFhJvZcrKw8LMx3586Dfn4OBFpKrrFsgqk82U2V66AwG2pWnvlMfj5y8SJSU/NWY63Tel19XPDVwrzI29ZiPW35K4sTUCn8JsxaIHR1VLi62BQV5hYXpxcXp5WUZJSVZsLBNc5KTLiqoX62oCCluDgDZCoqciorc8WcU1aWhbUqytDTUS0vSedxZvt6qgd6a/DDANJNE2Ntk4R2CY+NNOOHGqcnOvNy4jzcLxUX5Ym728qS7rKvhlyxMtflrsx0tZdfMyyttDSjrq6wsaG4ob6ovDxLYlh8bJChvjrUO6Dc2cmqsDAbjAfDSksk9m/qzExPj7qgpTwz2Ukh9rs4WxcVZZaWbsps7T0zPy9JU0MxMTEU9G+5mlpTkw8GgExhYUZwoFtTfQFhtBVGdDvubC/jLE+Fh3rFRAeA2uv7uqHT/1YGb5eWZNx0Pr0El5mZGaOidAbWQFV5lre3U3FRLiwVybIpwWXcXif4JAOmQF1NvqWxOMDfNSc7HlecXglLTrzqamsLMCXYsWTtXd+2KMv7ioO1pR4ECHd5CqYJli44vwSXDtPX2IirqMgrLEwRL6esW3WdFRnha2Sg3t1RcdnVtqgwB4fLxOGybpq7jNT4gNys2LzcRA11xcH++iXxHYB/J8PSKilKkTgWTMIVp1VX5zc2lNTX467NSI6fr7P3lUu4opSziifLSkvj40PffPOo/FntWM3Dkbt3Zf74+eU9u77Zd+DTvYciox+/ehXR10eampCinDOCuPh434DC/KjbYpDknvRvdddqeXGitamkqDBN8gvlKMpF0WUUXUVRAYqyxWeEACX2dqYoykfRNTjDXp5hMsZIxD7SbJ9onSFuuOTuerEUl8bjEGFK6JQh8dsYY53tkCKVNDeVNjeVUEnYSRCARVlbW3ytOwmtXTsQQS/dnRX2tqaAQa1NuKKi9GsC7MyspJAQn+joq8ssklhSMElou2hpwKDhB/vq01KjxZIrFPIAirLE9vM361sGfcTSXHdqvHNmsjsxIVTcnCceJud65kO/NtYGTObMDf8+3NBQc1tbtfiQXVaS2tddwxY/GdjkpXmC5GU/WJFLzHHwA4w3NjqAyZT8QwI8sW9XxZ88sW03934Dc28vwxX7ZPVuYveo7Qa1a2IL76qQty6gC/hMyarYwvAns7mxUF9HFT/UDDtTZ6fYb6KFNRp1jUmFObrjuFZnprpMjbXravKTk0Ilk0ijjpCIg7Mz/eXlOfAJx6TZfgGfDovz2irF7EFF8+mpYZfszFYWJ9msqehIPy6XJpm+sdGOzIw4Dpuura1GnB24tja2dg0mLVdXZFlbGjQ3FBcWpIoFlq+tUsn0SRgN0vt2oDqGu0ozN7sgfr1p4t98sxlWaVF+UkdH7WYcdXXVhoZ6JCVdFZsKi1/QUJvn5+NcXIhhUFpaKp8vKCsbcfdrxOdUo062/Ijg0Og2I5Mia+tiX9/HmpsfKCtTm5jo26jFEhLvUIv99hjU1lyanZ2IouuoACaM09KEO3r0EJU8CmtFxKehIgbs+RetDQWCRVhGKLooe+bEiRMygYH+gYEBpqYmo/hODmvS7qJReUmmBINo5MF5+mhLc0VBYUZmWkxWWmxeXkptLY48OwgClWWQg+TA6hGskkJDrnh5OtDJQyXFaXDQ0oiDTkuKku1tTcDLbc0lOTmYYTwuNfRqYEtLW29vf1/fQHBwEI2KB0vAMEtzPehrqL8hOSlCJOIlxIW6ujpHRQaucuhTE92QoJUUZ3V21Az21cKynp7omp3qyc6Kq6go1FRXFYmWRAK65MVUYGyw6DwArpnphbm5yb6+Vl8vRx8v7FUaPz+ffXu/ffPNtzvaa4Vr5LTk0N7u6q3f/BQ/EBzv6qhqbymTPBkc6KuTYNDsbD8MViSC1by4vkZFhfMCHoVKhDBgQu8icb/rfIjMRegdDiRnRBKr1qibMj+zgM5jzzJoI0K4yqcLxV9EuIXYhtp50CziU0H4dmKbatfXKCzxszkOa/pmSUybCLQtSYwEzaTp7gnCIJxBBfQNFs4J1yiThNbMtPALWkqjwy0VpRkNDdiWY+Nk/hfNJ/9y+MnB9nrwxtZhijabrzNW2TMNtbn6umqNdYWJCSEQ83W1ZbYXjV1dbdwv2+bnJLi52rg6W7u6OFxxtyeTCOg6U9wvtJ0jzXSHBF52sDcHz0swiMGYEImEkRGBr7zy6ttvvbnrHzu3b7/vrbfePq+mXF9XJhLOg8EbXYsYkF+kJAYDBsGunJ2TgHI48y0ek33fc1drhLwlVLgsEjKgFwDZy4of1WVeGRvrNDLQhP3vD8Gg4oLk+vpSANP19cXqqoLERM3WNvPKSr3ICBcelwl2ZmdE+vu64MQYlJqaIgGXmuoZZ8+OYNssd+fqyjqi5GR1tQce34b9S01kent7x92fi/0+GBQv/hdyGGtr89kZUXLyijYXrWdmYHmx+KukMlyKtZWBUAhBwl1gTtVW45ydnYqLca2trcXFpT5ezoLVWQsz7I0HgJihgQaod5oby0pKsmuDPPFudqNuds0+zkVFGdWVBRCr1RXZpaXZWDrBmn7k4YcQBIG4PXPqGBxctDKE7SgrPcIOw6BZDIOysd9wy82OLyoq7u/vx+PxjY2Nra3tAX5uKLpQhku1MNcFnYBBhYWpubkpOFypo6PjpUuOfr4uWVnpRcWQSeHy8vJzs+LBQkiCAIMgvYeK79lnnxFHFEv8ojAWouJgoPV2VZmZaJNII8ePH3/vvQ/ee/+D93d8+N57O77+evf33+85IXNkZWkiPjagr6dmE4Owx+GMsYa64tjoYODqynyAxc08aHa2T7zrivx8XFOTw1dYdO8rji5O1vm5CdfSgXmRkDlJ6AA9IsEcYAowhCXUmOKvjy9gQQ67vYghBhRsx56a6NLUUEqKh02Ps8Yhwb4thJSER5FICrEDSE9YIvFrbqAZXV/gr5KbG3FCAe2aGFM8fNDGEoh7XBfQ+Dyatqayvq66gb6GYI0mTieZ4n45Em0Ar+Oj7aANmoiEEPM9U5PDovV5UC7G0EXx7yKMd3eUJ8UHagMGjQAGZUL5DJOoYXEeKUYQS6SjpBx2GpCUMKha45LEw1yEUdMpgyVFSVDaN9YXJcaHCAQLVMrMhgfADCFLbAyWSYm/hYDHcAHremF1ZWaov87X22ErBrHZ5P7+ri+++Oqll175/ruvL1obPf74E7o66irKZ/fu3TdO6BY7CrOczyWN41uiI32sLPUxDCpJR9vaF2wOLVCRqto/T06prKxUiNhTKIdEmBgyO/BCdYprT2+9vt55WHt/HAaVgGNH8X0ODseHhmwdHXRSU51raw2ysLcdmAmxARgGFaVuxSAggUDY1kMdHGaiN5G3t7eZmdntMeit3x2DcrJitbU19HS1+/r6urt7DPT1pid6+VxiXk6spYUeTDybPW9re9HE2Li/p9Hd3XbP97tHRkZVVRQL8xOsLPUqyrIAg4YHG8dHWwuKM0qjg6hudnPezsDzVxxqgj2z81Mnx9rrqvOgGsfqtwXCiy8+D9DT1lKqqiwHB06XLGA1JMUH2dkYizGoNCcHw6DoyID+/sHy8nIXF5fY2FjmwtIVD2dUQM3PiTU305FgUF5eUk1NUWpqWkJiYnBwiJ+PS2pK8uDgUF9ff01tfXzsVXNT7WsYFIfDZb/7zlviu1d1sGOsr9E4LCKfC1kDs7Wp2NhIk0we+fsnOw8e2KuqqiQvd0ZD4/y3u798/fU3k5OiGNTBiHAvwCDx+xBjDBr2/gqVPJiSFJYYH5qSFBEfGwwdgR+uYVCvOD1G/f1cIe+jkgcy0qNnp7qdHC0aagvSUyLG8a3gDAX5E8GB7mAAxBKwkE8b6q//Yc83g311zU24tJQIKCTxQ03pqZH1NfmwGVRVZInf/OD2dFY11RetccnrgrkmcdxC89GhJsgjIFwD/FxBMypa7O+ugTNiMTpoGO5vIOBbM1Ija6tyIfK5y1inUHpERfiekDmUmhwG0w3mQaEBUwZisHOAtohQ79OnjnI51DUOUbBKnp7omJka4XEoMEx1tbOa6ucK8lKhDmqqy4+O8NHSPDe2gUFgCRoWGXDYaN9B1R9G+hphvBwWlcOi8NhY6pSXHa+lqQTwFxsTQicP52ZHX9BWFo8lmH+t4BKsUg30zmio7y4tTheXewCgXCppwNnB8oKWir6exmB/c39PjYebjRiDpiQYxOGQmppq5eRk6+uKIDNlL88kxAWvcWZBwNLSsqm+JPyql5aGElje1FAKExEa7GZlod/aXJKdCWGMsoixfQ3Irq+Qliakv/6+TqszYw4uqQU4d91j0b52BQWphvp/LAZB3SBYXiLFRrsFBtoPDw76+Wp0dRsFBbjBnMIqvSUG3YEGBwd9fHz+KAzC/hkzKDoqKqo3DQq5GmZjbQqhnpURaWNtyOHQZGRkkpKSh4dHZGXPWFmanj9/nsvlHjp09JK9pd1Fw8pNDBprK8Bllof7MTwcKN7OwEwvpxZ/t6yCNAgkwKCy0kyosGATe/GF5wB6WhqLlZVk4cDBzgx23bgYf8i9V9kSDAJwFILCsLDQtTW+lZXV0hIrPT2zpQG3ujINhpmZXJBgUGIidpcnPzdRX183Mz1mjUssLSmorCiphf9whanJESZGmjNTGxhUXp776isvRUX4vPjiS9mZyVYWWhetYR2fiQz37WwtNTLUoFLxH3/8gbOTlbX1eWcnXQsLDROjC97eWPI1SWgLDfEYGWzq664pLoyrKk/GFSUzaHg6ZSg5MRzAbmKsfXlx/OdabKZXfBNBWFOZI35JbXWC0AHQwF9jQE1hYqzt6W7PoA2pqshjv/MiYqwsTkCqBVgMkLT7m88z06NCQzxBzN/XNTnhqpqqgoebXWtLBSSJcB7QDdSqn1cE+IB0w8XJytHBAsDF08Ne9syxnq766EhfyVUAIHU1OGA1NeKcHS2veNiDZlUVOShw6mrzIQkSd7oQE+V/+tSR7s7q3u5GsdgliEaYHRBrbixPSbyqdO7MupAOEQ5FE7hicmJIyKcTp7qhzHn1tdcYjEkmfbi2Kjv8qoeWxtktGAQ4glbmZdCnhyBvsrG+YG0lc9H6lKnJ0eCgy0tLFLkzxx959E+jIx1UYl9GWri2ppIET0WihaUl4ldf7jI0MAwKPFlS+k8/P4+OhqqarJya4pyV5YnqytyHHnzwvLoKZIKtTUWXXay2YhCXQ2xsrIK9fWa6f2ZqIDExdpFBaGutKyzIMzOzHOhrAAtfevH5b775msOm9vdUBfm7wHYLC68EF9PUgnpZRbOpSHkmkuG/oyjJfXq6PzLA0jfEr7NnqKyiJjjQy8hQHRL/Pw6DoMhd5SxPwb4yPtYTHmZAJDqGh+tNjHUvzY+FhrjDTvyLMKirq8vV1fWPwaAcLA8SpSWHa2tpmJoaDwwMQAZhYGAwMti8sjielR5pc9FohU1ycrDw9/fLLyj46stP8/OT09MS1c5rZGclT4y1QYRvyYMwDCqLu0oR50F0wCBPh7pAj8z8lAlxHlRWBhjEh6z76aefAuipr81XkDuxUYsJaPHRfnY2JqsrmxgEBQsjIy0qNjbB1MIhPiE1wM8dkhcmfSQ7PdLcVGcLBvFZ8wMyx74njNT299Z0tZcvzg9RqH2CJWJ5SaqBvrokD8rNia+oyH7u+Rf++c/P9+/f//LLbysofoaiKVVVuk8/9XRNZZa56QUiceDzz3dpa2pkZp5H0Sy18zuPHz0OiQAE6thIc9hVT/xQMxQLUxM5ImF9bLRnZXkOJCmJCWFQi8EB1CPXYxB2xxRwB6wlzQ7DmsjPjR8ndJYUp3p7OYJXaRQsjQq7emWOOri8NMFaIPC4RI3ziqYmF+TlZAAFYHtwdbEGsHawNwv0v5ydGRUU6KatpUylDkFGdvr0URZrqrQkHXKrgYEGKmXQ3Q2y1K/9fJxGhpqgCdSDkFWdOX1saXG8vCzTw90OBDLTogwNNCLDfextTdcFUEMRBGtkXR3V2Ch/gKrqyiwQA3wEqNLTPR8d5Q/Kxwnt9rYm44S2FdYkuGIc3zw5PshhTfPYM1PjHXU1RVDREKe7wYcRoVeuz4NEuOLM1159+aeDP0xPDFmY/4SislCfkSkHjA0VUOEigzpUUZYDk07AN2P3kjbyoBCARSZz4plnnpI9Ix8dfa69/aCxhv4DCg8iIQhyEOmoKgOBlkYcfqgV7Gmqz3dztXa49DMGLS6MM5mzPj6eNjZ20dGxCQlJUVHh6enpAQEhoVcDKcR+qAQHemo726u57JnOttLgQFdxHgQRESsQiAjtESVhHxcmuuCHhpaWJhrz3I5/hBz47AEFxR/kTss5XdK1MNP7AzFIfKNtZXF+bJ1PjYkKyM/XSkkyb2uqwm44kvrDQjwkeZC83PGs7Kx7wSChcJ1EgrIaTU5OzcsI+fdiEFbysGE3ppL6AD6VlVWtL1r3dddylydp5AEoeawtDSB/ppMH7Oxsp6anc3KyfXx9Q4L9IINlMQkjA3XmZhcqyjbvBw001OFKynPrw30Jl23H3exbvZxw+akVlfnzc6PV2FNVwCAOabr7gw/eBRiqr8nT0jgHB7DxQp6ckhhibyO5H1SaKzZsnja0tDBlbiSvJ7tNVXbn5HjfIgMPxhTkxm7eD0pNCV3mCDKym97beczeKdjb2+uyq2dGbt7B5u8y+iOqijJNjDZqsZTkcCJx7MiRw7t3f/Ppp599+umXCgqfU6lh2dkazz/3XH1NroWZzvR0b3t7bVREiJ+fDJUaraT0ydEjR9bXKPO04bGRJkgu8MMtDXWFw4MZK6yqpARfHy+Xq8GeEeG++blJVNIgLIst96QxDFoXzEOK4evtNDHWCjkIxHZ+ThwkMl988VlzQyHkTTRSv7+Pc09HBQwNxjsz0enr5QgnU5NCAbk+/+enHa2l3R0VH+x4NzkhZHSo0dXZytXJqq46t6m+ANKfwb5a1uIk5CmXXaxp5P7Gunw/b6eIUC/JScjUWhqxLKm/p5q1OJUQF1RektZQmw8aCnITAPugRxgahdjncdk2PiZA/DX6saT44JLilKb6QhCDchvEWIvjGakRwABY8/ThkYHaCcLA4jwBelxkjHJYk3OUwZnJTsACSGa33A8CDFrHDzd99unfYBamJ3qOH/va0HCHkdHH2trvXbTWgTIQdhTu8jSsQMAgmFbdn+8H0UXrjAUGfmy429joy9i4nVqn1RAzBOlFEBWkMb+AvTjBXpoEeyizfe3NOO8r9mIM2rgfRKfjYf2Aexvri6sqiiIjI9qay3G4gqaGCiqxf2FuBDwMbQG/4KC3sxKgc+N+UHas+JbTCHFqcH5+hk6fiPc1Nv/hUb1j92ntQvbsRP7+MmJmfNzmotkfWIs1NEAttkinYG8vgNu1tBSzM2KhgABAJ8/2QjkMuXNxYYrOBVV1dVUXZ6e7spubq5fXFThQUJCvr0wZoYj+fRgkDvVFACDO8iQsuwMHDgwPNC8vEABNYTyVZemQB8FqYLMmgwK9oSCKj48LCgr87LPP0lIiVtnTk2NtF60NJPekJc/FGLTR2urinLzk7LTo7JTY/PzUmloccbpf/Fwsq7w8G0WZ4CYISMJoC3mmd3q8gzDaOjvVxaAO52bHSJ7Ng2F5eYmYYcS+ecakvaWCkyZioPoRYWwArJIYBpmzBIOyM8MIJI6jP8M5jGnq2HHZ1dXFxeeSR+6f6x49V3qmpiDH0lxvWoxBMdHgUzZkYQV58V999eVgX/MFLaXnnvvLM888+dFHOwAFLM11KZRhwNy+rqrPPv3oueeeevLJw/VpowAAIABJREFUx7Q1lXmcWRoWY11JCcEAtaPDLaHBniFB7pDLgKlQWpJn++aoI5Kf77n+uRiHuzLFXprgrkzDioEqRszT3lccfLwcIQZggID13OUpGBRlthf7k9QPxSakRUIeCboA2OJzZ/OyY+3tTMFLS/OjPDaWfUDoAq9xZiD4qcReSFpXV6ag+cIcHq5Cj6ANTgKuQYmEiVE3xEADRCDIANYAdgD6QCtYAKB2ZWkcWsEZiRhTLLYkEZvtXV4kQBM4gB5h75mawN5PppJ6YalAVIs/+wZ6q9NTQyGXET8XyxRv14KmhsLC/MTS4jRwe0LcVX9fX18vr9joCHAanSxuSOoHJ5BmeqoqMjaei8WHCIUM2NUBH2G+PN1tbC7qZmdEW9kZGNtqmVhoDffXwyVJ1yAwMtgAxdR1z8XmCSg6D5dYTOzefHdnFYyaNNMLmAsTIRmypDkMZ3y0JTEu0FqMQTnY3QkONKSSB8BpfT31ddVl2Qmh0R56rmr/sNiPyH7zaHCws7Wl4eAfh0GNjTgoCGAuoByDLTApWcHJUXV2qp9OxV7USEm6Cql3Znp0eKj37FQ37GH3zgO9Nbzl0U4C79+EQeDx4qI0yGlhSubECCreyTfeSILV3N6Cc3SwRNcZsI4h0mCPheCvrshsa8aNDjfCHgXTCVtlWUnGte8HDYotHIXNp66uqKG+uL6+iDQ7IPl+UHVFdl0tbIwMmHtou4j9zOsQLHRs/6cPwxmoAqB8EH8/qASH3YDEDIPAbm0sdLc/lZ99lTlHgGUBhoGzbKwNYRSDffXp6THYD3cvdAs4Q+yFvs62su72cuZ8T0SP9xJjjDDcBBg0NdEFqVBSYhjolLyzNjvdA6EFS7+jtbyrvQI/1Ah4anvReG5udGUBe1OMgG+DSz2dVeOjrbBLz4lnF1KY/p5a2HAg45ud6iXN9El+WUnytrDkfVTJc7G4mMB5LAyWoSHt+lfhMNBZwXAEvHeHV34k2MTjzECuAcHP5xKxF+IoA3/4u0jYiEj9koMt9gwwaIPEqa4yXIqerip+qKW8JKMD+2GW1cV5PIAaAC7AGWxmMCgMl1kT81uGAysBRtfbVWFipFVfW5CC3RpfhvwIW5mUQXA4j0OCnEXAIQnZZCGXjE3itbYwOxRib3yM/yYGxUQHsNnE9TUqAI1YYFi8VgcZVInN1zE0Bw8X5sVdtDKE4q6oKBXKHKp4gMDQEWthjDE3Oj7RX1tXkZMaVJgdOTjQBCnzwB/0bL6oILmjvVIkoIGRkAdBLezsZFBekgI5OIwOwgpXkBjodzk9NSoy3BeCV/Ji8z3zOJ9NwH7T/mYMMnfyGxusREXza1zSb8KokD4+2hbg7w47NmTvAb4uQf6uwYFucCBm5wA/F58rDtjvk6VG+Ho7Bvq5hIV4hl+9IuHgwMv+vs7waWSgAbkA5A5TE50Q2DQK7DNDkqenkl9xnqMOQ34EwVlbnRcY6B4V4Qulx7VeNtk50N8Vqgk3VxsAFMywADeJYdCLuNgJCrvqHeDnLDHsioedva0J7JOgOcDfDZIzsBD0BPq5hgZ7AMNBdIBPkP9lOG9hpgvowGFNBwd5JsYHQ6UDfUGKgdkfcFk8HE8ooWH4ZiY6SQmhQX6u4k49JCOVSEK/fj6YMSNDTZIfVMKYPgKDpWE/WvIzj2FPu5gZqZFRkX5YWx/M4JvG+1/Ofi7XBuUsYfCMvx9Moov3lUvamkrgh872CnB4VKSv2Ht3VrgxrdBcR1t5aKAxIT4kMSHk2qW7NAT9QQGX7WyM3C/bir92sJCcFBYbEwiz738PzQOw5tjas7M1GR9tDwryiI8NlETEJsNygqUeGuIRFuoTHuYD69BQX4M43YsK6L9VPN5r2KILzY3F4NjwUC9YWuI17BYZ5hsacmVjLP6uTg7mUeG+UIslxoUAnv7CLojoOrF99FYYdNEtKCLYMS05DEr634Sh5o+J8gc4BxAxNda+mU2Mtc1MLkDJY2yoeUsBTMZIy9xUBwIV0r/IcB9YCoBit2SIRohhaHI7bdCdsZGWq7NVSlIoGAZq72AYSDpeMk9KCIHlAik0LIg7WGhnY5wQGwjCcGCor347SWArCz2QNzHWuuVVYyNNaysDGMjtxggMHgjDvBEK1Za+3nlocofu/icZ1oy1pUFcTAAECcy1kaHGPTY0EX/CeouJ9HN1ttbXU4O5uPe2MGturheTE6+mJIZCAauve/4XNTc11nJysIiLDoB6/HYLb4u8FiRNsVH+EES/VTzeIycnXIUFBo69fRxpwSUAdFjqGucVczJjbqknMS4Y9uOkBFAYDJwCnIhxUnxQQ3Va9wT/NhgU6pOYmJSY9BtxYlJycnL2r6acnJyUlNTExMTk5BQ4uD2npKWl3VVVZmamWNXdDcvMzIIhJCUlZ2Vl3VkSBEAMhO8qeVcCDXcc48ZIYQhp6ekwnOz/rwQOBz9k/0sOgIWUkZHxS70H8hkZmViAJCam/0vOh7WX9EsiAoR/y3i857CFNXZXV6SnZ2DRmJp6OwtjYqLi4mIjY5LCIhNCIxKuAocnhIQnxMUnVZdndE+sXYdB298aBAwyc/SZo4yjUpKSlKT0W9A6ilJW0Ml5dJSGDlHQ3hm0eQylLmPvyrXhORgG/fV6DDJ38p0c65U6TkpSktKvJyGfTWbw+qbW+6dEPRNo6whaNyAq7RD0jvMo9Nn2Ua4Ug6QkJSn9nhgkYM/QVltGhMMkNDCh2fRyTnU/Wtq13jexNjk73SbFIClJSUq/byEmYE9Tuc3D66Fp7cfOux0/72bqllvYzuub4BOmp9vwUgySkpSk9Dtj0OycIKOafkLTIzp3qKht8bimp3ts58CMSIpBUpKSlH53EgnZY0Qurl1Q1MRsGUXrCWha02JSA7ttjE+YkWKQlKQkpd8fgybJ3Nymteo+tLyLX9zFL+gRpTatdY7xpBgkJSlJ6Xen1dWVGRqrd5zTOcruxLPb8ew2PLt5aGVomk2hz3YSVqUYJCUpSel3JB6PPU2mdYxQmgbJjQPwSWsepDcP0fFE1jqf1jEmxSApSUlKv3MetLJEX1tdFK6x0HWu+EeHBeIfnFsXrdGk3w+SkpSk9LtjEGuRzl5Z4HKWICfi83kCwdr6Ol+ECqUYJCUpSUmKQVKSkpSkGCTFIClJSUr/4xgkEAj4UpKSlP4jaW1t7X8cg3p6etzd3b2kJCUp/UcShGdUVNTIyMj/JgZlZ2dfFJOtlKQkpf9UsrKysrCwmJqa+l/DIDab7ePjY21tfenSJSspSUlK/5FkY2Pj6OgIBwkJCf9rGNTf329ubm5nZ+fp6Tk8PIyXkpSk9J9HRUVFkChAsRIQEPAHY9B9vzUGDQ4OWlpaAsr6+flJHxBISUr/mdTb2wu5AmBQSEjIH4NBz/z+GOTr6ysUCqWTLSUp/QdSR0eHhYWFFIOkJCUpSTFIikFSkpIUg6QYJCUpSUmKQVIMkpKUpBgkxSApSUlKUgySYpCUpCTFICkGSenep3yVTCaTfjVxOJy79iUSiebm5n6RWgqFwuPx7qpZIBDQaLR7UchgMH6Rf6D3e/TPwsKCFIP+3Ri0XYpB//1kZ2cHi8np15GDg4Oent76+vqd+youLlZTU/tFmq2srODzrqMIDw83MDC4F4Vnz55tb2+/d//A0CQ23JUUFBSIRKIUg/4dGPRXKQb9D5GtrS0kEb9ej7W19V31xMfHl5eX/yK1TCbz0qVLdxXz8fGZmJi4F4WxsbE4HO4XYdA9LkVPT8/+/n4pBkkxSEq/jCBympubCwoKBgYG/mUlfD4fZu2uGJSUlBQQEADl1eTk5NYKC+qj6enpWzaBGude8iDAoODgYACXlZWV28nAAMfGxhISEsrKyu59aLAg09LSADpv8M/4+DiLxdp6xsPDAxawFIOkGCSlX0aqqqpQxcTExFy+fPlfaF5SUgIwAVXYvWAQxP97770XGhqqo6NDJpM3z0Mw/x975wHexnHte76be/Nu7Jfcd1+cuCVxcuPYceIa2XGJXGPLsbplFUuyuiVLlMROgr0T7GKVRIrqEklRYu9i7wUESbCAaKwgOhtI9LrvACvCECVLtChZADz/bz58g53ZObOzOz+cWczOstlszLhwQl5e3j0wCMZi7777LpFITExM/K5qAEdCQkJyc3O/F4PAC/v000+dnZ0XuGMw7BKLxZjx4an29nbEIMQgpHvUhx9+6Ofnh8flcjn04a6urvLycrjCgC90Oh0GWUlJSZAEwyJIBVgoFIqUlBQYxIHT8f777wNTYN/FMCgnJ2fLli3QpaEcMBEdHQ0lA4zAP2psbIQMsPGtt94CRwlMZGZmVldXCwSC4ODgux4FlODi4rJnzx7YCzwsAE1xcTEQraGh4cyZM1B5Pp8P3SYmJub7Mgi6Gey4fPlyGOtBPCMjIy4uDugDlcdvQgPBv/rqK9yjRAxCDEL63vrggw9wBkGPhZ4MfRh6FwxqoLtC721qagIEwGAE37Jjxw4Y8hQUFIBHU1dXB0MwV1fX7u5u2B2uyLsyqKSkBPIDKbKzs+fm5latWgVnXKVSQYEnTpyADCwWC7o0RIA+a9as+eabb3p6esC7uetRXLp0CUdMUVERDJoAc7t27QJqAB83b95cU1MTHx8PVDp//jz4WUC6xbcPUBIODVoGuANHCpUHroHf5+vrixPn9OnTaWlpEAkPD0cMQgxC+t6Cfu7k5JSQkABMgQ4PA58LFy5Al96/fz84O46Ojlu3boWv4A0BhqBjZ2VlwegjICAAIjgsoO8JhULYclcGASCgQAKBABESibRp0ybwd2A7nG4oWa/Xy2QyICAQislkHjhwAIwODw+Hhobe9SiANeCqQM0dHBwAMTB0ArcIHKL09HRgGQyjYCPY3bt3L+SEOi++fYA1H330ETQLuD+nTp0CREINodobN27EV/AaGBgAiFOpVGhDxCDEIKTvraiwKHoPvbO5E/86RB3Sy/VT3ClaN00sFPeSeqmd1Gne9AhtBFJhI3fYcB8HaFVfX4/fV25tbYWRDjg4d2VQ5uXMq5euzonm9Ar9DH9moGsAbMF2NpNNp9AxQxRTipWMHgZEJjmTYFowJvDx9rnrUcRGxV67dI03zOMMclSzKvm0vJ9swAGUDyXjle/r6IN4akJqa23r4tvHy82roaKB0kYRjglH6aOzwlloIkyNQeX5I3w8zxhzTCwQJ0YlwoEgBiEGIX0/7fPc9/qm19/c9eZLm156ceOLb+x445Utr/xt29/+vvPvf9v6N9gO4fXtr7+98+3Xtrz2zu533t7+9sp9K8E3gSGSr1FhYWHgCICvAY7MnW3lluc+/+nzUDiYeO3L16Dklze9DEZf/+p1MAcRCGAUbL26+dU3d7z5j93/eG3ja9Hx0XdnUFrs3zb8bdn2ZVDUq1texWsOpYEhiLzx1RtwdG/vehvq/5sPfxORG1FCL2kYbbhrhUH2/vZvfmlohGXbDIVD5fHS8C14naGqr297/ekPnz7bdBZKJnPJiEE/EIPQPGkb0MacjT/3+/nLx19+MfnF7wq/jf3tryN//XjU40/HPP2o36P/uvgv3c1aTGcG5THy7DztXjr+0ovHv9PWs/HP4raejH7yV+G/+lnozwQKwV1LJjYTf+L5E0PJ330Uf4j7A5T827jfPpPwzP8L/X9/jP+jVnf3a2x7/vZHfR+9c/v8LvZ3UPLvEn73u7jf/SLgF59c/AQx6MEyCD2rYUtalb7KocwhsikypC4kpD4kvDE8iZSUQk5JaEsIawg7Tjqe1J4U2RwZVBcU2hga2xnrVe3lW+17b7Yu9Vx649Qbl3svB1UFgS0Ica1xJ8knk0nJEU0Rx1qPnSCdgM/g+uDgumBiOzG+I35H7g6RTHTXkj2rPFdnrIaiQmoMxULNof5wFHAsxEYixI+3H49uiQ6qDwppCIkgRRCbiAcKDyyGQesy19mX2Ec1R+HtA6VBg5jaB2pu3j4x5Bjvam/PSk/EoKUwSDwtkEqmFLIZlUqi0Si1WhWmV2OIQbaqtRlrN1zZEN0ULZQIhVIhjCMOFx3enbPbvcJ9eHrYo8LDocABiJBLz73YenFL+BZCA2EpDFqWusy3xpcxwQBbEKDkPTl7DuUdahxrzOjNOJB9ACyep5wvGizaF73PvdR9X9E+yHb3uzZVXu+fex9AgB8F1NztuhscBRxLv7A/riXOPtce6JDZn5nbn7uNuM271hvIshgGQeMAhoDReMldvK4jRUd25+52ve46ND0Edo8WHAW7OfScy+2X8fbxrvJGDFoKgxTyWYVCIZcr5AqVQqlRqDRKtUaP6TGNEDHIZhl0tuss/lWtU+cO5P406KcDogH4+suIX8Y3xVcPV5eOlF5uvfzozx5985s3Q1pD7plBr6W8FtEYIVHdmM3MnmU/Hvl4eH24QqPYk7/nozMfkbikPFpeg7Bh2fJlz/7t2S+zv5xQTCyGQe+dfS++Ld60pVfYC0cBx6LT695Me/NQ/qFmdnMBs6BsuOzp3z394soXD10/pNUvlkGnO0/jXzU6TSG98D+C/qNH0ANfH49+PLoh2tA+w6WZpMz/88j/+fvXfw9oCUAMumepVVKxRE3n6ilDWjJT005Xtw6oKzqVg1yNQsZHDLJZBpn6GIgioDwS+gj+AOpjkY/tvbYXoFAxVnG57fJ/2P3Hc+ufC20PXQqDYLgnVohNG5859szFHsOf3Hvz9/419q/pvellrLI6Yd2yfyx77MnHNmZunFROLpJBMLIzbVFqlXAUcCwQf/v02yvSVlyjXisfKgdYPPnkk0+9+tTB8oOAp0Uy6BT5lGnLwMTAz0J/BtCE+BPRT+zK2mVon9GKTHLm//5f//vZNc8GtQUhBt2zdBrpCE/e0Ksh0bWtNF0zVVvbr80nachM5eDYaDtikE0yaH3m+hOkE/p5MaeY27K3KTVKiO/M3UmfpINPlMfMy2zNXOm00r3GHQZTS2EQjFym5FMmcweLDoIfAZFjLceSSEnAjmxqNiBvq+dWhyyHfSWLHYsBg2DEZCpWppbBUcCxQBzGTSWsEignm5ZdTC9e47jGo8zDvnSxY7E1GWuS25NNJQ/PDEPJUpUU4rvzd8NYjzZBy2PkZZGyVjqudK92h0EfYtBSGDTMk9dRNG00bRNV19CnrerRFpI03YMq5ghikC1q1WXDPenQ+tCYxpiYZkMAFqSSU/E4ROJa4qBvQ4huiY4lx/rV+fnX+N+brYuUi2+dfutM15nw2nC8fAgpHYb7uxA5Tjp+vO14VFMU2ILPiLaIRHIiOEeLYRChkgDeiqGchhhTyVB5OBaInOw4mdiaeOMomqOjSFFRbVGHiw8v/p50WEPYbdsHKh/fEo+XHNMSA+0TUB/gU+2DGLQkP4hv8IPa6dpmI4Oqe7RFJA1lUMUaRQyyRa24uOKJ0Cc+Ov/RP07/4x9nboTlZ5ab4hBePP7iswnP/inxT389/tcnwp4AbN2brYzeDDsPu08ufrKgfPOwLHUZbuvPSX9+LuG5X4T/gj1794l/3lXeP/X+6ccXPr7DUbxy8hW85BeSX/h9zO+fS3xuMQwCJ+hXwb9afPs8SXxyxaUViEGIQUiLVeVQZWSt4a/lOwTwAogNRAgQiayLzB3IvTdbIzMjcY1xd7Zl+P/baMsQ6olxrXFzqrm7ltzF64qti71zyeDrmUqOqIs43Xl6MdOaYJwYVRv1vdoneyAbMegHYxAVMQgJ6cemh8kg+sJ50ohBSEiIQYhBSEhIiEGIQUhIiEGIQUhISIhBiEFISIhBiEFISEiIQYhBSEiIQYhBmN6wCMC3QalUqk0BvpqnKhQqs1TVzTsqYIspFXLeUqx5qvL7GFXewah5lW4xaqqSCjO+tVlulMYoOdKiZd5icDL0esziz/jSjd7mylepNFbGoH+zMAY5OWGvvIItW4a9/vqN8PLL2AcfiHx93fHg5+fh4+Pm5GTv7HzY2dne0fGQt7frfKqbnx/B09MZT8U/TTsa9yW4uzvg22FHN7ejvr4e5iW7uBwxFmtIJRCczFINRvEkPNXL6yajXl4uZkbtIbO5UQ8Px3mj9q6uR8yr5O/v4ep6FJJg+8aNGzw8CPjiqvv27du/f78v0qIFLXbgwAE87urqtnXrZl9fT4s9405ON4qFnOZVgnCzURczox7mRiHcYtQJko4cORAcHGQJDKq/mUGF1sKgv/8dW79e5OzM2b9fsG+f4MgR7jff8J98UqPXczAMAhciHE5Hf3/1wEBNb28Vj9ep0+FJEHhq9ejQUDOVWk2l1kCeqal+2GU+lS+Tsej0ejyJTq+TSpnmqdPT/VDmwEBtX18VFKJWj8ynwicXDBmNGlKhAjrduMmoRsMeGWmZN1o1OdlnXqxcPshkNuBGYfe5OYZ56szMAGyEwGI1Hjy4Wyi8sc7O5cuXr1y5goYMi9eFCxcKCgrw+NDQiI+PE4bNPaAzrtXCGW81O+O9N5/xIQbjO8+4WGw441SqoVg46UrlTUYFgm6TUTa7Xav91ihUYHS0DVKhZEgViXr0+m+LVSqHoTQ42Pr6qw4Ohx8+g3jyuh51G03bMqBr7NfW9GoLSOpuq2DQO+9gJ08OHTkiunx5uLKSsX37VF4e69lntXo9DxoazgSH00Wl1tHpcI5rhcIeDBPg2yGi0YwPD7cODBhSabR6sZhuTOUZg9B4ZTTCdghMZpNCAedeaEo1sqAedoTdoZW0Wo6xWK7xk8/jdZuM8vnd+EZjqgBywpWBG4XP6ekBs2IFYAVs4UbBukw2ZG4Uagjb8R3h4vPxcZmcnMbb4fTp0+ZvKx0eHi4qKpJKpTMzM3y+4VUQ4+PjhYWF+Cv6cEFr19TUXLx4sdcoCoUyMXHTymEAb7VaveBknTlzBn/F6ALxeNDUHHD96XS6aSOZTMZfpnpnwWgIyhwZGYFqT01N/TAMAmrjL+oBjY6yw8K8dDrBD3XGBfdwxuFahSvWuC8X31cg6MGLBaNcbqdx4w2jgJuxMZLJ6ORkv3mxSuXo4GAzlMxiNbe05BMIbohB986gN9/EzpwZHBzs9fPjQWhrG2hpGXjmGUiRGt8nTGezSXB6IKhUcEnJjEFi/JyemOgdH++AJLiAjOdGYdxLakwVwM/a+DgZUkUi+NWaNKZK8Axq9RjsyOF0QpiZocHv53yxkDonkTDZbEOxHA5ZoRhaYBS8nnmjXUZnzdyokM/vwo0acTlhblSnY0MSlAlGjdexMjY2eGpqpri4eO3atQ4ODuavEm1paQEWiESiOqOgbwNNGhoamEymKQ9cwtDykZGRY2Njn3/++dGjR+Pi4szblsFgyGRQK8OrjSEPROLj4yEbi8WCMwWFm2eurKwkEAgANXt7e9NGOKcw3rnzGZybm4s3Cn9hIf7iwwchoCS0kpOT08GDB6G2paWlv/rVr4hEolgsFghE/v6uEgnju864RrPYMw4/Xbec8f77ccapcD0DrudTJTLZIH5tQwaplDVfIJ4qhvymKx+8MOOO0vkqTYCtwUHwxMGbbh4ba/P390YMuncGvfUWlpw8jGFtQUFcV1fB9DS5tZX13/89HRcXEh7uSSAc9vZ28PI66ufnHB8fFBcXHBcXZAzBgYFuBMIRSPX0PBoU5B4fHzqfFHTsWKCvryNsx1OJRC+z1ODoaD/YCGUaS3aIjvaPjw8xpYaHe88bdfD1dcI3mlKDg93xVCgBKmC2IxgNgkp6et6oUliY581G/cHivNGjUVF+cXHhGzeuXbbsdTujoP+bM4hEIgmFQoAFQAc4AvSBjd3d3UDrb0+8Tic33pmEOFxea9asAU8E3JyysrKsrCzwic6fP48/Zb5p06aAgADTLXDYCBFw4s1PBPTkwMBA2AXIBQ4ReBl4yfiOubm55eXl586dg41QJfhqejEZoMHHx7D4DmwBT+OLL76AkiEO4MMdNwBTYmIiHAXsC74eQBNMwAFCtu91wYCP5u/vD2317LPPglFoLrzpfv7zn+fk5G7atN7f3/m7zrhZ4y/ljLuan3EIdzjjMTELzrivudGICB+TUR8fR7hizY2GhHiYjAYELDAaDIfp4WFfUnIJvDO5fHhmhurr64kYtCQGXbjAionhuLkJIiI4R4+KmpvpTz2lJJG6Ojuh0/WYApncZR66uiimJIh/r1TzYsGKedIPaLQTftJDQ0NfffVV6EguLi4VFRXmDAI3ZwGDwIA5g8wF+EhNTQUq5eTk7N27t6mpCXrsoUOH8LEbAO7atWt3PhESiQRws2PHDohfvXp1y5Yt+MWKvzEVRj1JSUlRUVFAFih/27ZtppcvAw58fW8s0tjT04MTB5y4lJSUrVu3ghMHhIKRJvALDgecLCiwtbUVHDcoBLbcwxAMLEIkPz8f2u3RRx+FMsFtdHNzN7X/0s549w9/md0x9TZG4+ISQ0LcYewJPtHkZC9i0JIYtHw5Fh094u3NXbVK/Nln4v37RRkZrOef/1HcVYXeCP4C/s546KgwuDAlQS9ls9l8Pr+xsbG9vR38C/wyMh+LmQSjKujSMBADJwh6+/79+69cuQLFwkbYHTLACCs8PNz8zg6M7IAXC8qBfU+ePIkZ3++8bt261atXZ2RkrFq1CuAIdqF8GARByUAcGBP19fXhe83MzMCAKD09HXwcKAEudLB16dIlyPnZZ585Ojp+/fXX4JfBGBA+d+7cWVVVBX7W9u3bYYv57a3vq8zMTKghTjEoMCws7MdzP76ysurcuWP4PQfEoKUy6KOPsMceU7/99uz774tXrFB88IHkmWdkv/41trgX8Fm3gDumu8jQP8GFMSWBvwMgAF8G+AIjLNgCPIJODh3+tndkoGMDwvAxzvDwMJlMBsrARvw2EAg8owV3rG91qaamplQqw6wlGKyB5wW7FxcXwycAEc8PMILKwFkG7wbGbqYdoVaQE0Z5NBqq6HZ9AAAgAElEQVQNRlhQDYjgwz0YMcFesC/8soMvtmfPnsOHDwO/wJeBQvBF+O9NwMfKyko8Pj4+7ufn9+NhUHFx6aVLicY7RILp6X4/P8SgJTDoyJH01FRBWtpcWppm69aSo0cHzp7Fysp+FFdSCIz7PTz8jdq9ezeMcfznBWMrcDegX0Ee+IWHLfhXGC7536KgoKBYo8AfiYyMBDcEPqEE2ILvC4qOjoaiTLtAOaYkk8AvCw4Oxq3HmglKg41QLG4C8kAEz2naEbZANSAPjMXCjTLVylQxqMDy5cvffPNNgC9sge1gyP9eBS0GHhYed3V1hXHij4pBFy8mGBkEP1EtHh6u1sQgS1vLNTDwKIYNGP+SnE1J8SCRrv94riTwAsCDmDIKhk4SiWTKTDBOmbpZt26xLkH9tUbdlwMxbzFoRv2PwXNeyCCFVMpqasp1d3dBDLp3Bvn6EmQyJriUc3MMf3/nmpo6DAkJ6W4MSk9P1mj4DEYjMAj5QUtikL+/JzCIx+seHycHBbkiBiEh3VUlJWXHj4cKhd1MZhPyg5buB3kwGIY5poChwEAXxCAkpLuqtLScSCRwuZ3gB5FIRV5eHohB984gNzdHaETAOY/XFRZGQAxCQloMgyIivGDoMDLSzud3Wdk8aUtjkLu7E5lcAn6QQjF66lRUVVUNusKQkO7KIPjBnpjo1Wg41jdP2gIZ1N5eaHzARw4MqqysRlcYEtKdVVJSFhvrj2FTGCayvjmKlsYgV1fHwcEm48PEstTUSMQgJKS7av6/eeucJ21pDPLx8cD/m8cwKWIQEtL3YZBhnvTUVB96VmOp84OkUoZxjqIMjcWQkL6nHySi0Wqt7L95S2WQCMOmw8O9qqtr0RWGhHRXBhmfF5NPTvY3NGRb2RxFC2SQXM7SajmTk31onjQS0iIZdPlyokIxRqc3NDXlIQYtcZ60l1g8APXkcNA8aSSkRam0tDwuLoDH62Iymxobc9BYbEkM8vJy6+2tpNEauNzugADkByEhLYpBRKInMAj8IAql3MeHgBi0pHnSHR3FDEajQECJjvatrq5FVxgS0l0ZZJwn3QEYmpzs9fPzQgxa0hxFYBDgXKPhnz4dg/4XQ0JaDIPCwjxmZ2n4Gmbov/mlPy9WPDvLwDAFmh+EhLQYlZSUJiWFGF/UIURruS6dQU4cTofx3UlojiIS0qJk/F8sCZ8nbX1zFC1wDTO5nGWcoyhFcxSRkBbJoPl50sKJiR5v74e/dscwT15L0bTRNM0D2iaqtrpPm9+h6WQpbzDoXctmkGmedEpKBGIQEtKiGSSHjkOhlLu5OVsCg2q6zRjUr83r0JCtikEirVYQEuJeXV2LrjAkpEWMxQzv1eByuyxknrR1M0ihGFQoRgSC7oAAtI4iEtKiGHThQpxEwqTRGpqb8xCDljpPWiSiMJlNHE4nmieNhLQYlZaWR0X5cLmdLFZzY2MOYtCSGEQguHR2ltLpjeBVIj8ICWmRDAoP94QuQ6c30Gi1ljBH0YoZhM+ThqacnOyLjw+qrq5FVxgS0l0ZhM+TnpqizsxQEYOWOk+aRCoaHGzW66esYp70zMzMwYMHnZ2djx496uTkdOTIERcXF4jDCd69e7enp2egUdAgkBr4YOTo6Ojn54fHXV1dv/76a2ejwKKDgwNeK/yzoqIC9VibZFBYmIdcPoxhIguZH2TFDHJ1dezsLFMqR61lnvTo6Oh//dd/QfcmEAgbNmwICQlZuXJlVFTU1q1bly1blpOTw+fzBQJBbW0tsIlvFHydMEooFPLvh+zt7aHZ8XhSUtITTzwRGRm5b9++w4cPA4mgJr6+vmvXrvXx8YmLi0M91vZUXFyamhqBzw+ykHnS1n0/aGKix4rmSQ8MDEAPj46Oht4Op3Pnzp0nT57csmVLamrqp59+2traimejUqnmb0CXyWRSqfR+vY8YnCAoEI/n5+eDNwSumb+/P2ARahUREQEwys7Ofu211wCRqMfaJIOM86RvrOVqdWMxy3pWw8/PUy5nWtE8aTab/T//8z/Q7RMSEuCQCwsLobcXFRUVFxfv3bu3q6sLWEMkEt3c3FJSUvBdAEyAp1WrVgGn7s1oe3s7XDpnz55NTk4WiURfffXVtm3bwBYkXbt27ZtvvoExV/68wBcD52jXrl3x8fEnTpxAPdYmGTQ/T1rE53d6erojBt2fedLJyaGW/34xGo3m6uoaHh7u4OCgVCrNk6Dzb968+amnnrKzs9uzZ8+ZM2fw7WKxOC8vD5gF+ABYdHZ21tfXNzc3d3d34/druFyuyYH6rkZ++umnoVgA2ezsLPAF4j/96U+BeufPn6+srFyQH87FqVOnli9fHhYWhnqs7TJIodGMt7cXWt08aQtdT1qpZFvFf/Ojo6MvvfRSUFAQDHnIZLJ5UmZm5o4dO8BLAkDs3r3bxCDckTl37hxEvjEKAAROSmJioqenJ51OB5zBaK6pqekOdoeGhuAC0ul0EN+6dSuYePTRR+3t7S9cuAAu2E0XhE535cqVffv2gbMGDhHqsTbJoPR0OLMzIyNtDQ3WNz/I0sZihnnSYjGdyyUHBlrBHEUGgwHdG0ZbcEZ5PJ550unTp9va2lQqVVxcHIFAOHnypCkJAASgUavVTk5OgCr8moCrAZoORnPgzhw9ehRacpF1AG8LdqFSqRDPysoCJ8s8FawAemJjY9evXw+gRD3W9lRSUnb6dPT0dD+dbkHzpGtvZtAdnlm1tPWkPdnsdmhKLrfLKuZJgz/y4YcfhoSEBAQEgAtjnpSammryZcbGxqBBTEmNjY3Xrl2DCHgowCl8I7hR6enpUKBMJistLV0wsruDzO80A4BgDGieCmcBBmhubm6HDh1C/4vZpObnKHYymU3AIALB7aEzaIQvb+jVtNO1zVRdQ5+2ukdbRNJQTGt3WDKDPDyc8bVcrYVBg4OD69atCw0N9fHxAZ/IPOnixYswzoqKioqOjoY2Wbt2bdS8wCcCLykmJgY+T5w4geeBCIzXwGdJSEhIS0sDXkQtTitXroTBIB6H0d+CSUBwFsCKn5/fgQMHwBtCPdYmGRQR4YUzaGSkxd/fGzFoSXMUyeQSGq1+dpZ+/DjR8u9JM5nML7/8MiwsDI6ay+WaJ8nl8oGBAYpR0CyQk/JgxGKxent78TiNRoPBl3k1NBoNIA9GYQBBIB3qsbbqB/F4nVLp4MwM1SLWMLNqBrW3F46NkTBsLi0t2vL/mx8ZGXnnnXeCjers7LTAGup0OhjiHT582NfXNzExEfVYW2RQWXi4l0YDP4ETlrKWq/UyyNXVoa+vSqeD1pRbxRxFOp1+5MgR/L/52dlZC6whuEVwLlJSUoCVRCIR9VjbU3Fx6dmzsfharohB9+H9YrOzA1Y0T3psdOzFl18kRhNjE2N7qD0WWEO9Xp+dnb1z587Y2NgHccEhWQKDjO96luLv1bCId/tYL4P8/DxlMnyetMwqxmKjnNFVH69a8daKv/72r077nEIDQ/WY3qJqqFKpIiMjL168+Morr4SGhqIea5MMMs2THhtrIxBcEYOWPkdRgGGSY8cCFnNPWqvSzgnmIDLLmdXr9BKBRKPUKKYVylmlWqaWiWQ6jW6OOwdkgAymbFKhVKPQKGYUSrFSI9dIRVKd1pgNu5EN4nqtMZtcoxArIEB++Ar7mmfr6+17z+49dzt3CPvs9n38zMdqTG1pflBeXt6WLVuSk5PN5ygh2RyDFDLZUHNzrkW869mqGWT0g4QSCcvff1Hveh7IHUh9NzVrc1b62vQrX1zJXJd5ddNViGRtzLq68eqVzw2R9DXpVzZdSV+ffmXzlYx1GbAlc30mfF7ZcCXriyzT14y1GYZyPk83fK5JhyR8uylAaVCmobTNhtKyN2UnfpG45hdrIuwiguyCfO18N7+y2dIYhPtBFy5cQM+s2jCD0tOTtVqh8X3zuZYwR9Hax2IsgYAyPk5e5PygjpSO4kPFvC4eOD58Cl82KZugTcxx5sRj4inWFDg4wj4heDG8bp5qToVnE/QIINskY3J2fFbMFk8yJyGboFcAPhFkwLPBLoZsEzJIhWwQID98hY2mbPxuPpVF3fB/N8TYxYTbhQOGtry8xQL9oJycnG3btsEZQc+s2qRKSspOnCCKRBQGo7GpCflBS/aDmMwGGq2ex+sODFzU82IdJzuqfR7abaOxibG3H317q93WDXYb1tmte//Z9zWYxtL8oJiYmFOnTr377rvomVWbVGlpOZFI4HI7gUFtbYVeXu6IQUtdRxFcSi63KzTUYzEMIqeQKz0rH9bp53F5j/zikc07Nm/fu9032LexudHSLlCdTpeZmbl//35/f3/0zKqtMigiwovDIQ8Pt/J4ZDRP+v7Mk5bLh1NToxZzT/q7GCSTyeh05oM+/XQ6/eDBg7HHYv38v11IzKKEP7MKrtCGDRsiIyNRj7VVP0gk6lGr2WieNNZP7ffw9PD29T6WcOwe/qXG50kLBFAZ+SLXMPsuBlVWVm3c+PGJE/H9/fQHd/oHWYOrP14TFRwd5Bk0MT5pgRco/BKcO3cOfhgOHDhg/twski3dD4qJ8dXrJzBMtMg5iuRusjvB3cvH6/jJh/G++QfLoL5+DxcPLzevmPBYxZzh33E8aBQave7uSHJ1dRwaaoamxDDlIhnUkdJRSbgNgwoKiq9eDRUK644f9zl5MrG3t/9BnH7+FP8n//jJuuA1DucP7zy+kzXFskAGnTlzBjxTe3t7xCCb1PwcRSV0nOnp/tsySKvSquVqU39sbWhzc3TzdPM8nmh7DMrr9/i5h9+j/oG/CIx5Kibm6VhDeCo27DdhtHzaXXf39nGfUfSrMbYKmz6RRlykH1ThcZvXRRSWXo+Icy4uSq2vPxUf7xgd7ZeamtTfT7u/zd0vood0HL5Cj0ggE5JJThcply3tAtVoNOBvR0VFrV692nxNayRbYtC5y8egy6gwtmCm08eXcGuey59dDn8qPObJmNjfxCa/kBD+63DfR/w8H/U8/qbNMagzjZLwR6Kgs36KXi/qr4Yg7K/mtFcf+31w5+nuu+6+7Ytta1/8bONL6ze/tPFvT7/SRbv7Lt/lBzHam4OObPrk8w+8vffs3//51BTJ3X03gbAvJiais5Ny3xgkpIfWH2kYvXSmy59Q+VURo8jSLlCdTpeRkXHo0KHAwED0zKpNqrah7vXfvvb5s+vXPPPZyhc+2fvVnlvzJPxPUl3oRS6plkeurA+5zCNXiShNbfFX4p9JsjUGkU91n30vrv9q4an349JXnUhffeLUB3H9V4oufBRf5VkrGhANlg9OD00zShgzIzP0EjrEYQtsH2sc45K5+9fsP2J31NfOL8Qu5F92/8pMzpwdnYXMhmwVgyKqaKxpjNvB5XfzR+pGJugTjGJG/u78cx+cI50gQWlTg1NDlUPCfiG7nccNPS976Y9Fab4Vlaf6+q6EhR39+uv1K1e+3dV1LTTUJSqKeF9GZ/1CRmIbYULWcKUv7GyXzzVqjqVdoCqVCoZgqampb731Fnpm1SZV1VL1qd2nx588cfpvZ+ztDttvtue0cdjNbGGfELrD9OA0rYQe9WTsSE0ZhjFr/C67/8SrwuMi/Eyzm8qP/T7RBhmU+kaMYoZ84ZOkI3auh+1cz/0zUTHdeeHjxKj/ic35KidvV17G2oy8PXnp69PhM2NNRt7OvKwvsnJ35Obtzlv3wjp3O/dAu8Bwu/B1P10XsyPm2ufX8vbmZazLyN2Zm7UxC0rI3pp9dctVyH9lwxUo7dgfjp1862Toz0Nzdufg2a5uupq1p6zmA3/Mzg67GoFhIxg2IBQ2bNr0cWDgQQwbwzB2fn7Mgb1flpOuV41WVQ9X1wzXQKgdqa0bqTMF+AobIbVyqBJC1dCNnJBUP1oPoXmsObIpNqbZsZSZyJoqrB5Kzui7YmkXKP7M6o4dO9AcRZtlUHPVP+3+2Xe8T8qXhjwesvrPqwt3FeZsz8nalAUdJPPzzJw9OT7/6ccqLy1zPH/YzsXFjmBv51r0zRlGUVHCn2zOD+pI7U5dFg2IxTBq7u60nK/SwFcA+p5+M7Y1kaTTGNZg1ygMs/jUcrUprlXf+Bd/zz/3eNgRiHbEGLuYtXZr2+nt5tl0at2NfmW8va1VGfYqOlCU8o8UMVv8bTajFXVFhcx5K4WeV1eXNjPT1tBwJjDwAIbxudyq1NSAkBDPiuvX5Uq5XGMICo3iuwKewRQWpLaMk1M7fbmSah3WUz2cdLk3wwL9IPyZ1Zdffhk9s2qjDKpcZbc6+63s8p3l0H32r94/z4Jvu1vyX473puf1phf3XyukZhfBZ8+lIuq1/MTnbI5BlHM9xF8E1rpn1hIySo6cLjmcVupwptj+jO9/uHek3n2Jr61rtn74sw9WPvLZmkdWv/DvfyZ1kxZ1zPNsMldpUcnVoti2jqyrV8MnJxv5/Kq0NP9Tp8K8vFxyc/PlcuV9Od7ByZGt2av9KuwJxV/vz91QQC+0QD8If2Y1KSkJPbNqk6prqnvppy9+arfifbv33n/kvb1f7r01T+zTx85+El3jd6nW/0KN/4XGkPT2iLxrG08m/MbmGESt7nd9yc3ldx4+zwVc3ZJ7bWve1U0wOMrNPpDL7eTedXdHZ/v8irTK5szWvgKCn31dbcM91yS/sOTCpUCppFuhaBEKSy9fJoaH++XnFyoUqvvY3DQazT2McDjQ4cPNHzMmhlRalaVdoCY/CD2zaqsqL6tw9z3Y2JXb0lPQOVBK8LrNmvZNkY1ZX2XjnRFC8gcpTr9xc37W7fiXtvffPK3fI8DDO9Q7LvVeXuHg4eHc01MxPNyKYZPnz8ctZf2gwsKSq1fD5PLOy5eDAwM9iopK1WrtfW9u9hj7j8/8MSQwJCE2gdRCssALFL8ftG3bNrSGma2qtLQ8MtJbLh/EsCmZjLmYNcx6WD1u/m5eIV7Hz9geg5b2rIabmyOJVDQzQ8MwxRLXUSwtLdu+/ZOYmICSknKd7kGdfvCDnJycwsPD4XNmZsYCL1Dwg4A+KSkpH3zwAXpm1SZVUlKakBCMYeLFz5N+4M9qzDOoja5rpmrr+qyJQU5sdvt9WctVJBKVlJTpH/CihqOjozDGCQoKIhKJ+BvfLU34/KADBw74+Pig+UE2qfl50ob1pKemLIhBfaM68qAWQnWvNq/dShjk60uQy/G1XK1jPWkmk7lz50783T7j4+MWWEN8nnRkZOSmTZvQM6u2yqD5tVyF4Af5+BAsgUH1veruIW15l+Y6RZPdqs5tU1OGrGktV8N60ikpEZbPoKGhoRUrVoSEhPj5+bFYLAusIZyFs2fPenp67tu3Dz0vZtMMMvhBPT0Vbm7OD51Bhnc992gow+ABaWr6NPkkdXabusuq1pMW6XSi0FCP6upay2fQypUrQ0NDfX19BwYGLJZBcLUdPnwYMci2x2J8fndDQ7YlrOU6xJXXUDR9I9o6qqZhQFNI1lxrU1vH++aBQQrFoFI5KhRSAgJcLP9dzzAW27FjB5FIdHNzEwgEFlhDtVoN11lMTMxnn32Gnlm1XT8oXipl0Wj1zc15lsAggx9E0bTRNEUdmiKSBpygnHYrYZC/vxcMaAcHmzmcTqt43/zIyMgbb7wRHBwMwzESyRL/m8fXUTx48GBQUBBaR9EmVVpaHh3ty+V2sljNjY05FsKgmm5N64CmeUDbRNXWULV5HRqyVTDI09O1q6uMTm/gcrsCApwtn0H4f/MRERFHjx6VSCQWWEP8v/m0tLS///3v6JlVW2VQeLgndBnoOFRqtSX8L4YzCPwgnEHV/dbDIDc3x46OYmjKiYneuLhAy78fxGazn3vuucDAwMjIyIaGBgusIf5eje3bt8fHx6NnVm2VQRERXuPjHRMTfRbynlUrZhC+pj2L1aTTTZ4+HWP5/4sNDAzAwYIfZG9vr1AoLNMPMj2zip7VsFUGhYV5yGSDGCaamupDftCSGOTq6kgml8rlw0ufJ/2D+UG///3vwQ+KiYmpr6+3TD8IvWfVtlVSUnryZDiGSfD5QYhBS2KQh4eLUEi5L/OkfzA/CE4k+EFHjhyxzPdq4H7Q+fPnly1bhtbusEkVF5devpw0P0+6D43FlvqeVbmchc+TXuSa9g9XY2Njf/rTn8APioqKam5utkw/KDs7e/v27dHR0eiZVVtl0Pw8aZFA0G0J7zi0YgaZz5M+fjzM8hlEp9MdHR3xZ1anp6ct0w+KjY2FUdiHH36I/hezaQbJtVpOR0exhcyTtnYGidTq8cBA65gfBGOcoKCgsLCw7u5uC6yhTqdLT08/ePAgXHDomVWbHovNQgdvaLCg+UHWyiCFYnBujsHldi7yffMPV/g8aQAQgUDgcrmWWUm4ziIiIrZs2YLmSdukSkrKzpyJmZkZoNMbLGeetLUyyN/fk8PpwOcoWsU86cHBwc8++yw0NBQOube3F7bgJOJwOPDJ58OgEpuZmYGmgDHR3NwcfBUKhaYM+Cf+kIdYLFYbNTs7a9pong3fEVKhKI1GA/kXZMNNi0Qi+JRIJEqlEpygiYmJy5cvQ/V27doFgzLUY21P+Pwg+NlmMpuamnIJBDfEoKX8L+YMA1oGo9FaGDQ0NPTpp58CgwIDA319fePi4sAngk/YAi0Acej24eHhUUaBMwJfiUTirdliYmLwbNHR0ZGRkbDxu7JBIXi2O5SGp5pKg2w+Pj6Ojo6QB/VYG2YQdJyhoSZL+F/sob5vfslzFMnkEhqtHhzL5OSwqqoaCz/9dDr94MGD0Lf9/PxOnDjh5OR06tSpw4cPw+fRo0dhi6urKyDA398/ODgYiABDNjjrgAPIcOTIETwbbHFzc4NUAFlQUBCABtoQ9oVsaWlpeGkODg7JycmwHbJBnoCAACgWLqOTJ09CEp4tNTUV4klJSWAF0BMSEgJ24UTAXhcvXlyxYgWACfVYm2SQ8VkN8twcc2aGahFrmN2ZQcvH7B6zYAa1txeNjLTBmCMtLdry/xeD4Y+dnd3q1auBRM8//zyQ6MknnwSPBj7BK/njH/8IcHnrrbe2bdu2YcOGd999F0jx3HPPQbYnnngCXBj4BFLAFmdn5+XLl2/ZsmXjxo3vvPMOgAn2BdBABijtqaeeAu5A+UAlKOSLL7748ssv33zzTUDeH/7wB0h6/PHH8Wywy1/+8heg20cffbR+/fqvvvrqjTfecHFxeeaZZ3A3DfVYW2RQGTBIrR7HsAlLWcvVehnk6urQ01Oh1XIwTJ6aGtnY2GLhp1+pVJaXl+dbgwoKCmDkiHqs7am4uPTMmRh8jiJi0NKfm3cDZ9I4T1p2+nTMli2bAwN9g4L8XF2dwQUIWLLa2urRJYtkewwyrmEmBQZZyDOrVswgPz9PmQxfT1p+5kxsaKh7UlJ4RETAsWO+bm6uAoFAJBJMTQHsBfcmFotyD7VCQrJwBpnmSbPZ7Zbwv5gVM2h+jqIAGjQhIfjUqajgYH9nZ6f09KTo6BtzW4RCTC6/59s3LMQgJBtlkEKhGGlpyXN3d0EMWhKDjH6QUCYbCghwSU2NDAsLdHd3vXQpISrK8J/O+fNYTAy2dy+mVt9L9TgcJmIQku0xKD09WaebMK6jmGsJcxSteywml7NEol4Ohxwc7G7OoOjoCL0e8/HBamuxiQlD5s5OjEIBrGD19VhjI9bVhdXVYW1tWFOTIbWyEsvNNUTodKynBzEIyWZVUlKWkhI+MdHDYDQ2NeVCf0EMWgqDCIODTTRaPY/XHRTkZs6gyEiDHySVGlyhmhpscBCLjMQSErD8fMzJCUtNxU6fxvbvx7y8MBIJKyszuEtRURiNhu3ciW3bZoggBiHZpEpLy4lEAj5HsbW1wNPTHTFoqesoMplNPF5XWBjhVj8oPt7g/gQEYM3NWGwsduwY1t6OnTxpiMNGBwesxfhvfk4OlpgIlTGgat067PBhjMdDDEKyWQZFRHjB0GFoqIXD6fD397Z4BlnDPGmZbCgtLfrEiXATg2JjoyHDhQvYqVOY8ekow/irzvgsB59v8IMgQBIQCldeHpaebogMDGDXrmH4Oqs83iBiEJJN+kFCYbdKNWYl86Qtm0Ht7YXgBGGY/PTpGBODMjKSob1GR0fF4tHZ2VE+f3RsbHRiYnRy0hDh8Ubn5m4EoRByGTbOzBgCSCQy7MJmG+IsVg9iEJLt3Q+KivLR60XWM0/asteTptPrjfODFOZ+UE5O2urVq0KWrNraEp1Oh65aJFtScXHphQvxljVPmiev61G30bQtA7rGfm1Nr7aApO62CgZ5e7tLJPj8IJk5gy5ejI+Luw/vKRYIhpEfhGR7DDKfJ40YdF/mB+HzpGPM7wfh/4uZ1N0Nw2CsqAj7XgvJo3vSSDbJINM8aRar0SLmKFo1g4zzpIUYNhsd7ZeSEvFdDIqLw9auxTZuxIaHEYOQEIMM86TFYnpjYw5i0FIZJJez9HrezAxtwTzpBQwCxccbntvo78dcXQ1/kLm5YR4emJ8fxuUanKNTpwx/nC2oAmIQkk0yKD09Sa3m0OkNTU0WsZarFTPI399TIqGPj3fcOk/6VgaBK8RmG2YtHjliQE99veETBmiJiYaJixs2GLYvePUpYhCS7amkpCwxMZjP72Iym6zPD/o3C2OQj487lVpNo9Xz+d2BgW53YNDcnGEslpVliANxdu0yRMLDMQIBu34d6+vD9uzBbn2zMWIQku0Jnx/E43WBH0Qml3h7ExCD7p1Bbm6OJFIRg9EoEHRHRvqmpESa/hdLSIhfkHlszEAiGHlFRxscItCXX2KmJp2exsbHF5YvFI4gBiHZHoMiIrzGx8lsdodIRLGIedLWyyB3d6eOjmLwg2Bwe+ZMrOl/satXU3bt2pllpmvXsoqKsvLysmJisjw9s/Lzs86fzzp6NCsuzpAEKijIKizMWiASqQ7ND0KyPQaFhXlMT/frdDzr+2/eAv2g9uINem0AAB9VSURBVPai6ekBDFOaz5MGBu3evSv7diooyC4tNURyc7OvX88uKsq+gzo66hGDkGzuflBpfHwghs1gmMj65ihaHoOcRkfbjP/NyxfMUbx1LHYPQmMxJNvT/BxF65wn/W+WO0dRtuCZ1QX3pC9cwDw9Dat2TE9jIyM3lua4q9A9aSSbZND8HEUhMMjHB92Tvg9zFPkL/KBbGVRain3zDUYkGhbl4HAw46tJsZkZA5JwicWYXo8YhPTjYRD4QcK+vio3N2fEoKUzSKTXTxGJnneYJw2KibmxiIe7u2GOokCAffqpYbWgzk5sdBRzdsaSkzGlEjEI6ccyFhMKexoasi1kjmItxYxBfdp8krrLWhikUAyqVGyRqCcw0PUO84PAxwkIMMwDAmVmYtnZGIOB7dtn4NGJE4YFg774whDXaBCDkH4MDEqQyYZotPrmZouYJ32X981bMoP8/b2mpvqGhlq43M47z5OGYdeOHdjVq4a4lxcWHGyYLhQfj6WlGVYvm5jAwsIMK72isRiSzau0tDwmxg+6jHFN+xxLWE/6TgxiGBn0mKUyyNPTlUIpp9MbeLwucz/ofq3dwecPIQYh2R6DwsM98XnSfX1VlvC/mBUzyM3NsaOjmE5vnJjoiYsLMt0PyslJW7VqZfDNCgkxhNtGFsRNQmuYIdkkg4zzpDuEwl4Lec+qFTPIuKZ9MZPZqNNNnD17zPS/WHp6ko+PN5vNHh8f53E4XA6HPS+OcQtsH2ezIWKIsxfKsIshnY3WckWySQaFhXlIJCwME05N9SE/aKlruXZ0lMhkgximXPDfvOk9q2KVyrxc8Grk84aUer3sdkYlWq3c6P6g96wi2Z5KSkpPnCDCZY7PD0IMWqIf5CwQdGGY6NY5ilFRkZAhs6/Pr7R0b34+xEfEYqVGQ+Hzd2dmNo6NydTqzVevuldU1I+OmpdJn5jwra6+YvwLDd2TRrI9FReXXr6chM+TBj/Izw8xaMnvWcXnSZs/LwYMiomO0gOkKioM9JmZAeJsyswspNPha/bAQKYRMQG1tcS6utPG9/uQuNxpuVyr1wOYktraFMZ/6RGDkGySQaa1XIVCipeXB2LQ/ZknnZIScSuDvKuq8Jw4g64PwqgNK2QwCowwim5u3nLlyvD0dOv4+JbMTLfr13V6/b6CAmCQRKVCDEKyaQbJdToumVxiCfOkbYBBIo2GFxx80xpmOIN8qqvbx8ZyBgYg85murlImc3x2NrCmBgJndvabwkLgkVdlZR6NtvHyZb+aGrVOd7S0NJ9GUxkrgxiEZLtjsTk2u8NC5klbN4MUikGJhMXjdS143zx+T3pQLE5qaqJOTkJcpddf7u9v5/ES29ogdPD5SR0dDWx2Rn//tEpVMTJSyGJBnuNkciKJNGcci6F70ki2p5KSsnPnYsViGp3egOZJ34d50jxeJ4PRCAwynyednp7k5+fL4/GmRSKFWDwlEkFcKBDIpqdnJiZUYjGEGZEIPmcnJ+XT0yKBQDo1BakCPl85MwNByOfDLkNDfYhBSDam0tLyyEhvLreTyWxqaspFDFoSgzw8nGFAizPI3A/KzT392Wf/8l+yamqK0RxFJNtjUESEFzAIOg6L1WDpcxQtfy1XYBCNVj8zM3D8OPHkyQjTsxrHjsUuvXroWQ0km2RQeLgnh0OenWXMzFAt5H3z9T1m75vv1RaSNFaznnR7e9HwcCuGzZrPkzY9sypWiEuoJQqNgiqiVg9Va/U3TJC5ZMYko53TrtFpWsZbZhQz+PZeQS9kg434V3RPGskmGUQkElQqNoZNWMo6inx5Q68Zg3q0RSQNxSoY5OrqQKFcV6vZt5knHWX4XyyyKfJc+7nEtsQ2TtsXV74Ymh7Cd0xoSzjWcsyh1KFP2Lfp6qYp+RS+vYnd9HnG54AnxCDb1sjMSJ+gjyKg3DnQRDSZWmZjx15cXAqdxbLWcrVeBnl6uk5P9xvXk144TzomOhoY5FlpaF/3Cnf4TGpPAm8Id3YOXDtQSC+81HMJ8FQ5VCnXyE93ngbnCMdTj6AHMci29dfjf/116K/h889Jf8bDi8df/E3sb56IfuKpmKcgPBnz5OPRj/+7z79fZ123PQYZ1zCTAoOmp/ss4X6QFTPIz8/TtJ60+bt9TAwiVBrWynWrcDMwiJTEl/B1mM6/xj+7Pzufng8/dO+efVcgEXTzu+2L7bdmb8VRNSYeQwyybT2f+Dz4yF5VXrHNsX41fvDpXu7eL+yfkE0IpcLx2XHOLAcG8r+P+33OQI7tMcg0T5rD6fD0dEMMWvocRQEwKCkp5OTJhWOxuNa4443HU8mpzezm9RfXB9YGgstztvusY6Gjc7kzIAlcJI1OQ5+gO5Y5Lk9dntyevD5zvU+1D36HCDHIVvXayddcr7v+Z/B/AoY6eZ2ECoKdt107p31SPklsIBYzisFZhmx/SvxTAb3ARhmkUCpHW1vz3dxcEIOW/l4NkVw+EhDgYr6GWXx8HJ6HMmGo6qRukiFm9M324Rup09QxhcHZ0WM3FrIXaoSDkkHKDIUhYfSJb2QTCIYRg2xSr558Fehj52f3q8hfzSpn/zv8v+087ABGIqkIfo1a2a14tr8k/+VExwlwkyHACB1Cr7AXAgzblRql9TIoPT1Zr58cHGxpbMyxiPWk78ygdy17LKZQDE5O9nM4ZPM5ilevpuzduycvL6+ooKiytLKwoLC0qBQilSWV+fn58BXi14uvF+QXlBSW5BlVXlwOqaYASbCRTG5A84Ns1Q/yqPSw87R7LPKxKdmUgUHOdiQuiTvHBT9IopLg2V5IfuFU5ynaBA08ZcYkgznJZE4ZQimztHW81UqPvaSkLDU1YnKyl8FotJA5itbNoOHhFhqtnsfrNp+jCAz66qvtl5es9vZaxCCb1EvHX0poS/j4wscrL6+Maor67NJnH6Z9yJkzvHdlQjbx7W2j5OfzaHm37i6QCLp4XVZ67Pj8IHyedEtLvqenO2LQ0tdRbOLxukJDPczHYug9q0h30OPRj7+W9NrnVz5fl7Huw3MfrstcB/G1GWshbL66Gb7icTuC3W0ZNDoziv+LaqUMiojw4nA6Bwebx8fb/f29EYPuwzxpqZR16lTUrWuYpXSkgM8cWBUI4/kF+07KJmNaYsQK8bGWY+CB33BTmSWB1YFzyjn8K7onbas63XXaq9zLvcLdPLhed3UtvymEVoeOzIzcujts7OB2WC+DiESCQNClUIxYzjxpK2ZQe3shEP3W/+bxedKh9aEHiw4eLT7Km+OpdWq1Vo0Z3jWm12N6hUbhUOpQP1p/pOSIVqeVqqSQBNkOFh7sE/YhBiHdQcAgEodktQwqi4z01ukEVjNP+l2LniftODBQq9fzMUxx23c9X+m/8lbaWweLD4K/E90cHdcal03NJjYQA2sDG8caM3oznMudKXwKX8InVBLOd5+HXWJbYhGDkO7CoGkrZlBxcen583HWNE/akhnk7e0ukdDx+UG3ZdDV/qv+Nf4rLq3o4nX988I/DxcfhkvnX5f+9eH5D6fl01QR9d2z707JpkhckmOZ44qLK2CXsIYwNE8ayYb9oJvnSfdbBIPu/L75d61gfpBhLVd8LBYc7Ofs7ITPUYQMR0uPRjRGgL8zKZtMJacGVAQAcU6RT53sOAmpbDH7AuUCRLhz3PDG8G1XtnlXeW+7tg3GaPifI4hBSDbpB5nmSQ8NNVvI++atmEHGedJCDJuLjfU/ezb21KmE6OiwrKwTsbExS68eWrsDySb9IHye9Nwc0/iuZxeLZ9CYRTMIf6/G3BwjKMh1/fqVTk7fODgc2L79i3Xr1oWGhhLDiGGg0DCIwyd8xSP4FjxuikCqKeAb6+vLDfevkZBuYZD1/i9mnCedpNHwLGiOovUyyN/fE/wgLrdzfJwcHOyWkZE1MjI2OjrGZnNArCVLIplD/Q3pVln1/KCSkrKkpBCBoBtfyxX5QUtikI+PB41Wi8+TDgx0aWxsRt0DCTHozsLnB3G5XeAHdXQUe3t7IAbdO4Pc3BxJpCIGwzBPOjzcs6amDnUPpB+GQZ28TutlUESEFwwdxsZIQmG3RcyTtl4GGedJF4MfpFSy09KiKyurUfdAQgy6K4PCwjwmJ/u0Wu7MjFX8N2/RfpBhPenJyX4MU5w6FVVf34i6B9IPIKFSSJ2mWmnl4af62DF/DJvGMJGlzFG0Xga5ujoOD7cY/5tXJCQEJyen9PVRTYFC6TUPvb39piSIL0g137Gnp888Cb4uPvV7Gr1D6oMy+oDawbxYOC5raPx7MNpDo9G5I9yGtobsmmzuEHdocBg2WtcZj4mJP3MmBsPkFjRP2qr/m5+fozhFoVQFBUFD2RMIh/HPiAifqCg/PMTEBAYEuOLb3dwOeXs7RkX5m1KjowN8fBw9POw9PA67uh6CnKbU6Gj/yEhfAuEIJEGAfUNDCWapAWFhXu7uh3GjkGGB0cBAN5NRLy8HUxK+r6+vE74XGPX3dzE3Cp+enkdNRkNCPMyNEonesB2KhU8oITzc25QKRoODPUztAIXcbDTQz8/ZmHoEioW4WTv4g10vr2+NBge7mxsND/fBk4yp9kSil7nRkBCCWeMfgUYzbwc4OpNROOoFRr29HUyNHxTkZm4U2tPM6KGwME8zowGhoZ4mo7c2/gM442F7dn75yN8esfunnd1yu0eW/+yd99+Iigq5pzN+8A5nHKq04IzDKV76GYdiIQ7nkUqtgy4DP95TU30+PgTEoKXPUQQG8QDqU1NUDoeMB72eY5wJKjEGQL6Qz++G7Wx2h0DQDV6oWapMq2VzuZ0Q2GzStMHHnplPhU+pVMoaH+/gcDrHxkhS6SCGzZl2xDCxySjkgXJuNioSCCh4Es+w3IzQPBVqCBahWDAKg3Ojb/ytUbl8EHaEDGBUIoFjnDUzOjszMzA+TsYPR60evdnopFDYgxuF3Y2NY57Kg5oYjXaIRL3GC9FkVKZUDhuPxVCl2Vm60ah03uicWEw3GjXsq1SOzJeJFzsNpUEqXivj6TA3ygejxubtgLph2ISZUTnU32QUjgua1MyoBI7dlAptYmYUUmeg3R7oGYfUm884VlZ42W6t3ScFn+y8vtPO3s7Be4/xSrSuMy43ngIuVI9Krbay/+Z/YqEMEqnVY4ODLQMDdTRaA41WbzyFQmNPgCCUSFh0umE7BBarWakcNT5ixsXJNTnZDztCBviE06/Xc+dTDWiDk0ql1kIq/HTA5WVM4hlTBRoNe3i4Fd8XSoYuOm/UkCqTDTEYN4wymU0KxbCZUeH09IDJ6MhIu1bLMUuFHtttMgrxecgaioWckN+0L5RjblQuHwFbuFEGoxHqYH6kUEMa7caOUHONZtzcKBzdvNFa41IEPKNdQzvodFxoGZPRqal+83ZQqUahVY2NXw8ZoAObN/7cHAOvD2SAcwRnyrxK0CvgGPEjZbPJ5kb1eh50m/nUWmP/+bYdFpxxsPIDnHHgY2pypN0qu2tD14Zmh35y9N/tPXdimMrsjDfOn/HGm8+44OYz3na/zrhCcc9nXDAx0dfQkG0FcxSXj9o9ZqkM8vBwVihYwILBwaaBgRo6vQ66vVTKNLsc+cAjOA3GUDs01Gz8Dfk2FcbDVKphx4GBWvgZmb/UeMY+wOVwOvr7IRVOcN3ERI8xCb84+BrN2NBQC74vgwF9gG5WrAD6oXGvWtgR6qZSjZgbnZ6GPlCLV4nNbjf+gAtM3Y/H6zQWazA63wduGIVf75GRVjwVglg8YF6sXG6gHl4yiwV9YMg8FX5ITUZHR9t0unEzozzwFPBjgQzGH3C+ySjkHBtrM1XJ6DV8Wyy4TmALSoZ9mcwGo6vybersLM3U+MPDLUY/UTCfyhOJKPNGa+e9J/5844+Ds2AyCkMG83YA6j2UMw4nLoboZ/cvu9+d/N1Lp16y22l30HU7hqlNZxxv4Qd2xutuPePQ5vd8xqHMpqYcJ6cjD51Bw1xgkOG5+RaaromqrenT5ndoOlkqpuUzyMcHdnXx8HBwcDjo7Gzv5HTIze2ov7+Hr6+7Kbi4HHZ0PISnEgiO/v4EX183PMnHxxWSnJzs8VRvb1c/Pw9TqpeX83yxhgx+fu4Q5lM9zI26uh6ZN3pjX9hiMurhcZNRiMBGCHiql5eLn9+3qXA4jo6GYvEA282qBEYdTVVycTEYNasSbvRGldzdHW426g67mKoEh/ZdRiGbj89NRgkEJzOjh2826gENbmb0qNHot40P280a3+kOjQ9fzRvf09O88Q8vaHw4uodyxqGFv9r+5aufvfrCxhee3/D8q2tf3bBxra+vt9We8cOHD38dEOD/0BnEmVDUdqub+9UNvRqAUSVFk9+m7htRDY5ZPIMMA3GJTCqVyWSK+SCXSKTmAbaYUqXSBanmO0Kq7A6p8NU89c5GwdB3G11QpaUYlf3gRhV3MLqUxl9Q7N2qJH8oZxxKU6s1mB4TTAloHBqmw7RancQgaz3jCsWi3g7yQBkkk81RR6Y66JJ22hzJEGbbBuaa++f6RiTCiXEyS2HpDEJC+uHFnmV38bt+PMf7QBmkUkoHx3jNvePNfZwWKq91QNg2IGyniVjcWb1a0MFEDEJCukVW/dy8pTFIoZBIZ4Va5YxeM4fp5cb7axoM0xpWXVYJSAw5YhAS0kINTw9b7/pBFsig2RmhVDItl4mVSqlardRoVDqdWo9pEYOQkL6TQe2cdqurtv6WYH0M+rc/9iMGISFZHYPSOtNciw4F1ruHtXiGNHtACG0m+Fa77S/YOXy7lxdZHIN+hRiEhGTNYzGfKgJr9opgoiog5pBHnINH7JEruWFaPSO65Uj9yN1X3UIMQkKyLFndetLhzSFdw+dOZUb2ZxCntq+dctmdnRfbWHfhNMW3md2GGIQYhGRlsrr1g5J7Y+2JWztOB2B/+h1mZ2cIztuPx3sdubyVLLz7JIMfC4N0Oq1ej2VkYNHRGJF4U4iNxQoL0ZWPZCkaE4+BH6TQKL5XUGqUEL7vXncobfEWk3pjvjm2q3/n2hsAgvDL/zod6nTg4hbEoG8ZhGEGT+gXv8D+8pe5996b/uCD6VWrJt9/f/q996aeeUb6wgvoykeyFPEkvOuD12uGa2pHautG6vAAcQiwsXq4umqoyhTwbBDqR+sh4DnxPJVDlRBMeUxF4Xnwokyl4XFTTrwoCCaLptLgqykPhNqRuuiukK9DvuyPc8d+/sgNBn3xz5PHPA+c24QYdBODNBrs6acxCqUPw5rhwPv6qBjWjmFNV64wX3wRXflISPeoqLawsrZjqRnh0+cCsI/ewravbixNyM9LTG7zaBlvRwxayKDGxgEMaxMIeohEjlwOo+7Ws2cHX3oJXUhISPeowBrfWaxSwK4Jj3ElxngQYwgZGREYxjlD8UH/i30Xg1oh6dlnFTMz3YhBSEhLVEQj0blwZ3iLm2fZfueC3RCC648G1bltvrqyXzRgTQz6yQ/IoJ4e6mOPqaenEYOQkJYqlVbFnRWyZ3lciYArEULgzPHZYu6EbGoxu1sUg6g/AIOamoBBLcCg//xPndEPajl3DjEICemh6cfFoKeewtraqMAdgYDi6ChQq8kQv3iRhe5JIyEhBj1wBmm12C9/Ca6Q/PnnpX/5i/TNN2f//GcpxH/5S+Wrr6IrAQnp4aitre3o0aMuLi5xcXG2zCB8jmJdHZadjWVl3RRyc7H2dnQlICE9HKlUqrGxsfHxcaFQaLMMehB8RUJCWrpEIlFubm5paWlRUVFj4/1/lfFDZhCFQgEHz8/Pj0gklpWVlSMhIVmYCgoKwEtwc3NzdHSMjY21NQYJBILIyEgfHx/AkLu7uxsSEpKFCUYq/v7+AQEBnp6eNnhPGsRgMOAg4fA8kJCQLFXQQwkEQnx8vA0ySKPR8Hi8mpqa8+fPpyMhIVmeoG9WVFRAPyWRSNBhHyaD/u0BMAgJCenHrO+7njRiEBISEmIQEhISYhBqOyQkJMQgJCQkxCAkJCQkxCAkJCQrZZB4WiCZm5JLZ5RKCWIQEhLSD80g6dyESjGrVUv0WjmmV2OYxhh0ejViEBIS0gOWSimVKZScKf0QT8MYV9PY6v5RNWVQLRJrtcpbGPQTxCAkJKT7Ko1aKphS9Y3qKMO6Npq2sU9T26MtblN3s1TTM5wf4lkNJCSkH7O0aum4UN41pO8dxchMrLFPV9ODXe/U9wwpx7hjiEFISEgPmEEaKWdCXdw86RKaWUGabRjAXIi5CRn9VLZucGy0nY4YhISE9CCl00jZQuX1DulBn3O7XFNcidnrv446V8bpHdWyRhGDkJCQHjyDBjny2l49iaG197+4/uuIrKbp4h6MxFSxkB+EhIT04AdjUgZbnt+iaaRiZR3yq41TZQNYerOqlaZk3oFBI6we1HRISEhLl0Yt5Yjkjb3qVqqmg65rY2J1/ZpKioo+rh5mf+c96ThGf6tOq9CqpYagkermg0opUSgkCrkFBaiSeQ1RQOHHE+TyOegCSoWl9ETNPDFMXRK2SOamhjhT7bSJ+h5hHUVY2y2spQhruoWdzGnJHJfMUtyGQe7BccwB0qxcwxUp2AI5d0LNFiqHuPIRvlwqk89M8eZmhLMWEMTTAplkSiJXjwkUwzxD9ZYUeA8tQOWHuUsIvId54GB9yHorz11SGHmolTd0SZ6EwuTNiYUPuUtOC6SzEzKFSjClHBcquJPqcZESajjIkQumlTKpmM9lMIeoNFb/APPbMMamaeWDHUzlbRhECInr7+sensC6h7RdQ1h5m7i0TVzToy1qUxkKFQkUshmpZPrhh7kplVI6KsKaqZpaiqah995Dfa+mrkf9sAJUvqb73kNdz5KOfSk1r+9V1/YYGv+eD+EhVt7Q8t3W2vIQqrrUvUNwCLyZmUm59CH3RLViljul7x3Vdw3pSlsmqzvlTVR9KclwmFzhNI9LFU/SxRN0w+d8ZHaKoZYwbzDosVsYRKF0UTkYg4fVdYk3H4olpjY0DWDXO9TUEckgm6dWzsllYgsIM2qVjDamaadr22ha+Lz3QDOU8PCCZimhfWnHfi8VHtCSmdr+MS38SkGgDGvhZ6DdWipv1S1vFpr7NRSWqqqTNzs7rZA/5J6oVUuGeJruEV3PiM4lJPOA97l641zEln4NbVQ0NtY/LaJPCm8KI6x22XQ/maW6DYM8Q+O6u7t6x7DyVv6XR+KdidnlZOX1Ll15h6ZveI42wtNr5Uql1AKCRKtR9o1oWmi6ZuqSw8BDDNqlhJYf/MCbqLoulq6dqb3eramkaCp7NIUkTRvdOipv1S1vHhr6tMCgmm6eRDqnUj3knqjXKRjjmlaappOlqyCJd7mmHPC+WNAiBdT2DQqHR/pnJr6lz/QEc0JAa20qlopHOgfVdv+4HYO6ujq7R7CMUsaKbf4x51vqmVhJl7akQ90zCAwSYHq1Wq20gKDQ6dQ9w+omqraxT9uwlNCvbXx4Aeq/lAAlLOXY76HCsBeZoSWxtBUUTVWPprpXU0SC6886Km/VLW8eYCTYzVLWdPNlcrlG85A7I4YZnkSt74VBia5jEHMLz173dURm7WQLXUdhCoeGv2UQ0Ic33iPi9Qt5dLWcc/uxmFdoXAe5s74f6xrGLpUOfvpVQNTFtvIBLIek7mLN0UcFxhf2qCwh6HWa7kF1bZ+2qldT3bOkUNOrfVihuk9b3b+E0PtDH3h1j7aRCgDS5rRp8toNIbddUzdgHZW/6UD6razlzcN1CoyIwQ/iyxUKrfYh90RgQveQuqpb28bUe0blf34g6mrLVEkfBh3TnEHgAfHYvU31BZOi4aa6vNlJeteQ5jZ+kFdYXGdnV1kndp2saRjATubQU4tG8zq1GY3KbmDQmBDDdOCAWELAMG0zVZnXpi4gGX6KlxIKSOqHFfI7NHlLCAUP6cBz29Q5bersNvW1NnUuSW1dlb8vLV/4UCuf3apuo6nqe4RKlVKvf/g9sZOpzm9WV1O0yVf6L1bwyvqxjBZVRbeqhykcHLrBIHCCwAMCAM2KOUI+XaMUdjAVt2GQa2AMqaOdPo6RGcouptJ4r1vfSlN1MJS0sTm2YBLD9Hq91hIC0JAzoYWKdbFU3YNLCl0PL3SylGTmvYclHvs9VnveKFQeD9ZUeVPLM62w5ecDXPb/v52z50kYiMP4OZpoXARW4xdwN0bjB+ATGL8Lq4sDODg4ODnq4OyASqC00IEWy7X0jZK2KgRB+sZLvQIDUeMgIW3CPfmlaXLp5flfc0/+txzU7LLQHo4GKAJC3YZBGyYbDsnZaEkrUnBNB1Fzc1WnqnqsaGqNaucdijyRf7pHR7Dn7C0KoFz2rvNaCfqgb2exzVPjLH1ZhyRUzeKLUmDkPCMXApQCq6i64Xv62DPGbiTwPXPoGJKmcJIEZQxmheBESW0qrqX7oe9Hzxi5RsPU6ZpaZKdxIRNsEB00bHa7+rDPez3YbzN2Vx45Wq/F+QPz443x/RarOOBAQRmUSqUmGbTLbpzo1w9GRXZI+PmTstCnoFXkrGItWhCR8sP9SSjTLsNPBOFWo9JJOQRnoYMMBe0oWCJrNjJDTFzNg4YoHg2hPHEo3i0JHnopCYPpk647N49jsC/M9UE79FaSX08K4IhfO/4dcCgGuYXaJwwGg1kIlCQi2MuCeGaWQSB+BRJpEMuAWDpabC/Av6ddxoeLVLoia4tZ6g+NoOHEBdg+n2UQFhYWVljCGYSFhRWmvgDp/qcPYvC1hwAAAABJRU5ErkJggg==)


**3.**    连接仪器

!(data:image/png;base64,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)


**4.**    写操作（包括出错判断）

!(data:image/png;base64,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)


`     `!(data:image/png;base64,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)


**5.**    读操作（包括出错处理）

`   `!(data:image/png;base64,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)


!(data:image/png;base64,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)


**6.**    退出

`      `!(data:image/png;base64,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)


**7.**    运行结果

!(data:image/png;base64,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)

**命令速查**A-Z


*IDN?

*RCL USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10 

*RST

*SAV USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10

*TRG


**C**

```
:COUNter:ATTenuation 1X|10X
:COUNter:ATTenuation?
```

```
:COUNter:AUTO
```

```
:COUNter:COUPing AC|DC
:COUNter:COUPing?
```

```
:COUNter:GATEtime AUTO|USER1|USER2|USER3|USER4|USER5|USER6
:COUNter:GATEtime?
```

```
:COUNter:HF ON|OFF
```

```
:COUNter:HF?
```

```
:COUNter:IMPedance 50|1M
:COUNter:IMPedance?
```

```
:COUNter:LEVE <value>|MINimum|MAXimum
:COUNter:LEVE? [MINimum|MAXimum]
:COUNter:MEASure?
:COUNter:SENSitive <value>|MINimum|MAXimum
:COUNter:SENSitive? [MINimum|MAXimum]
:COUNter[:STATe] ON|OFF
:COUNter[:STATe]?
:COUNter:STATIstics:CLEAr
:COUNter:STATIstics:DISPlay DIGITAL|CURVE
:COUNter:STATIstics:DISPlay?
```

```
:COUNter:STATIstics[:STATe] ON|OFF
:COUNter:STATIstics[:STATe]?
```

```
:COUPling:AMPL:DEViation <deviation>
:COUPling:AMPL:DEViation?
```

```
:COUPling:AMPL[:STATe] ON|OFF
:COUPling:AMPL[:STATe]?
```

```
:COUPling:CHannel:BASE CH1|CH2
:COUPling:CHannel:BASE?
```

```
:COUPling:FREQuency:DEViation <deviation>
:COUPling:FREQuency:DEViation?
:COUPling:FREQuency[:STATe] ON|OFF
:COUPling:FREQuency[:STATe]?
```

```
:COUPling:PHASe:DEViation <deviation>
:COUPling:PHASe:DEViation?
:COUPling:PHASe[:STATe] ON|OFF
:COUPling:PHASe[:STATe]?
```

```
:COUPling[:STATe] ON|OFF
:COUPling[:STATe]?
```


**D**

```
:DISPlay:BRIGhtness <brightness>|MINimum|MAXimum
:DISPlay:BRIGhtness? [MINimum|MAXimum]
:DISPlay:SAVer:IMMediate
:DISPlay:SAVer[:STATe] ON|OFF
:DISPlay:SAVer[:STATe]?
```


**H**

```
:HCOPy:SDUMp:DATA?
```

**M**

```
:MEMory:STATe:DELete USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```

```
:MEMory:STATe:LOCK USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10,ON|OFF
:MEMory:STATe:LOCK? USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```

```
:MEMory:STATe:VALid? USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```

```
:MMEMory:CATalog?
:MMEMory:CDIRectory <directory_name>
:MMEMory:CDIRectory?
:MMEMory:COPY <directory_name>,<file_name>
```

```
:MMEMory:DELete <file_name>
:MMEMory:LOAD <file_name>
:MMEMory:MDIRectory <dir_name>
```

```
:MMEMory:RDIRectory?
:MMEMory:STORe <file_name>
```


**O**

```
:OUTPut[<n>]:IMPedance <ohms>|INFinity|MINimum|MAXimum
```

```
:OUTPut[<n>]:IMPedance? [MINimum|MAXimum
:OUTPut[<n>]:LOAD <ohms>|INFinity|MINimum|MAXimum
```

```
:OUTPut[<n>]:LOAD? [MINimum|MAXimum
:OUTPut[<n>]:NOISe:SCALe <percent>|MINimum|MAXimum
:OUTPut[<n>]:NOISe:SCALe? [MINimum|MAXimum
:OUTPut[<n>]:NOISe[:STATe] ON|OFF
:OUTPut[<n>]:NOISe[:STATe]?
```

```
:OUTPut[<n>]:POLarity NORMal|INVerted
:OUTPut[<n>]:POLarity?
```

```
:OUTPut[<n>][:STATe] ON|OFF
:OUTPut[<n>][:STATe]?
```

```
:OUTPut[<n>]:SYNC:POLarity POSitive|NEGative
:OUTPut[<n>]:SYNC:POLarity?
```

```
:OUTPut[<n>]:SYNC[:STATe] ON|OFF
:OUTPut[<n>]:SYNC[:STATe]?
```


**P**

```
:PA:GAIN 1X|10X
```

```
:PA:GAIN?
```

```
:PA:OFFSet[:STATe] ON|OFF
```

```
:PA:OFFSet[:STATe]?
```

```
:PA:OFFSet:VALUe <value>|MINimum|MAXimum
```

```
:PA:OFFSet:VALUe? [MINimum|MAXimum
:PA:OUTPut:POLarity NORMal|INVerted
```

```
:PA:OUTPut:POLarity?
```

```
:PA:SAVE
```

```
:PA[:STATe] ON|OFF
```

```
:PA[:STATe]?
```


**S**

[:SOURce<n>]:APPLy:CUSTom[<freq>[,<amp>[,<offset>[,<phase>]]]]
[:SOURce<n>]:APPLy:HARMonic [<freq>[,<amp>[,<offset>[,<phase>]]]
[:SOURce<n>]:APPLy:NOISe [<amp>[,<offset>]
[:SOURce<n>]:APPLy:PULSe [<freq>[,<amp>[,<offset>[,<delay>]]]
[:SOURce<n>]:APPLy:RAMP [<freq>[,<amp>[,<offset>[,<phase>]]]
[:SOURce<n>]:APPLy:SINusoid [<freq>[,<amp>[,<offset>[,<phase>]]]]
[:SOURce<n>]:APPLy:SQUare [<freq>[,<amp>[,<offset>[,<phase>]]]] 
[:SOURce<n>]:APPLy:USER [<freq>[,<amp>[,<offset>[,<phase>]]]]
[:SOURce<n>]:APPLy?

[:SOURce<n>]:BURSt:GATE:POLarity NORMal|INVerted 
[:SOURce<n>]:BURSt:GATE:POLarity? 

[:SOURce<n>]:BURSt:INTernal:PERiod <period>|MINimum|MAXimum 
[:SOURce<n>]:BURSt:INTernal:PERiod? [MINimum|MAXimum
[:SOURce<n>]:BURSt:MODE TRIGgered|GATed|INFinity 
[:SOURce<n>]:BURSt:MODE? 
[:SOURce<n>]:BURSt:NCYCles <cycles>|MINimum|MAXimum 
[:SOURce<n>]:BURSt:NCYCles? [MINimum|MAXimum
[:SOURce<n>]:BURSt:PHASe <phase>|MINimum|MAXimum 
[:SOURce<n>]:BURSt:PHASe? [MINimum|MAXimum
[:SOURce<n>]:BURSt[:STATe] ON|OFF 
[:SOURce<n>]:BURSt[:STATe]? 
[:SOURce<n>]:BURSt:TDELay <delay>|MINimum|MAXimum 
[:SOURce<n>]:BURSt:TDELay? [MINimum|MAXimum
[:SOURce<n>]:BURSt:TRIGger[:IMMediate]
[:SOURce<n>]:BURSt:TRIGger:SLOPe POSitive|NEGative 
[:SOURce<n>]:BURSt:TRIGger:SLOPe? 

[:SOURce<n>]:BURSt:TRIGger:SOURce INTernal|EXTernal|MANual 
[:SOURce<n>]:BURSt:TRIGger:SOURce?

[:SOURce<n>]:BURSt:TRIGger:TRIGOut OFF|POSitive|NEGative 
[:SOURce<n>]:BURSt:TRIGger:TRIGOut? 

[:SOURce<n>]:FREQuency:CENTer <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:CENTer? [MINimum|MAXimum
[:SOURce<n>]:FREQuency[:FIXed] <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency[:FIXed]? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:SPAN <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:SPAN? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:STARt <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:STARt? [MINimum|MAXimum] 
[:SOURce<n>]:FREQuency:STOP <frequency>|MINimum|MAXimum 
[:SOURce<n>]:FREQuency:STOP? [MINimum|MAXimum
[:SOURce<n>]:FUNCtion:ARB:STEP

[:SOURce<n>]:FUNCtion:RAMP:SYMMetry <symmetry>|MINimum|MAXimum 
[:SOURce<n>]:FUNCtion:RAMP:SYMMetry? [MINimum|MAXimum
[:SOURce<n>]:FUNCtion[:SHAPe] <wave> 
[:SOURce<n>]:FUNCtion[:SHAPe]? 

[:SOURce<n>]:FUNCtion:SQUare:DCYCle <percent>|MINimum|MAXimum 
[:SOURce<n>]:FUNCtion:SQUare:DCYCle? [MINimum|MAXimum
[:SOURce<n>]:HARMonic:AMPL <sn>,<value>|MINimum|MAXimum 
[:SOURce<n>]:HARMonic:AMPL? <sn>[,MINimum|MAXimum
[:SOURce<n>]:HARMonic:ORDEr <value>|MINimum|MAXimum 
[:SOURce<n>]:HARMonic:ORDEr? [MINimum|MAXimum
[:SOURce<n>]:HARMonic:PHASe <sn>,<value>|MINimum|MAXimum 
[:SOURce<n>]:HARMonic:PHASe? <sn>[,MINimum|MAXimum
[:SOURce<n>]:HARMonic:TYPe EVEN|ODD|ALL|USER 
[:SOURce<n>]:HARMonic:TYPe? 

[:SOURce<n>]:HARMonic:USER <user> 
[:SOURce<n>]:HARMonic:USER?

[:SOURce<n>]:MARKer:FREQuency <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MARKer:FREQuency? [MINimum|MAXimum
[:SOURce<n>]:MARKer[:STATE] ON|OFF 
[:SOURce<n>]:MARKer[:STATe]?

[:SOURce<n>]:MOD[:STATe] ON|OFF 
[:SOURce<n>]:MOD[:STATe]?

[:SOURce<n>]:MOD:TYPe AM|FM|PM|ASK|FSK|PSK|PWM|BPSK|QPSK|3FSK|4FSK|OSK 
[:SOURce<n>]:MOD:TYPe?

[:SOURce<n>]:MOD:AM[:DEPTh] <depth>|MINimum|MAXimum 
[:SOURce<n>]:MOD:AM[:DEPTh]? [MINimum|MAXimum
[:SOURce<n>]:MOD:AM:INTernal:FREQuency <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:AM:INTernal:FREQuency? [MINimum|MAXimum
[:SOURce<n>]:MOD:AM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:AM:INTernal:FUNCtion? 

[:SOURce<n>]:MOD:AM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:AM:SOURce?

[:SOURce<n>]:MOD:FM[:DEViation] <deviation>|MINimum|MAXimum 
[:SOURce<n>]:MOD:FM[:DEViation]? [MINimum|MAXimum
[:SOURce<n>]:MOD:FM:INTernal:FREQuency <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:FM:INTernal:FREQuency? [MINimum|MAXimum
[:SOURce<n>]:MOD:FM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:FM:INTernal:FUNCtion? 

[:SOURce<n>]:MOD:FM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:FM:SOURce?

[:SOURce<n>]:MOD:PM[:DEViation] <deviation>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PM[:DEViation]? [MINimum|MAXimum
[:SOURce<n>]:MOD:PM:INTernal:FREQuency <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PM:INTernal:FREQuency? [MINimum|MAXimum
[:SOURce<n>]:MOD:PM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:PM:INTernal:FUNCtion? 

[:SOURce<n>]:MOD:PM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:PM:SOURce?

[:SOURce<n>]:MOD:ASKey:AMPLitude <amplitude>|MINimum|MAXimum 
[:SOURce<n>]:MOD:ASKey:AMPLitude? [MINimum|MAXimum
[:SOURce<n>]:MOD:ASKey:INTernal[:RATE] <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:ASKey:INTernal[:RATE]? [MINimum|MAXimum
[:SOURce<n>]:MOD:ASKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:ASKey:SOURce? 

[:SOURce<n>]:MOD:ASKey:POLarity POSitive|NEGative 
[:SOURce<n>]:MOD:ASKey:POLarity?

[:SOURce<n>]:MOD:FSKey[:FREQuency] <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:FSKey[:FREQuency]? [MINimum|MAXimum
[:SOURce<n>]:MOD:FSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:FSKey:INTernal:RATE? [MINimum|MAXimum
[:SOURce<n>]:MOD:FSKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:FSKey:SOURce? 

[:SOURce<n>]:MOD:FSKey:POLarity POSitive|NEGative 
[:SOURce<n>]:MOD:FSKey:POLarity?

[:SOURce<n>]:MOD:PSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PSKey:INTernal:RATE? [MINimum|MAXimum
[:SOURce<n>]:MOD:PSKey:PHASe <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PSKey:PHASe? [MINimum|MAXimum
[:SOURce<n>]:MOD:PSKey:POLarity POSitive|NEGative 
[:SOURce<n>]:MOD:PSKey:POLarity?

[:SOURce<n>]:MOD:PSKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:PSKey:SOURce?

[:SOURce<n>]:MOD:BPSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:BPSKey:INTernal:RATE? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:BPSKey:PHASe <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:BPSKey:PHASe? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:BPSKey:DATA 01|10|PN15|PN21 
[:SOURce<n>]:MOD:BPSKey:DATA?

[:SOURce<n>]:MOD:QPSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:INTernal:RATE? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:QPSKey:PHASe1 <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:PHASe1? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:QPSKey:PHASe2 <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:PHASe2? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:QPSKey:PHASe3 <phase>|MINimum|MAXimum 
[:SOURce<n>]:MOD:QPSKey:PHASe3? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:QPSKey:DATA PN15|PN21 
[:SOURce<n>]:MOD:QPSKey:DATA?

[:SOURce<n>]:MOD:3FSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:3FSKey:INTernal:RATE? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:3FSKey[:FREQuency] <n>,<frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:3FSKey[:FREQuency]? <n>[,MINimum|MAXimum
[:SOURce<n>]:MOD:4FSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:4FSKey:INTernal:RATE? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:4FSKey[:FREQuency] <n>,<frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:4FSKey[:FREQuency]? <n>[,MINimum|MAXimum
[:SOURce<n>]:MOD:OSKey:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:OSKey:SOURce? 
[:SOURce<n>]:MOD:OSKey:INTernal:RATE <rate>|MINimum|MAXimum 
[:SOURce<n>]:MOD:OSKey:INTernal:RATE? [MINimum|MAXimum] 
[:SOURce<n>]:MOD:OSKey:TIME <time>|MINimum|MAXimum 
[:SOURce<n>]:MOD:OSKey:TIME? [MINimum|MAXimum
[:SOURce<n>]:MOD:PWM:INTernal:FREQuency <frequency>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PWM:INTernal:FREQuency? [MINimum|MAXimum
[:SOURce<n>]:MOD:PWM:INTernal:FUNCtion SINusoid|SQUare|TRIangle|RAMP|NRAMp|NOISe|USER

[:SOURce<n>]:MOD:PWM:INTernal:FUNCtion?

[:SOURce<n>]:MOD:PWM:SOURce INTernal|EXTernal 
[:SOURce<n>]:MOD:PWM:SOURce?

[:SOURce<n>]:MOD:PWM[:DEViation]:DCYCle <percent>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PWM[:DEViation]:DCYCle? [MINimum|MAXimum
[:SOURce<n>]:MOD:PWM[:DEViation][:WIDTh] <deviation>|MINimum|MAXimum 
[:SOURce<n>]:MOD:PWM[:DEViation][:WIDTh]? [MINimum|MAXimum
[:SOURce<n>]:PERiod[:FIXed] <period>
[:SOURce<n>]:PERiod[:FIXed]?

[:SOURce<n>]:PHASe[:ADJust] <phase>|MINimum|MAXimum 
[:SOURce<n>]:PHASe[:ADJust]? [MINimum|MAXimum
[:SOURce<n>]:PHASE:INITiate

[:SOURce<n>]:PULSe:DCYCle <percent>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:DCYCle? [MINimum|MAXimum
[:SOURce<n>]:PULSe:DELay <delay>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:DELay? [MINimum|MAXimum
[:SOURce<n>]:PULSe:HOLD WIDTh|DUTY 
[:SOURce<n>]:PULSe:HOLD?

[:SOURce<n>]:PULSe:TRANsition[:LEADing] <seconds>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:TRANsition[:LEADing]? [MINimum|MAXimum
[:SOURce<n>]:PULSe:TRANsition:TRAiling <seconds>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:TRANsition:TRAiling? [MINimum|MAXimum
[:SOURce<n>]:PULSe:WIDTh <seconds>|MINimum|MAXimum 
[:SOURce<n>]:PULSe:WIDTh? [MINimum|MAXimum
[:SOURce<n>]:SWEep:HTIMe:STARt <seconds>|MINimum|MAXimum 
[:SOURce<n>]:SWEep:HTIMe:STARt? [MINimum|MAXimum
[:SOURce<n>]:SWEep:HTIMe:STOP <seconds>|MINimum|MAXimum 
[:SOURce<n>]:SWEep:HTIMe:STOP? [MINimum|MAXimum
[:SOURce<n>]:SWEep:RTIMe <seconds>|MINimum|MAXimum 
[:SOURce<n>]:SWEep:RTIMe? [MINimum|MAXimum
[:SOURce<n>]:SWEep:SPACing LINear|LOGarithmic|STEp 
[:SOURce<n>]:SWEep:SPACing?

[:SOURce<n>]:SWEep:STATe ON|OFF 
[:SOURce<n>]:SWEep:STATe?

[:SOURce<n>]:SWEep:STEP <steps>|MINimum|MAXimum

[:SOURce<n>]:SWEep:STEP? [MINimum|MAXimum
[:SOURce<n>]:SWEep:TIME <seconds>|MINimum|MAXimum 
[:SOURce<n>]:SWEep:TIME? [MINimum|MAXimum
[:SOURce<n>]:SWEep:TRIGger[:IMMediate
[:SOURce<n>]:SWEep:TRIGger:SLOPe POSitive|NEGative 
[:SOURce<n>]:SWEep:TRIGger:SLOPe?

[:SOURce<n>]:SWEep:TRIGger:SOURce INTernal|EXTernal|MANual 
[:SOURce<n>]:SWEep:TRIGger:SOURce?

[:SOURce<n>]:SWEep:TRIGger:TRIGOut OFF|POSitive|NEGative 
[:SOURce<n>]:SWEep:TRIGger:TRIGOut?

[:SOURce<n>]:VOLTage[:LEVel][:IMMediate][:AMPLitude] <amplitude>|MINimum|MAXimum 
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate][:AMPLitude]? [MINimum|MAXimum
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:HIGH <voltage>|MINimum|MAXimum 
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:HIGH? [MINimum|MAXimum
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:LOW <voltage>|MINimum|MAXimum 
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:LOW? [MINimum|MAXimum
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:OFFSet <voltage>|MINimum|MAXimum 
[:SOURce<n>]:VOLTage[:LEVel][:IMMediate]:OFFSet? [MINimum|MAXimum
[:SOURce<n>]:VOLTage:UNIT VPP|VRMS|DBM 
[:SOURce<n>]:VOLTage:UNIT?   

```
:SYSTem:BEEPer[:IMMediate
:SYSTem:BEEPer:STATe ON|OFF
:SYSTem:BEEPer:STATe?
```

```
:SYSTem:COMMunicate:LAN:AUTOip[:STATe] ON|OFF
:SYSTem:COMMunicate:LAN:AUTOip[:STATe]?
```

```
:SYSTem:COMMunicate:LAN:DHCP[:STATe] ON|OFF
:SYSTem:COMMunicate:LAN:DHCP[:STATe]?
```

```
:SYSTem:COMMunicate:LAN:DNS <address>
:SYSTem:COMMunicate:LAN:DNS?
```

```
:SYSTem:COMMunicate:LAN:GATEway <address>
:SYSTem:COMMunicate:LAN:GATEway?
```

```
:SYSTem:COMMunicate:LAN:IPADdress <ip_addr>
:SYSTem:COMMunicate:LAN:IPADdress?
```

```
:SYSTem:COMMunicate:LAN:MAC?
```

```
:SYSTem:COMMunicate:LAN:SMASk <mask>
:SYSTem:COMMunicate:LAN:SMASk?
```

```
:SYSTem:COMMunicate:LAN:STATic[:STATe] ON|OFF
:SYSTem:COMMunicate:LAN:STATic[:STATe]?
```

```
:SYSTem:COMMunicate:USB:INFormation?
```

```
:SYSTem:COMMunicate:USB[:SELF]:CLASs COMPuter|PRINter
:SYSTem:COMMunicate:USB[:SELF]:CLASs?
```

```
:SYSTem:CSCopy CH1|CH2,CH2|CH1
```

```
:SYSTem:CWCopy CH1|CH2,CH2|CH1
```

```
:SYSTem:ERRor?
```

```
:SYSTem:KLOCk[:STATe] ON|OFF
:SYSTem:KLOCk[:STATe]?
```

```
:SYSTem:LANGuage ENGLish|SCHinese
:SYSTem:LANGuage?
```

```
:SYSTem:POWeron DEFault|LAST
:SYSTem:POWeron?
```

```
:SYSTem:POWSet AUTO|USER
:SYSTem:POWSet?
```

```
:SYSTem:PRESet DEFault|USER1|USER2|USER3|USER4|USER5|USER6|USER7|USER8|USER9|USER10
```

```
:SYSTem:RESTART
```

```
:SYSTem:ROSCillator:SOURce INTernal|EXTernal
:SYSTem:ROSCillator:SOURce?
```

```
:SYSTem:SHUTDOWN
```

```
:SYSTem:VERSion?
```


**T**

[:TRACe]:DATA:DAC16 VOLATILE,<flag>,<binary_block_data>

[:TRACe]:DATA:DAC VOLATILE,[<binary_block_data>|<value>,<value>,<value>...
[:TRACe]:DATA[:DATA] VOLATILE,<value>{,<value>} 

[:TRACe]:DATA:POINts:INTerpolate LINear|OFF 
[:TRACe]:DATA:POINts:INTerpolate?

[:TRACe]:DATA:POINts VOLATILE,<value>|MINimum|MAXimum

[:TRACe]:DATA:POINts? VOLATILE[,MINimum|MAXimum
[:TRACe]:DATA:VALue? VOLATILE,<point>

[:TRACe]:DATA:VALue VOLATILE,<point>,<data>

[:TRACe]:DATA:LOAD? VOLATILE

[:TRACe]:DATA:LOAD? <num>
