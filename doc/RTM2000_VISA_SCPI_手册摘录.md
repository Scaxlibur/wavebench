# R&S RTM2000 VISA/SCPI Remote Control Guide


> 由 `RTM2_UserManual_en_10.html` 及其 `part*.htm` 碎片自动清洗合并。

> 原始内容来自 R&S RTM2000 User Manual 的远程命令/VISA 相关章节。


## 说明


- 已移除 HTML 导航、页内目录、样式和图片分隔线。

- SCPI 示例、仪器响应和代码片段尽量保留为 `text` 代码块。

- 由于源文件来自 PDF 转 HTML，个别换行、连字符和表格仍可能需要人工复核。


<!-- 来源：RTM2_UserManual_en_10_files\part1.htm -->

### 18 Remote Commands Reference

18 Remote Commands Reference

This chapter provides the description of all remote commands available for R&S RTM. The commands are sorted according to the menu structure of the instrument. A list of commands in alphabetical order ist given in the "List of Commands" at the end of this documentation.

- Conventions used in Command Description 404

- Programming Examples 405

- Common Commands 409

- Acquisition and Setup 413

- Trigger 447

- Display 462

- Reference Waveforms 470

- Measurements 475

- Mathematics 497

- Spectrum Analysis 500

- Masks 524

- Search 530

- Protocol Analysis 547

- Power Analysis (Option R&S RTM-K31) 665

- Mixed Signal Option (MSO, R&S RTM-B1) 717

- Digital Voltmeter and Counter (Option R&S RTM-K32) 727

- Data and File Management 730

- General Instrument Setup 755

- Status Reporting 759

<!-- 来源：RTM2_UserManual_en_10_files\part2.htm -->

## 18.1 Conventions used in Command Description

Note the following conventions used in the remote command descriptions:

<!-- 来源：RTM2_UserManual_en_10_files\part3.htm -->

### ● Command usage

- Command usage

If not specified otherwise, commands can be used both for setting and for querying parameters.

If a command can be used for setting or querying only, or if it initiates an event, the usage is stated explicitly.

<!-- 来源：RTM2_UserManual_en_10_files\part4.htm -->

### ● Parameter usage

- Parameter usage

If not specified otherwise, a parameter can be used to set a value and it is the result of a query.

Parameters required only for setting are indicated as Setting parameters. Parameters required only to refine a query are indicated as Query parameters. Parameters that are only returned as the result of a query are indicated as Return values.

<!-- 来源：RTM2_UserManual_en_10_files\part5.htm -->

### ● Conformity

- Conformity

Commands that are taken from the SCPI standard are indicated as SCPI con- firmed. All commands used by the R&S RTM follow the SCPI syntax rules.

<!-- 来源：RTM2_UserManual_en_10_files\part6.htm -->

### ● Asynchronous commands

- Asynchronous commands

A command which does not automatically finish executing before the next com- mand starts executing (overlapping command) is indicated as an Asynchronous command.

<!-- 来源：RTM2_UserManual_en_10_files\part7.htm -->

### ● Reset values (*RST)

- Reset values (*RST)

Default parameter values that are used directly after resetting the instrument ( *RST command) are indicated as *RST values, if available.

<!-- 来源：RTM2_UserManual_en_10_files\part8.htm -->

### ● Default unit

- Default unit

This is the unit used for numeric values if no other unit is provided with the parame- ter.

<!-- 来源：RTM2_UserManual_en_10_files\part9.htm -->

## 18.2 Programming Examples

- Data Export 405

- Search 407

- Data and File Management 408

<!-- 来源：RTM2_UserManual_en_10_files\part10.htm -->

### 18.2.1 Data Export

- Reading Waveform Data in Real Format 405

- Reading Waveform Data in Unsigned Integer Format 406

### 18.2.1.1 Reading Waveform Data in Real Format

Set data format and sample range, read channel header and data.

Command description in Chapter 18. 17.1, "Waveform Data Transfer", on page 730.

```text
* Connected to: TCPIP0::192.168.1.1::inst0::INSTR SYST:ERR?
<-- 0,"No error"
*IDN?
<-- Rohde&Schwarz,RTM1052,1305.0008K52/101489,04.502
*RST
CHAN:TYPE HRES // Set high resolution mode (16 bit data) ACQ:WRAT MSAM // Set maximum waveform rate
TIM:SCAL 1E-7 // Set time base
FORM REAL // Set REAL data format
FORM:BORD LSBF // Set little endian byte order
CHAN:DATA:POIN DMAX // Set sample range to memory data in displayed time range SING;*OPC? // Start single acquisition
<-- 1
CHAN:DATA:HEAD? // Read header
<-- -4.9980E-07,5.0000E-07,5000,1 // Xstart, Xstop, record length in samples CHAN:DATA? // Read channel data
<-- #520000>??[>??[>??[>??[>??[>??... // Binary block data,
// 4-byte floating point number/sample
```

### 18.2.1.2 Reading Waveform Data in Unsigned Integer Format

Read the channel header, the waveform conversion data, set the UINT binary data for- mat and read the channel data.

Command description in: Chapter 18.17.1, "Waveform Data Transfer", on page 730.

```text
*RST
TIM:SCAL 1E-7
CHAN:DATA:POIN DMAX // Set data range SING;*OPC?
<-- 1
CHAN:DATA:HEAD? // Read header
<-- -4.9980E-07,5.0000E-07,5000,1 // Xstart, Xstop, record length in samples CHAN:DATA:YRES? // Read vertical resolution
<-- 8
CHAN:DATA:YOR? // Read voltage value for binary value 0
<-- -2.549999943E-2
CHAN:DATA:XOR? // Read time of the first sample
<-- -4.998000058E-7
CHAN:DATA:XINC? // Read time between two adjacent samples
<-- 2.000000023E-10
FORM UINT,8;FORM? // Set data format to unsigned integer, 8 bit
<-- UINT,8
CHAN:DATA:YINC? // Read voltage value per bit
<-- 1.999999949E-4
CHAN:DATA? // Read channel data
<-- 128,125,120... // 5000 bytes total
FORM UINT,16;FORM? // Change data format to unsigned integer, 16 bit
<-- UINT,16
CHAN:DATA:YINC? // Read voltage value per bit
<-- 7.812499803E-7
CHAN:DATA? // Read channel data
<-- 32768,32000,30720... // 10000 bytes total
```

Note the following correlations:

- The number of received data values matches the number of samples indicated in the header.

- The time of the first sample (XORigin) matches the start time Xstart indicated in the header.

- The Y-increment adjusts to the data length defined in the data format (8 or 16 bit).

<!-- 来源：RTM2_UserManual_en_10_files\part11.htm -->

### Data conversion

Definition: the sample numbers start with 0 and end with record length - 1.

<!-- 来源：RTM2_UserManual_en_10_files\part12.htm -->

### Sample time

t n = n * xIncrement + xOrigin

First sample: t 0 = -4.998000058E-7 (= Xstart)

Last sample: t 4999 = 4999 * 2E −10 − 4.998E −7 = 5.0 E −7 (= Xstop)

<!-- 来源：RTM2_UserManual_en_10_files\part13.htm -->

### Sample value

Y n = yOrigin + (yIncrement * byteValue n )

The format UINT,8 has the data range 0 to 255. The voltage value for byte value 128 is:

Y n = −2.55E -2 + (2E −4 * 128) = 0.0001

The center of the display at position 0 div always has the byte value 127.5. The corre- sponding voltage value is:

Y n = −2.55E -2 + (2E −4 * 127.5) = 0

<!-- 来源：RTM2_UserManual_en_10_files\part14.htm -->

### 8-bit and 16-bit data

At the end of the above example, the 8-bit waveform is read as 16-bit data, for exam- ple, 0xFF is read 0xFF00, or 0x1A is read 0x1A00. The yOrigin value is the same in both cases, but the yIncrement differs.

|  | 8-bit data | 16-bit data | Result |
| --- | --- | --- | --- |
| yIncrement * byteValue n | 2e -4 * 128 | 7,8125E -7 * 32768 | 0,0256 V |
| 2e -4 * 125 | 7,8125E -7 * 32000 | 0,025 V |  |

In the reverse case, if a 16-bit waveform is read with 8-bit data format, data precision may be reduced. Data values ar truncated, and only the more significiant bits remain. For example, the 16-bit data 0xabcd is read 0xab in 8-bit format, and cd is lost.

<!-- 来源：RTM2_UserManual_en_10_files\part15.htm -->

### 18.2.2 Search

### 18.2.2.1 Searching for a Pulse of Specified Width

Search for positive pulses with pulse width 12 ± 10 µs (2 µs to 22 µs). Command description in: Chapter 18.12, "Search", on page 530.

```text
SEAR:STAT ON // Turn on search
SEAR:COND WIDTH // Select search condition
SEAR:SOUR CH2 // Configure search source SEAR:TRIG:WIDT:POL POS // Configure search parameters: Polarity
SEAR:TRIG:WIDT:RANG WITH // Configure search parameters: Condition = within SEAR:TRIG:WIDT:WIDT 12e-6 // Configure search parameters: Pulse width SEAR:TRIG:WIDT:DELT 10e-6 // Configure search parameters: +/- delta
SEAR:RESD:SHOW ON // Show result table
SEAR:RCO? // Get number of search events found
<-- 1.400E+01
SEAR:RES:ALL? // Get all search results
<-- 1,5.201200e-06,0,WIDTH,POSITIVE,1.220160e-05,2,4.120040e-05,0,WIDTH, POSITIVE,3.076800e-06,3,4.732480e-05,0,WIDTH,POSITIVE,9.127200e-06,4, 6.499960e-05,0,WIDTH,POSITIVE,1.835160e-05,5,8.634920e-05,0,WIDTH,POSITIVE,
3.052000e-06,6,1.293984e-04,0,WIDTH,POSITIVE,9.176800e-06,7,1.477228e-04,0, WIDTH,POSITIVE,3.052000e-06,8,1.623224e-04,0,WIDTH,POSITIVE,3.102000e-06,9, 1.684724e-04,0,WIDTH,POSITIVE,1.215160e-05,10,1.953216e-04,0,WIDTH,POSITIVE,
3.027200e-06,11,2.044716e-04,0,WIDTH,POSITIVE,6.052000e-06,12,2.252212e-04,0, WIDTH,POSITIVE,3.052000e-06,13,2.435456e-04,0,WIDTH,POSITIVE,3.027200e-06,14, 2.496456e-04,0,WIDTH,POSITIVE,6.702000e-06
```

<!-- 来源：RTM2_UserManual_en_10_files\part16.htm -->

### 18.2.3 Data and File Management

- Saving Screenshots to File 408

- Saving, Copying, and Loading Setup Data 408

### 18.2.3.1 Saving Screenshots to File

Save two display images in png format to the PIX folder on a USB flash drive that is connected to the front panel. One screenshot is colored and the other is grayscaled. Finally, the data of the gray screenshot is read for further user on the control computer.

Command description in: Chapter 18. 17.4, "Screenshots", on page 751.

```text
*RST
MMEM:CDIR "/USB_FRONT" MMEM:MDIR "/USB_FRONT/PIX" MMEM:CDIR "/USB_FRONT/PIX/"
HCOP:DEST "MMEM" HCOP:LANG PNG HCOP:COL:SCH COL MMEM:NAME "COLORED" HCOP:IMM HCOP:COL:SCH GRAY MMEM:NAME "GRAY" HCOP:IMM
MMEM:CAT? "*.PNG" MMEM:DATA? "GRAY.PNG"
```

### 18.2.3.2 Saving, Copying, and Loading Setup Data

Save instrument settings to a file on internal storage device, duplicate this file and save it to a USB stick attached to the front panel. Finally, there are three setup files on the internal storage /INT/SETTINGS, and one file on the USB flash device.

Command description in: Chapter 18.17.3, "Instrument Settings", on page 745.

```text
CHAN1:STAT ON // Turn channel 1 on
CHAN2:STAT ON // Turn channel 2 on
TIM:ZOOM:STAT ON // Show zoom diagram
MMEM:CDIR "/INT/SETTINGS" // Set storage device and directory MMEM:STOR:STAT 1,"ZOOM_A.SET" // Save settings to internal storage MMEM:CAT? "*.SET" // Check
<-- 332112,8633856,"ZOOM_A.SET,,2759"
MMEM:COPY "ZOOM_A.SET","ZOOM_B.SET" // Copy file
MMEM:CAT? "*.SET" // Check
<-- 332112,8633856,"ZOOM_A.SET,,2759","ZOOM_B.SET,,2759" MMEM:COPY "/INT/SETTINGS/ZOOM_B.SET","/USB_FRONT/ZOOM_B.SET"
// Save copied file to USB stick
MMEM:CDIR "/USB_FRONT" // Check MMEM:CAT? "*.SET"
<-- 4890624,-641765376,"ZOOM_B.SET,,2759"
MMEM:COPY "/USB_FRONT/ZOOM_B.SET","/USB_FRONT/ZOOM_USB.SET"
// Duplicate file on USB stick
MMEM:CAT? "*.SET" // Check
<-- 4890624,-641765376,"ZOOM_B.SET,,2759","ZOOM_USB.SET,,2759"
MMEM:DEL "ZOOM_B.SET" // Delete original file
MMEM:CAT? "*.SET" // Check
<-- 4886528,-641765376,"ZOOM_USB.SET,,2759" MMEM:COPY "/USB_FRONT/ZOOM_USB.SET","/INT/SETTINGS/"
// Copy new file to the instrument
MMEM:CDIR "/INT/SETTINGS" // Check MMEM:CAT? "*.SET"
<-- 332112,8633856,"ZOOM_A.SET,,2759","ZOOM_B.SET,,2759","ZOOM_USB.SET,,2759"
*RST;*OPC?
<-- 1
MMEM:CDIR "/INT/SETTINGS"
MMEM:LOAD:STAT 1,"ZOOM_USB.SET" // Load settings
```

<!-- 来源：RTM2_UserManual_en_10_files\part17.htm -->

## 18.3 Common Commands

Common commands are described in the IEEE 488.2 (IEC 625-2) standard. These commands have the same effect and are employed in the same way on different devi- ces. The headers of these commands consist of "*" followed by three letters. Many common commands are related to the Status Reporting System.

Available common commands:

*CAL? 410

*CLS 410

*ESE 410

*ESR? 410

*IDN? 410

*OPC 411

*OPT? 411

*PSC 411

*RST 412

*SRE 412

*STB? 412

*TRG 412

*TST? 412

*WAI 413

<!-- 来源：RTM2_UserManual_en_10_files\part18.htm -->

### *CAL?

Performs a self-alignment of the instrument and then generates a status response. Return values ≠ 0 indicate an error.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part19.htm -->

### *CLS

Clear status

Sets the status byte (STB), the standard event register (ESR) and the EVENt part of the QUEStionable and the OPERation registers to zero. The command does not alter the mask and transition parts of the registers. It clears the output buffer.

### Usage: Setting only

### *ESE <Value> Event status enable

Sets the event status enable register to the specified value. The query returns the con- tents of the event status enable register in decimal form.

<!-- 来源：RTM2_UserManual_en_10_files\part20.htm -->

### Parameters:

<Value> Range: 0 to 255

<!-- 来源：RTM2_UserManual_en_10_files\part21.htm -->

### *ESR?

Event status read

Returns the contents of the event status register in decimal form and subsequently sets the register to zero.

<!-- 来源：RTM2_UserManual_en_10_files\part22.htm -->

### Return values:

<Contents> Range: 0 to 255

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part23.htm -->

### *IDN?

Identification

Returns the instrument identification.

<!-- 来源：RTM2_UserManual_en_10_files\part24.htm -->

### Return values:

<ID> "Rohde&Schwarz,<device type>,<serial number>,<firmware ver- sion>"

<ID> "Rohde&Schwarz,<device type>,<part number>/serial num- ber>,<firmware version>"

### Example: Rohde&Schwarz,RTM,1316.1000k14/200153,1.30.0.25

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part25.htm -->

### *OPC

Operation complete

Sets bit 0 in the event status register when all preceding commands have been execu- ted. This bit can be used to initiate a service request. The query form writes a "1" into the output buffer as soon as all preceding commands have been executed. This is used for command synchronization.

<!-- 来源：RTM2_UserManual_en_10_files\part26.htm -->

### *OPT?

Option identification query

Queries the options included in the instrument. For a list of all available options and their description refer to the data sheet.

<!-- 来源：RTM2_UserManual_en_10_files\part27.htm -->

### Return values:

<Options> The query returns a list of options. The options are returned at fixed positions in a comma-separated string. A zero is returned for options that are not installed.

### Usage: Query only

### *PSC <Action> Power on status clear

Determines whether the contents of the ENABle registers are preserved or reset when the instrument is switched on. Thus a service request can be triggered when the instru- ment is switched on, if the status registers ESE and SRE are suitably configured. The query reads out the contents of the "power-on-status-clear" flag.

<!-- 来源：RTM2_UserManual_en_10_files\part28.htm -->

### Parameters:

<Action> 0 | 1

<!-- 来源：RTM2_UserManual_en_10_files\part29.htm -->

### 0

The contents of the status registers are preserved.

<!-- 来源：RTM2_UserManual_en_10_files\part30.htm -->

### 1

Resets the status registers.

<!-- 来源：RTM2_UserManual_en_10_files\part31.htm -->

### *RST

Reset

Sets the instrument to a defined default status. The default settings are indicated in the description of commands.

### Usage: Setting only

### *SRE <Contents> Service request enable

Sets the service request enable register to the indicated value. This command deter- mines under which conditions a service request is triggered.

<!-- 来源：RTM2_UserManual_en_10_files\part32.htm -->

### Parameters:

<Contents> Contents of the service request enable register in decimal form.

Bit 6 (MSS mask bit) is always 0. Range: 0 to 255

<!-- 来源：RTM2_UserManual_en_10_files\part33.htm -->

### *STB?

Status byte query

Reads the contents of the status byte in decimal form.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part34.htm -->

### *TRG

Trigger

Triggers all actions waiting for a trigger event. In particular, *TRG generates a manual trigger signal. This common command complements the commands of the TRIGger subsystem.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part35.htm -->

### *TST?

Self-test query

Initiates self-tests of the instrument and returns an error code

<!-- 来源：RTM2_UserManual_en_10_files\part36.htm -->

### Return values:

<ErrorCode> integer > 0 (in decimal format)

An error occurred.

(For details see the Service Manual supplied with the instru- ment).

<!-- 来源：RTM2_UserManual_en_10_files\part37.htm -->

### 0

No errors occurred.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part38.htm -->

### *WAI

Wait to continue

Prevents servicing of the subsequent commands until all preceding commands have been executed and all signals have settled (see also command synchronization and

```text
*OPC ).
```

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part39.htm -->

## 18.4 Acquisition and Setup

- Starting and Stopping Acquisition 413

- Time Base 414

- Acquisition 416

- Vertical 421

- Waveform Data 427

- Probes 431

- History and Segmented Memory (Option R&S RTM-K15) 437

- History Viewer 438

- Timestamps 442

- Export 445

<!-- 来源：RTM2_UserManual_en_10_files\part40.htm -->

### 18.4.1 Starting and Stopping Acquisition

RUN 413

RUNContinous 413

SINGle 414

RUNSingle 414

ACQuire:NSINgle:COUNt 414

STOP 414

<!-- 来源：RTM2_UserManual_en_10_files\part41.htm -->

### RUN

Starts the continuous acquisition.

### Usage: Event

Asynchronous command

<!-- 来源：RTM2_UserManual_en_10_files\part42.htm -->

### RUNContinous

Same as RUN.

### Usage: Event

Asynchronous command

<!-- 来源：RTM2_UserManual_en_10_files\part43.htm -->

### SINGle

Starts a defined number of acquisitions. The number of acquisitions is set with

```text
ACQuire:NSINgle:COUNt.
```

### Usage: Event

Asynchronous command

<!-- 来源：RTM2_UserManual_en_10_files\part44.htm -->

### RUNSingle

Same as SINGle.

### Usage: Event

Asynchronous command

### ACQuire:NSINgle:COUNt <NSingleCount>

```text
Sets the number of waveforms acquired with RUNSingle.
```

<!-- 来源：RTM2_UserManual_en_10_files\part45.htm -->

### Parameters:

<NSingleCount> Number of waveforms

*RST: 1

<!-- 来源：RTM2_UserManual_en_10_files\part46.htm -->

### STOP

Stops the running acquistion.

### Usage: Event

Asynchronous command

<!-- 来源：RTM2_UserManual_en_10_files\part47.htm -->

### 18.4.2 Time Base

TIMebase:SCALe 414

TIMebase:RATime? 415

TIMebase:ACQTime 415

TIMebase:RANGe 415

TIMebase:DIVisions? 415

TIMebase:POSition 416

TIMebase:REFerence 416

### TIMebase:SCALe <TimeScale>

Sets the horizontal scale for all channel and math waveforms.

<!-- 来源：RTM2_UserManual_en_10_files\part48.htm -->

### Parameters:

<TimeScale> Range: 1e-9 to 50; lower limits are possible if zoom or

FFT is enabled.

Increment: 1, 2, 5 progression, for example, 1 ms/div, 2 ms/div,

5 ms/div, 10, 20, 50...

*RST: 100e-6

Default unit: s/DIV

<!-- 来源：RTM2_UserManual_en_10_files\part49.htm -->

### TIMebase:RATime?

```text
Queries the real acquisition time used in the hardware. If FFT analysis is performed, the value can differ from the adjusted acquisition time ( TIMebase:ACQTime ).
```

<!-- 来源：RTM2_UserManual_en_10_files\part50.htm -->

### Return values:

<HWAcqTime> Range: Depends on various settings

Default unit: s

### Usage: Query only

### TIMebase:ACQTime <AcquisitionTime>

Defines the time of one acquisition, that is the time across the 10 divisions of the dia- gram: Timebase Scale*10.

<!-- 来源：RTM2_UserManual_en_10_files\part51.htm -->

### Parameters:

<AcquisitionTime> *RST: 1e-3

Default unit: s

### TIMebase:RANGe <AcquisitionTime>

Defines the time of one acquisition, that is the time across the 10 divisions of the dia- gram: Timebase Scale*10.

<!-- 来源：RTM2_UserManual_en_10_files\part52.htm -->

### Parameters:

<AcquisitionTime> Range and increment depend on time base and other settings

*RST: 1e-3

Default unit: s

<!-- 来源：RTM2_UserManual_en_10_files\part53.htm -->

### TIMebase:DIVisions?

Queries the number of horizontal divisions on the screen.

<!-- 来源：RTM2_UserManual_en_10_files\part54.htm -->

### Return values:

<HorizDivCount> Range: 10 to 10

Increment: 0

*RST: 10

Default unit: DIV

### Usage: Query only

### TIMebase:POSition <Offset>

Defines the trigger position (trigger offset) - the time interval between trigger point and reference point to analize the signal some time before or after the trigger event.

See also: TIMebase:REFerence on page 416

<!-- 来源：RTM2_UserManual_en_10_files\part55.htm -->

### Parameters:

<Offset> Range: Depends on time base setting

*RST: 0

Default unit: s

### TIMebase:REFerence <ReferencePoint>

Sets the reference point of the time scale (Time Reference) in % of the display. The reference point defines which part of the waveform is shown. If the trigger position is zero, the trigger point matches the reference point.

See also: TIMebase:POSition on page 416

<!-- 来源：RTM2_UserManual_en_10_files\part56.htm -->

### Parameters:

<ReferencePoint> Range: 10 to 90

Increment: 10

*RST: 50

Default unit: %

<!-- 来源：RTM2_UserManual_en_10_files\part57.htm -->

### 18.4.3 Acquisition

AUToscale 416

ACQuire:MODE 417

ACQuire:INTerpolate 417

ACQuire:AVERage:COUNt 417

ACQuire:AVERage:COMPlete? 417

ACQuire:WRATe 418

ACQuire:POINts[:VALue] 418

CHANnel<m>:TYPE 419

CHANnel<m>:ARIThmetics 419

TIMebase:ROLL:ENABle 420

ACQuire:FILTer:FREQuency 420

ACQuire:POINts:ARATe? 420

ACQuire:SRATe? 421

<!-- 来源：RTM2_UserManual_en_10_files\part58.htm -->

### AUToscale

Performs an autoset process: analyzes the enabled channel signals, and obtains appropriate horizontal, vertical, and trigger settings to display stable waveforms.

### Usage: Event

Asynchronous command

### ACQuire:MODE <AcquisitionMode>

Selects the method of adding waveform points to the samples of the ADC in order to fill the record length.

<!-- 来源：RTM2_UserManual_en_10_files\part59.htm -->

### Parameters:

<AcquisitionMode> RTIMe | ETIMe

<!-- 来源：RTM2_UserManual_en_10_files\part60.htm -->

### RTIMe

Real Time Mode: At slow time base settings the sampled points of the input signal are used to build the waveform, no waveform points are added. With fast time base settings, the sample rate is higher than the ADC sample rate. Waveform samples are added to the ADC samples with sin(x)/x interpolation.

<!-- 来源：RTM2_UserManual_en_10_files\part61.htm -->

### ETIMe

Equivalent time: The waveform points are taken from several acquisitions of a repetive signal at a different time in relation to the trigger point.

*RST: RTIME

### ACQuire:INTerpolate <Interpolation> Defines the interpolation mode.

See also: "Interpolation" on page 32

<!-- 来源：RTM2_UserManual_en_10_files\part62.htm -->

### Parameters:

<Interpolation> SINX

<!-- 来源：RTM2_UserManual_en_10_files\part63.htm -->

### LINear

Linear interpolation between two adjacent sample points.

<!-- 来源：RTM2_UserManual_en_10_files\part64.htm -->

### SINX

Interpolation by means of a sin(x)/x curve.

<!-- 来源：RTM2_UserManual_en_10_files\part65.htm -->

### SMHD

Sample & Hold causes a histogram-like interpolation.

*RST: SINX

### ACQuire:AVERage:COUNt <AverageCount>

Defines the number of waveforms used to calculate the average waveform. The higher the number, the better the noise is reduced.

<!-- 来源：RTM2_UserManual_en_10_files\part66.htm -->

### Parameters:

<AverageCount> Only numbers from the 2 n progression are permitted (2, 4, 8,...)

Range: 2 to 1024

*RST: 2

<!-- 来源：RTM2_UserManual_en_10_files\part67.htm -->

### ACQuire:AVERage:COMPlete?

Returns the state of averaging.

<!-- 来源：RTM2_UserManual_en_10_files\part68.htm -->

### Return values:

<AverageComplete> 0 | 1

<!-- 来源：RTM2_UserManual_en_10_files\part69.htm -->

### 0

```text
The number of acquired waveforms is less than the number required for average calculation. See ACQuire:AVERage: COUNt.
```

<!-- 来源：RTM2_UserManual_en_10_files\part70.htm -->

### 1

The instrument acquired a sufficient number of waveforms to determine the average.

### Usage: Query only

### ACQuire:WRATe <WaveformRate>

Defines the mode to set the sample rate (samples per second saved in the memory) and the waveform acquisition rate (waveforms per second).

<!-- 来源：RTM2_UserManual_en_10_files\part71.htm -->

### Parameters:

<WaveformRate> AUTO | MWAVeform | MSAMples | MANual

<!-- 来源：RTM2_UserManual_en_10_files\part72.htm -->

### AUTO

To display the best waveform, the instrument selects the opti- mum combination of waveform acquisition rate and sample rate using the full memory depth (maximum record length).

<!-- 来源：RTM2_UserManual_en_10_files\part73.htm -->

### MWAVeform

Maximum waveform rate: The instrument combines sample rate and memory depth to acquire at maximum waveform acquisition rate. In connection with persistence, the mode can display rare signal anomalies.

<!-- 来源：RTM2_UserManual_en_10_files\part74.htm -->

### MSAMples

Maximum sample rate: The instrument acquires the signal at maximum sample rate and uses the full memory depth. The result is a waveform with maximum number of waveform sam- ples, high degree of accuracy, and low risk of aliasing.

<!-- 来源：RTM2_UserManual_en_10_files\part75.htm -->

### MANual

```text
The instrument acquires the signals at a sample rate that fills up an user-defined record length. Set the record length using ACQuire:POINts[:VALue].
```

MANual is only available if the History option R&S RTM-K15 is installed.

*RST: AUTO

### ACQuire:POINts[:VALue] <RecordLength>

The query returns the record length, the number of recorded waveform points in a seg- ment.

If option R&S RTM-K15 is installed, and ACQuire:WRATe on page 418 is set to MAN- ual, the command can set the record length of a segment.

<!-- 来源：RTM2_UserManual_en_10_files\part76.htm -->

### Parameters:

<RecordLength> Record length in Sa

### CHANnel<m>:TYPE <DecimationMode>

Selects the method to reduce the data stream of the ADC to a stream of waveform points with lower sample rate.

<!-- 来源：RTM2_UserManual_en_10_files\part77.htm -->

### Suffix:

<m> 1..4

The command affects all channels regardless of the indicated channel number. The suffix can be omitted.

<!-- 来源：RTM2_UserManual_en_10_files\part78.htm -->

### Parameters:

<DecimationMode> SAMPle | PDETect | HRESolution

<!-- 来源：RTM2_UserManual_en_10_files\part79.htm -->

### SAMPle

Input data is acquired with a sample rate which is aligned to the time base (horizontal scale) and the record length.

<!-- 来源：RTM2_UserManual_en_10_files\part80.htm -->

### PDETect

Peak Detect: the minimum and the maximum of n samples in a sample interval are recorded as waveform points.

<!-- 来源：RTM2_UserManual_en_10_files\part81.htm -->

### HRESolution

High resolution: The average of n sample points is recorded as waveform point.

*RST: SAMPle

### CHANnel<m>:ARIThmetics <TrArithmetic>

Selects the method to build the resulting waveform from several consecutive acquisi- tions of the signal.

<!-- 来源：RTM2_UserManual_en_10_files\part82.htm -->

### Suffix:

<m> 1..4

The command affects all channels regardless of the indicated channel number. The suffix can be omitted.

<!-- 来源：RTM2_UserManual_en_10_files\part83.htm -->

### Parameters:

<TrArithmetic> OFF | ENVelope | AVERage | SMOoth | FILTer

<!-- 来源：RTM2_UserManual_en_10_files\part84.htm -->

### OFF

The data of the current acquisition is recorded according to the decimation settings.

<!-- 来源：RTM2_UserManual_en_10_files\part85.htm -->

### ENVelope

Detects the minimum and maximum values in an sample interval over a number of acquisitions.

<!-- 来源：RTM2_UserManual_en_10_files\part86.htm -->

### AVERage

```text
Calculates the average from the data of the current acquisition and a number of acquisitions before. The number of used acquisitions is set with ACQuire:AVERage:COUNt.
```

<!-- 来源：RTM2_UserManual_en_10_files\part87.htm -->

### SMOoth

Calculates a mean value of several adjacent sample points. Thus, smoothing is a moving average that uses the full data and can be used for non-periodic signals. It works like a low-pass, and increases the vertical resolution at the expense of band- width reduction.

<!-- 来源：RTM2_UserManual_en_10_files\part88.htm -->

### FILTer

```text
Sets a low-pass filter with 3 db attenuation at a configurable limit frequency set with ACQuire:FILTer:FREQuency. The filter removes higher frequencies from the channel signals.
```

*RST: OFF

### TIMebase:ROLL:ENABle <Roll> Enables the roll mode.

<!-- 来源：RTM2_UserManual_en_10_files\part89.htm -->

### Parameters:

<Roll> ON | OFF

*RST: OFF

### ACQuire:FILTer:FREQuency <FilterFrequency>

Sets the limit frequency for CHANnel<m>:ARIThmetics is set to FILTer.

<!-- 来源：RTM2_UserManual_en_10_files\part90.htm -->

### Parameters:

<FilterFrequency> Limit frequency with 3 dB attenuation Default unit: Hz

<!-- 来源：RTM2_UserManual_en_10_files\part91.htm -->

### ACQuire:POINts:ARATe?

Retrieves the sample rate of the ADC, that is the number of points that are sampled by the ADC in one second.

<!-- 来源：RTM2_UserManual_en_10_files\part92.htm -->

### Return values:

<AcquisitionRate> ADC sample rate

Range: 2.5E3 to 5E9 Increment: 1E3

*RST: 5E9

Default unit: Hz

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part93.htm -->

### ACQuire:SRATe?

Returns the sample rate, that is the number of recorded waveform samples per sec- ond.

<!-- 来源：RTM2_UserManual_en_10_files\part94.htm -->

### Return values:

<SampleRate> Range: 2 to 1E11

Increment: depends on time base, waveform rate, number of active channels

*RST: 1E7

Default unit: Sa/s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part95.htm -->

### 18.4.4 Vertical

CHANnel<m>:STATe 421

CHANnel<m>:AOFF 422

CHANnel<m>:AON 422

CHANnel<m>:COUPling 422

CHANnel<m>:SCALe 423

CHANnel<m>:RANGe 423

CHANnel<m>:POSition 424

CHANnel<m>:OFFSet 424

CHANnel<m>:BANDwidth 424

CHANnel<m>:POLarity 425

CHANnel<m>:OVERload 425

CHANnel<m>:SKEW 426

CHANnel<m>:THReshold 426

CHANnel<m>:THReshold:HYSTeresis 426

CHANnel<m>:LABel 426

CHANnel<m>:LABel:STATe 427

CHANnel<m>:ZOFFset[:VALue] 427

### CHANnel<m>:STATe <State> Switches the channel signal on or off.

<!-- 来源：RTM2_UserManual_en_10_files\part96.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part97.htm -->

### Parameters:

<State> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part98.htm -->

### CHANnel<m>:AOFF

Switches all analog channels off.

<!-- 来源：RTM2_UserManual_en_10_files\part99.htm -->

### Suffix:

<m> The suffix is irrelevant.

### Usage: Event

### Firmware/Software: FW 05.7xx

<!-- 来源：RTM2_UserManual_en_10_files\part100.htm -->

### CHANnel<m>:AON

Switches all analog channels on.

<!-- 来源：RTM2_UserManual_en_10_files\part101.htm -->

### Suffix:

<m> The suffix is irrelevant.

### Usage: Event

### Firmware/Software: FW 05.7xx

### CHANnel<m>:COUPling <Coupling>

Selects the connection of the indicated channel signal - coupling and termination.

<!-- 来源：RTM2_UserManual_en_10_files\part102.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part103.htm -->

### Parameters:

<Coupling> DC | DCLimit | AC | ACLimit | GND

<!-- 来源：RTM2_UserManual_en_10_files\part104.htm -->

### DC

Direct connection with 50 Ω termination.

<!-- 来源：RTM2_UserManual_en_10_files\part105.htm -->

### DCLimit

Direct connection with 1 MΩ termination.

<!-- 来源：RTM2_UserManual_en_10_files\part106.htm -->

### AC

Connection through DC capacitor that removes the DC offset voltage from the input signal.

<!-- 来源：RTM2_UserManual_en_10_files\part107.htm -->

### ACLimit

Connection through DC capacitor with 1 MΩ termination. The capacitor removes the DC offset voltage from the input signal.

<!-- 来源：RTM2_UserManual_en_10_files\part108.htm -->

### GND

Connection to the ground. All channel data is set to a constant ground value.

*RST: DCLimit

### CHANnel<m>:SCALe <Scale>

Sets the vertical scale for the indicated channel.

<!-- 来源：RTM2_UserManual_en_10_files\part109.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part110.htm -->

### Parameters:

<Scale> Scale value, given in Volts per division.

Range: 1e-3 to 10 (without probe attenuation)

*RST: 5e-3

Default unit: V/DIV

### CHANnel<m>:RANGe <Range>

```text
Sets the voltage range across the 8 vertical divisions of the diagram. Use the com- mand alternativly instead of CHANnel<m>:SCALe.
```

<!-- 来源：RTM2_UserManual_en_10_files\part111.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The maximum channel number is instrument-dependent.

<!-- 来源：RTM2_UserManual_en_10_files\part112.htm -->

### Parameters:

<Range> Voltage range value

Range: 8e-3 to 80 (without probe attenuation)

*RST: 40e-3

Default unit: V

### CHANnel<m>:POSition <Position>

Sets the vertical position of the indicated channel and its horizontal axis in the window.

<!-- 来源：RTM2_UserManual_en_10_files\part113.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part114.htm -->

### Parameters:

<Position> Position value, given in divisions.

Range: -5 to 5

*RST: 0

Default unit: DIV

### CHANnel<m>:OFFSet <Offset>

The offset voltage is subtracted to correct an offset-affected signal.

<!-- 来源：RTM2_UserManual_en_10_files\part115.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part116.htm -->

### Parameters:

<Offset> Offset value

Range: Values depend on vertical scale and probe attenua- tion.

Increment: Value depends on vertical scale and probe attenua- tion.

Default unit: V

### CHANnel<m>:BANDwidth <BandwidthLimit> Selects the bandwidth limit for the indicated channel.

<!-- 来源：RTM2_UserManual_en_10_files\part117.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part118.htm -->

### Parameters:

<BandwidthLimit> FULL | B400 | B200 | B20

<!-- 来源：RTM2_UserManual_en_10_files\part119.htm -->

### FULL

Use full bandwidth.

Instruments with 1 GHz bandwidth: If termination is 50 Ω, the full bandwidth of 1 GHz is available. If termination is 1 MΩ, the full bandwith is limited to 500 MHz.

<!-- 来源：RTM2_UserManual_en_10_files\part120.htm -->

### B400 | B200 | B20

Limit to 400MHz, 200 MHz, or 20 MHz, respectively. Available values depend on the instrument's bandwidth.

*RST: FULL

### CHANnel<m>:POLarity <Polarity>

Turns the inversion of the signal amplitude on or off. To invert means to reflect the volt- age values of all signal components against the ground level. Inversion affects only the display of the signal but not the trigger.

<!-- 来源：RTM2_UserManual_en_10_files\part121.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part122.htm -->

### Parameters:

<Polarity> NORMal | INVerted

*RST: NORM

### CHANnel<m>:OVERload <Overload>

Retrieves the overload status of the specified channel from the status bit. When the overload problem is solved, the command resets the status bit.

<!-- 来源：RTM2_UserManual_en_10_files\part123.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part124.htm -->

### Parameters:

<Overload> ON | OFF

Use OFF to reset the overload status bit.

*RST: OFF

### Example: CHANnel2:OVERload?

Queries the overload status of channel 2.

```text
CHANnel2:OVERload OFF
```

Resets the overload status bit.

### CHANnel<m>:SKEW <Skew>

Skew or deskew compensates delay differences between channels caused by the dif- ferent length of cables, probes, and other sources. Correct deskew values are impor- tant for accurate triggering.

<!-- 来源：RTM2_UserManual_en_10_files\part125.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part126.htm -->

### Parameters:

<Skew> Deskew value Default unit: s

### CHANnel<m>:THReshold <Threshold>

Threshold value for digitization of analog signals. If the signal value is higher than the threshold, the signal state is high (1 or true for the boolean logic). Otherwise, the signal state is considered low (0 or false) if the signal value is below the threshold.

<!-- 来源：RTM2_UserManual_en_10_files\part127.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part128.htm -->

### Parameters:

<Threshold> Default values are: TTL: 1.4 V

ECL: -1.3 V

CMOS: 2.5 V

*RST: 1.4

Default unit: V

### CHANnel<m>:THReshold:HYSTeresis <ThresholdHysteresis>

Defines the size of the hysteresis to avoid the change of signal states due to noise.

<!-- 来源：RTM2_UserManual_en_10_files\part129.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part130.htm -->

### Parameters:

<ThresholdHysteresis>SMALl | MEDium | LARGe

*RST: SMAL

### CHANnel<m>:LABel <Label>

Specifies a name for the selected channel.

<!-- 来源：RTM2_UserManual_en_10_files\part131.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part132.htm -->

### Parameters:

<Label> String value

String with max. 8 characters, only ASCII characters can be used

### CHANnel<m>:LABel:STATe <State> Shows or hides the channel name.

<!-- 来源：RTM2_UserManual_en_10_files\part133.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part134.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### CHANnel<m>:ZOFFset[:VALue] <ZeroOffset> Sets the zero offset.

Differences in DUT and oscilloscope ground levels may cause larger zero errors affect- ing the waveform. If the DUT is ground-referenced, the "Zero Offset" corrects the zero error and sets the probe to the zero level.

You can assess the zero error by measuring the mean value of a signal that should return zero.

<!-- 来源：RTM2_UserManual_en_10_files\part135.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part136.htm -->

### Parameters:

<ZeroOffset> *RST: 0

Default unit: V

<!-- 来源：RTM2_UserManual_en_10_files\part137.htm -->

### 18.4.5 Waveform Data

Consider also the following commands:

- FORMat[:DATA] on page 731

- CHANnel<m>:DATA:XINCrement? on page 742

- CHANnel<m>:DATA:XORigin? on page 742

- CHANnel<m>:DATA:YINCrement? on page 743

- CHANnel<m>:DATA:YORigin? on page 743

- CHANnel<m>:DATA:YRESolution? on page 743

- CHANnel<m>:DATA:ENVelope:XINCrement? on page 742

- CHANnel<m>:DATA:ENVelope:XORigin? on page 742

- CHANnel<m>:DATA:ENVelope:YINCrement? on page 743

- CHANnel<m>:DATA:ENVelope:YORigin? on page 743

- CHANnel<m>:DATA:ENVelope:YRESolution? on page 743

CHANnel<m>:DATA? 428

CHANnel<m>:DATA:HEADer? 428

CHANnel<m>:DATA:ENVelope? 429

CHANnel<m>:DATA:ENVelope:HEADer? 429

CHANnel<m>:DATA:POINts 430

<!-- 来源：RTM2_UserManual_en_10_files\part138.htm -->

### CHANnel<m>:DATA?

Returns the data of the analog channel waveform for transmission from the instrument to the controlling computer. The waveforms data can be used in MATLAB, for example.

To set the export format, use FORMat[:DATA] on page 731.

```text
To set the range of samples to be returned, use CHANnel<m>:DATA:POINts. For envelope waveforms, use the CHANnel<m>:DATA:ENVelope? command. Suffix:
```

<m> 1. 4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part139.htm -->

### Return values:

<Data> List of values according to the format settings - the voltages of recorded waveform samples.

### Example: FORM ASC CHAN1:DATA?

```text
-0.125000,-0.123016,-0.123016,-0.123016,
-0.123016,-0.123016,...
```

### Example: See Chapter 18.2.1, "Data Export", on page 405

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part140.htm -->

### CHANnel<m>:DATA:HEADer?

Returns information on the channel waveform. For envelope waveforms, use the

```text
CHANnel<m>:DATA:ENVelope:HEADer? command.
```

#### Table 18-1: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Record length of the waveform in Samples | 200000 |
| 4 | Number of values per sample interval, usually 1. | 1 |

<!-- 来源：RTM2_UserManual_en_10_files\part141.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part142.htm -->

### Return values:

<DataHeader> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part143.htm -->

### CHANnel<m>:DATA:ENVelope?

Returns the data of the envelope. The envelope consists of two waveforms. The wave- forms data can be used in MATLAB, for example.

Use this command only for envelope waveforms. For other channel waveforms use

```text
CHANnel<m>:DATA?.
```

To set the export format, use FORMat[:DATA] on page 731.

```text
To set the range of samples to be returned, use CHANnel<m>:DATA:POINts.
```

<!-- 来源：RTM2_UserManual_en_10_files\part144.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part145.htm -->

### Return values:

<Data> List of values according to the format settings - the voltages of the envelope points. The list contains two values for each sam- ple interval.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part146.htm -->

### CHANnel<m>:DATA:ENVelope:HEADer?

Returns information on the envelope waveform.

Use this command only for envelope waveforms. for all other channel waveforms use

```text
CHANnel<m>:DATA:HEADer?.
```

#### Table 18-2: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Number of samples | 200000 |
| 4 | Number of values per sample interval. For envelope waveforms the value is 2. | 2 |

<!-- 来源：RTM2_UserManual_en_10_files\part147.htm -->

### Suffix:

<m> 1..4

<!-- 来源：RTM2_UserManual_en_10_files\part148.htm -->

### Return values:

<DataHeader> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,2

### Usage: Query only

### CHANnel<m>:DATA:POINts <Points>

```text
As a setting, the command selects a range of samples that will be returned with CHANnel<m>:DATA? and CHANnel<m>:DATA:ENVelope?. As a query, it returns the number of returned samples for the selected range.
```

If ACQuire:WRATe is set to MSAMples (maximum sample rate), the memory usually contains more data samples than the screen can display. In this case, you can decide which data will be saved: samples stored in the memory or only the displayed samples.

### Note: The sample range can only be changed in STOP mode. If the acquisition is run- ning, DEF is always used automatically. If the acquisition has been stopped, data can be read from the memory, and all settings are available.

<!-- 来源：RTM2_UserManual_en_10_files\part149.htm -->

### Suffix:

<m> 1..4

The command affects all channels, and the suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part150.htm -->

### Setting parameters:

<Points> DEFault | MAXimum | DMAXimum Sets the range for data queries.

<!-- 来源：RTM2_UserManual_en_10_files\part151.htm -->

### DEFault

Waveform points that are visible on the screen. At maximum waveform rate, the instrument stores more samples than visible on the screen, and DEF returns less values than acquired.

<!-- 来源：RTM2_UserManual_en_10_files\part152.htm -->

### MAXimum

All waveform samples that are stored in the memory. Only avail- able if acquisition is stopped.

<!-- 来源：RTM2_UserManual_en_10_files\part153.htm -->

### DMAXimum

Display maximum: Waveform samples stored in the current waveform record but only for the displayed time range. At maxi- mum waveform rate, the instrument stores more samples than visible on the screen, and DMAX returns more values than DEF. Only available if acquisition is stopped.

*RST: DEFault

<!-- 来源：RTM2_UserManual_en_10_files\part154.htm -->

### Return values:

<Points> Number of data points in the selected range.

Default unit: Samples

### Example: CHAN:DATA:POIN DEF CHAN:DATA:POIN?;:CHAN2:DATA:POIN?

Returned values: 10416;10416 CHAN:DATA:POIN DMAX CHAN:DATA:POIN?;:CHAN2:DATA:POIN?

Returned values: 124992;124992 CHAN:DATA:POIN MAX CHAN:DATA:POIN?;:CHAN2:DATA:POIN?

Returned values: 4194302;4194302

### Example: See Chapter 18.2.1.1, "Reading Waveform Data in Real For- mat", on page 405

<!-- 来源：RTM2_UserManual_en_10_files\part155.htm -->

### 18.4.6 Probes

PROBe<m>:SETup:ATTenuation[:AUTO]? 432

PROBe<m>:SETup:ATTenuation:UNIT 432

PROBe<m>:SETup:ATTenuation:MANual 432

PROBe<m>:SETup:BANDwidth? 433

PROBe<m>:SETup:CAPacitance? 433

PROBe<m>:SETup:DCOFfset? 433

PROBe<m>:SETup:IMPedance? 433

PROBe<m>:SETup:MODE 434

PROBe<m>:SETup:NAME? 434

PROBe<m>:SETup:OFFSwitch 434

PROBe<m>:SETup:TYPE? 435

PROBe<m>:SETup:UOFFset 435

PROBe<m>:SETup:CMOFfset 435

PROBe<m>:ID:BUILd? 436

PROBe<m>:ID:PARTnumber? 436

PROBe<m>:ID:PRDate? 436

PROBe<m>:ID:SRNumber? 437

PROBe<m>:ID:SWVersion? 437

<!-- 来源：RTM2_UserManual_en_10_files\part156.htm -->

### PROBe<m>:SETup:ATTenuation[:AUTO]?

Returns the attenuation of an automatically detected probe.

<!-- 来源：RTM2_UserManual_en_10_files\part157.htm -->

### Suffix:

<m> 1. 4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part158.htm -->

### Return values:

<ProbeAttenuation> Range: 0.001 to 1000

### Usage: Query only

### PROBe<m>:SETup:ATTenuation:UNIT <Unit> Selects the unit that the probe can measure.

<!-- 来源：RTM2_UserManual_en_10_files\part159.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part160.htm -->

### Parameters:

<Unit> V | A

### Firmware/Software: FW 03.700

### PROBe<m>:SETup:ATTenuation:MANual <ManualAttenuation>

Sets the attenuation or gain of the probe if the probe was not detected by the instru- ment.

<!-- 来源：RTM2_UserManual_en_10_files\part161.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part162.htm -->

### Parameters:

<ManualAttenuation> Range: 0.001 to 10000

*RST: 1

### Firmware/Software: FW 03.700

<!-- 来源：RTM2_UserManual_en_10_files\part163.htm -->

### PROBe<m>:SETup:BANDwidth?

Queries the bandwidth of the probe.

<!-- 来源：RTM2_UserManual_en_10_files\part164.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part165.htm -->

### Return values:

<Bandwidth> Range: 10e5 to 20e8

Increment: 10 Default unit: Hz

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part166.htm -->

### PROBe<m>:SETup:CAPacitance?

Queries the input capacity of the probe.

<!-- 来源：RTM2_UserManual_en_10_files\part167.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part168.htm -->

### Return values:

<InputCapacitance> Range: 0.1e-12 to 1.0e-9

Increment: 1.0e-12 Default unit: F

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part169.htm -->

### PROBe<m>:SETup:DCOFfset?

Retrieves the DC voltage that is measured by the integrated voltmeter of R&S active probes. Switch the voltmeter on before, see PROBe<m>:SETup:OFFSwitch

on page 434.

<!-- 来源：RTM2_UserManual_en_10_files\part170.htm -->

### Suffix:

<m> Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part171.htm -->

### Return values:

<Offset> Range: -1.0e26 to 1.0e-26 Increment: 1e-3

Default unit: V

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part172.htm -->

### PROBe<m>:SETup:IMPedance?

Queries the termination of the probe.

<!-- 来源：RTM2_UserManual_en_10_files\part173.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part174.htm -->

### Return values:

<Termination> 50OHm | 1MOHm | UNKNown

### Usage: Query only

### PROBe<m>:SETup:MODE <Mode>

Select the action that is started with the probe button.

<!-- 来源：RTM2_UserManual_en_10_files\part175.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part176.htm -->

### Parameters:

<Mode> RCONtinuous | RSINgle | AUToset | NOACtion

<!-- 来源：RTM2_UserManual_en_10_files\part177.htm -->

### RCONtinuous

Run continuous: The acquisition is running as long as the probe button is pressed.

<!-- 来源：RTM2_UserManual_en_10_files\part178.htm -->

### RSINgle

Run single: starts one acquisition.

<!-- 来源：RTM2_UserManual_en_10_files\part179.htm -->

### AUTOSET

Starts the autoset procedure.

<!-- 来源：RTM2_UserManual_en_10_files\part180.htm -->

### NOACtion

Nothing is started on pressing the micro button.

*RST: RCONtinuous

<!-- 来源：RTM2_UserManual_en_10_files\part181.htm -->

### PROBe<m>:SETup:NAME?

Queries the name of the probe.

<!-- 来源：RTM2_UserManual_en_10_files\part182.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part183.htm -->

### Return values:

<Name> string

### Usage: Query only

### PROBe<m>:SETup:OFFSwitch <DCOffsetOnOff>

Switches the integrated voltmeter of an R&S active probe on or off.

The command is only available if an R&S active probe with R&S ProbeMeter is used.

<!-- 来源：RTM2_UserManual_en_10_files\part184.htm -->

### Suffix:

<m> Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part185.htm -->

### Parameters:

<DCOffsetOnOff> ON | OFF

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part186.htm -->

### PROBe<m>:SETup:TYPE?

Queries the type of the probe.

<!-- 来源：RTM2_UserManual_en_10_files\part187.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part188.htm -->

### Return values:

<Type> NONE | ACTive | PASSive

<!-- 来源：RTM2_UserManual_en_10_files\part189.htm -->

### NONE

not detected

<!-- 来源：RTM2_UserManual_en_10_files\part190.htm -->

### ACTive

active probe

<!-- 来源：RTM2_UserManual_en_10_files\part191.htm -->

### PASSive

passive probe

### Usage: Query only

### PROBe<m>:SETup:UOFFset <UserOffset> Sets an additional probe offset.

<!-- 来源：RTM2_UserManual_en_10_files\part192.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part193.htm -->

### Parameters:

<UserOffset> Range: Depends on the probe characteristics.

*RST: 0

Default unit: V

### PROBe<m>:SETup:CMOFfset <CommonModeOffset>

Sets the common-mode offset. The setting is only available for differential probes.

<!-- 来源：RTM2_UserManual_en_10_files\part194.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part195.htm -->

### Parameters:

<CommonModeOffset>*RST: 0

Default unit: V

<!-- 来源：RTM2_UserManual_en_10_files\part196.htm -->

### PROBe<m>:ID:BUILd?

Queries the build number of the probe software.

<!-- 来源：RTM2_UserManual_en_10_files\part197.htm -->

### Suffix:

<m> 1. 4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part198.htm -->

### Return values:

<BuildNumber> 32 bit number

Range: 0 to 4294967295

Increment: 1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part199.htm -->

### PROBe<m>:ID:PARTnumber?

Queries the R&S part number of the probe.

<!-- 来源：RTM2_UserManual_en_10_files\part200.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part201.htm -->

### Return values:

<PartNumber> string

Returns the part number in a string.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part202.htm -->

### PROBe<m>:ID:PRDate?

Queries the production date of the probe.

<!-- 来源：RTM2_UserManual_en_10_files\part203.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part204.htm -->

### Return values:

<ProductionDate> string

Returns the date in a string.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part205.htm -->

### PROBe<m>:ID:SRNumber?

Queries the serial number of the probe.

<!-- 来源：RTM2_UserManual_en_10_files\part206.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part207.htm -->

### Return values:

<SerialNumber> string

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part208.htm -->

### PROBe<m>:ID:SWVersion?

Queries the version of the probe firmware.

<!-- 来源：RTM2_UserManual_en_10_files\part209.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part210.htm -->

### Return values:

<SoftwareVersion> string

Returns the version number in a string.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part211.htm -->

### 18.4.7 History and Segmented Memory (Option R&S RTM-K15)

This section lists the commands of option R&S RTM-K15. The following commands are also important:

- ACQuire:WRATe on page 418

- ACQuire:POINts[:VALue] on page 418

- Ultra Segmentation Settings 437

### 18.4.7.1 Ultra Segmentation Settings

ACQuire:COUNt? 437

ACQuire:SEGMented:MAXimum 438

ACQuire:NSINgle:MAXimum 438

ACQuire:AVAilable? 438

ACQuire:SEGMented:STATe 438

<!-- 来源：RTM2_UserManual_en_10_files\part212.htm -->

### ACQuire:COUNt?

Returns the maximum number of segments that can be captured with the current con- figuration.

<!-- 来源：RTM2_UserManual_en_10_files\part213.htm -->

### Return values:

<NoOfSegments> Number of available segments in the memory

### Usage: Query only

### ACQuire:SEGMented:MAXimum <MaxAcquisitions>

### ACQuire:NSINgle:MAXimum <MaxAcquisitions>

Sets the maximum possible number of segments for a RUN Nx SINGLE acquisition. Thus, all segments of the memory are captured.

<!-- 来源：RTM2_UserManual_en_10_files\part214.htm -->

### Parameters:

<MaxAcquisitions> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part215.htm -->

### ACQuire:AVAilable?

Returns the number of segments that are currently saved in the memory. This number is available for history viewing.

<!-- 来源：RTM2_UserManual_en_10_files\part216.htm -->

### Return values:

<Acquisitions> Number of captured segments

### Usage: Query only

### ACQuire:SEGMented:STATe <State>

Enables the ultra segementation mode. The acquisitions are performed very fast with- out processing and displaying the waveforms. When acquisition has been stopped, the latest waveform is displayed, the older ones are stored in segments.

<!-- 来源：RTM2_UserManual_en_10_files\part217.htm -->

### Parameters:

<State> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part218.htm -->

### 18.4.8 History Viewer

CALCulate:MATH<m>:HISTory:CURRent 439

BUS<b>:HISTory:CURRent 439

DIGital<m>:HISTory:CURRent 439

SPECtrum:HISTory:CURRent 439

CHANnel<m>:HISTory:CURRent 439

CALCulate:MATH<m>:HISTory:PALL 439

BUS<b>:HISTory:PALL 439

DIGital<m>:HISTory:PALL 439

SPECtrum:HISTory:PALL 440

CHANnel<m>:HISTory:PALL 440

CALCulate:MATH<m>:HISTory:STARt 440

BUS<b>:HISTory:STARt 440

DIGital<m>:HISTory:STARt 440

SPECtrum:HISTory:STARt 440

CHANnel<m>:HISTory:STARt 440

CALCulate:MATH<m>:HISTory:STOP 440

BUS<b>:HISTory:STOP 440

DIGital<m>:HISTory:STOP 440

SPECtrum:HISTory:STOP 440

CHANnel<m>:HISTory:STOP 440

CALCulate:MATH<m>:HISTory:PLAYer:SPEed 441

BUS<b>:HISTory:PLAYer:SPEed 441

DIGital<m>:HISTory:PLAYer:SPEed 441

SPECtrum:HISTory:PLAYer:SPEed 441

CHANnel<m>:HISTory:PLAYer:SPEed 441

CALCulate:MATH<m>:HISTory:REPLay 441

BUS<b>:HISTory:REPLay 441

DIGital<m>:HISTory:REPLay 441

SPECtrum:HISTory:REPLay 441

CHANnel<m>:HISTory:REPLay 441

CALCulate:MATH<m>:HISTory:PLAYer:STATe 442

BUS<b>:HISTory:PLAYer:STATe 442

DIGital<m>:HISTory:PLAYer:STATe 442

SPECtrum:HISTory:PLAYer:STATe 442

CHANnel<m>:HISTory:PLAYer:STATe 442

### CALCulate:MATH<m>:HISTory:CURRent <CurrentAcquisition> BUS<b>:HISTory:CURRent <CurrentAcquisition> DIGital<m>:HISTory:CURRent <CurrentAcquisition> SPECtrum:HISTory:CURRent <CurrentAcquisition> CHANnel<m>:HISTory:CURRent <CurrentAcquisition>

Accesses a particular acquisition segment in the memory to display it. The query returns the index of the segment that is shown.

<!-- 来源：RTM2_UserManual_en_10_files\part219.htm -->

### Suffix:

<m> 1. 4

Selects the input channel or math waveform. 0 15

Selects the digital channel.

<b> 1. 4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part220.htm -->

### Parameters:

<CurrentAcquisition> Segment index. There are two ways to enter the index.

Negative index count: the newest segment has the index "0", older segments have a negative index: -(n-1),.... -1, 0 Positive index count: the oldest segment has the index 1, and the newest segment has the index n: 1, 2,..., n

where n is the number of acquired segments.

### CALCulate:MATH<m>:HISTory:PALL <PlayAll> BUS<b>:HISTory:PALL <PlayAll> DIGital<m>:HISTory:PALL <PlayAll>

### SPECtrum:HISTory:PALL <PlayAll>

### CHANnel<m>:HISTory:PALL <PlayAll> Enables the replay of all acquired segments.

<!-- 来源：RTM2_UserManual_en_10_files\part221.htm -->

### Suffix:

<m> 1..4

Selects the input channel or math waveform. 0..15

Selects the digital channel.

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part222.htm -->

### Parameters:

<PlayAll> ON | OFF

```text
If set to OFF, define the range of segments to be shown using CHANnel<m>:HISTory:STARt and CHANnel<m>:HISTory: STOP
```

*RST: ON

### CALCulate:MATH<m>:HISTory:STARt <StartAcquisition> BUS<b>:HISTory:STARt <StartAcquisition> DIGital<m>:HISTory:STARt <StartAcquisition> SPECtrum:HISTory:STARt <StartAcquisition> CHANnel<m>:HISTory:STARt <StartAcquisition>

Sets the index of the oldest segment to be displayed.

<!-- 来源：RTM2_UserManual_en_10_files\part223.htm -->

### Suffix:

<m> 1..4

Selects the input channel or math waveform. 0..15

Selects the digital channel.

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part224.htm -->

### Parameters:

<StartAcquisition> Start index. You can enter a positive or negative index, see

```text
CHANnel<m>:HISTory:CURRent.
```

### CALCulate:MATH<m>:HISTory:STOP <StopAcquisition> BUS<b>:HISTory:STOP <StopAcquisition> DIGital<m>:HISTory:STOP <StopAcquisition> SPECtrum:HISTory:STOP <StopAcquisition> CHANnel<m>:HISTory:STOP <StopAcquisition>

Sets the index of the latest segment to be displayed.

<!-- 来源：RTM2_UserManual_en_10_files\part225.htm -->

### Suffix:

<m> 1..4

Selects the input channel or math waveform. 0..15

Selects the digital channel.

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part226.htm -->

### Parameters:

<StopAcquisition> Stop index. You can enter a positive or negative index, see

```text
CHANnel<m>:HISTory:CURRent.
```

### CALCulate:MATH<m>:HISTory:PLAYer:SPEed <PlayerSpeed> BUS<b>:HISTory:PLAYer:SPEed <PlayerSpeed> DIGital<m>:HISTory:PLAYer:SPEed <PlayerSpeed> SPECtrum:HISTory:PLAYer:SPEed <PlayerSpeed> CHANnel<m>:HISTory:PLAYer:SPEed <PlayerSpeed>

Sets the speed of the history replay.

<!-- 来源：RTM2_UserManual_en_10_files\part227.htm -->

### Suffix:

<m> 1..4

Selects the input channel or math waveform. 0..15

Selects the digital channel.

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part228.htm -->

### Parameters:

<PlayerSpeed> SLOW | MEDium | FAST | AUTO

*RST: AUTO

### CALCulate:MATH<m>:HISTory:REPLay <Replay> BUS<b>:HISTory:REPLay <Replay> DIGital<m>:HISTory:REPLay <Replay> SPECtrum:HISTory:REPLay <Replay> CHANnel<m>:HISTory:REPLay <Replay>

If set to ON, the replay of the selected history segments repeats automatically.

<!-- 来源：RTM2_UserManual_en_10_files\part229.htm -->

### Suffix:

<m> 1..4

Selects the input channel or math waveform. 0..15

Selects the digital channel.

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part230.htm -->

### Parameters:

<Replay> ON | OFF

*RST: OFF

### CALCulate:MATH<m>:HISTory:PLAYer:STATe <PlayerState> BUS<b>:HISTory:PLAYer:STATe <PlayerState> DIGital<m>:HISTory:PLAYer:STATe <PlayerState> SPECtrum:HISTory:PLAYer:STATe <PlayerState> CHANnel<m>:HISTory:PLAYer:STATe <PlayerState>

Starts and stops the replay of the history segments.

<!-- 来源：RTM2_UserManual_en_10_files\part231.htm -->

### Suffix:

<m> 1..4

Selects the input channel or math waveform. 0..15

Selects the digital channel.

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part232.htm -->

### Parameters:

<PlayerState> RUN | STOP

*RST: STOP

<!-- 来源：RTM2_UserManual_en_10_files\part233.htm -->

### 18.4.9 Timestamps

You can query the timestamps of history segments in two ways:

- Query for the timestamps of all history segments using...:HISTory:...:ALL

commands.

- Query for the timestamp of a specific segment using...:HISTory:... com- mands. Select the segment of interest using CHANnel<m>:HISTory:CURRent

The following commands use numeric suffixes:

- CHANnel<m>: Selects the analog input channel.

- MATH<m>: Selects the math waveform, range 1..4

- DIGital<m>: Selects the digital channel, range 0..15

- BUS<b>: Selects the bus, range 1..4

CALCulate:MATH<m>:HISTory:TSRelative? 443

BUS<b>:HISTory:TSRelative? 443

DIGital<m>:HISTory:TSRelative? 443

SPECtrum:HISTory:TSRelative? 443

CHANnel<m>:HISTory:TSRelative? 443

CALCulate:MATH<m>:HISTory:TSRelative:ALL? 443

BUS<b>:HISTory:TSRelative:ALL? 443

DIGital<m>:HISTory:TSRelative:ALL? 443

SPECtrum:HISTory:TSRelative:ALL? 443

CHANnel<m>:HISTory:TSRelative:ALL? 443

CALCulate:MATH<m>:HISTory:TSABsolute? 444

BUS<b>:HISTory:TSABsolute? 444

DIGital<m>:HISTory:TSABsolute? 444

SPECtrum:HISTory:TSABsolute? 444

CHANnel<m>:HISTory:TSABsolute? 444

CALCulate:MATH<m>:HISTory:TSABsolute:ALL? 444

BUS<b>:HISTory:TSABsolute:ALL? 444

DIGital<m>:HISTory:TSABsolute:ALL? 444

SPECtrum:HISTory:TSABsolute:ALL? 444

CHANnel<m>:HISTory:TSABsolute:ALL? 444

CALCulate:MATH<m>:HISTory:TSDate? 444

BUS<b>:HISTory:TSDate? 444

DIGital<m>:HISTory:TSDate? 444

SPECtrum:HISTory:TSDate? 445

CHANnel<m>:HISTory:TSDate? 445

CALCulate:MATH<m>:HISTory:TSDate:ALL? 445

BUS<b>:HISTory:TSDate:ALL? 445

DIGital<m>:HISTory:TSDate:ALL? 445

SPECtrum:HISTory:TSDate:ALL? 445

CHANnel<m>:HISTory:TSDate:ALL? 445

<!-- 来源：RTM2_UserManual_en_10_files\part234.htm -->

### CALCulate:MATH<m>:HISTory:TSRelative? BUS<b>:HISTory:TSRelative?

### DIGital<m>:HISTory:TSRelative? SPECtrum:HISTory:TSRelative? CHANnel<m>:HISTory:TSRelative?

```text
Returns the time difference of the selected segment to the newest segment. To select a segment, use CHANnel<m>:HISTory:CURRent.
```

<!-- 来源：RTM2_UserManual_en_10_files\part235.htm -->

### Return values:

<Time> Time to newest acquisition

### Example: CHAN:HIST:CURR -5 CHAN:HIST:TSR?

```text
--> -1.138757760000E-02
```

Returns the relative time of the sixth segment. The newest seg- ment has index 0.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part236.htm -->

### CALCulate:MATH<m>:HISTory:TSRelative:ALL? BUS<b>:HISTory:TSRelative:ALL?

### DIGital<m>:HISTory:TSRelative:ALL? SPECtrum:HISTory:TSRelative:ALL? CHANnel<m>:HISTory:TSRelative:ALL?

Returns the time differences to the newest acquisition of all history segments.

<!-- 来源：RTM2_UserManual_en_10_files\part237.htm -->

### Return values:

<TimeToNewestAcq> List of Values

The list starts with the oldest segment, and the newest segment is the last one.

Example: CHANnel2:HISTory:TSRelative:ALL?

```text
--> -4.184565632000E-01,-4.094896352000E-01,-4.005227104000E-01,
-3.915557824000E-01,...,-8.966924800000E-03,-0.000000000000E+00
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part238.htm -->

### CALCulate:MATH<m>:HISTory:TSABsolute? BUS<b>:HISTory:TSABsolute?

### DIGital<m>:HISTory:TSABsolute? SPECtrum:HISTory:TSABsolute? CHANnel<m>:HISTory:TSABsolute?

```text
Returns the absolute daytime of the selected acquisition ( CHANnel<m>:HISTory: CURRent ).
```

<!-- 来源：RTM2_UserManual_en_10_files\part239.htm -->

### Return values:

<Hour>, <Minute>,

<Seconds>

Comma-separated list

### Example: CHAN:HIST:CURR -1 CHAN:HIST:TSAB?

```text
--> 16,24,3.302100000000E+01
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part240.htm -->

### CALCulate:MATH<m>:HISTory:TSABsolute:ALL? BUS<b>:HISTory:TSABsolute:ALL?

### DIGital<m>:HISTory:TSABsolute:ALL? SPECtrum:HISTory:TSABsolute:ALL? CHANnel<m>:HISTory:TSABsolute:ALL?

Returns the absolute daytimes of all history segments.

<!-- 来源：RTM2_UserManual_en_10_files\part241.htm -->

### Return values:

<Hour>,<Minute>,

<Second>

Comma-separated list of hour, minute, and second values.

The list starts with the oldest segment, and the newest segment is the last one.

Example: CHANnel2:HISTory:TSABsolute:ALL?

```text
--> 14,59,4.558154343680E+01,14,59,4.559051036480E+01, 14,59,4.559947728960E+01,...
```

### Usage: Query only

### CALCulate:MATH<m>:HISTory:TSDate? BUS<b>:HISTory:TSDate?

### DIGital<m>:HISTory:TSDate?

### SPECtrum:HISTory:TSDate? CHANnel<m>:HISTory:TSDate?

```text
Returns the date of the selected acquisition ( CHANnel<m>:HISTory:CURRent ).
```

<!-- 来源：RTM2_UserManual_en_10_files\part242.htm -->

### Return values:

<Year>, <Month>,

<Day>

Comma-separated list

### Example: CHAN:HIST:CURR -5 CHAN:HIST:TSD?

```text
--> 2014,7,1
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part243.htm -->

### CALCulate:MATH<m>:HISTory:TSDate:ALL? BUS<b>:HISTory:TSDate:ALL?

### DIGital<m>:HISTory:TSDate:ALL? SPECtrum:HISTory:TSDate:ALL? CHANnel<m>:HISTory:TSDate:ALL?

Returns the dates of all history segments.

<!-- 来源：RTM2_UserManual_en_10_files\part244.htm -->

### Return values:

<Year>,<Month>,

<Day>

Comma-separated list of year, month, and day values.

The list starts with the oldest segment, and the newest segment is the last one.

Example: CHANnel2:HISTory:TSDate:ALL?

```text
--> 2014,11,26,2014,11,26,2014,11,26,2014,11,26,...
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part245.htm -->

### 18.4.10 Export

EXPort:ATABle:NAME 445

EXPort:ATABle:SAVE 446

SPECtrum:HISTory:EXPort:NAME 446

SPECtrum:HISTory:EXPort:SAVE 446

### EXPort:ATABle:NAME <ExportPath>

Defines the path and filename of the acqisition timestamps file. The file format is CSV. If the file already exists, it will be overwritten.

<!-- 来源：RTM2_UserManual_en_10_files\part246.htm -->

### Parameters:

<ExportPath> string

String parameter

Example: EXPort:ATABle:NAME "/USB_FRONT/EXPORT/TIMES"

<!-- 来源：RTM2_UserManual_en_10_files\part247.htm -->

### EXPort:ATABle:SAVE

```text
Saves the acquisition timestamps table to the file that is defined by the EXPort: ATABle:NAME command.
```

Example: EXPort:ATABle:SAVE

The file contains the following timestamp values:

```text
"","Date","Time"
"Start of Acquisition","2014-11-24","14:35:59" "Last Acquisition","2014-11-24","14:36:01" "Acquisitions","150"
"Number","Relative Time","Time to previous", "Date","Time"
"0","-0.000000000000000E+00","1.009638400000000E-02", "2014-11-24","14:36:01","0.0000000000E+00"
"-1","-1.009638400000000E-02","2.000568800000000E-02", "2014-11-24","14:36:00","9.8990361600E-01"
"-2","-3.010207200000000E-02","2.000216800000000E-02", "2014-11-24","14:36:00","9.6989792800E-01"
"-3","-5.010424000000000E-02","2.001423200000000E-02", "2014-11-24","14:36:00","9.4989576000E-01"
"-4","-7.011847200000000E-02","2.000044000000000E-02", "2014-11-24","14:36:00","9.2988152800E-01"
"-5","-9.011891200000001E-02","9.917412000000000E-03", "2014-11-24","14:36:00","9.0988108800E-01"
"-6","-1.000363240000000E-01","1.009686000000000E-02", "2014-11-24","14:36:00","8.9996367600E-01".....
```

### Usage: Event

### SPECtrum:HISTory:EXPort:NAME <ExportPath>

Defines the path and filename of the spectrum analysis timestamps file. The file format is CSV. If the file already exists, it will be overwritten.

<!-- 来源：RTM2_UserManual_en_10_files\part248.htm -->

### Parameters:

<ExportPath> string

Example: SPECtrum:HISTory:EXPort:NAME "/USB_FRONT/EXPORT/TIMES"

<!-- 来源：RTM2_UserManual_en_10_files\part249.htm -->

### SPECtrum:HISTory:EXPort:SAVE

Saves the spectrum analysis timestamps table to the file that is defined by the

```text
SPECtrum:HISTory:EXPort:NAME command.
```

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part250.htm -->

## 18.5 Trigger

- General A Trigger Settings 447

- Edge Trigger 450

- Width Trigger 451

- Video/TV Trigger 453

- Pattern Trigger 454

- Runt 457

- Rise Time / Fall Time Trigger 457

- B-Trigger 459

<!-- 来源：RTM2_UserManual_en_10_files\part251.htm -->

### 18.5.1 General A Trigger Settings

TRIGger:A:MODE 447

TRIGger:A:LEVel<n>[:VALue] 447

TRIGger:A:FINDlevel 448

TRIGger:A:SOURce 448

TRIGger:A:TYPE 448

TRIGger:EXTern:COUPling 449

TRIGger:EXTern:TERMination 449

TRIGger:EXTern:OVERload 449

TRIGger:A:HOLDoff:MODE 449

TRIGger:A:HOLDoff:TIME 449

### TRIGger:A:MODE <TriggerMode>

Sets the trigger mode. The trigger mode determines the behaviour of the instrument if no trigger occurs.

<!-- 来源：RTM2_UserManual_en_10_files\part252.htm -->

### Parameters:

<TriggerMode> AUTO | NORMal

<!-- 来源：RTM2_UserManual_en_10_files\part253.htm -->

### AUTO

The instrument triggers repeatedly after a time interval if the trig- ger conditions are not fulfilled. If a real trigger occurs, it takes precedence.

<!-- 来源：RTM2_UserManual_en_10_files\part254.htm -->

### NORMal

The instrument acquires a waveform only if a trigger occurs.

*RST: AUTO

### TRIGger:A:LEVel<n>[:VALue] <Level>

Sets the trigger treshold voltage for all A trigger types that require a trigger level.

<!-- 来源：RTM2_UserManual_en_10_files\part255.htm -->

### Suffix:

<n> 1..5

Selects the trigger input. 1...4 select the corresponding channel, 5 is the external trigger input. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part256.htm -->

### Parameters:

<Level> Range: Depends on vertical scale.

Default unit: V

<!-- 来源：RTM2_UserManual_en_10_files\part257.htm -->

### TRIGger:A:FINDlevel

Sets the trigger level of the A-trigger event to 50% of the signal amplitude.

### Usage: Event

### TRIGger:A:SOURce <Source>

Sets the trigger source for the selected A trigger type.

<!-- 来源：RTM2_UserManual_en_10_files\part258.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | EXTernanalog | LINE | SBUS1.. SBUS4 | D0..D15

<!-- 来源：RTM2_UserManual_en_10_files\part259.htm -->

### CH1 | CH2 | CH3 | CH4

One of the input channels is the trigger source. Available chan- nels depend on the instrument type.

<!-- 来源：RTM2_UserManual_en_10_files\part260.htm -->

### EXTernanalog

External trigger input on the rear panel

<!-- 来源：RTM2_UserManual_en_10_files\part261.htm -->

### LINE

AC line for the edge trigger

<!-- 来源：RTM2_UserManual_en_10_files\part262.htm -->

### SBUS1.. SBUS4

Serial buses 1 to 4

The UART, SPI, SSPI and audio protocols require two bus lines (bus 1 and 2 or bus 3 and 4). Bus 2 and/or bus 4 is not available if one of these protocols is selected.

<!-- 来源：RTM2_UserManual_en_10_files\part263.htm -->

### D0..D15

If MSO option R&S RTM-B1 is installed, the digital channels D0 to D15 can be used as trigger sources for edge, width and pat- tern trigger.

### TRIGger:A:TYPE <Type>

Sets the trigger type for the A trigger.

<!-- 来源：RTM2_UserManual_en_10_files\part264.htm -->

### Parameters:

<Type> EDGE | WIDTh | TV | BUS | LOGic | RISetime | RUNT

EDGE: edge trigger WIDTh: width trigger TV: video trigger

BUS: requires at least one protocol option (R&S RTM-K1 to K5) See: Chapter 11, "Protocol Analysis", on page 192

LOGic: pattern trigger, logic trigger RIStime: rise time trigger

RUNT: runt trigger

### TRIGger:EXTern:COUPling <ExternCoupling>

Sets the coupling for the external trigger input. The command is relevant if TRIGger: B:SOURce is set to EXTernanalog.

<!-- 来源：RTM2_UserManual_en_10_files\part265.htm -->

### Parameters:

<ExternCoupling> AC | DC

*RST: AC

### TRIGger:EXTern:TERMination <ExternTermination> Adjusts the input impedance of the external trigger input.

The command is only available for instruments with 1 GHz bandwidth.

<!-- 来源：RTM2_UserManual_en_10_files\part266.htm -->

### Parameters:

<ExternTermination> ON | OFF

0 = 1 MΩ

1 = 50 Ω

*RST: OFF

### TRIGger:EXTern:OVERload <ExternOverload>

Retrieves the overload status of the external trigger input from the status bit. When the overload problem is solved, use the command to reset the status bit.

The command is only available for instruments with 1 GHz bandwidth.

<!-- 来源：RTM2_UserManual_en_10_files\part267.htm -->

### Parameters:

<ExternOverload> ON | OFF

Use OFF to reset the overload status bit.

*RST: OFF

### Example: TRIGger:EXTern:OVERload?

Queries the overload status of the external trigger input.

```text
TRIGger:EXTern:OVERload OFF
```

Resets the overload status bit.

### TRIGger:A:HOLDoff:MODE <HoldOffMode> Enables or disables the holdoff time.

<!-- 来源：RTM2_UserManual_en_10_files\part268.htm -->

### Parameters:

<HoldOffMode> TIME | OFF

*RST: Off

### TRIGger:A:HOLDoff:TIME <HoldOffTime>

Defines the holdoff time. The next trigger occurs only after the holdoff time has passed.

<!-- 来源：RTM2_UserManual_en_10_files\part269.htm -->

### Parameters:

<HoldOffTime> Default unit: s

<!-- 来源：RTM2_UserManual_en_10_files\part270.htm -->

### 18.5.2 Edge Trigger

TRIGger:A:EDGE:SLOPe 450

TRIGger:A:EDGE:COUPling 450

TRIGger:A:EDGE:FILTer:LPASs 450

TRIGger:A:EDGE:FILTer:NREJect 451

TRIGger:A:HYSTeresis 451

TRIGger:A:LEVel<n>:HYSTeresis 451

### TRIGger:A:EDGE:SLOPe <Slope>

Sets the slope for the edge trigger (A trigger).

<!-- 来源：RTM2_UserManual_en_10_files\part271.htm -->

### Parameters:

<Slope> POSitive | NEGative | EITHer

<!-- 来源：RTM2_UserManual_en_10_files\part272.htm -->

### POSitive

Rising edge, a positive voltage change

<!-- 来源：RTM2_UserManual_en_10_files\part273.htm -->

### NEGative

Falling edge, a negative voltage change

<!-- 来源：RTM2_UserManual_en_10_files\part274.htm -->

### EITHer

Rising as well as the falling edge

*RST: POSitive

### TRIGger:A:EDGE:COUPling <Coupling> Sets the coupling for the trigger source.

<!-- 来源：RTM2_UserManual_en_10_files\part275.htm -->

### Parameters:

<Coupling> DC | AC | HF

<!-- 来源：RTM2_UserManual_en_10_files\part276.htm -->

### DC

Direct Current coupling. The trigger signal remains unchanged.

<!-- 来源：RTM2_UserManual_en_10_files\part277.htm -->

### AC

Alternating Current coupling. A 5 Hz high pass filter removes the DC offset voltage from the trigger signal.

<!-- 来源：RTM2_UserManual_en_10_files\part278.htm -->

### HF

High frequency coupling. A 15 kHz high-pass filter removes lower frequencies from the trigger signal. Use this mode only with very high frequency signals.

*RST: DC

<!-- 来源：RTM2_UserManual_en_10_files\part279.htm -->

### TRIGger:A:EDGE:FILTer:LPASs <State>

Turns an additional 5 kHz low-pass filter in the trigger path on or off. This filter removes higher frequencies and is available with AC and DC coupling.

<!-- 来源：RTM2_UserManual_en_10_files\part280.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part281.htm -->

### TRIGger:A:EDGE:FILTer:NREJect <State>

Turns an additional 100 MHz low-pass filter in the trigger path on or off. This filter removes higher frequencies and is available with AC and DC coupling.

<!-- 来源：RTM2_UserManual_en_10_files\part282.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### TRIGger:A:HYSTeresis <Hysteresis>

Sets a hysteresis range around the trigger level of the A trigger event. If the signal jit- ters inside this range and crosses the trigger level thereby, no trigger event occurs.

Hysteresis is available for edge trigger.

<!-- 来源：RTM2_UserManual_en_10_files\part283.htm -->

### Parameters:

<Hysteresis> AUTO | SMALl | MEDium | LARGE | MANual

<!-- 来源：RTM2_UserManual_en_10_files\part284.htm -->

### MANual

```text
Sets the hysteresis to a user-defined value, which is defined using TRIGger:A:LEVel<n>:HYSTeresis.
```

The value is only available on instruments with 1 GHz band- width.

*RST: AUTO

### TRIGger:A:LEVel<n>:HYSTeresis <LevelHysteresis>

```text
Sets the hysteresis value if TRIGger:A:HYSTeresis is set to MANual. The command is only available on instruments with 1 GHz bandwidth.
```

<!-- 来源：RTM2_UserManual_en_10_files\part285.htm -->

### Parameters:

<LevelHysteresis> Default unit: DIV

<!-- 来源：RTM2_UserManual_en_10_files\part286.htm -->

### 18.5.3 Width Trigger

TRIGger:A:WIDTh:POLarity 451

TRIGger:A:WIDTh:RANGe 452

TRIGger:A:WIDTh:DELTa 452

TRIGger:A:WIDTh:WIDTh 452

### TRIGger:A:WIDTh:POLarity <Polarity> Sets the polarity of the pulse.

<!-- 来源：RTM2_UserManual_en_10_files\part287.htm -->

### Parameters:

<Polarity> POSitive | NEGative

<!-- 来源：RTM2_UserManual_en_10_files\part288.htm -->

### POSitive

Positive going pulse, the width is defined from the rising to the falling slopes.

<!-- 来源：RTM2_UserManual_en_10_files\part289.htm -->

### NEGative

Negative going pulse, the width is defined from the falling to the rising slopes.

*RST: POSitive

### TRIGger:A:WIDTh:RANGe <RangeMode>

Defines how the measured pulse width is compared with the given limit(s).

<!-- 来源：RTM2_UserManual_en_10_files\part290.htm -->

### Parameters:

<RangeMode> WITHin | OUTSide | SHORter | LONGer

<!-- 来源：RTM2_UserManual_en_10_files\part291.htm -->

### WITHin | OUTSide

```text
Triggers on pulses inside or outside a range defined by time ± delta. The time is specified with TRIGger:A:WIDTh:WIDTh, the range around is defined with TRIGger:A:WIDTh:DELTa.
```

<!-- 来源：RTM2_UserManual_en_10_files\part292.htm -->

### SHORter | LONGer

Triggers on pulses shorter or longer than a time set with

```text
TRIGger:A:WIDTh:WIDTh.
```

*RST: LONGer

### TRIGger:A:WIDTh:DELTa <Delta>

```text
Defines a range around the width value specified using TRIGger:A:WIDTh:WIDTh.
```

<!-- 来源：RTM2_UserManual_en_10_files\part293.htm -->

### Parameters:

<Delta> Range ±Δt ("Variation" softkey)

Range: Depends on the defined pulse width (TRIG:A:WIDTH:WITDH)

### TRIGger:A:WIDTh:WIDTh <Time1>

```text
For the ranges WITHin and OUTSide (defined using TRIGger:A:WIDTh:RANGe ), the
```

<Time1> defines the center of a range which is defined by the limits ±<Delta> (set with

```text
TRIGger:A:WIDTh:DELTa ).
```

For the ranges SHORter and LONGer, the width defines the maximum and minimum pulse width, respectively.

<!-- 来源：RTM2_UserManual_en_10_files\part294.htm -->

### Parameters:

<Time1> Center value, maximum value or minimum value depending on the defined range type.

Range: 20E-9 to 6.87194685440

Increment: Depends on the <Time1> value

*RST: 20E-9

<!-- 来源：RTM2_UserManual_en_10_files\part295.htm -->

### 18.5.4 Video/TV Trigger

TRIGger:A:TV:STANdard 453

TRIGger:A:TV:POLarity 453

TRIGger:A:TV:FIELd 453

TRIGger:A:TV:LINE 454

### TRIGger:A:TV:STANdard <Standard> Selects the color television standard.

<!-- 来源：RTM2_UserManual_en_10_files\part296.htm -->

### Parameters:

<Standard> PAL | NTSC | SECam | PALM | I576 | P720 | P1080 | I1080

PALM = PAL-M

I576 = SDTV 576i (PAL and SECAM)

P720 | P1080 = HDTV 720/1080p (progressive scanning) I1080 = HDTV 1080i (interlaced scanning)

*RST: PAL

### TRIGger:A:TV:POLarity <Polarity>

Selects the polarity of the signal. Note that the sync pulse has the opposite polarity. The edges of the sync pulses are used for triggering,

See also: "Signal" on page 65

<!-- 来源：RTM2_UserManual_en_10_files\part297.htm -->

### Parameters:

<Polarity> POSitive | NEGative

<!-- 来源：RTM2_UserManual_en_10_files\part298.htm -->

### POSitive

If the video modulation is positive, the sync pulses are negative.

<!-- 来源：RTM2_UserManual_en_10_files\part299.htm -->

### NEGative

If the modulation is negative, sync pulses are positive.

*RST: NEGative

### TRIGger:A:TV:FIELd <Field>

Sets the trigger on the beginning of the video signal fields, or on the beginning of video signal lines.

<!-- 来源：RTM2_UserManual_en_10_files\part300.htm -->

### Parameters:

<Field> EVEN | ODD | ALL | LINE | ALINe

<!-- 来源：RTM2_UserManual_en_10_files\part301.htm -->

### EVEN | ODD

Triggers only on the field start of even or odd fields. Only availa- ble for interlaced scanning.

<!-- 来源：RTM2_UserManual_en_10_files\part302.htm -->

### ALL

All fields, triggers on the frame start (progressive scanning) or any field start (interlaced scanning).

<!-- 来源：RTM2_UserManual_en_10_files\part303.htm -->

### LINE

```text
Triggers on the beginning of a specified line in any field. The line number is set with TRIGger:A:TV:LINE.
```

<!-- 来源：RTM2_UserManual_en_10_files\part304.htm -->

### ALINe

Triggers on the beginning of all video signal lines.

*RST: ALL

### TRIGger:A:TV:LINE <Line>

```text
Sets an exact line number if TRIGger:A:TV:FIELd is set to LINE.
```

<!-- 来源：RTM2_UserManual_en_10_files\part305.htm -->

### Parameters:

<Line> Range: 1 to 525 (NTSC, PAL-M); 625 (PAL, SECAM,

SDTV I-576); 750 (HDTV P720); 1125 (HDTV I1080, HDTV P1080)

Increment: 1

*RST: 1

<!-- 来源：RTM2_UserManual_en_10_files\part306.htm -->

### 18.5.5 Pattern Trigger

- Pattern Definition 454

- Time Limitation 456

### 18.5.5.1 Pattern Definition

TRIGger:A:PATTern:SOURce 455

TRIGger:A:PATTern:FUNCtion 455

TRIGger:A:PATTern:CONDition 455

### TRIGger:A:PATTern:SOURce <SourceString>

<!-- 来源：RTM2_UserManual_en_10_files\part307.htm -->

### Parameters:

<SourceString> string containing 0, 1, or X for each channel

1: high, the signal voltage is higher than the trigger level. 0: low, the signal voltage is lower than the trigger level. X: Don't care. the channel does not affect the trigger.

Without MSO option, the pattern has 4 or 2 bits, depending on the number of channels: <ch1><ch2>[<ch3><ch4>].

With MSO option, the pattern has 18 or 20 bits:

<ch1><ch2>[<ch3><ch4>]<d0><d1><d2>...<d15>.

### Example: Without MSO option R&S RTM-B1:

```text
TRIG:A:PATT:SOUR "1X10"
CH1, CH3, and NOT CH4 are logically combined with TRIGger:A:PATTern:FUNCtion, CH2 does not matter (don't care).
```

### Example: With MSO option R&S RTM-B1:

```text
TRIG:A:PATT:SOUR "XXXX111101010011XXXX"
Analog channels CH1 to CH4 do not matter (don't care). Digital channels D0 to D15 are logically combined with TRIGger:A: PATTern:FUNCtion.
```

### TRIGger:A:PATTern:FUNCtion <Function>

Sets the logical combination of the trigger states of the channels.

<!-- 来源：RTM2_UserManual_en_10_files\part308.htm -->

### Parameters:

<Function> AND | OR

<!-- 来源：RTM2_UserManual_en_10_files\part309.htm -->

### AND

The required states of all channels must appear in the input sig- nal at the same time.

<!-- 来源：RTM2_UserManual_en_10_files\part310.htm -->

### OR

At least one of the channels must have the required state.

*RST: AND

### TRIGger:A:PATTern:CONDition <ConditionString>

Sets the trigger point depending on the result of the logical combination of the channel states.

<!-- 来源：RTM2_UserManual_en_10_files\part311.htm -->

### Parameters:

<ConditionString> "TRUE" | "FALSE"

*RST: "TRUE"

### 18.5.5.2 Time Limitation

TRIGger:A:PATTern:MODE 456

TRIGger:A:PATTern:WIDTh:RANGe 456

TRIGger:A:PATTern:WIDTh[:WIDTh] 456

TRIGger:A:PATTern:WIDTh:DELTa 457

### TRIGger:A:PATTern:MODE <PatternMode>

Disables the time limitation or sets the time comparison mode.

<!-- 来源：RTM2_UserManual_en_10_files\part312.htm -->

### Parameters:

<PatternMode> OFF | TIMeout | WIDTh

<!-- 来源：RTM2_UserManual_en_10_files\part313.htm -->

### OFF

Disables the time limitation.

<!-- 来源：RTM2_UserManual_en_10_files\part314.htm -->

### TIMeout

Defines how long at least the result of the state pattern condition must be true or false.

<!-- 来源：RTM2_UserManual_en_10_files\part315.htm -->

### WIDTh

```text
Defines a time range for keeping up the true result of the pattern condition. The range is defined using TRIGger:A:PATTern: WIDTh:RANGe.
```

### TRIGger:A:PATTern:WIDTh:RANGe <PatternRange> Selects how the time limit of the pattern state is defined.

The time is specified using TRIGger:A:PATTern:WIDTh[:WIDTh] on page 456, the range around is specified using TRIGger:A:PATTern:WIDTh:DELTa

on page 457.

<!-- 来源：RTM2_UserManual_en_10_files\part316.htm -->

### Parameters:

<PatternRange> WITHin | OUTSide | SHORter | LONGer

<!-- 来源：RTM2_UserManual_en_10_files\part317.htm -->

### WITHin

Triggers if the pattern state remains unchanged longer than

Time - Delta and shorter than Time + Delta.

<!-- 来源：RTM2_UserManual_en_10_files\part318.htm -->

### OUTSide

Triggers if the pattern state remains unchanged either shorter than Time - Delta or longer than Time + Delta.

<!-- 来源：RTM2_UserManual_en_10_files\part319.htm -->

### SHORter | LONGer

Triggers if the pattern state changes before or after the specified time.

### TRIGger:A:PATTern:WIDTh[:WIDTh] <PatternWidth>

For the ranges WITHin and OUTSide, the <PatternWidth> defines the center of a range which is defined by the limits ±<Delta>.

For the ranges SHORter and LONGer, the pattern width defines the maximum and minimum values, respectively.

<!-- 来源：RTM2_UserManual_en_10_files\part320.htm -->

### Parameters:

<PatternWidth> Default unit: s

### TRIGger:A:PATTern:WIDTh:DELTa <PatternDelta>

```text
Defines a range around the pattern width value specified using TRIGger:A: PATTern:WIDTh[:WIDTh].
```

<!-- 来源：RTM2_UserManual_en_10_files\part321.htm -->

### Parameters:

<PatternDelta> Default unit: s

<!-- 来源：RTM2_UserManual_en_10_files\part322.htm -->

### 18.5.6 Runt

### TRIGger:A:RUNT:POLarity <Polarity>

Sets the polarity of a pulse, that is the direction of the first pulse slope.

<!-- 来源：RTM2_UserManual_en_10_files\part323.htm -->

### Parameters:

<Polarity> POSitive | NEGative

*RST: POS

<!-- 来源：RTM2_UserManual_en_10_files\part324.htm -->

### TRIGger:A:LEVel<n>:RUNT:LOWer <Level>

### TRIGger:A:LEVel<n>:RUNT:UPPer <Level>

Set the lower and the upper voltage threshold, respectively. The instrument triggers if the amplitude crosses the first threshold twice in succession without crossing the sec- ond one.

The upper level corresponds to the trigger level ( TRIGger:A:LEVel<n>[:VALue] on page 447). The lower level corresponds to the threshold value of the trigger channel ( CHANnel<m>:THReshold on page 426).

<!-- 来源：RTM2_UserManual_en_10_files\part325.htm -->

### Suffix:

<n> 1..5

Indicates the trigger source:

1...4 = channel 1...4 5 = not available

<!-- 来源：RTM2_UserManual_en_10_files\part326.htm -->

### Parameters:

<Level> Default unit: V

<!-- 来源：RTM2_UserManual_en_10_files\part327.htm -->

### 18.5.7 Rise Time / Fall Time Trigger

TRIGger:A:LEVel<n>:RISetime:LOWer 458

TRIGger:A:LEVel<n>:RISetime:UPPer 458

TRIGger:A:RISetime:SLOPe 458

TRIGger:A:RISetime:RANGe 458

TRIGger:A:RISetime:TIME 459

TRIGger:A:RISetime:DELTa 459

<!-- 来源：RTM2_UserManual_en_10_files\part328.htm -->

### TRIGger:A:LEVel<n>:RISetime:LOWer <Level>

### TRIGger:A:LEVel<n>:RISetime:UPPer <Level>

Set the lower and upper voltage threshold, respectively. When the signal crosses these levels, the slew rate measurement starts or stops depending on the selected polarity.

The upper level corresponds to the trigger level ( TRIGger:A:LEVel<n>[:VALue] on page 447). The lower level corresponds to the threshold value of the trigger channel ( CHANnel<m>:THReshold on page 426).

<!-- 来源：RTM2_UserManual_en_10_files\part329.htm -->

### Suffix:

<n> 1. 5

Indicates the trigger source:

1...4 = channel 1. 4

5 = not available

<!-- 来源：RTM2_UserManual_en_10_files\part330.htm -->

### Parameters:

<Level> Default unit: V

### TRIGger:A:RISetime:SLOPe <Polarity>

Sets the edge of whic the transition time is to be analyzed:

<!-- 来源：RTM2_UserManual_en_10_files\part331.htm -->

### Parameters:

<Polarity> POSitive | NEGative

POSitive: rise time trigger NEGative: Fall time trigger

*RST: POS

### TRIGger:A:RISetime:RANGe <Range>

Selects how the time limit of the rise or fall time is defined.

<!-- 来源：RTM2_UserManual_en_10_files\part332.htm -->

### Parameters:

<Range> LONGer | SHORter | WITHin | OUTSide

<!-- 来源：RTM2_UserManual_en_10_files\part333.htm -->

### LONGer | SHORter

Triggers on transition times longer or shorter than the time

```text
TRIGger:A:RISetime:TIME.
```

<!-- 来源：RTM2_UserManual_en_10_files\part334.htm -->

### WITHin | OUTSide

```text
Triggers on transition times inside or outside the time range TIMe ± DELTa. Use TRIGger:A:RISetime:TIME and TRIGger:A:RISetime:DELTa to set the time range.
```

*RST: LONG

### TRIGger:A:RISetime:TIME <RiseTime>

For the ranges LONGer and SHORter, the command defines the minimum and maxi- mum transition times, respectively.

```text
For the ranges WITHin and OUTSide, the command defines the center of a time range which is defined using TRIGger:A:RISetime:DELTa.
```

See also: TRIGger:A:RISetime:RANGe

<!-- 来源：RTM2_UserManual_en_10_files\part335.htm -->

### Parameters:

<RiseTime> Default unit: s

### TRIGger:A:RISetime:DELTa <Variation>

Sets a time range around the time value defined using TRIGger:A:RISetime:TIME

```text
if TRIGger:A:RISetime:RANGe is set to WITHin | OUTSide.
```

<!-- 来源：RTM2_UserManual_en_10_files\part336.htm -->

### Parameters:

<Variation> Default unit: s

<!-- 来源：RTM2_UserManual_en_10_files\part337.htm -->

### 18.5.8 B-Trigger

TRIGger:B:ENABle 459

TRIGger:B:SOURce 459

TRIGger:B:EDGE:SLOPe 460

TRIGger:B:LEVel 460

TRIGger:B:FINDlevel 460

TRIGger:B:MODE 460

TRIGger:B:DELay 460

TRIGger:B:EVENt:COUNt 461

TRIGger:B:HYSTeresis 461

TRIGger:B:LEVel:HYSTeresis 461

### TRIGger:B:ENABle <State>

Activates or deactivates the second trigger. The instrument triggers if both trigger event conditions (A and B) are fulfilled.

<!-- 来源：RTM2_UserManual_en_10_files\part338.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### TRIGger:B:SOURce <Source>

Selects one of the input channels as B-trigger source. Available channels depend on the instrument type.

<!-- 来源：RTM2_UserManual_en_10_files\part339.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4

*RST: CH1

### TRIGger:B:EDGE:SLOPe <Slope>

Sets the edge for the B-trigger.

<!-- 来源：RTM2_UserManual_en_10_files\part340.htm -->

### Parameters:

<Slope> POSitive | NEGative | EITHer

*RST: POSitive

### TRIGger:B:LEVel <Level>

Sets the trigger level for the B-trigger event.

<!-- 来源：RTM2_UserManual_en_10_files\part341.htm -->

### Parameters:

<Level> *RST: 0

Default unit: V

<!-- 来源：RTM2_UserManual_en_10_files\part342.htm -->

### TRIGger:B:FINDlevel

Sets the trigger level of the B-trigger event to 50% of the signal amplitude.

### Usage: Event

### TRIGger:B:MODE <Mode>

Defines the delay type of the B-trigger.

<!-- 来源：RTM2_UserManual_en_10_files\part343.htm -->

### Parameters:

<Mode> DELay | EVENts

<!-- 来源：RTM2_UserManual_en_10_files\part344.htm -->

### DELay

Time delay, set with TRIGger:B:DELay

<!-- 来源：RTM2_UserManual_en_10_files\part345.htm -->

### EVENts

Event count delay, set with TRIGger:B:EVENt:COUNt

*RST: DELay

### TRIGger:B:DELay <DelayTime>

Sets the time the instrument waits after an A-event until it recognizes B-events. Before setting the dalay time, TRIGger:B:MODE must be set to DELAy.

| Parameters: |  |  |
| --- | --- | --- |
| <DelayTime> | Range: | 20e-9 to 6,871946854 |
|  | Increment: | Depends on the <DelayTime> value. The longer the |
|  |  | <DelayTime>, the longer is the increment value. |
|  | *RST: | 20e-9 |

Default unit: s

### TRIGger:B:EVENt:COUNt <EventCnt>

Sets a number of B-trigger events that fulfill all B-trigger conditions but do not cause the trigger. The oscilloscope triggers on the n-th event (the last of the specified number of events).

Before setting the event number, TRIGger:B:MODE must be set to EVENts.

<!-- 来源：RTM2_UserManual_en_10_files\part346.htm -->

### Parameters:

<EventCnt> Number of B-events

Range: 1 to 65535

Increment: 1

*RST: 1

### TRIGger:B:HYSTeresis <Hysteresis>

Sets a hysteresis range around the trigger level of the B trigger event. If the signal jit- ters inside this range and crosses the trigger level thereby, no trigger event occurs.

<!-- 来源：RTM2_UserManual_en_10_files\part347.htm -->

### Parameters:

<Hysteresis> AUTO | SMALl | MEDium | LARGe | MANual

<!-- 来源：RTM2_UserManual_en_10_files\part348.htm -->

### MANual

```text
Sets the hysteresis to a user-defined value, which is defined using TRIGger:B:LEVel:HYSTeresis.
```

The value is only available on instruments with 1 GHz band- width.

*RST: AUTO

### TRIGger:B:LEVel:HYSTeresis <HysteresisValue>

```text
Sets the hysteresis value if TRIGger:B:HYSTeresis is set to MANual. The com- mand is only available on instruments with 1 GHz bandwidth.
```

<!-- 来源：RTM2_UserManual_en_10_files\part349.htm -->

### Parameters:

<HysteresisValue> Default unit: DIV

<!-- 来源：RTM2_UserManual_en_10_files\part350.htm -->

## 18.6 Display

<!-- 来源：RTM2_UserManual_en_10_files\part351.htm -->

### 18.6.1 Basic Display Settings

This chapter describes commands that configure the screen display.

### 18.6.1.1 General Display Settings

DISPlay:DIALog:CLOSe 462

DISPlay:DIALog:MESSage 462

DISPlay:MODE 462

DISPlay:PALette 463

DISPlay:DIALog:TRANsparency 463

### DISPlay:DIALog:CLOSe Closes an open dialog box. Usage: Event

### DISPlay:DIALog:MESSage <MessageText>

```text
Sends a message text to the instrument and displays it in a message box. To close the message box, use DISPlay:DIALog:CLOSe.
```

<!-- 来源：RTM2_UserManual_en_10_files\part352.htm -->

### Setting parameters:

<MessageText> String

String that contains the message.

### Example: DISP:DIAL:MESS 'My message' DISP:DIAL:CLOS

### Usage: Setting only

### DISPlay:MODE <Mode> Sets the diagram mode.

<!-- 来源：RTM2_UserManual_en_10_files\part353.htm -->

### Parameters:

<Mode> YT | XY

<!-- 来源：RTM2_UserManual_en_10_files\part354.htm -->

### YT

Default time diagram with a time axis in x-direction and the sig- nal amplitudes displayed in y-direction.

<!-- 来源：RTM2_UserManual_en_10_files\part355.htm -->

### XY

XY-diagram, combines the voltage levels of two waveforms in one diagram.

*RST: YT

### DISPlay:PALette <Palette>

Sets the color and brightness of the displayed waveform samples depending on their cumulative occurance.

<!-- 来源：RTM2_UserManual_en_10_files\part356.htm -->

### Parameters:

<Palette> NORMal | INVerse | FCOLor | IFColor

<!-- 来源：RTM2_UserManual_en_10_files\part357.htm -->

### NORMal

Values that occur frequently are brighter than rare values.

<!-- 来源：RTM2_UserManual_en_10_files\part358.htm -->

### INVerse

Rare values are brighter than frequent values, inverse to the NORMal brightness.

<!-- 来源：RTM2_UserManual_en_10_files\part359.htm -->

### FColor

Rare values are displayed in blue, while more frequent values are red and very frequent values are displayed in yellow or white, with various colors inbetween.

<!-- 来源：RTM2_UserManual_en_10_files\part360.htm -->

### IFColor

Inverses the FColor setting: rare values are yellow or white while frequent values are blue.

*RST: NORMal

### DISPlay:DIALog:TRANsparency <Transparency>

Sets the transparency of result boxes that overlay the waveforms, for example, boxes with statistical results or digital voltmeter results.

<!-- 来源：RTM2_UserManual_en_10_files\part361.htm -->

### Parameters:

<Transparency> Range: 0 to 100

Increment: 1 Default unit: %

### 18.6.1.2 XYZ-Setup

DISPlay:XY:XSOurce 463

DISPlay:XY:Y1Source 464

DISPlay:XY:Y2Source 464

DISPlay:XY:ZMODe 464

DISPlay:XY:ZTHReshold 465

DISPlay:XY:ZSOurce 465

### DISPlay:XY:XSOurce <Source>

Defines the source to be displayed in x direction in an XY-diagram, replacing the usual time base.

<!-- 来源：RTM2_UserManual_en_10_files\part362.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4

CH3 and CH4 are only available with 4-channel R&S RTM oscil- loscopes.

*RST: CH1

### DISPlay:XY:Y1Source <Source>

Defines the (first) source to be displayed in y direction in an XY-diagram.

<!-- 来源：RTM2_UserManual_en_10_files\part363.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4

CH3 and CH4 are only available with 4-channel R&S RTM oscil- loscopes.

*RST: CH2

### DISPlay:XY:Y2Source <Source>

Defines an optional second source to be displayed in y direction in an XY-diagram. The command is only relevant for 4-channel R&S RTM instruments.

<!-- 来源：RTM2_UserManual_en_10_files\part364.htm -->

### Parameters:

<Source> NONE | CH1 | CH2 | CH3 | CH4

*RST: NONE

### DISPlay:XY:ZMODe <Mode>

Activates or deactivates the intensity control of the waveform via an additional signal source and sets the intensity mode.

<!-- 来源：RTM2_UserManual_en_10_files\part365.htm -->

### Parameters:

<Mode> ANALog | DIGital | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part366.htm -->

### ANALog

Modulated intensity; Intensity is modulated continuously accord- ing to the selected Source Z.

<!-- 来源：RTM2_UserManual_en_10_files\part367.htm -->

### DIGital

```text
Intensity is determined by a threshold value defined with DISPlay:XY:ZTHReshold. If the Z signal value is below the selected threshold, the corresponding x/y point is not displayed. If the Z signal value is above the threshold, the x/y point is dis- played with the defined intensity level.
```

<!-- 来源：RTM2_UserManual_en_10_files\part368.htm -->

### OFF

Intensity control is deactivated.

*RST: OFF

### DISPlay:XY:ZTHReshold <Zthreshold>

Defines the threshold for intensity with a two-state modulation, if DISPlay:XY:ZMODe

is set to DIGital.

<!-- 来源：RTM2_UserManual_en_10_files\part369.htm -->

### Parameters:

<Zthreshold> Threshold for visibility on the screen

Range: -10 to 10

Increment: depends on the scaling of the channel that is assigned to Z

*RST: 0

Default unit: V

### DISPlay:XY:ZSOurce <Source>

Defines the source to be used to determine the intensity of the xy-waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part370.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4

CH3 and CH4 are only available with 4-channel R&S RTM oscil- loscopes.

*RST: CH1

### 18.6.1.3 Intensities

DISPlay:INTensity:WAVeform 465

DISPlay:INTensity:BACKlight 465

DISPlay:INTensity:GRID 466

DISPlay:PERSistence:STATe 466

DISPlay:PERSistence:TIME 466

DISPlay:PERSistence:INFinite 467

DISPlay:PERSistence:TIME:AUTO 467

DISPlay:PERSistence:CLEar 467

### DISPlay:INTensity:WAVeform <Intensity>

Defines the strength of the waveform line in the diagram.

<!-- 来源：RTM2_UserManual_en_10_files\part371.htm -->

### Parameters:

<Intensity> Value in percent

Range: 0 to 100

Increment: 1

*RST: not available, *RST does not change the intensity Default unit: %

### DISPlay:INTensity:BACKlight <Intensity>

Defines the intensity of the background lighting of the display.

<!-- 来源：RTM2_UserManual_en_10_files\part372.htm -->

### Parameters:

<Intensity> Value in percent

Range: 10 to 100

Increment: 1

*RST: not available, *RST does not change the intensity Default unit: %

### DISPlay:INTensity:GRID <Intensity>

Defines the intensity of the grid on the screen.

<!-- 来源：RTM2_UserManual_en_10_files\part373.htm -->

### Parameters:

<Intensity> Value in percent

Range: 0 to 100

Increment: 1

*RST: not available, *RST does not change the intensity Default unit: %

### DISPlay:PERSistence:STATe <State>

Defines whether the waveform persists on the screen or whether the screen is refreshed continuously.

<!-- 来源：RTM2_UserManual_en_10_files\part374.htm -->

### Parameters:

<State> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part375.htm -->

### ON

```text
The waveform persists for the time defined using DISPlay: PERSistence:TIME.
```

<!-- 来源：RTM2_UserManual_en_10_files\part376.htm -->

### OFF

The waveform does not persist on the screen. Only the currently measured values are displayed at any time.

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part377.htm -->

### DISPlay:PERSistence:TIME <Time>

Persistence time if persistence is active (see DISPlay:PERSistence:STATe

on page 466).

```text
Each new data point in the diagram area remains on the screen for the duration defined here. To set infinite persistence, use DISPlay:PERSistence:INFinite.
```

<!-- 来源：RTM2_UserManual_en_10_files\part378.htm -->

### Parameters:

<Time> Range: 50E-3 to Infinite

Increment: minimum 50E-3 s, increasing increment with increasing persistence time

*RST: 50E-3

Default unit: s

### DISPlay:PERSistence:INFinite <InfPersistence>

```text
Sets the persistence time to infinite if DISPlay:PERSistence:STATe is ON. each new data point remains on the screen infinitely until this setting is changed or the per- sistence is cleared.
```

<!-- 来源：RTM2_UserManual_en_10_files\part379.htm -->

### Parameters:

<InfPersistence> ON | OFF

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part380.htm -->

### DISPlay:PERSistence:TIME:AUTO <Auto>

The optimal persistence time is determined automatically by the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part381.htm -->

### Parameters:

<Auto> ON | OFF

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part382.htm -->

### DISPlay:PERSistence:CLEar

Removes the displayed persistent waveform from the screen.

### Usage: Event

### 18.6.1.4 Waveform, Auxilary Cursors and Grid Settings

DISPlay:STYLe 467

DISPlay:GRID:STYLe 467

### DISPlay:STYLe <Style>

Defines how the waveform data is displayed

<!-- 来源：RTM2_UserManual_en_10_files\part383.htm -->

### Parameters:

<Style> VECTors | DOTS

<!-- 来源：RTM2_UserManual_en_10_files\part384.htm -->

### VECTors

Individual data points are connected by a line.

<!-- 来源：RTM2_UserManual_en_10_files\part385.htm -->

### DOTS

Only the data points are displayed.

*RST: VECT

### DISPlay:GRID:STYLe <Style> Defines how the grid is displayed.

<!-- 来源：RTM2_UserManual_en_10_files\part386.htm -->

### Parameters:

<Style> LINes | RETicle | NONE

<!-- 来源：RTM2_UserManual_en_10_files\part387.htm -->

### LINes

Displays the grid as horizontal and vertical lines.

<!-- 来源：RTM2_UserManual_en_10_files\part388.htm -->

### RETicle

Displays crosshairs instead of a grid.

<!-- 来源：RTM2_UserManual_en_10_files\part389.htm -->

### NONE

No grid is displayed.

*RST: LIN

### 18.6.1.5 Virtual Screen

DISPlay:VSCReen:ENABle 468

DISPlay:VSCReen:POSition 468

### DISPlay:VSCReen:ENABle <Enable>

Enables or disables the virtual screen. If enabled, the virtual screen has 20 divisions, 8 of them are displayed.

<!-- 来源：RTM2_UserManual_en_10_files\part390.htm -->

### Parameters:

<Enable> ON | OFF

*RST: OFF

### DISPlay:VSCReen:POSition <Position>

Selects the divisions to be displayed on the virtual screen. The virtual screen has 20 divisions, 8 of them are displayed.

<!-- 来源：RTM2_UserManual_en_10_files\part391.htm -->

### Parameters:

<Position> Indicated the position of the middle visible division.

Range: -6 to 6. At -6, the lower 8 divisons are visible. 0 indi- cates the center of the virtual screen, and the div- ions -4 to 4 are visible.

<!-- 来源：RTM2_UserManual_en_10_files\part392.htm -->

### 18.6.2 Zoom

TIMebase:ZOOM:STATe 468

TIMebase:ZOOM:SCALe 469

TIMebase:ZOOM:TIME 469

TIMebase:ZOOM:POSition 469

ACQuire:SRATe:ZOOM? 469

### TIMebase:ZOOM:STATe <ZoomState> Switches the zoom window on or off.

<!-- 来源：RTM2_UserManual_en_10_files\part393.htm -->

### Parameters:

<ZoomState> ON | OFF

*RST: OFF

### TIMebase:ZOOM:SCALe <ZoomScale>

Defines the time base in the zoom diagram in seconds per division.

<!-- 来源：RTM2_UserManual_en_10_files\part394.htm -->

### Parameters:

<ZoomScale> Range: Depends on various other settings

Default unit: s/DIV

### TIMebase:ZOOM:TIME <Time>

Defines the offset of the trigger point to the reference point of the zoom diagram.

<!-- 来源：RTM2_UserManual_en_10_files\part395.htm -->

### Parameters:

<Time> *RST: 0

Default unit: s

### TIMebase:ZOOM:POSition <Position>

Defines the position of the zoom reference point (the reference point of the zoom win- dow) in relation to the reference point of original time base.

<!-- 来源：RTM2_UserManual_en_10_files\part396.htm -->

### Parameters:

<Position> Range: Depends on the zoom time base, nearly 0 to 100 % for large zoom

*RST: 50

Default unit: %

<!-- 来源：RTM2_UserManual_en_10_files\part397.htm -->

### ACQuire:SRATe:ZOOM?

Returns the sample rate of the zoom window.

<!-- 来源：RTM2_UserManual_en_10_files\part398.htm -->

### Return values:

<SampleRateZoom> Range: 2 to 1E11

Increment: 1E3

*RST: 1E7

Default unit: Sa/s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part399.htm -->

### 18.6.3 Markers (Timestamps)

TSTamp:SET 470

TSTamp:NEXT 470

TSTamp:PREVious 470

TSTamp:CLEar 470

TSTamp:ACLear 470

<!-- 来源：RTM2_UserManual_en_10_files\part400.htm -->

### TSTamp:SET

```text
Sets a new marker (timestamp) at the reference point of the display, unless an existing marker is already set there. The reference point is set with TIMebase:REFerence.
```

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part401.htm -->

### TSTamp:NEXT

### Usage: Event

Moves the next marker (timestamp, to the right) to the reference point of the display or zoom area.

<!-- 来源：RTM2_UserManual_en_10_files\part402.htm -->

### TSTamp:PREVious

Moves the previous marker (timestamp, to the left) to the reference point of the display or zoom area.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part403.htm -->

### TSTamp:CLEar

Deletes the marker (timestamp) at the reference point. The reference point is set with

```text
TIMebase:REFerence.
```

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part404.htm -->

### TSTamp:ACLear

Deletes all markers (timestamps).

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part405.htm -->

## 18.7 Reference Waveforms

For data queries and conversion, consider also the following commands:

- FORMat[:DATA] on page 731

- REFCurve<m>:DATA:XINCrement? on page 742

- REFCurve<m>:DATA:XORigin? on page 742

- REFCurve<m>:DATA:YINCrement? on page 743

- REFCurve<m>:DATA:YORigin? on page 743

- REFCurve<m>:DATA:YRESolution? on page 743

REFCurve<m>:STATe 471

REFCurve<m>:SOURce 471

REFCurve<m>:SOURce:CATalog? 472

REFCurve<m>:UPDate 472

REFCurve<m>:SAVE 472

REFCurve<m>:LOAD 472

REFCurve<m>:LOAD:STATe 473

REFCurve<m>:HORizontal:SCALe 473

REFCurve<m>:HORizontal:POSition 473

REFCurve<m>:VERTical:SCALe 473

REFCurve<m>:VERTical:POSition 474

REFCurve<m>:DATA? 474

REFCurve<m>:DATA:HEADer? 474

REFCurve<m>:DATA:POINts? 475

### REFCurve<m>:STATe <State>

Displays or hides the selected reference waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part406.htm -->

### Suffix:

<m> 1. 4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part407.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### REFCurve<m>:SOURce <Source>

Defines the source of the reference waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part408.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part409.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | MA1 | MA2 | MA3 | MA4 | RE1 | RE2 | RE3 | RE4 | D70 | D158

Any active channel, math, or reference waveform. Available channels depend on the instrument type.

If MSO option R&S RTM-B1 is installed, you can use also the pods as reference source: D70 is the pod with digital channels D0 to D7, and D158 is the pod with D8 to D15.

*RST: CH1

<!-- 来源：RTM2_UserManual_en_10_files\part410.htm -->

### REFCurve<m>:SOURce:CATalog?

Returns the source waveform - channel, math or reference waveform.

If MSO option R&S RTM-B1 is installed, the source can also be a pod: D70 is the pod with digital channels D0 to D7, and D158 is the pod with D8 to D15.

<!-- 来源：RTM2_UserManual_en_10_files\part411.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part412.htm -->

### Return values:

<Catalog> CH1 | CH2 | CH3 | CH4 | MA1 | MA2 | MA3 | MA4 | RE1 | RE2 | RE3 | RE4 | D70 | D158

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part413.htm -->

### REFCurve<m>:UPDate

```text
Updates the selected reference by the waveform defined with REFCurve<m>:SOURce.
```

<!-- 来源：RTM2_UserManual_en_10_files\part414.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

### Usage: Event

### REFCurve<m>:SAVE <FileName>

Stores the reference waveform the specified file.

<!-- 来源：RTM2_UserManual_en_10_files\part415.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part416.htm -->

### Setting parameters:

<FileName> String with path and file name

### Usage: Setting only

### REFCurve<m>:LOAD <FileName>

```text
Loads the waveform data from the indicated reference file to the reference storage. To load the instrument settings, use REFCurve<m>:LOAD:STATe.
```

<!-- 来源：RTM2_UserManual_en_10_files\part417.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part418.htm -->

### Setting parameters:

<FileName> String with path and file name

### Usage: Setting only

<!-- 来源：RTM2_UserManual_en_10_files\part419.htm -->

### REFCurve<m>:LOAD:STATe

Loads the instrument settings in addition to the reference waveform data. The wave- form data must be loaded before the settings, see REFCurve<m>:LOAD on page 472.

The settings are only available if the file was stored to the internal storage /INT/ REFERENCE and never written to an external storage (USB stick).

<!-- 来源：RTM2_UserManual_en_10_files\part420.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part421.htm -->

### REFCurve<m>:HORizontal:SCALe <Scale>

Changes the horizontal scale (timebase) of the reference waveform independent of the channel waveform settings.

<!-- 来源：RTM2_UserManual_en_10_files\part422.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part423.htm -->

### Parameters:

<Scale> *RST: 100e-6 Default unit: s/DIV

### REFCurve<m>:HORizontal:POSition <Position>

Changes the horizontal position of the reference waveform independent of the channel waveform settings.

<!-- 来源：RTM2_UserManual_en_10_files\part424.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part425.htm -->

### Parameters:

<Position> *RST: 0

Default unit: s

### REFCurve<m>:VERTical:SCALe <Scale>

Changes the vertical scale of the reference waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part426.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part427.htm -->

### Parameters:

<Scale> *RST: 1

Default unit: V/DIV

### REFCurve<m>:VERTical:POSition <Position> Changes the vertical position of the reference waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part428.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part429.htm -->

### Parameters:

<Position> *RST: 0

Default unit: DIV

<!-- 来源：RTM2_UserManual_en_10_files\part430.htm -->

### REFCurve<m>:DATA?

Returns the data of the reference waveform for transmission from the instrument to the controlling computer. The waveforms data can be used in MATLAB, for example.

To set the export format, use FORMat[:DATA] on page 731.

<!-- 来源：RTM2_UserManual_en_10_files\part431.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part432.htm -->

### Return values:

<Data> List of values according to the format settings.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part433.htm -->

### REFCurve<m>:DATA:HEADer?

Returns information on the reference waveform.

#### Table 18-3: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Record length of the waveform in Samples | 200000 |
| 4 | Number of values per sample interval, usually 1. | 1 |

<!-- 来源：RTM2_UserManual_en_10_files\part434.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part435.htm -->

### Parameters:

<Header> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part436.htm -->

### REFCurve<m>:DATA:POINts?

```text
Returns the number of data samples that are returned with REFCurve<m>:DATA?.
```

<!-- 来源：RTM2_UserManual_en_10_files\part437.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part438.htm -->

### Return values:

<DataPoints> Amount of data points

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part439.htm -->

## 18.8 Measurements

This chapter describes functions that configure or perform cursor and automatic mea- surements.

- Cursor Measurements 475

- Quick Measurements 484

- Automatic Measurements 485

- Automatic Measurements - Statistics 490

- Reference Level 495

<!-- 来源：RTM2_UserManual_en_10_files\part440.htm -->

### 18.8.1 Cursor Measurements

CURSor<m>:AOFF 476

CURSor<m>:STATe 476

CURSor<m>:SOURce 476

CURSor<m>:FUNCtion 477

CURSor<m>:TRACking[:STATe] 479

CURSor<m>:X1Position 479

CURSor<m>:X2Position 479

CURSor<m>:X3Position 479

CURSor<m>:Y1Position 479

CURSor<m>:Y2Position 479

CURSor<m>:Y3Position 479

CURSor<m>:YCOupling 480

CURSor<m>:XCOupling 480

CURSor<m>:SWAVe 480

CURSor<m>:SSCReen 480

CURSor<m>:SPPeak 480

CURSor<m>:SNPeak 480

CURSor<m>:TRACking:SCALe[:STATe] 481

CURSor<m>:RESult? 481

CURSor<m>:XDELta:INVerse? 481

CURSor<m>:XDELta[:VALue]? 481

CURSor<m>:YDELta:SLOPe? 482

CURSor<m>:YDELta[:VALue]? 482

CURsor<m>:XRATio:UNIT 482

CURSor<m>:XRATio[:VALue]? 483

CURSor<m>:YRATio:UNIT 483

CURSor<m>:YRATio[:VALue]? 483

<!-- 来源：RTM2_UserManual_en_10_files\part441.htm -->

### CURSor<m>:AOFF

Switches the cursor off.

<!-- 来源：RTM2_UserManual_en_10_files\part442.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

### Usage: Event

### CURSor<m>:STATe <State>

Activates or deactivates the cursor measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part443.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part444.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### CURSor<m>:SOURce <Source>

Defines the source of the cursor measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part445.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part446.htm -->

### Parameters:

<Source> NONE | CH1 | CH2 | CH3 | CH4 | MA1 | MA2 | MA3 | MA4 | MA5 | RE1 | RE2 | RE3 | RE4 | XY1 | XY2 | D0..D15 | D70 |

D158 | SPECtrum | MINHold | MAXHold | AVERage

<!-- 来源：RTM2_UserManual_en_10_files\part447.htm -->

### CH1 | CH2 | CH3 | CH4

Active channel waveform 1 to 4

<!-- 来源：RTM2_UserManual_en_10_files\part448.htm -->

### MA1 | MA2 | MA3 | MA4 | MA5

Active math channels 1 to 5

<!-- 来源：RTM2_UserManual_en_10_files\part449.htm -->

### RE1 | RE2 | RE3 | RE4

Active reference channels 1 to 4

<!-- 来源：RTM2_UserManual_en_10_files\part450.htm -->

### XY1

Active XY-waveform

<!-- 来源：RTM2_UserManual_en_10_files\part451.htm -->

### D0..D15

Active igital channels D0 to D15, available if MSO option

R&S RTM-B1 is installed. The following cursor measurements are possible: time, ratio X, count, duty ratio, burst width. Availa- ble sources depend on the selected measurement type.

<!-- 来源：RTM2_UserManual_en_10_files\part452.htm -->

### D70 | D158

Active digital pods D0...D7 and D8...D15, available if MSO option R&S RTM-B1 is installed. The following cursor measure- ments are possible: V-marker.

<!-- 来源：RTM2_UserManual_en_10_files\part453.htm -->

### SPECtrum | MINHold | MAXHold | AVERage

Available if option R&S RTM-K18 is installed. The measurement source is a spectrum analysis waveform.

SPECtrum: normal spectrum waveform

MINHold: waveform of the minimum amplitude spectrum MAXHold: waveform of the maximum amplitude spectrum AVERage: avarage amplitude spectrum

*RST: CH1

### CURSor<m>:FUNCtion <Type> Defines the cursor measurement type.

<!-- 来源：RTM2_UserManual_en_10_files\part454.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part455.htm -->

### Parameters:

<Type> HORizontal | VERTical | PAIRed | HRATio | VRATio | PPCount | NPCount | RECount | FECount | MEAN | RMS | RTIMe | FTIMe | PEAK | UPEakvalue | LPEakvalue | BWIDth

*RST: VERT

| Value | Description | Queries for results |
| --- | --- | --- |
| HORizontal | Sets two horizontal cursor lines and measures the vol- tages at the two cursor positions and the delta of the two values. | CURSor<m>:Y1Position CURSor<m>:Y2Position CURSor<m>:YDELta[:VALue]? CURSor<m>:YDELta:SLOPe? |
| VERTical | Sets two vertical cursor lines and measures the time from the trigger point to each cursor, the time between the two cursors and the frequency calculated from that time. | CURSor<m>:X1Position CURSor<m>:X2Position CURSor<m>:XDELta[:VALue]? CURSor<m>:XDELta:INVerse? |
| PAIRed | V-Marker same as CURSor<m>:TRACking[:STATe] | CURSor<m>:Y1Position CURSor<m>:Y2Position CURSor<m>:XDELta[:VALue]? CURSor<m>:YDELta[:VALue]? |
| HRATio | Sets three horizontal cursor lines. Queries return the ratio of the y-values (e.g. overshooting) between the first and second cursors and the first and third cursors. | CURSor<m>:YRATio:UNIT CURSor<m>:YRATio[:VALue]? CURSor<m>:Y1Position CURSor<m>:Y2Position CURSor<m>:Y3Position |
| VRATio | Sets three vertical cursor lines. Queries return the ratio of the x-values (e.g. a duty cycle) between the first and second cursors and the first and third cursors. | CURsor<m>:XRATio:UNIT CURSor<m>:XDELta[:VALue]? CURSor<m>:X1Position CURSor<m>:X2Position CURSor<m>:X3Position |
| PPCount NPCount RECount FECount | Count positive pulses Count negative pulses Count rising edges Count falling edges Sets two vertical and one horizontal cursor line. The time base is defined by the vertical cursors, the hori- zontal cursor defines the threshold value. | CURSor<m>:RESult? |
| MEAN RMS | Mean value Root mean square Values are measured between two vertical cursor lines. | CURSor<m>:RESult? |
| RTIMe FTIMe | Rise time, tr Fall time, tf Measures the rise or fall time of the first edge after the first vertical cursor between the upper and lower refer- ence levels. The reference level for rise and fall time measurement is set with REFLevel:RELative: MODE. | CURSor<m>:RESult? |

| Value | Description | Queries for results |
| --- | --- | --- |
| PEAK | Vpp, absolute difference between the two peak values | CURSor<m>:RESult? |
| UPEakvalue | Vp+, upper peak value |  |
| LPEakvalue | Vp-, lower peak value |  |
|  | Values are measured between two vertical cursor lines. |  |
| BWIDth | Burst width, the duration of a burst. Two vertical cur- sors mark the beginning and the end of the burst. The horizontal cursor sets the threshold value, and the time between the first and the last edge of the burst is returned. | CURSor<m>:RESult? |

### CURSor<m>:TRACking[:STATe] <State>

If set to ON, the V-Marker cursor measurement is enabled.

<!-- 来源：RTM2_UserManual_en_10_files\part456.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part457.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### CURSor<m>:X1Position <Xposition1> CURSor<m>:X2Position <Xposition2> CURSor<m>:X3Position <Xposition3>

The commands specify the x-positions of vertical cursor lines on the time axis. The third cursor is only used for Ratio X measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part458.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part459.htm -->

### Parameters:

<Position> Range: Depends on horizontal settings.

### CURSor<m>:Y1Position <Yposition1> CURSor<m>:Y2Position <Yposition2> CURSor<m>:Y3Position <Yposition3>

The commands specify the positions of horizontal cursor lines on the y-axis. The third cursor is only used for Ratio Y measurements.

<!-- 来源：RTM2_UserManual_en_10_files\part460.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part461.htm -->

### Parameters:

<Position> Range: Depends on various other settings.

### CURSor<m>:YCOupling <Coupling>

### CURSor<m>:XCOupling <Coupling>

If enabled, the cursors of a set are coupled so that the distance between the two remains the same if one cursor is moved.

<!-- 来源：RTM2_UserManual_en_10_files\part462.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part463.htm -->

### Parameters:

<Coupling> ON | OFF

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part464.htm -->

### CURSor<m>:SWAVe

Autoset for cursor lines, sets the cursor lines to typical points of the waveform depend- ing on the selected measurement type. For example, for voltage measurement, the cursor lines are set to the upper and lower peaks of the waveform. For time measure- ment, the cursor lines are set to the edges of two consecutive positive or two consecu- tive negative pulses.

### Usage: Event

### Firmware/Software: FW 03.700

<!-- 来源：RTM2_UserManual_en_10_files\part465.htm -->

### CURSor<m>:SSCReen

Resets the cursors to their initial positions. This is helpful if the cursors have disap- peared from the display or need to be moved for a larger distance.

### Usage: Event

### Firmware/Software: FW 03.700

<!-- 来源：RTM2_UserManual_en_10_files\part466.htm -->

### CURSor<m>:SPPeak

For FFT analysis only: sets the selected cursor to the previous (left) level peak.

### Usage: Event

### Firmware/Software: FW 03.700

<!-- 来源：RTM2_UserManual_en_10_files\part467.htm -->

### CURSor<m>:SNPeak

For FFT analysis only: sets the selected cursor to the next (right) level peak.

### Usage: Event

### Firmware/Software: FW 03.700

<!-- 来源：RTM2_UserManual_en_10_files\part468.htm -->

### CURSor<m>:TRACking:SCALe[:STATe] <State>

Enables the adjustment of cursor lines if the vertical or horizontal scales are changed.

<!-- 来源：RTM2_UserManual_en_10_files\part469.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part470.htm -->

### Parameters:

<State> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part471.htm -->

### ON

Cursor lines keep their relative position to the waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part472.htm -->

### OFF

Cursor lines remain on their position on the display if the scaling is changed.

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part473.htm -->

### CURSor<m>:RESult?

```text
Returns the measurement result for count, mean, RMS, rise and fall time, peak mea- surements, and burst width. Make sure to set CURSor<m>:FUNCtion correctly.
```

<!-- 来源：RTM2_UserManual_en_10_files\part474.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part475.htm -->

### Return values:

<Value> Measurement result

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part476.htm -->

### CURSor<m>:XDELta:INVerse?

Returns the inverse time difference between the two cursors (1/Δt).

<!-- 来源：RTM2_UserManual_en_10_files\part477.htm -->

### Suffix:

| <m> | 1 The numeric | suffix is irrelevant. |
| --- | --- | --- |
| Return values: <DeltaInverse> | Range: | -100e24 to 100e24 |
|  | Increment: | 0.1 |
|  | *RST: Default unit: | 0 1/s |
| Usage: | Query only |  |

### CURSor<m>:XDELta[:VALue]?

Returns the time difference between the two cursors (Δt).

| Suffix: <m> | 1 |  |
| --- | --- | --- |
|  | The numeric | suffix is irrelevant. |
| Return values: <Delta> | Range: | -100e24 to 100e24 |
|  | Increment: | 0.1 |
|  | *RST: Default unit: | 0 s |
| Usage: | Query only |  |

<!-- 来源：RTM2_UserManual_en_10_files\part478.htm -->

### CURSor<m>:YDELta:SLOPe?

Returns the inverse value of the voltage difference - the reciprocal of the vertical dis- tance of two horizontal cursor lines: 1/ Δ V.

<!-- 来源：RTM2_UserManual_en_10_files\part479.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part480.htm -->

### Return values:

<DeltyYslope> Inverse value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part481.htm -->

### CURSor<m>:YDELta[:VALue]?

Queries the delta of the values in y-direction at the two cursors.

<!-- 来源：RTM2_UserManual_en_10_files\part482.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part483.htm -->

### Return values:

<DeltaY> Delta value in V

### Usage: Query only

### CURsor<m>:XRATio:UNIT <Unit>

```text
Sets the unit for X Ratio measurements with CURSor<m>:XRATio[:VALue]?.
```

<!-- 来源：RTM2_UserManual_en_10_files\part484.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part485.htm -->

### Parameters:

<Unit> RATio | PCT | GRD | PI

RATio - floating value PCT - percent

GRD - degree PI - radian

*RST: RAT

<!-- 来源：RTM2_UserManual_en_10_files\part486.htm -->

### CURSor<m>:XRATio[:VALue]?

Returns the ratio of the x-values (e.g. a duty cycle) between the first and second cur- sors and the first and third cursors: (x2-x1)/(x3-x1).

```text
Set the unit of the result with CURsor<m>:XRATio:UNIT.
```

<!-- 来源：RTM2_UserManual_en_10_files\part487.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part488.htm -->

### Return values:

<Ratio> Numeric value corresponding to the specified unit.

### Usage: Query only

### CURSor<m>:YRATio:UNIT <Unit>

Sets the unit for Y Ratio measurements with CURSor<m>:YRATio[:VALue]?

on page 483.

<!-- 来源：RTM2_UserManual_en_10_files\part489.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part490.htm -->

### Parameters:

<Unit> RATio | PCT

RATio - floating value PCT - percent

*RST: RAT

<!-- 来源：RTM2_UserManual_en_10_files\part491.htm -->

### CURSor<m>:YRATio[:VALue]?

Returns the ratio of the y-values (e.g. overshooting) between the first and second cur- sors and the first and third cursors: (y2-y1)/(y3-y1).

```text
For this measurement, set the cursor measurement type CURSor<m>:FUNCtion to
HRATio.
Set the unit of the result with CURSor<m>:YRATio:UNIT.
```

<!-- 来源：RTM2_UserManual_en_10_files\part492.htm -->

### Suffix:

<m> 1

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part493.htm -->

### Return values:

<Ratio> Numeric value corresponding to the specified unit.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part494.htm -->

### 18.8.2 Quick Measurements

MEASurement<m>:ALL[:STATe] 484

MEASurement<m>:AON 484

MEASurement<m>:AOFF 484

MEASurement<m>:ARESult? 484

### MEASurement<m>:ALL[:STATe] <State>

Starts or stops the quick measurement and sets the status bit.

<!-- 来源：RTM2_UserManual_en_10_files\part495.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### Firmware/Software: FW 03.800

<!-- 来源：RTM2_UserManual_en_10_files\part496.htm -->

### MEASurement<m>:AON

Starts the quick measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part497.htm -->

### Suffix:

<m> 1..4

The numeric suffix is irrelevant.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part498.htm -->

### MEASurement<m>:AOFF

Stops the quick measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part499.htm -->

### Suffix:

<m> 1..4

The numeric suffix is irrelevant.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part500.htm -->

### MEASurement<m>:ARESult?

Returns the results of the quick measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part501.htm -->

### Suffix:

<m> 1..4

Selects the measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part502.htm -->

### Return values:

<QuickMeasData> List of values

Quick measurement results are listed in the following order: PEAK, UPE, LPE, RMS, MEAN, PER, FREQ, RTIM, FTIM

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part503.htm -->

### 18.8.3 Automatic Measurements

MEASurement<m>[:ENABle] 485

MEASurement<m>:MAIN 485

MEASurement<m>:SOURce 487

MEASurement<m>:DELay:SLOPe 489

MEASurement<m>:RESult[:ACTual]? 489

MEASurement<m>:CATegory? 489

### MEASurement<m>[:ENABle] <State>

Activates or deactivates the selected measurement (1-4). Only the results of active measurements are displayed in the result table.

<!-- 来源：RTM2_UserManual_en_10_files\part504.htm -->

### Suffix:

<m> 1. 4

Selects the measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part505.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### MEASurement<m>:MAIN <MeasType>

```text
Defines the measurement type to be performed on the selected source. To query the results, use MEASurement<m>:RESult[:ACTual]?.
```

<!-- 来源：RTM2_UserManual_en_10_files\part506.htm -->

### Suffix:

<m> 1..4

Selects the measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part507.htm -->

### Parameters:

<MeasType> FREQuency | PERiod | PEAK | UPEakvalue | LPEakvalue | PPCount | NPCount | RECount | FECount | HIGH | LOW | AMPLitude | MEAN | RMS | RTIMe | FTIMe | PDCYcle | NDCYcle | PPWidth | NPWidth | CYCMean | CYCRms | STDDev | CYCStddev | TFRequency | TPERiode | DELay | PHASe | BWIDth | POVershoot | NOVershoot | TBFRequency | TBPeriod

For a detailed description, see "Meas. Type" on page 115.

<!-- 来源：RTM2_UserManual_en_10_files\part508.htm -->

### FREQuency

Frequency of the signal. The result is based on the length of the left-most signal period within the displayed section of the wave- form of the selected channel.

<!-- 来源：RTM2_UserManual_en_10_files\part509.htm -->

### PERiod

Length of the left-most signal period within the displayed section of the waveform of the selected channel.

<!-- 来源：RTM2_UserManual_en_10_files\part510.htm -->

### PEAK

Peak-to-peak value within the displayed section of the waveform of the selected channel.

<!-- 来源：RTM2_UserManual_en_10_files\part511.htm -->

### UPEakvalue

Maximum value within the displayed section of the waveform of the selected channel.

<!-- 来源：RTM2_UserManual_en_10_files\part512.htm -->

### LPEakvalue

Minimum value within the displayed section of the waveform of the selected channel.

<!-- 来源：RTM2_UserManual_en_10_files\part513.htm -->

### PPCount

Counts positive pulses.

<!-- 来源：RTM2_UserManual_en_10_files\part514.htm -->

### NPCount

Counts negative pulses.

<!-- 来源：RTM2_UserManual_en_10_files\part515.htm -->

### RECount

Counts the number of rising edges.

<!-- 来源：RTM2_UserManual_en_10_files\part516.htm -->

### FECount

Counts the number of falling edges.

<!-- 来源：RTM2_UserManual_en_10_files\part517.htm -->

### HIGH

Mean value of the high level of a square wave.

<!-- 来源：RTM2_UserManual_en_10_files\part518.htm -->

### LOW

Mean value of the low level of a square wave.

<!-- 来源：RTM2_UserManual_en_10_files\part519.htm -->

### AMPLitude

Amplitude of a square wave.

<!-- 来源：RTM2_UserManual_en_10_files\part520.htm -->

### MEAN

Mean value of the complete displayed waveform of the selected channel.

<!-- 来源：RTM2_UserManual_en_10_files\part521.htm -->

### RMS

RMS (Root Mean Square) value of the voltage of the complete displayed waveform of the selected channel.

<!-- 来源：RTM2_UserManual_en_10_files\part522.htm -->

### RTIMe | FTIMe

```text
Rise or falling time of the left-most rising edge within the dis- played section of the waveform of the selected channel. The ref- erence level for this mesurement is set with REFLevel: RELative:MODE.
```

<!-- 来源：RTM2_UserManual_en_10_files\part523.htm -->

### PDCycle | NDCycle

Measure the positive or negative duty cycle.

<!-- 来源：RTM2_UserManual_en_10_files\part524.htm -->

### PPWidth | NPWidth

Measure the width of positive or negative pulses.

<!-- 来源：RTM2_UserManual_en_10_files\part525.htm -->

### CYCMean

Mean value of the left-most signal period of the waveform of the selected channel.

<!-- 来源：RTM2_UserManual_en_10_files\part526.htm -->

### CYCRms

RMS (Root Mean Square) value of the voltage of the left-most signal period of the waveform of the selected channel.

<!-- 来源：RTM2_UserManual_en_10_files\part527.htm -->

### STDDev

Measures the standard deviation of the waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part528.htm -->

### CYCStddev

Measures the standard deviation of one cycle, usually of the first, left-most signal period.

<!-- 来源：RTM2_UserManual_en_10_files\part529.htm -->

### TFRequency | TPERiode

Measure the frequency of the trigger signal and the length of the its periods (hardware counter).

<!-- 来源：RTM2_UserManual_en_10_files\part530.htm -->

### DELay

```text
Time difference between two edges of the same or different waveforms. The waveforms are selected with MEASurement<m>:SOURce, and the edges with MEASurement<m>:DELay:SLOPe.
```

<!-- 来源：RTM2_UserManual_en_10_files\part531.htm -->

### PHASe

```text
Phase difference between two waveforms (time difference/ period * 360). The waveforms are selected with MEASurement<m>:SOURce.
```

<!-- 来源：RTM2_UserManual_en_10_files\part532.htm -->

### BWIDth

Burst width, the duration of one burst, measured from the first edge to the last edge that cross the middle reference level.

<!-- 来源：RTM2_UserManual_en_10_files\part533.htm -->

### POVershoot | NOVershoot

Positive and negative overshoot of a square wave.

<!-- 来源：RTM2_UserManual_en_10_files\part534.htm -->

### TBFRequency | TBPeriod

Measures the frequency of the B-trigger signal and the length of the B-trigger signal periods.

*RST: NONE (measurement is off)

### MEASurement<m>:SOURce <SignalSource>[,<ReferenceSource>]

Selects one of the active signal, reference or math channels as the source(s) of the selected measurement. Available sources depend on the selected measurement type.

<!-- 来源：RTM2_UserManual_en_10_files\part535.htm -->

### Suffix:

<m> 1..4

Selects the measurement place.

<!-- 来源：RTM2_UserManual_en_10_files\part536.htm -->

### Parameters:

<SignalSource> NONE | CH1 | CH2 | CH3 | CH4 | MA1 | MA2 | MA3 | MA4 | MA5 | RE1 | RE2 | RE3 | RE4 TRIGger | D0..D15 | D70 | D158 |

SPECtrum | MINHold | MAXHold | AVERage | CH1 | CH2 | CH3 | CH4 | MA1 | MA2 | MA3 | MA4 | MA5 | RE1 | RE2 | RE3 |

RE4 | TRIGger | D0..D15 | D70 | D158 | SPECtrum | MINHold | MAXHold | AVERage

Waveform to be measured, required for all measurement types.

<!-- 来源：RTM2_UserManual_en_10_files\part537.htm -->

### CH1 | CH2 | CH3 | CH4

Active signal channels 1 to 4

<!-- 来源：RTM2_UserManual_en_10_files\part538.htm -->

### MA1 | MA2 | MA3 | MA4 | MA5

Active math channels 1 to 5

<!-- 来源：RTM2_UserManual_en_10_files\part539.htm -->

### RE1 | RE2 | RE3 | RE4

Active reference channels 1 to 4

<!-- 来源：RTM2_UserManual_en_10_files\part540.htm -->

### TRIGger

Only return value. TRIG is returned if the measurement type is a trigger measurement: TFRequency | TPERiode measure the A- trigger source, TBFRequency | TBPeriod measure the B-trigger source.

<!-- 来源：RTM2_UserManual_en_10_files\part541.htm -->

### D0..D15

Active digital channels, if MSO option R&S RTM-B1 is installed. The following automatic measurements are possible: frequency, period, edge and pulse counts, phase, delay, duty cycle, burst width.

<!-- 来源：RTM2_UserManual_en_10_files\part542.htm -->

### D70 | D158

Active digital channels D0...D7 (pod 1) and D8...D15 (pod 2), available if MSO option R&S RTM-B1 is installed.

<!-- 来源：RTM2_UserManual_en_10_files\part543.htm -->

### SPECtrum | MINHold | MAXHold | AVERage

Available if option R&S RTM-K18 is installed. The measurement source is a spectrum analysis waveform.

SPECtrum: normal spectrum waveform

MINHold: waveform of the minimum amplitude spectrum MAXHold: waveform of the maximum amplitude spectrum AVERage: avarage amplitude spectrum

*RST: CH1

<ReferenceSource> NONE | CH1 | CH2 | CH3 | CH4 | MA1 | MA2 | MA3 | MA4 |

MA5 | RE1 | RE2 | RE3 | RE4 | NONE | CH1 | CH2 | CH3 | CH4 | MA1 | MA2 | MA3 | MA4 | MA5 | RE1 | RE2 | RE3 | RE4 | D0..D15 | D70 | D158

Second waveform, reference source that is required for delay and phase mesurements.

### MEASurement<m>:DELay:SLOPe <SignalSlope>,<ReferenceSlope>

Sets the edges to be used for delay measurement. The associated waveforms are defined with MEASurement<m>:SOURce

<!-- 来源：RTM2_UserManual_en_10_files\part544.htm -->

### Parameters:

<SignalSlope> POSitive | NEGative

Slope of source 1 ( first waveform)

*RST: POS

<ReferenceSlope> POSitive | NEGative

Slope of source 2 (second waveform)

*RST: POS

### Firmware/Software: 03.400

### MEASurement<m>:RESult[:ACTual]? [<MeasType>] Returns the result of the specified measurement type.

<!-- 来源：RTM2_UserManual_en_10_files\part545.htm -->

### Suffix:

<m> 1..4

Selects the measurement place.

<!-- 来源：RTM2_UserManual_en_10_files\part546.htm -->

### Query parameters:

<MeasType> FREQuency | PERiod | PEAK | UPEakvalue | LPEakvalue | PPCount | NPCount | RECount | FECount | HIGH | LOW | AMPLitude | MEAN | RMS | RTIMe | FTIMe | PDCYcle | NDCYcle | PPWidth | NPWidth | CYCMean | CYCRms | STDDev | CYCStddev | TFRequency | TPERiode | DELay | PHASe | BWIDth | POVershoot | NOVershoot | TBFRequency | TBPeriod

Specifies the measurement type. See MEASurement<m>:MAIN

on page 485.

<!-- 来源：RTM2_UserManual_en_10_files\part547.htm -->

### Return values:

<Value> Measurement result. If no measurement was executed, no value (NAN) is returned.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part548.htm -->

### MEASurement<m>:CATegory?

Returns the measurement category. Currently, the instrument supports only yt-mea- surements.

<!-- 来源：RTM2_UserManual_en_10_files\part549.htm -->

### Suffix:

<m> 1..4

Selects the measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part550.htm -->

### Return values:

<Category> AMPTime

AMPtime: yt-measurements

*RST: AMPT

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part551.htm -->

### 18.8.4 Automatic Measurements - Statistics

You can query the statistical results using the MEAS:STAT commands. To export stat- istical results to a csv file, use the EXP:MEAS:STAT commands. Note that export of statistics is possible only remotely, but not in manual operation.

MEASurement<m>:STATistics[:ENABle] 490

MEASurement<m>:STATistics:WEIGht 490

MEASurement<m>:STATistics:RESet 491

MEASurement<m>:RESult:AVG? 491

MEASurement<m>:RESult:STDDev? 491

MEASurement<m>:RESult:NPEak? 492

MEASurement<m>:RESult:PPEak? 492

MEASurement<m>:RESult:WFMCount? 492

MEASurement<m>:STATistics:VALue:ALL? 492

MEASurement<m>:STATistics:VALue<n>? 493

EXPort:MEASurement<m>:STATistics:NAME 493

EXPort:MEASurement<m>:STATistics:SAVE 493

EXPort:MEASurement<m>:STATistics:ALL:NAME 494

EXPort:MEASurement<m>:STATistics:ALL:SAVE 494

### MEASurement<m>:STATistics[:ENABle] <StatisticEnable>

Activates or deactivates the statistical evaluation for the selected measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part552.htm -->

### Suffix:

<m> 1. 4

Selects the measurement place.

<!-- 来源：RTM2_UserManual_en_10_files\part553.htm -->

### Parameters:

<StatisticEnable> ON | OFF

*RST: OFF

### Firmware/Software: FW 03.700

### MEASurement<m>:STATistics:WEIGht <AverageCount>

Sets the number of measured waveforms used for calculation of average and standard deviation.

<!-- 来源：RTM2_UserManual_en_10_files\part554.htm -->

### Suffix:

<m> 1..4

Selects the measurement place.

<!-- 来源：RTM2_UserManual_en_10_files\part555.htm -->

### Parameters:

<AverageCount> Range: 2 to 1000

Increment: 1

*RST: 1000

### Firmware/Software: FW 03.700

<!-- 来源：RTM2_UserManual_en_10_files\part556.htm -->

### MEASurement<m>:STATistics:RESet

Deletes the statistical results for the selected measurement, and starts a new statistical evaluation if the acquisition is running. The waveform count is set to 0 and all measure- ment values are set to NAN.

<!-- 来源：RTM2_UserManual_en_10_files\part557.htm -->

### Suffix:

<m> 1. 4

Selects the measurement place.

### Usage: Event

### Firmware/Software: FW 03.700

### MEASurement<m>:RESult:AVG? <AverageValue> Returns the average value of the current mesurement series.

```text
The number of waveforms used for calculation is defined with MEASurement<m>: STATistics:WEIGht.
```

<!-- 来源：RTM2_UserManual_en_10_files\part558.htm -->

### Suffix:

<m> 1..4

Selects the measurement place.

<!-- 来源：RTM2_UserManual_en_10_files\part559.htm -->

### Query parameters:

<AverageValue> Statistic value Usage: Query only Firmware/Software: FW 03.700

### MEASurement<m>:RESult:STDDev? <StandardDeviation>

Returns the statistical standard deviation of the current mesurement series.

```text
The number of waveforms used for calculation is defined with MEASurement<m>: STATistics:WEIGht.
```

<!-- 来源：RTM2_UserManual_en_10_files\part560.htm -->

### Suffix:

<m> 1..4

Selects the measurement place.

<!-- 来源：RTM2_UserManual_en_10_files\part561.htm -->

### Query parameters:

<StandardDeviation> Statistic value

### Usage: Query only

### Firmware/Software: FW 03.700

### MEASurement<m>:RESult:NPEak? <NegativePeak>

Returns the minimum measurement value of the current measurement series.

<!-- 来源：RTM2_UserManual_en_10_files\part562.htm -->

### Suffix:

<m> 1..4

Selects the measurement place.

<!-- 来源：RTM2_UserManual_en_10_files\part563.htm -->

### Query parameters:

<NegativePeak> Minimum measurement value Usage: Query only Firmware/Software: FW 03.700

### MEASurement<m>:RESult:PPEak? <PositivePeak>

Returns the maximum measurement value of the current measurement series.

<!-- 来源：RTM2_UserManual_en_10_files\part564.htm -->

### Suffix:

<m> 1..4

Selects the measurement place.

<!-- 来源：RTM2_UserManual_en_10_files\part565.htm -->

### Query parameters:

<PositivePeak> Maximum measurement value Usage: Query only Firmware/Software: FW 03.700

### MEASurement<m>:RESult:WFMCount? <WaveformCount> Returns the current number of measured waveforms.

<!-- 来源：RTM2_UserManual_en_10_files\part566.htm -->

### Suffix:

<m> 1..4

Selects the measurement place.

<!-- 来源：RTM2_UserManual_en_10_files\part567.htm -->

### Query parameters:

<WaveformCount> Number of measured waveforms

### Usage: Query only

### Firmware/Software: FW 03.700

<!-- 来源：RTM2_UserManual_en_10_files\part568.htm -->

### MEASurement<m>:STATistics:VALue:ALL?

Returns all values from the statistics buffer.

Note that valid buffered values can only be read if the acquisition is stopped. As long as the acquisition is running, the buffer contents is changing and the buffered values are not valid for reading.

<!-- 来源：RTM2_UserManual_en_10_files\part569.htm -->

### Suffix:

<m> 1..4

Selects the measurement place.

<!-- 来源：RTM2_UserManual_en_10_files\part570.htm -->

### Return values:

<ValueList> Comma-separated list of statistical values

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part571.htm -->

### MEASurement<m>:STATistics:VALue<n>?

Returns one statistical value from the indicated buffer place.

Note that valid buffered values can only be read if the acquisition is stopped. As long as the acquisition is running, the buffer contents is changing and the buffered values are not valid for reading.

<!-- 来源：RTM2_UserManual_en_10_files\part572.htm -->

### Suffix:

<m> 1..4

Selects the measurement place.

<n> *

```text
Buffer place. The buffer size is limited by MEASurement<m>: STATistics:WEIGht.
```

<!-- 来源：RTM2_UserManual_en_10_files\part573.htm -->

### Return values:

<StatisticValue> Statistical value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part574.htm -->

### EXPort:MEASurement<m>:STATistics:NAME

Defines the path and filename of the statistics file. The file format is CSV. If the file already exists, it will be overwritten.

<!-- 来源：RTM2_UserManual_en_10_files\part575.htm -->

### Suffix:

<m> 1..15

1..4: measurement places of automatic measurements

5..15: measurement places for power measurements.

<!-- 来源：RTM2_UserManual_en_10_files\part576.htm -->

### Parameters:

<FileName> String parameter

<!-- 来源：RTM2_UserManual_en_10_files\part577.htm -->

### EXPort:MEASurement<m>:STATistics:SAVE

```text
Saves statistical results of the indicated measurement place to the file that is defined by the EXPort:MEASurement<m>:STATistics:NAME command.
```

<!-- 来源：RTM2_UserManual_en_10_files\part578.htm -->

### Suffix:

<m> 1..15

1..4: measurement places of automatic measurements

5..15: measurement places for power measurements.

### Usage: Event

See also: EXPort:MEASurement<m>:STATistics:ALL:SAVE on page 494.

<!-- 来源：RTM2_UserManual_en_10_files\part579.htm -->

### EXPort:MEASurement<m>:STATistics:ALL:NAME

Defines the path and filename of the statistics file. The file format is CSV. If the file already exists, it will be overwritten.

<!-- 来源：RTM2_UserManual_en_10_files\part580.htm -->

### Suffix:

<m> 1..4

The suffix is irrelevant, all results are returned.

<!-- 来源：RTM2_UserManual_en_10_files\part581.htm -->

### Parameters:

<FileName> String parameter

<!-- 来源：RTM2_UserManual_en_10_files\part582.htm -->

### EXPort:MEASurement<m>:STATistics:ALL:SAVE

Saves statistical results of all measurement places to the file that is defined by the

```text
EXPort:MEASurement<m>:STATistics:ALL:NAME command.
```

<!-- 来源：RTM2_UserManual_en_10_files\part583.htm -->

### Suffix:

<m> 1..4

The suffix is irrelevant, all results are returned.

### Example: The file contains general information, statistical results, long term statistics, and the individual values that are used to calcu- late the statistics. The number of values is "Average No." "Vendor","Rohde&Schwarz",

```text
"Device/Mat.-No.","RTM2022 / 5710.0999k22", "Serial No.","900001",
"Firmware Version","Beta 05.601",
"Date","2014-11-18 / 16:40:27",
"Meas. Place",,"1",,"2",,"3",,
"Type",,"Frequency",,"Mean Value",,"Frequency",,
"Source 1",,"CH1",,"CH1",,"CH2",,
"Source 2",,,,,,,,,,
"Wave count",,42,,39,,37,, "Current",,4.998250e+05,,5.648727e-01,,4.998250e+05,, "Average No.",,1.000000e+03,,1.000000e+03,,1.000000e+03,, "Minimum",,4.997501e+05,,5.633875e-01,,4.997501e+05,, "Maximum",,4.998250e+05,,5.650349e-01,,4.998250e+05,, "Mean",,4.998179e+05,,5.642045e-01,,4.998169e+05,,
"σ-Deviation",,2.199706e+01,,3.677224e-04,,2.326898e+01,,
"Time of first value",,,,,,,,,,
"Time of last value",,,,,,,,,,
"Long term Minimum",,4.997501e+05,,5.633875e-01,,4.997501e+05,, "Long term Maximum",,4.998250e+05,,5.650349e-01,,4.998250e+05,, "Long term Mittelwert",,4.998179e+05,,5.642045e-01,,4.998169e+05,, "Long term σ-Deviation",,2.226370e+01,,3.725295e-04,,2.358995e+01,,
"Long term start time",,,,,,,,,,
"Long term end Time",,,,,,,,,,
"Index","Time Offset","Value","Time Offset","Value", "Time Offset","Value",
1,,4.998250e+05,,5.649274e-01,,4.997501e+05,
2,,4.998250e+05,,5.649072e-01,,4.998250e+05,
3,,4.998250e+05,,5.650349e-01,,4.998250e+05,
4,,4.998250e+05,,5.641094e-01,,4.998250e+05,
5,,4.998250e+05,,5.640586e-01,,4.998250e+05,
6,,4.997501e+05,,5.642784e-01,,4.998250e+05,
7,,4.998250e+05,,5.637245e-01,,4.998250e+05,...
```

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part584.htm -->

### 18.8.5 Reference Level

REFLevel:RELative:MODE 496

REFLevel:RELative:LOWer 496

REFLevel:RELative:UPPer 496

REFLevel:RELative:MIDDle 496

### REFLevel:RELative:MODE <RelativeMode>

Sets the lower and upper reference levels for rise and fall time mesurements (cursor and automatic mesurements) as well as the middle reference level for phase and delay measurements. The levels are defined as percentages of the high signal level. The set- ting is valid for all measurement places.

<!-- 来源：RTM2_UserManual_en_10_files\part585.htm -->

### Parameters:

<RelativeMode> TEN | TWENty | FIVE | USER

TEN: 10, 50 and 90%

TWENty: 20, 50 and 80%

FIVE: 5, 50 and 95 %

```text
USER: levels are defined with REFLevel:RELative:LOWer, REFLevel:RELative:MIDDle, and REFLevel:RELative: UPPer.
```

*RST: TEN

### Example: REFL:REL:MODE TWENty MEAS2:MAIN RTIM

Sets the reference levels for all measurement places and meas- ures the rise time between these levels for measurement place 2:

lower reference level = 20% of high signal level upper reference level = 80% of high signal level

### REFLevel:RELative:LOWer <LowerLevel>

### REFLevel:RELative:UPPer <UpperLevel>

Set the lower and upper reference levels for rise and fall time mesurements (cursor and automatic mesurements) if REFLevel:RELative:MODE is set to USER. The lev- els are defined as percentages of the high signal level. They are valid for all measure- ment places.

<!-- 来源：RTM2_UserManual_en_10_files\part586.htm -->

### Parameters:

<LowerLevel> *RST: 10

Default unit: %

<UpperLevel> *RST: 90

Default unit: %

### Firmware/Software: 03.400

### REFLevel:RELative:MIDDle <MiddleLevel>

Set the middle reference level used for phase and delay measurements, if REFLevel: RELative:MODE is set to USER. The level is defined as percentages of the high signal level. The setting is valid for all measurement places.

<!-- 来源：RTM2_UserManual_en_10_files\part587.htm -->

### Parameters:

<MiddleLevel> *RST: 50

Default unit: %

### Firmware/Software: 03.400

<!-- 来源：RTM2_UserManual_en_10_files\part588.htm -->

## 18.9 Mathematics

This chapter describes commands that configure or perform mathematical functions. For data queries and conversion, consider also the following commands:

- FORMat[:DATA] on page 731

- CALCulate:MATH<m>:DATA:XINCrement? on page 742

- CALCulate:MATH<m>:DATA:XORigin? on page 742

- CALCulate:MATH<m>:DATA:YINCrement? on page 743

- CALCulate:MATH<m>:DATA:YORigin? on page 743

- CALCulate:MATH<m>:DATA:YRESolution? on page 743

CALCulate:MATH<m>:STATe 497

CALCulate:MATH<m>:SCALe 497

CALCulate:MATH<m>:POSition 498

CALCulate:MATH<m>[:EXPRession][:DEFine] 498

CALCulate:MATH<m>:DATA? 499

CALCulate:MATH<m>:DATA:HEADer? 499

CALCulate:MATH<m>:DATA:POINts? 500

### CALCulate:MATH<m>:STATe <State>

Defines whether the selected mathematical channel is active or not. Only if a channel is active it is visible on the screen and can be selected as a source for analysis and display functions.

<!-- 来源：RTM2_UserManual_en_10_files\part589.htm -->

### Suffix:

<m> 1. 4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part590.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### CALCulate:MATH<m>:SCALe <Scale>

Sets the vertical scale for the specified math waveform.

```text
In FFT mode, the command sets the vertical scale of the FFT window. The scale unit for FFT is set with CALCulate:MATH<m>:FFT:MAGNitude:SCALe.
```

<!-- 来源：RTM2_UserManual_en_10_files\part591.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

IN FFT mode, the numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part592.htm -->

### Parameters:

<Scale> Scale value

Range: -1.0E-24 to 5.0E+25

Increment: 1, 2, 5 progression, for example, 1mV/div, 2mV/div,

5mV/div, 10, 20, 50...

*RST: 1

### CALCulate:MATH<m>:POSition <Position>

Sets the vertical position of the specified math waveform in the window.

<!-- 来源：RTM2_UserManual_en_10_files\part593.htm -->

### Suffix:

<m> 1. 4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part594.htm -->

### Parameters:

<Position> Position value, given in divisions.

Range: -1.880E+02 to 2.120E+02

Increment: 0.01 in reset state

*RST: 2

### CALCulate:MATH<m>[:EXPRession][:DEFine] <RemComplExpr>

Defines the equation to be calculated for the selected math waveform as a regular expression.

For details on available operators, see "Operator" on page 123.

<!-- 来源：RTM2_UserManual_en_10_files\part595.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part596.htm -->

### Parameters:

<RemComplExpr> String parameter, consisting of the mathematical operation and the source(s) written in parenthesis.

### Example: CALC:MATH<2>:EXPR:DEF "CH1+CH2"

| Operation | Expression string | Comment |
| --- | --- | --- |
| Addition | "ADD(CH1,CH2)" | "CH1+CH2" is also possible |
| Subtraction | "SUB(CH1,CH2)" | "CH1-CH2" is also possible |
| Multiplication | "MUL(CH1,CH2)" | "CH1*CH2" is also possible |
| Division | "DIV(CH1,CH2)" | "CH1/CH2" is also possible |
| Maximum amplitude | "MAX(CH1,CH2)" |  |
| Minimum amplitude | "MIN(CH1,CH2)" |  |
| Square | "SQR(CH1)" |  |
| Square Root | "SQRT(CH1)" |  |

| Operation | Expression string | Comment |
| --- | --- | --- |
| Absolute value | "ABS(CH1)" |  |
| Positive wave | "POS(CH1)" |  |
| Negative wave | "NEG(CH1)" |  |
| Reciprocal | "REC(CH1)" |  |
| Inverse | "INV(CH1)" |  |
| Common logarithm (basis 10) | "LOG(CH1)" |  |
| Natural logarithm (basis e) | "LN(CH1)" |  |
| Derivative | "DERI(CH1)" |  |
| Integral | "INT(CH1)" |  |
| IIR low pass | "IIRL(CH1,1E6)" | CH1 – Source waveform 1e6 – constant value, cut-off frequency of the low or high pass |
| IIR high pass | "IIRH(CH1,1E6)" |  |
| FFT | "FFTMAG(CH1)" | FFT function of the source waveform See also: Chapter 18.10, "Spectrum Analysis", on page 500 |

<!-- 来源：RTM2_UserManual_en_10_files\part597.htm -->

### CALCulate:MATH<m>:DATA?

Returns the data of the math waveform points for transmission from the instrument to the controlling computer. The waveforms data can be used in MATHLAB, for example.

To set the export format, use FORMat[:DATA] on page 731.

<!-- 来源：RTM2_UserManual_en_10_files\part598.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part599.htm -->

### Return values:

<Data> List of values according to the format settings - voltages, or magnitudes of a spectrum.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part600.htm -->

### CALCulate:MATH<m>:DATA:HEADer?

Returns information on the math waveform.

#### Table 18-4: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Record length of the waveform in Samples | 200000 |
| 4 | Number of values per sample interval, usually 1. | 1 |

<!-- 来源：RTM2_UserManual_en_10_files\part601.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part602.htm -->

### Return values:

<Header> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part603.htm -->

### CALCulate:MATH<m>:DATA:POINts?

```text
Returns the number of data samples that are returned with CALCulate:MATH<m>: DATA?.
```

<!-- 来源：RTM2_UserManual_en_10_files\part604.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part605.htm -->

### Return values:

<DataPoints> Amount of data points

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part606.htm -->

## 18.10 Spectrum Analysis

- Basic FFT 500

- Spectrum Waveform Data 505

- Spectrum Analysis (Option R&S RTM-K18) 508

<!-- 来源：RTM2_UserManual_en_10_files\part607.htm -->

### 18.10.1 Basic FFT

To define an FFT for a channel, use CALC:MATH<m>:EXPR "FFTMAG(CHx)". You can define this expression for any of the math waveforms 1 to 5 (suffix <m>) and use the other commands for the math waveform that is defined as FFT.

CALCulate:MATH<m>:FFT:WINDow:TYPE 501

CALCulate:MATH<m>:ARIThmetics 501

CALCulate:MATH<m>:FFT:AVERage:COUNt 502

CALCulate:MATH<m>:FFT:AVERage:COMPlete? 502

CALCulate:MATH<m>:FFT:MAGNitude:SCALe 503

CALCulate:MATH<m>:FFT:BANDwidth[:RESolution]:ADJusted? 503

CALCulate:MATH<m>:FFT:BANDwidth[:RESolution]:AUTO 503

CALCulate:MATH<m>:FFT:BANDwidth[:RESolution]:RATio 503

CALCulate:MATH<m>:FFT:BANDwidth[:RESolution][:VALue] 504

CALCulate:MATH<m>:FFT:CFRequency 504

CALCulate:MATH<m>:FFT:FULLspan 504

CALCulate:MATH<m>:FFT:SPAN 504

CALCulate:MATH<m>:FFT:STARt 504

CALCulate:MATH<m>:FFT:STOP 505

CALCulate:MATH<m>:FFT:TIME:RANGe 505

CALCulate:MATH<m>:FFT:TIME:POSition 505

CALCulate:MATH<m>:FFT:SRATe? 505

### CALCulate:MATH<m>:FFT:WINDow:TYPE <WindowType>

Window functions are multiplied with the input values and thus can improve the FFT display.

<!-- 来源：RTM2_UserManual_en_10_files\part608.htm -->

### Parameters:

<WindowType> RECTangular | HAMMing | HANNing | BLACkmanharris | FLATtop

<!-- 来源：RTM2_UserManual_en_10_files\part609.htm -->

### RECTangular

The rectangular window has high frequency accuracy with thin spectral lines, but with increased noise. Use this function pref- erably with pulse response tests where start and end values are zero.

<!-- 来源：RTM2_UserManual_en_10_files\part610.htm -->

### HAMMing

The Hamming window has higher noise level inside the spec- trum than Hann or Blackman, but smaller than the rectangular window. The width of the spectral lines is thinner than the other bell-shaped functions. Use this window to measure amplitudes of a periodical signal precisely.

<!-- 来源：RTM2_UserManual_en_10_files\part611.htm -->

### HANNing

The noise level within the spectrum is reduced and the width of the spectral lines enlarges. Use this window to measure ampli- tudes of a periodical signal precisely.

<!-- 来源：RTM2_UserManual_en_10_files\part612.htm -->

### BLACkmanharris

In the Blackman window the amplitudes can be measured very precisely. However, determining the frequency is more difficult. Use this window to measure amplitudes of a periodical signal precisely.

<!-- 来源：RTM2_UserManual_en_10_files\part613.htm -->

### FLATtop

The flat top window has low amplitude measurement errors but a poor frequency resolution. Use this window for accurate sin- gle-tone measurements and for measurement of amplitudes of sinusoidal frequency components.

*RST: HANNing

### CALCulate:MATH<m>:ARIThmetics <Arithmetics> Defines the mode for FFT calculation and display.

<!-- 来源：RTM2_UserManual_en_10_files\part614.htm -->

### Parameters:

<Arithmetics> OFF | ENVelope | AVERage

<!-- 来源：RTM2_UserManual_en_10_files\part615.htm -->

### OFF

The FFT is performed without any additional weighting or post- processing of the acquired data. The new input data is acquired and displayed, and thus overwrites the previously saved and dis- played data.

<!-- 来源：RTM2_UserManual_en_10_files\part616.htm -->

### ENVelope

In addition to the normal spectrum, the maximal oscillations are saved separately and updated for each new spectrum. The max- imum values are displayed together with the newly acquired val- ues and form an envelope. This envelope indicates the range of all FFT trace values that occurred.

<!-- 来源：RTM2_UserManual_en_10_files\part617.htm -->

### AVERage

The average of several spectrums is calculated. The number of spectrums used for the averaging is defined using the com- mand. This mode is useful for noise rejection.

*RST: OFF

### CALCulate:MATH<m>:FFT:AVERage:COUNt <AverageCount>

Defines the number of spectrums used for averaging if CALCulate:MATH<m>: ARIThmetics is set to AVERage.

<!-- 来源：RTM2_UserManual_en_10_files\part618.htm -->

### Parameters:

<AverageCount> Integer value

Range: 2 to 512 Increment: 2^n

*RST: 2

<!-- 来源：RTM2_UserManual_en_10_files\part619.htm -->

### CALCulate:MATH<m>:FFT:AVERage:COMPlete?

Returns the state of spectrum averaging.

<!-- 来源：RTM2_UserManual_en_10_files\part620.htm -->

### Return values:

<AverageComplete> 0 | 1

<!-- 来源：RTM2_UserManual_en_10_files\part621.htm -->

### 0

```text
The number of acquired waveforms is less than the number required for spectrum average calculation. See CALCulate: MATH<m>:FFT:AVERage:COUNt.
```

<!-- 来源：RTM2_UserManual_en_10_files\part622.htm -->

### 1

The instrument acquired a sufficient number of waveforms to determine the average.

### Usage: Query only

### CALCulate:MATH<m>:FFT:MAGNitude:SCALe <Magnitude Scale> Defines the scaling unit of the y-axis.

```text
To set the scale value, use CALCulate:MATH<m>:SCALe.
```

<!-- 来源：RTM2_UserManual_en_10_files\part623.htm -->

### Parameters:

<Magnitude Scale> LINear | DBM | DBV

<!-- 来源：RTM2_UserManual_en_10_files\part624.htm -->

### LINear

linear scaling; displays the RMS value of the voltage.

<!-- 来源：RTM2_UserManual_en_10_files\part625.htm -->

### DBM

logarithmic scaling; related to 1 mW

<!-- 来源：RTM2_UserManual_en_10_files\part626.htm -->

### DBV

logarithmic scaling; related to 1 Veff

*RST: DBM

### Example: CALC:MATH:FFT:MAGN:SCAL DBM CALC:MATH:SCAL 20

Set the Y-scale of the FFT window to 20 dBm.

<!-- 来源：RTM2_UserManual_en_10_files\part627.htm -->

### CALCulate:MATH<m>:FFT:BANDwidth[:RESolution]:ADJusted?

Queries the effective resolution bandwidth.

<!-- 来源：RTM2_UserManual_en_10_files\part628.htm -->

### Return values:

<AdjResBW> Range: Depends on various other settings.

Default unit: Hz

### Usage: Query only

### CALCulate:MATH<m>:FFT:BANDwidth[:RESolution]:AUTO <SpanRBWCoupling> Couples the frequency span to the RBW.

<!-- 来源：RTM2_UserManual_en_10_files\part629.htm -->

### Parameters:

<SpanRBWCoupling> ON | OFF

### CALCulate:MATH<m>:FFT:BANDwidth[:RESolution]:RATio <SpanRBWRatio>

Defines the ratio of span (Hz) / resolution bandwidth (Hz). The span/RBW ratio is half the number of points used for FFT which is defined with manual operation in the menu.

<!-- 来源：RTM2_UserManual_en_10_files\part630.htm -->

### Parameters:

<SpanRBWRatio> Range: The value is changed in 2^n steps from 2^10 to

2^15 (1024, 2048,4096,8192,16384, 32768).

### Example: CALC:MATH:FFT:BAND:RAT 32768

Sets the number of points to 65536.

### CALCulate:MATH<m>:FFT:BANDwidth[:RESolution][:VALue] <ResolutionBW>

Defines the resolution bandwidth - the minimum frequency step at which the individual components of a spectrum can be distinguished

<!-- 来源：RTM2_UserManual_en_10_files\part631.htm -->

### Parameters:

<ResolutionBW> Range: Depends on various other settings.

Default unit: Hz

### CALCulate:MATH<m>:FFT:CFRequency <CenterFreq>

```text
Defines the position of the displayed frequency domain, which is (Center - Span/2) to (Center + Span/2). The width of the domain is defined using the CALCulate: MATH<m>:FFT:SPAN command.
```

<!-- 来源：RTM2_UserManual_en_10_files\part632.htm -->

### Parameters:

<CenterFreq> Range: Limited by the first data point (minimum) and last

data point (maximum) of the FFT curve.

Increment: Depends on the span and the number of data points (span/RBW ratio).

Default unit: Hz

<!-- 来源：RTM2_UserManual_en_10_files\part633.htm -->

### CALCulate:MATH<m>:FFT:FULLspan

Performs FFT calculation for the full frequency span.

### Usage: Event

### CALCulate:MATH<m>:FFT:SPAN <FreqSpan>

```text
The span is specified in Hertz and defines the width of the displayed frequency range, which is (Center - Span/2) to (Center + Span/2). The position of the span is defined using the CALCulate:MATH<m>:FFT:CFRequency command.
```

<!-- 来源：RTM2_UserManual_en_10_files\part634.htm -->

### Parameters:

<FreqSpan> Range: Depends on various other settings, mainly on time

base and span/RBW ratio. Increment: Only 1 | 2 | 5 in first digit Default unit: Hz

### CALCulate:MATH<m>:FFT:STARt <StartFreq>

Defines the start frequency of the displayed frequency domain at the left display edge:

Center - Span/2

You can set start and stop frequency instead of defining a center frequency and span.

<!-- 来源：RTM2_UserManual_en_10_files\part635.htm -->

### Parameters:

<StartFreq> Range: Depends on various other settings, mainly on time

base, span/RBW ratio, and center frequency.

Default unit: Hz

### CALCulate:MATH<m>:FFT:STOP <StopFreq>

Defines the stop frequency of the displayed frequency domain at the right display edge: Center + Span/2

You can set start and stop frequency instead of defining a center frequency and span.

<!-- 来源：RTM2_UserManual_en_10_files\part636.htm -->

### Parameters:

<StopFreq> Range: Depends on various other settings, mainly on time

base, span/RBW ratio, and center frequency.

Default unit: Hz

### CALCulate:MATH<m>:FFT:TIME:RANGe <WindowWidth>

Defines the width of the time base extract from the Y(t)-window for which the FFT is calculated.

<!-- 来源：RTM2_UserManual_en_10_files\part637.htm -->

### Parameters:

<WindowWidth> Range: depends on the time base

Default unit: s

### Firmware/Software: FW 03.800

### CALCulate:MATH<m>:FFT:TIME:POSition <WindowPosition>

Defines the position of the time base extract in the Y(t)-window for which the FFT is calculated.

<!-- 来源：RTM2_UserManual_en_10_files\part638.htm -->

### Parameters:

<WindowPosition> Range: depends on the time base and the width of the FFT time base extract

Default unit: s

### Firmware/Software: FW 03.800

<!-- 来源：RTM2_UserManual_en_10_files\part639.htm -->

### CALCulate:MATH<m>:FFT:SRATe?

Returns the sample rate of data used in an FFT analysis.

<!-- 来源：RTM2_UserManual_en_10_files\part640.htm -->

### Return values:

<SampleRate> Default unit: Sa/s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part641.htm -->

### 18.10.2 Spectrum Waveform Data

### Suffix <m>: Use the math waveform number for which you have set up FFT.

In addition to the commands described below, consider also the following commands:

- FORMat[:DATA] on page 731

- CALCulate:MATH<m>:DATA:XINCrement? on page 742

- CALCulate:MATH<m>:DATA:XORigin? on page 742

- CALCulate:MATH<m>:DATA:YINCrement? on page 743

- CALCulate:MATH<m>:DATA:YORigin? on page 743

- CALCulate:MATH<m>:DATA:YRESolution? on page 743

- CALCulate:MATH<m>:DATA:ENVelope:XINCrement? on page 742

- CALCulate:MATH<m>:DATA:ENVelope:XORigin? on page 742

- CALCulate:MATH<m>:DATA:ENVelope:YINCrement? on page 743

- CALCulate:MATH<m>:DATA:ENVelope:YORigin? on page 743

- CALCulate:MATH<m>:DATA:ENVelope:YRESolution? on page 743

<!-- 来源：RTM2_UserManual_en_10_files\part642.htm -->

### CALCulate:MATH<m>:DATA?

Returns the data of the math waveform points for transmission from the instrument to the controlling computer. The waveforms data can be used in MATHLAB, for example.

To set the export format, use FORMat[:DATA] on page 731.

<!-- 来源：RTM2_UserManual_en_10_files\part643.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part644.htm -->

### Return values:

<Data> List of values according to the format settings - voltages, or magnitudes of a spectrum.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part645.htm -->

### CALCulate:MATH<m>:DATA:HEADer?

Returns information on the math waveform.

#### Table 18-5: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Record length of the waveform in Samples | 200000 |
| 4 | Number of values per sample interval, usually 1. | 1 |

<!-- 来源：RTM2_UserManual_en_10_files\part646.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part647.htm -->

### Return values:

<Header> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part648.htm -->

### CALCulate:MATH<m>:DATA:POINts?

```text
Returns the number of data samples that are returned with CALCulate:MATH<m>: DATA?.
```

<!-- 来源：RTM2_UserManual_en_10_files\part649.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part650.htm -->

### Return values:

<DataPoints> Amount of data points

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part651.htm -->

### CALCulate:MATH<m>:DATA:ENVelope?

Returns the data of FFT envelope waveforms ( CALCulate:MATH<m>:ARIThmetics is set to ENV ). The envelope consists of two waveforms. The data of the two wave- forms is written into one data stream in interleaved order.

Use this command only for envelope waveforms. For other FFT and math waveforms, use CALCulate:MATH<m>:DATA? on page 499.

To set the export format, use FORMat[:DATA] on page 731.

<!-- 来源：RTM2_UserManual_en_10_files\part652.htm -->

### Suffix:

<m> 1..4

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part653.htm -->

### Return values:

<Data> List of values according to the format settings - the voltages of the envelope points. The list contains two values for each sam- ple interval.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part654.htm -->

### CALCulate:MATH<m>:DATA:ENVelope:HEADer?

Returns information on the envelope waveform.

Use this command only for envelope waveforms. For all other FFT waveforms, use

```text
CALCulate:MATH<m>:DATA:HEADer?.
```

#### Table 18-6: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Number of samples | 200000 |
| 4 | Number of values per sample interval. For envelope waveforms the value is 2. | 2 |

<!-- 来源：RTM2_UserManual_en_10_files\part655.htm -->

### Suffix:

<m> 1..4

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part656.htm -->

### Return values:

<Header> Comma-separated value list, string data

Example: -9.477E-008,9.477E-008,200000,2

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part657.htm -->

### CALCulate:MATH<m>:DATA:ENVelope:POINts?

```text
Returns the number of data samples that are returned with CALCulate:MATH<m>: DATA:ENVelope?.
```

<!-- 来源：RTM2_UserManual_en_10_files\part658.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part659.htm -->

### Return values:

<DataPoints> Amount of data points

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part660.htm -->

### 18.10.3 Spectrum Analysis (Option R&S RTM-K18)

- General Settings 508

- Spectogram Settings 510

- Marker Settings 511

- Frequency Domain Settings 517

- Time Domain Settings 519

- Waveform Settings 519

- Diagram Display Settings 522

### 18.10.3.1 General Settings

SPECtrum[:STATe] 508

SPECtrum:SOURce 509

SPECtrum:FREQuency:AVERage:COMPlete? 509

SPECtrum:FREQuency:AVERage:COUNt 509

SPECtrum:FREQuency:MAGNitude:SCALe 509

SPECtrum:FREQuency:POSition 509

SPECtrum:FREQuency:RESet 509

SPECtrum:FREQuency:SCALe 510

SPECtrum:FREQuency:WINDow:TYPE 510

<!-- 来源：RTM2_UserManual_en_10_files\part661.htm -->

### SPECtrum[:STATe]

Switches on the spectrum analysis.

<!-- 来源：RTM2_UserManual_en_10_files\part662.htm -->

### Parameters:

<State> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part663.htm -->

### SPECtrum:SOURce

Selects the source for the spectrum analysis diagrams.

<!-- 来源：RTM2_UserManual_en_10_files\part664.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4

<!-- 来源：RTM2_UserManual_en_10_files\part665.htm -->

### SPECtrum:FREQuency:AVERage:COMPlete?

Returns the state of spectrum averaging.

<!-- 来源：RTM2_UserManual_en_10_files\part666.htm -->

### Parameters:

<AverageComplete>

### Usage: Query only

### SPECtrum:FREQuency:AVERage:COUNt <AverageCount> Defines the number of spectrums used for averaging.

<!-- 来源：RTM2_UserManual_en_10_files\part667.htm -->

### Parameters:

<AverageCount>

### SPECtrum:FREQuency:MAGNitude:SCALe <MagnitudeScale> Defines the scaling unit of the y-axis.

<!-- 来源：RTM2_UserManual_en_10_files\part668.htm -->

### Parameters:

<MagnitudeScale> LINear | DBM | DBV

<!-- 来源：RTM2_UserManual_en_10_files\part669.htm -->

### LINear

linear scaling; displays the RMS value of the voltage.

<!-- 来源：RTM2_UserManual_en_10_files\part670.htm -->

### DBM

logarithmic scaling; related to 1 mW

<!-- 来源：RTM2_UserManual_en_10_files\part671.htm -->

### DBV

logarithmic scaling; related to 1 Veff

<!-- 来源：RTM2_UserManual_en_10_files\part672.htm -->

### SPECtrum:FREQuency:POSition

Defines the position of the spectrum.

<!-- 来源：RTM2_UserManual_en_10_files\part673.htm -->

### Parameters:

<Position>

<!-- 来源：RTM2_UserManual_en_10_files\part674.htm -->

### SPECtrum:FREQuency:RESet

Resets the Min, Max and Average waveforms to the current waveform.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part675.htm -->

### SPECtrum:FREQuency:SCALe

Sets the scaling of the spectrum analysis waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part676.htm -->

### Parameters:

<Scale>

<!-- 来源：RTM2_UserManual_en_10_files\part677.htm -->

### SPECtrum:FREQuency:WINDow:TYPE

Window functions are multiplied with the input values and thus can improve the spec- trum analysis display.

<!-- 来源：RTM2_UserManual_en_10_files\part678.htm -->

### Parameters:

<WindowFunction> RECTangular | HAMMing | HANNing | BLACkmanharris | FLATtop

<!-- 来源：RTM2_UserManual_en_10_files\part679.htm -->

### RECTangular

The rectangular window has high frequency accuracy with thin spectral lines, but with increased noise. Use this function pref- erably with pulse response tests where start and end values are zero.

<!-- 来源：RTM2_UserManual_en_10_files\part680.htm -->

### HAMMing

The Hamming window has higher noise level inside the spec- trum than Hann or Blackman, but smaller than the rectangular window. The width of the spectral lines is thinner than the other bell-shaped functions. Use this window to measure amplitudes of a periodical signal precisely.

<!-- 来源：RTM2_UserManual_en_10_files\part681.htm -->

### HANNing

The noise level within the spectrum is reduced and the width of the spectral lines enlarges. Use this window to measure ampli- tudes of a periodical signal precisely.

<!-- 来源：RTM2_UserManual_en_10_files\part682.htm -->

### BLACkmanharris

In the Blackman window the amplitudes can be measured very precisely. However, determining the frequency is more difficult. Use this window to measure amplitudes of a periodical signal precisely.

<!-- 来源：RTM2_UserManual_en_10_files\part683.htm -->

### FLATtop

The flat top window has low amplitude measurement errors but a poor frequency resolution. Use this window for accurate sin- gle-tone measurements and for measurement of amplitudes of sinusoidal frequency components.

### 18.10.3.2 Spectogram Settings

SPECtrum:SPECtrogram:RESet 511

SPECtrum:SPECtrogram:SCALe 511

<!-- 来源：RTM2_UserManual_en_10_files\part684.htm -->

### SPECtrum:SPECtrogram:RESet

Resets the current spectogram and starts a new recording of information.

### Usage: Event

### SPECtrum:SPECtrogram:SCALe <LinesPerAcquisition> Defines a zoom factor for the spectogram.

<!-- 来源：RTM2_UserManual_en_10_files\part685.htm -->

### Parameters:

<LinesPerAcquisition>Range: 1 to 20

Increment: 1

*RST: 1

### 18.10.3.3 Marker Settings

- Marker General Settings 511

- Marker Setup Settings 512

- Reference Marker Settings 513

- Marker Table 514

<!-- 来源：RTM2_UserManual_en_10_files\part686.htm -->

### Marker General Settings

SPECtrum:MARKer:DISPlay 511

SPECtrum:MARKer:SOURce 511

SPECtrum:MARKer[:ENABle] 512

### SPECtrum:MARKer:DISPlay <MarkerDisplay>

Enables the display of markers on the waveform diagram.

<!-- 来源：RTM2_UserManual_en_10_files\part687.htm -->

### Parameters:

<MarkerDisplay> OFF | INDex | RESult

<!-- 来源：RTM2_UserManual_en_10_files\part688.htm -->

### OFF

No marker display

<!-- 来源：RTM2_UserManual_en_10_files\part689.htm -->

### INDex

Markers are shown with index numbers of the peaks.

<!-- 来源：RTM2_UserManual_en_10_files\part690.htm -->

### RESult

Markers are shown with result values of the peaks.

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part691.htm -->

### SPECtrum:MARKer:SOURce

Sets the source for the marker search function.

<!-- 来源：RTM2_UserManual_en_10_files\part692.htm -->

### Parameters:

<Source> SPECtrum | MINHold | MAXHold | AVERage

*RST: SPEC

<!-- 来源：RTM2_UserManual_en_10_files\part693.htm -->

### SPECtrum:MARKer[:ENABle]

Enables the usage of markers.

<!-- 来源：RTM2_UserManual_en_10_files\part694.htm -->

### Parameters:

<MarkerEnable> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part695.htm -->

### Marker Setup Settings

SPECtrum:MARKer:SETup:DISTance 512

SPECtrum:MARKer:SETup:EXCursion 512

SPECtrum:MARKer:SETup:MLEVel 512

SPECtrum:MARKer:SETup:MMODe 512

SPECtrum:MARKer:SETup:MWIDth 513

<!-- 来源：RTM2_UserManual_en_10_files\part696.htm -->

### SPECtrum:MARKer:SETup:DISTance

Defines a distance between two subsequent peaks that has to be kept, for the peak to be detected.

<!-- 来源：RTM2_UserManual_en_10_files\part697.htm -->

### Parameters:

<Distance>

<!-- 来源：RTM2_UserManual_en_10_files\part698.htm -->

### SPECtrum:MARKer:SETup:EXCursion

Defines a level deifference between two subsequent peaks that has to be kept, for the peak to be detected.

<!-- 来源：RTM2_UserManual_en_10_files\part699.htm -->

### Parameters:

<Excursion>

<!-- 来源：RTM2_UserManual_en_10_files\part700.htm -->

### SPECtrum:MARKer:SETup:MLEVel

Sets the minimum level for marker peak detection.

<!-- 来源：RTM2_UserManual_en_10_files\part701.htm -->

### Parameters:

<MinimumLevel>

<!-- 来源：RTM2_UserManual_en_10_files\part702.htm -->

### SPECtrum:MARKer:SETup:MMODe

Sets the mode for marker detection.

<!-- 来源：RTM2_UserManual_en_10_files\part703.htm -->

### Parameters:

<MarkerMode> LONLy | ADVanced

<!-- 来源：RTM2_UserManual_en_10_files\part704.htm -->

### LONLy

```text
Level only detects a peak when a certain minimum level is reached. You can define the minimum level with SPECtrum: MARKer:SETup:MLEVel.
```

<!-- 来源：RTM2_UserManual_en_10_files\part705.htm -->

### ADVanced

Enables a more precise advanced peak definition.

<!-- 来源：RTM2_UserManual_en_10_files\part706.htm -->

### SPECtrum:MARKer:SETup:MWIDth

Sets the maximum width, that a peak can have for it to be detected.

<!-- 来源：RTM2_UserManual_en_10_files\part707.htm -->

### Parameters:

<MaximumWidth>

<!-- 来源：RTM2_UserManual_en_10_files\part708.htm -->

### Reference Marker Settings

SPECtrum:MARKer:REFerence:SETup:FREQuency 513

SPECtrum:MARKer:REFerence:SETup:INDex 513

SPECtrum:MARKer:REFerence:SETup:MODE 513

SPECtrum:MARKer:REFerence:SETup:SPAN 513

<!-- 来源：RTM2_UserManual_en_10_files\part709.htm -->

### SPECtrum:MARKer:REFerence:SETup:FREQuency

Sets the center frequency for the capture range, when

```text
EFFT:MARKer:REFerence:SETup:MODE RANGe.
```

<!-- 来源：RTM2_UserManual_en_10_files\part710.htm -->

### Parameters:

<ReferenceFrequency>

<!-- 来源：RTM2_UserManual_en_10_files\part711.htm -->

### SPECtrum:MARKer:REFerence:SETup:INDex

Sets the reference marker to the peak with the specified index, when

```text
EFFT:MARKer:REFerence:SETup:MODE INDicated.
```

<!-- 来源：RTM2_UserManual_en_10_files\part712.htm -->

### Parameters:

<ReferenceIndex>

<!-- 来源：RTM2_UserManual_en_10_files\part713.htm -->

### SPECtrum:MARKer:REFerence:SETup:MODE

Sets the mode for the selection of the reference peak. The peak with the highest level within the selected settings is set as the reference marker.

<!-- 来源：RTM2_UserManual_en_10_files\part714.htm -->

### Parameters:

<ReferenceMode> OFF | INDicated | RANGe

<!-- 来源：RTM2_UserManual_en_10_files\part715.htm -->

### SPECtrum:MARKer:REFerence:SETup:SPAN

Sets the span range, which is defined as the ratio of the capture range and the width of the specified reference mode, when EFFT:MARKer:REFerence:SETup:MODE RANGe.

<!-- 来源：RTM2_UserManual_en_10_files\part716.htm -->

### Parameters:

<ReferenceSpan>

<!-- 来源：RTM2_UserManual_en_10_files\part717.htm -->

### Marker Table

SPECtrum:MARKer:RCOunt? 514

SPECtrum:MARKer:RMODe 514

SPECtrum:MARKer:RTABle:ENABle 514

SPECtrum:MARKer:RTABle:POSition 515

SPECtrum:MARKer:RMARker? 515

SPECtrum:MARKer:RMARker:FREQuency? 515

SPECtrum:MARKer:RMARker:LEVel? 515

SPECtrum:MARKer:RESult<n>? 515

SPECtrum:MARKer:RESult<n>:ALL? 516

SPECtrum:MARKer:RESult<n>:ALL:DELTa? 516

SPECtrum:MARKer:RESult<n>:DELTa? 516

SPECtrum:MARKer:RESult<n>:FREQuency? 516

SPECtrum:MARKer:RESult<n>:FREQuency:DELTa? 517

SPECtrum:MARKer:RESult<n>:LEVel? 517

SPECtrum:MARKer:RESult<n>:LEVel:DELTa? 517

<!-- 来源：RTM2_UserManual_en_10_files\part718.htm -->

### SPECtrum:MARKer:RCOunt?

Returns the number of detected peaks.

<!-- 来源：RTM2_UserManual_en_10_files\part719.htm -->

### Parameters:

<ResultCount>

### Usage: Query only

### SPECtrum:MARKer:RMODe <ResultMode>

Sets the mode for the display of the results in the marker table.

<!-- 来源：RTM2_UserManual_en_10_files\part720.htm -->

### Parameters:

<ResultMode> ABSolute | FREQuency | LEVel | FLEVel

<!-- 来源：RTM2_UserManual_en_10_files\part721.htm -->

### ABSolute

The absolute values for both the frequency and level are dis- played.

<!-- 来源：RTM2_UserManual_en_10_files\part722.htm -->

### FREQuency

The delta between the reference freqeuncy and the correspond- ing freqeuncy value as well as the absolute level are displayed.

<!-- 来源：RTM2_UserManual_en_10_files\part723.htm -->

### LEVel

The delta between the reference level and the corresponding level value as well as the absolute frequency are displayed.

<!-- 来源：RTM2_UserManual_en_10_files\part724.htm -->

### FLEVel

The delta between the reference freqency/level and the corre- sponding freqency/level value are displayed.

### SPECtrum:MARKer:RTABle:ENABle <ResultTable> Enables the display of the marker table.

<!-- 来源：RTM2_UserManual_en_10_files\part725.htm -->

### Parameters:

<ResultTable> ON | OFF

*RST: OFF

### SPECtrum:MARKer:RTABle:POSition <TablePosition>

Defines the position of the marker table on the screen: top right, bottom right, or full screen. With full screen setting, the table covers nearly the complete righthand half of the screen.

<!-- 来源：RTM2_UserManual_en_10_files\part726.htm -->

### Parameters:

<TablePosition> TOP | BOTTom | FULLscreen

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part727.htm -->

### SPECtrum:MARKer:RMARker?

Returns the frequency and the level values of the present reference marker.

<!-- 来源：RTM2_UserManual_en_10_files\part728.htm -->

### Return values:

<ReferenceFrequency>

<ReferenceLevel>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part729.htm -->

### SPECtrum:MARKer:RMARker:FREQuency?

Queries the frequency of the reference marker.

<!-- 来源：RTM2_UserManual_en_10_files\part730.htm -->

### Return values:

<ReferenceFrequency>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part731.htm -->

### SPECtrum:MARKer:RMARker:LEVel?

Queries the level of the reference marker.

<!-- 来源：RTM2_UserManual_en_10_files\part732.htm -->

### Return values:

<ReferenceLevel>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part733.htm -->

### SPECtrum:MARKer:RESult<n>?

Returns the frequency and level values of the n-th marker.

<!-- 来源：RTM2_UserManual_en_10_files\part734.htm -->

### Suffix:

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part735.htm -->

### Return values:

<ResultFrequency>

<ResultLevel>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part736.htm -->

### SPECtrum:MARKer:RESult<n>:ALL?

Returns a list of all marker with the corresponding frequency and level values.

<!-- 来源：RTM2_UserManual_en_10_files\part737.htm -->

### Suffix:

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part738.htm -->

### Return values:

<ResultValues> List of numeric values with shape <freq>,<level>,....

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part739.htm -->

### SPECtrum:MARKer:RESult<n>:ALL:DELTa?

Queries the delta frequency and delta level, the difference between the freqeuncy/level of the specified marker and the freqeuncy/level of the reference marker.

<!-- 来源：RTM2_UserManual_en_10_files\part740.htm -->

### Suffix:

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part741.htm -->

### Return values:

<ResultValues> List of numeric values with shape <freq>,<level>,....

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part742.htm -->

### SPECtrum:MARKer:RESult<n>:DELTa?

Returns the difference in the values between the n-th marker and the reference marker.

<!-- 来源：RTM2_UserManual_en_10_files\part743.htm -->

### Suffix:

<n> *

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part744.htm -->

### SPECtrum:MARKer:RESult<n>:FREQuency?

Returns the frequency of the n-th marker.

<!-- 来源：RTM2_UserManual_en_10_files\part745.htm -->

### Suffix:

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part746.htm -->

### Return values:

<ResultFrequency>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part747.htm -->

### SPECtrum:MARKer:RESult<n>:FREQuency:DELTa?

Queries the delta frequency, the difference between the frequency of the specified marker and the level of the reference marker.

<!-- 来源：RTM2_UserManual_en_10_files\part748.htm -->

### Suffix:

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part749.htm -->

### Return values:

<ResultFrequencyDifference>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part750.htm -->

### SPECtrum:MARKer:RESult<n>:LEVel?

Returns the level of the n-th marker.

<!-- 来源：RTM2_UserManual_en_10_files\part751.htm -->

### Suffix:

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part752.htm -->

### Return values:

<ResultLevel>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part753.htm -->

### SPECtrum:MARKer:RESult<n>:LEVel:DELTa?

Queries the delta level, the difference between the level of the specified marker and the level of the reference marker.

<!-- 来源：RTM2_UserManual_en_10_files\part754.htm -->

### Suffix:

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part755.htm -->

### Return values:

<ResultLevelDifference>

### Usage: Query only

### 18.10.3.4 Frequency Domain Settings

<!-- 来源：RTM2_UserManual_en_10_files\part756.htm -->

### SPECtrum:FREQuency:CENTer

```text
Defines the position of the displayed frequency domain, which is (Center - Span/2) to (Center + Span/2). The width of the domain is defined using the command SPECtrum: FREQuency:SPAN.
```

<!-- 来源：RTM2_UserManual_en_10_files\part757.htm -->

### Parameters:

<CenterFrequency>

<!-- 来源：RTM2_UserManual_en_10_files\part758.htm -->

### SPECtrum:FREQuency:FULLspan

Performs the spectrum analysis calculation for the full frequency span.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part759.htm -->

### SPECtrum:FREQuency:SPAN

The span is specified in Hertz and defines the width of the displayed frequency range, which is (Center - Span/2) to (Center + Span/2).

<!-- 来源：RTM2_UserManual_en_10_files\part760.htm -->

### Parameters:

<Span>

<!-- 来源：RTM2_UserManual_en_10_files\part761.htm -->

### SPECtrum:FREQuency:STARt

Defines the start frequency of the displayed frequency domain at the left display edge:

Center - Span/2

You can set start and stop frequency instead of defining a center frequency and span.

<!-- 来源：RTM2_UserManual_en_10_files\part762.htm -->

### Parameters:

<StartFrequency> Range: Depends on various other settings, mainly on time

base, span/RBW ratio, and center frequency.

<!-- 来源：RTM2_UserManual_en_10_files\part763.htm -->

### SPECtrum:FREQuency:STOP

Defines the stop frequency of the displayed frequency domain at the right display edge: Center + Span/2

You can set start and stop frequency instead of defining a center frequency and span.

<!-- 来源：RTM2_UserManual_en_10_files\part764.htm -->

### Parameters:

<StopFrequency> Range: Depends on various other settings, mainly on time

base, span/RBW ratio, and center frequency.

### SPECtrum:FREQuency:BANDwidth[:RESolution]:AUTO <AutoSpanRBWratio> Enables the auto resolution bandwidth mode. In the auto mode "Span": "RBW" ratio of

~1:100 is set.

<!-- 来源：RTM2_UserManual_en_10_files\part765.htm -->

### Parameters:

<AutoSpanRBWratio>ON | OFF

*RST: ON

### SPECtrum:FREQuency:BANDwidth[:RESolution]:RATio <SpanRBWratio>

Defines the ratio of span (Hz) / resolution bandwidth (Hz). The span/RBW ratio is half the number of points used for FFT which is defined with manual operation in the menu.

<!-- 来源：RTM2_UserManual_en_10_files\part766.htm -->

### Parameters:

<SpanRBWratio> Range: The value is changed in 2^n steps from 2^10 to

2^15 (1024, 2048,4096,8192,16384, 32768).

### SPECtrum:FREQuency:BANDwidth[:RESolution][:VALue] <ResolutionBandwidth>

Defines the resolution bandwidth - the minimum frequency step at which the individual components of a spectrum can be distinguished.

<!-- 来源：RTM2_UserManual_en_10_files\part767.htm -->

### Parameters:

<ResolutionBandwidthR>ange: Depends on various other settings.

### 18.10.3.5 Time Domain Settings

SPECtrum:TIME:POSition 519

SPECtrum:TIME:RANGe 519

### SPECtrum:TIME:POSition <TimePosition>

Sets the time position of the analyzed time range.

<!-- 来源：RTM2_UserManual_en_10_files\part768.htm -->

### Parameters:

<TimePosition>

### SPECtrum:TIME:RANGe <TimeRange>

Sets the time range for the time domain diagram.

<!-- 来源：RTM2_UserManual_en_10_files\part769.htm -->

### Parameters:

<TimeRange>

### 18.10.3.6 Waveform Settings

SPECtrum:WAVeform:AVERage[:ENABle] 520

SPECtrum:WAVeform:MAXimum[:ENABle] 520

SPECtrum:WAVeform:MINimum[:ENABle] 520

SPECtrum:WAVeform:SPECtrum[:ENABle] 520

SPECtrum:WAVeform:AVERage:DATA? 520

SPECtrum:WAVeform:MAXimum:DATA? 520

SPECtrum:WAVeform:MINimum:DATA? 520

SPECtrum:WAVeform:SPECtrum:DATA? 520

SPECtrum:WAVeform:AVERage:DATA:HEADer? 520

SPECtrum:WAVeform:MAXimum:DATA:HEADer? 520

SPECtrum:WAVeform:MINimum:DATA:HEADer? 520

SPECtrum:WAVeform:SPECtrum:DATA:HEADer? 520

SPECtrum:WAVeform:AVERage:DATA:POINts? 521

SPECtrum:WAVeform:MAXimum:DATA:POINts? 521

SPECtrum:WAVeform:MINimum:DATA:POINts? 521

SPECtrum:WAVeform:SPECtrum:DATA:POINts? 521

SPECtrum:WAVeform:AVERage:DATA:XINCrement? 521

SPECtrum:WAVeform:MAXimum:DATA:XINCrement? 521

SPECtrum:WAVeform:MINimum:DATA:XINCrement? 521

SPECtrum:WAVeform:SPECtrum:DATA:XINCrement? 521

SPECtrum:WAVeform:AVERage:DATA:XORigin? 521

SPECtrum:WAVeform:MAXimum:DATA:XORigin? 521

SPECtrum:WAVeform:MINimum:DATA:XORigin? 521

SPECtrum:WAVeform:SPECtrum:DATA:XORigin? 521

SPECtrum:WAVeform:AVERage:DATA:YINCrement? 521

SPECtrum:WAVeform:MAXimum:DATA:YINCrement? 521

SPECtrum:WAVeform:MINimum:DATA:YINCrement? 521

SPECtrum:WAVeform:SPECtrum:DATA:YINCrement? 521

SPECtrum:WAVeform:AVERage:DATA:YORigin? 521

SPECtrum:WAVeform:MAXimum:DATA:YORigin? 521

SPECtrum:WAVeform:MINimum:DATA:YORigin? 522

SPECtrum:WAVeform:SPECtrum:DATA:YORigin? 522

SPECtrum:WAVeform:AVERage:DATA:YRESolution? 522

SPECtrum:WAVeform:MAXimum:DATA:YRESolution? 522

SPECtrum:WAVeform:MINimum:DATA:YRESolution? 522

SPECtrum:WAVeform:SPECtrum:DATA:YRESolution? 522

### SPECtrum:WAVeform:AVERage[:ENABle] <WaveformEnable> SPECtrum:WAVeform:MAXimum[:ENABle] <WaveformEnable> SPECtrum:WAVeform:MINimum[:ENABle] <WaveformEnable> SPECtrum:WAVeform:SPECtrum[:ENABle] <WaveformEnable>

Enables/diables the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part770.htm -->

### Parameters:

<WaveformEnable> ON | OFF

*RST: ON

<!-- 来源：RTM2_UserManual_en_10_files\part771.htm -->

### SPECtrum:WAVeform:AVERage:DATA? SPECtrum:WAVeform:MAXimum:DATA? SPECtrum:WAVeform:MINimum:DATA? SPECtrum:WAVeform:SPECtrum:DATA?

Returns the data of the indicated waveform points for transmission from the instrument to the controlling computer. The waveform data can be used in MATLAB, for example.

<!-- 来源：RTM2_UserManual_en_10_files\part772.htm -->

### Return values:

<Data> List of values

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part773.htm -->

### SPECtrum:WAVeform:AVERage:DATA:HEADer? SPECtrum:WAVeform:MAXimum:DATA:HEADer? SPECtrum:WAVeform:MINimum:DATA:HEADer? SPECtrum:WAVeform:SPECtrum:DATA:HEADer?

Returns information on the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part774.htm -->

### Return values:

<Header> StringData

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part775.htm -->

### SPECtrum:WAVeform:AVERage:DATA:POINts? SPECtrum:WAVeform:MAXimum:DATA:POINts? SPECtrum:WAVeform:MINimum:DATA:POINts? SPECtrum:WAVeform:SPECtrum:DATA:POINts?

Returns the number of data samples that are returned with

```text
SPECtrum:WAVeform:xxx:DATA for the indicated waveform.
```

<!-- 来源：RTM2_UserManual_en_10_files\part776.htm -->

### Return values:

<DataPoints>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part777.htm -->

### SPECtrum:WAVeform:AVERage:DATA:XINCrement? SPECtrum:WAVeform:MAXimum:DATA:XINCrement? SPECtrum:WAVeform:MINimum:DATA:XINCrement? SPECtrum:WAVeform:SPECtrum:DATA:XINCrement?

Return the level difference between two adjacent samples of the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part778.htm -->

### Return values:

<Xincrement>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part779.htm -->

### SPECtrum:WAVeform:AVERage:DATA:XORigin? SPECtrum:WAVeform:MAXimum:DATA:XORigin? SPECtrum:WAVeform:MINimum:DATA:XORigin? SPECtrum:WAVeform:SPECtrum:DATA:XORigin?

Returns the frequency of the first sample of the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part780.htm -->

### Return values:

<Xorigin>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part781.htm -->

### SPECtrum:WAVeform:AVERage:DATA:YINCrement? SPECtrum:WAVeform:MAXimum:DATA:YINCrement? SPECtrum:WAVeform:MINimum:DATA:YINCrement? SPECtrum:WAVeform:SPECtrum:DATA:YINCrement?

Returns the voltage value per bit of the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part782.htm -->

### Return values:

<Yincrement>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part783.htm -->

### SPECtrum:WAVeform:AVERage:DATA:YORigin? SPECtrum:WAVeform:MAXimum:DATA:YORigin?

### SPECtrum:WAVeform:MINimum:DATA:YORigin? SPECtrum:WAVeform:SPECtrum:DATA:YORigin?

Returns the vertical bit resolution of the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part784.htm -->

### Return values:

<Yorigin>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part785.htm -->

### SPECtrum:WAVeform:AVERage:DATA:YRESolution? SPECtrum:WAVeform:MAXimum:DATA:YRESolution? SPECtrum:WAVeform:MINimum:DATA:YRESolution? SPECtrum:WAVeform:SPECtrum:DATA:YRESolution?

Returns the vertical bit resolution of the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part786.htm -->

### Return values:

<Yresolution>

### Usage: Query only

### 18.10.3.7 Diagram Display Settings

SPECtrum:DIAGram:COLor:MAGNitude:MODE 522

SPECtrum:DIAGram:COLor:MAXimum[:LEVel] 522

SPECtrum:DIAGram:COLor:MINimum[:LEVel] 523

SPECtrum:DIAGram:COLor:SCHeme:FDOMain 523

SPECtrum:DIAGram:COLor:SCHeme:SPECtrogramm 523

SPECtrum:DIAGram:FDOMain[:ENABle] 523

SPECtrum:DIAGram:SPECtrogram[:ENABle] 523

SPECtrum:DIAGram:TDOMain[:ENABle] 523

### SPECtrum:DIAGram:COLor:MAGNitude:MODE <MagnitudeMode> Enables the magnitude coloring of the waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part787.htm -->

### Parameters:

<MagnitudeMode> ON | OFF

### SPECtrum:DIAGram:COLor:MAXimum[:LEVel] <MaximumLevel>

```text
Sets the level used as a maximum for the color scale selected with SPECtrum: DIAGram:COLor:SCHeme:FDOMain / SPECtrum:DIAGram:COLor:SCHeme: SPECtrogramm. All level values higher than the maximum will be displayed with the maximum color.
```

<!-- 来源：RTM2_UserManual_en_10_files\part788.htm -->

### Parameters:

<MaximumLevel>

### SPECtrum:DIAGram:COLor:MINimum[:LEVel] <MinimumLevel>

```text
Sets the level used as a minimum of the color scale selected with SPECtrum: DIAGram:COLor:SCHeme:FDOMain / SPECtrum:DIAGram:COLor:SCHeme: SPECtrogramm. All level values lower than the minimum will be displayed with the minimum color.
```

<!-- 来源：RTM2_UserManual_en_10_files\part789.htm -->

### Parameters:

<MinimumLevel>

### SPECtrum:DIAGram:COLor:SCHeme:FDOMain <ColorScheme>

Sets the color scale for the display of the waveform in the frequency domain diagram.

<!-- 来源：RTM2_UserManual_en_10_files\part790.htm -->

### Parameters:

<ColorScheme> MONochrom | TEMPerature | RAINbow

### SPECtrum:DIAGram:COLor:SCHeme:SPECtrogramm <ColorScheme> Sets the color scale for the display of the spectogram.

<!-- 来源：RTM2_UserManual_en_10_files\part791.htm -->

### Parameters:

<ColorScheme> MONochrom | TEMPerature | RAINbow

### SPECtrum:DIAGram:FDOMain[:ENABle] <Enable> Enables the display of the frequency domain diagram.

<!-- 来源：RTM2_UserManual_en_10_files\part792.htm -->

### Parameters:

<Enable> ON | OFF

### SPECtrum:DIAGram:SPECtrogram[:ENABle] <Enable> Enables the display of the spectrum diagram.

<!-- 来源：RTM2_UserManual_en_10_files\part793.htm -->

### Parameters:

<Enable> ON | OFF

### SPECtrum:DIAGram:TDOMain[:ENABle] <Enable> Enables the display of the time domain diagram.

<!-- 来源：RTM2_UserManual_en_10_files\part794.htm -->

### Parameters:

<Enable> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part795.htm -->

## 18.11 Masks

### 18.11.1 Mask Test Setup. 524

### 18.11.2 Actions on Violation 527

### 18.11.3 Mask Data. 529

<!-- 来源：RTM2_UserManual_en_10_files\part796.htm -->

### 18.11.1 Mask Test Setup

MASK:STATe 524

MASK:TEST 524

MASK:LOAD 524

MASK:SAVE 525

MASK:SOURce 525

MASK:CHCopy 525

MASK:YPOSition 525

MASK:YSCale 525

MASK:YWIDth 526

MASK:XWIDth 526

MASK:COUNt? 526

MASK:VCOunt? 526

MASK:RESet:COUNter 526

### MASK:STATe <State>

Turns the mask test mode on or off. When turning off, any temporarily stored new masks are deleted.

<!-- 来源：RTM2_UserManual_en_10_files\part797.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### MASK:TEST <Test>

Starts, finishes or interrupts a mask test.

<!-- 来源：RTM2_UserManual_en_10_files\part798.htm -->

### Parameters:

<Test> RUN | STOP | PAUSe

*RST: STOP

### MASK:LOAD <FileName>

Loads a stored mask from the specified file.

<!-- 来源：RTM2_UserManual_en_10_files\part799.htm -->

### Setting parameters:

<FileName> String parameter Path and file name

### Usage: Setting only

### MASK:SAVE <FileName>

Saves the current mask in the specified file.

<!-- 来源：RTM2_UserManual_en_10_files\part800.htm -->

### Setting parameters:

<FileName> String parameter Path and file name

### Usage: Setting only

### MASK:SOURce <Source>

Defines the channel to be compared with the mask.

<!-- 来源：RTM2_UserManual_en_10_files\part801.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4

CH3 and CH4 are only available on 4-channel R&S RTM mod- els.

*RST: CH1

<!-- 来源：RTM2_UserManual_en_10_files\part802.htm -->

### MASK:CHCopy

Creates a mask from the envelope waveform of the test source set with MASK:SOURce

.

### Usage: Event

### MASK:YPOSition <Yposition>

Moves the mask vertically within the display.

<!-- 来源：RTM2_UserManual_en_10_files\part803.htm -->

### Parameters:

<Yposition> Mask offset from the vertical center

Range: -200 to 200

Increment: 0,02

*RST: 0

Default unit: DIV

### MASK:YSCale <Yscale>

Changes the vertical scaling to stretch or compress the mask in y-direction.

<!-- 来源：RTM2_UserManual_en_10_files\part804.htm -->

### Parameters:

<Yscale> A value over 100% stretches the amplitudes; a value less than 100% compresses the amplitudes.

Range: 10 to 1000

Increment: 1

*RST: 100

Default unit: %

### MASK:YWIDth <Yaddition>

Changes the width of the mask in vertical direction.

<!-- 来源：RTM2_UserManual_en_10_files\part805.htm -->

### Parameters:

<Yaddition> The value is added to the y-values of the upper mask limit and subtracted from the y-values of the lower mask limit.

Range: 0 to 5,12

Increment: 0,04

*RST: 0

Default unit: DIV

### MASK:XWIDth <Xaddition>

Changes the width of the mask in horizontal direction.

<!-- 来源：RTM2_UserManual_en_10_files\part806.htm -->

### Parameters:

<Xaddition> The value is added to the positive x-values and subtracted from the negative x-values of the mask limits in relation to the mask center.

Range: 0 to 10

Increment: 0,01

*RST: 0

Default unit: DIV

<!-- 来源：RTM2_UserManual_en_10_files\part807.htm -->

### MASK:COUNt?

Returns the number of tested acquisitions.

<!-- 来源：RTM2_UserManual_en_10_files\part808.htm -->

### Return values:

<TotalCount> Total number of tested acquisitions

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part809.htm -->

### MASK:VCOunt?

Returns the number of acquistions that hit the mask.

<!-- 来源：RTM2_UserManual_en_10_files\part810.htm -->

### Return values:

<ViolationCount> Acquisition count

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part811.htm -->

### MASK:RESet:COUNter

Sets the counters of passed and failed acquisitions to Zero.

### Usage: Event

### Firmware/Software: FW 03.800

<!-- 来源：RTM2_UserManual_en_10_files\part812.htm -->

### 18.11.2 Actions on Violation

MASK:ACTion:SOUNd:EVENt:MODE 527

MASK:ACTion:STOP:EVENt:MODE 527

MASK:ACTion:SCRSave:EVENt:MODE 527

MASK:ACTion:PRINt:EVENt:MODE 527

MASK:ACTion:WFMSave:EVENt:MODE 527

MASK:ACTion:PULSe:EVENt:MODE 527

MASK:ACTion:SOUNd:EVENt:COUNt 528

MASK:ACTion:STOP:EVENt:COUNt 528

MASK:ACTion:SCRSave:EVENt:COUNt 528

MASK:ACTion:PRINt:EVENt:COUNt 528

MASK:ACTion:WFMSave:EVENt:COUNt 528

MASK:ACTion:PULSe:EVENt:COUNt 528

MASK:ACTion:SCRSave:DESTination 528

MASK:ACTion:WFMSave:DESTination 528

MASK:ACTion:PULSe:PLENgth 529

MASK:ACTion:PULSe:POLarity 529

### MASK:ACTion:SOUNd:EVENt:MODE <EventMode>

### MASK:ACTion:STOP:EVENt:MODE <EventMode>

### MASK:ACTion:SCRSave:EVENt:MODE <EventMode> MASK:ACTion:PRINt:EVENt:MODE <EventMode> MASK:ACTion:WFMSave:EVENt:MODE <EventMode> MASK:ACTion:PULSe:EVENt:MODE <EventMode>

Defines when and how often the action will be executed.

- SOUNd: Generates a beep sound on mask violation.

- STOP: Stops the waveform acquisition on mask violation.

- PRINt: Prints a screenshot to a printer connected to the USB connector on the front or rear panel.

```text
● SCRSave: Saves a screenshot on mask violation. To set path and filename of the screenshot, use MASK:ACTion:SCRSave:DESTination.
● WFMSave: Saves the waveform data on mask violation. To set path and filename of the data file, use MASK:ACTion:WFMSave:DESTination.
● PULSe: Creates a trigger out pulse on mask violation. To set the pulse width and polarity of the pulse, use the commands MASK:ACTion:PULSe:PLENgth and MASK:ACTion:PULSe:POLarity.
```

<!-- 来源：RTM2_UserManual_en_10_files\part813.htm -->

### Parameters:

<EventMode> OFF | EACH | SINGle | CYCLic

<!-- 来源：RTM2_UserManual_en_10_files\part814.htm -->

### OFF

No action is executed.

<!-- 来源：RTM2_UserManual_en_10_files\part815.htm -->

### EACH

The selected action is executed on each violation of the mask.

<!-- 来源：RTM2_UserManual_en_10_files\part816.htm -->

### SINGle

The selected action is executed once after the n-th violation.

<!-- 来源：RTM2_UserManual_en_10_files\part817.htm -->

### CYCLic

The selected action is executed repeatedly after each n-th viola- tion.

The number of violations <n> is set with the relevant MASK:ACTion:...:EVENt:COUNt command.

*RST: OFF

### Firmware/Software: FW 03.800, PULSe: 05.200

### MASK:ACTion:SOUNd:EVENt:COUNt <EventCount> MASK:ACTion:STOP:EVENt:COUNt <EventCount> MASK:ACTion:SCRSave:EVENt:COUNt <EventCount> MASK:ACTion:PRINt:EVENt:COUNt <EventCount> MASK:ACTion:WFMSave:EVENt:COUNt <EventCount> MASK:ACTion:PULSe:EVENt:COUNt <EventCount>

Sets the number of mask violations after which the action is executed. The command is only relevant if the associated MASK:ACTion:...:EVENt:MODE is set to SINGle or CYCLic.

<!-- 来源：RTM2_UserManual_en_10_files\part818.htm -->

### Parameters:

<EventCount> Integer value, number of mask violations

### Firmware/Software: FW 03.800, PULSe: 05.200

<!-- 来源：RTM2_UserManual_en_10_files\part819.htm -->

### MASK:ACTion:SCRSave:DESTination <File>

Defines the path and filename for a screenshot that will be saved on mask violation. The file format is PNG, the filename is incremented automatically

<!-- 来源：RTM2_UserManual_en_10_files\part820.htm -->

### Parameters:

<File> String parameter

### Example: MASK:ACT:SCRS:DEST "/USB_FRONT/MASKS/VIOL"

On first violation, the screeenshot is saved to VIOL.PNG, on second violation to VIOL01.PNG, the third to VIOL02.PNG...

<!-- 来源：RTM2_UserManual_en_10_files\part821.htm -->

### MASK:ACTion:WFMSave:DESTination <File>

Defines the path and filename for a waveform data that will be saved on mask viola- tion. The file format is CSV, the filename is incremented automatically

You can change the storage location, file name and/or file format manually in the FILE

> "Waveforms" menu. Remote control uses the recent settings.

<!-- 来源：RTM2_UserManual_en_10_files\part822.htm -->

### Parameters:

<File> String parameter

### Example: MASK:ACT:WFMS:DEST "/USB_FRONT/MASKS/VIOL"

On first violation, the waveform data is saved to VIOL.CSV, on second violation to VIOL01.CSV, the third to VIOL02.CSV...

### MASK:ACTion:PULSe:PLENgth <PulseLength>

Sets the pulse width of the trigger out pulse that is created on mask violation.

<!-- 来源：RTM2_UserManual_en_10_files\part823.htm -->

### Parameters:

<PulseLength> *RST: 1e-6

### MASK:ACTion:PULSe:POLarity <Polarity>

Sets the polarity of the trigger out pulse that is created on mask violation.

<!-- 来源：RTM2_UserManual_en_10_files\part824.htm -->

### Parameters:

<Polarity> POSitive | NEGative

*RST: POS

<!-- 来源：RTM2_UserManual_en_10_files\part825.htm -->

### 18.11.3 Mask Data

Consider also the following commands:

- FORMat[:DATA] on page 731

- MASK:DATA:XINCrement? on page 742

- MASK:DATA:XORigin? on page 742

- MASK:DATA:YINCrement? on page 743

- MASK:DATA:YORigin? on page 743

- MASK:DATA:YRESolution? on page 743

MASK:DATA? 529

MASK:DATA:HEADer? 530

MASK:SAVE 530

<!-- 来源：RTM2_UserManual_en_10_files\part826.htm -->

### MASK:DATA?

Returns the data of the mask. The mask consists of two limit curves. To set the export format, use FORMat[:DATA] on page 731.

<!-- 来源：RTM2_UserManual_en_10_files\part827.htm -->

### Return values:

<Data> List of values according to the format settings - the y-values of the mask points. The list contains two values for each sample interval.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part828.htm -->

### MASK:DATA:HEADer?

```text
Returns information on the mask data that is delivered with MASK:DATA?.
```

#### Table 18-7: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Number of samples | 200000 |
| 4 | Number of values per sample interval. For masks the value is 2. | 2 |

<!-- 来源：RTM2_UserManual_en_10_files\part829.htm -->

### Return values:

<DataHeader> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,2

### Usage: Query only

### MASK:SAVE <FileName>

Saves the current mask in the specified file.

<!-- 来源：RTM2_UserManual_en_10_files\part830.htm -->

### Setting parameters:

<FileName> String parameter Path and file name

### Usage: Setting only

<!-- 来源：RTM2_UserManual_en_10_files\part831.htm -->

## 18.12 Search

- General Search Configuration 531

- Edge Search Configuration 534

- Width Search Configuration 534

- Peak Search Configuration 536

- Rise/Fall Time Search Configuration 537

- Runt Search Configuration 539

- Data2Clock Search Configuration 541

- Pattern Search Configuration 542

- Search Results 545

<!-- 来源：RTM2_UserManual_en_10_files\part832.htm -->

### 18.12.1 General Search Configuration

SEARch:STATe 531

SEARch:CONDition 531

SEARch:SOURce 533

SEARch:GATE:MODE 533

SEARch:GATE:ABSolute:START 533

SEARch:GATE:ABSolute:STOP 534

### SEARch:STATe <SearchState> Enables and disables the search mode.

<!-- 来源：RTM2_UserManual_en_10_files\part833.htm -->

### Parameters:

<SearchState> ON | OFF

*RST: OFF

Example: Chapter 18.2.2.1, "Searching for a Pulse of Specified Width", on page 407

### Firmware/Software: FW 03.400

### SEARch:CONDition <SearchCondition> Selects the event you want to search for.

<!-- 来源：RTM2_UserManual_en_10_files\part834.htm -->

### Parameters:

<SearchCondition> EDGE | WIDTh | PEAK | RUNT | RTIMe | DATatoclock | PATTern | PROTocol

<!-- 来源：RTM2_UserManual_en_10_files\part835.htm -->

### EDGE

An edge search result is found when the waveform passes the given level in the specified direction.

<!-- 来源：RTM2_UserManual_en_10_files\part836.htm -->

### WIDTH

A width search finds pulses with an exact pulse width, or pulses shorter or longer than a given time, or pulses inside or outside the allowable time range.

<!-- 来源：RTM2_UserManual_en_10_files\part837.htm -->

### PEAK

The peak search finds pulses exceeding a given amplitude.

<!-- 来源：RTM2_UserManual_en_10_files\part838.htm -->

### RUNT

The runt search finds pulses lower than normal in amplitude. The amplitude crosses the first threshold twice without crossing the second one. In addition to the threshold amplitudes, you can define a time limit for the runt in the same way as for width search: runts with exact width, shorter or longer than a given time, or runts inside or outside the allowable time range.

<!-- 来源：RTM2_UserManual_en_10_files\part839.htm -->

### RTIMe

The rise or fall time search finds slopes with an exact rise or fall time, or rise/fall times shorter or longer than a given limit, or rise/ fall times inside or outside the allowable time range.

<!-- 来源：RTM2_UserManual_en_10_files\part840.htm -->

### DATatoclock

The Data2Clock search - also known as setup/hold - finds viola- tion of setup and hold times. It analyzes the relative timing between two signals: a data signal and the synchronous clock signal. Setup time is the time that the data signal is steady before clock edge. Hold time is the time that the data signal is steady after clock edge.

<!-- 来源：RTM2_UserManual_en_10_files\part841.htm -->

### PATTern

The pattern search finds logical combinations of channel states inside or outside a specified time range. For each channel, its state and threshold level is defined. The states are combined logically, and the time of true pattern results is compared with a specified time range.

<!-- 来源：RTM2_UserManual_en_10_files\part842.htm -->

### PROTocol

The protocol search finds various events in decoded data of CAN or LIN signals, for example, a specified frame type, identi- fier, data, and errors. Available search settings depend on the configured bus type. For bus types PARallel, I2C, SPI, SSPI, and UART no search is available.

See also: BUS<b>:TYPE on page 548

*RST: EDGE

Example: Chapter 18.2.2.1, "Searching for a Pulse of Specified Width", on page 407

### Firmware/Software: FW 03.400

### SEARch:SOURce <SearchSource> Selects the waveform to be analyzed.

<!-- 来源：RTM2_UserManual_en_10_files\part843.htm -->

### Parameters:

<SearchSource> CH1 | CH2 | CH3 | CH4 | MA1 | MA2 | MA3 | MA4 | RE1 | RE2 | RE3 | RE4 | SBUS1 | SBUS2 | SBUS3 | SBUS4

Any active channel, math, or reference waveform can be searched.

For protocol search on CAN and LIN signals, an active serial bus is the search source.

*RST: CH1

Example: Chapter 18.2.2.1, "Searching for a Pulse of Specified Width", on page 407

### Firmware/Software: FW 03.400

<!-- 来源：RTM2_UserManual_en_10_files\part844.htm -->

### SEARch:GATE:MODE

Defines the search area. If the search is performed on a running acquisition series, the instrument analyzes the displayed data. The search on a stopped acquisition analyzes the contents of the memory.

<!-- 来源：RTM2_UserManual_en_10_files\part845.htm -->

### Parameters:

<GateMode> OFF | DISPlay | ABSolute

<!-- 来源：RTM2_UserManual_en_10_files\part846.htm -->

### OFF

Running acquisition: all waveform samples that are displayed on the screen.

Stopped acquisition: all data samples that are stored in the memory.

<!-- 来源：RTM2_UserManual_en_10_files\part847.htm -->

### DISPlay

Search is restricted to the time range of the display.

<!-- 来源：RTM2_UserManual_en_10_files\part848.htm -->

### ABSolute

```text
Search is restricted to the time range defined by SEARch: GATE:ABSolute:START and SEARch:GATE:ABSolute:STOP
```

.

### SEARch:GATE:ABSolute:START <StartTime>

Sets the start time of the search area in relation to the trigger point if SEARch:GATE: MODE on page 533 is set to ABSolute.

<!-- 来源：RTM2_UserManual_en_10_files\part849.htm -->

### Parameters:

<StartTime> Default unit: s

### SEARch:GATE:ABSolute:STOP <StopTime>

Sets the end time of the search area in relation to the trigger point if SEARch:GATE: MODE on page 533 is set to ABSolute.

<!-- 来源：RTM2_UserManual_en_10_files\part850.htm -->

### Parameters:

<StopTime> Default unit: s

<!-- 来源：RTM2_UserManual_en_10_files\part851.htm -->

### 18.12.2 Edge Search Configuration

SEARch:TRIGger:EDGE:SLOPe 534

SEARch:TRIGger:EDGE:LEVel 534

SEARch:TRIGger:EDGE:LEVel:DELTa 534

### SEARch:TRIGger:EDGE:SLOPe <Slope> Sets the slope to be found.

<!-- 来源：RTM2_UserManual_en_10_files\part852.htm -->

### Parameters:

<Slope> POSitive | NEGative | EITHer

*RST: POS

### Firmware/Software: FW 03.400

### SEARch:TRIGger:EDGE:LEVel <Level> Sets the voltage level for the edge search.

<!-- 来源：RTM2_UserManual_en_10_files\part853.htm -->

### Parameters:

<Level> *RST: 0.6 V

### Firmware/Software: FW 03.400

### SEARch:TRIGger:EDGE:LEVel:DELTa <DeltaLevel>

Sets a hysteresis range above and below the search level to avoid unwanted search results caused by noise oscillation around the level.

<!-- 来源：RTM2_UserManual_en_10_files\part854.htm -->

### Parameters:

<DeltaLevel> Range: Lower limit depends on vertical scale and other set-

tings, no upper limit

*RST: 0.2 V

### Firmware/Software: FW 03.400

<!-- 来源：RTM2_UserManual_en_10_files\part855.htm -->

### 18.12.3 Width Search Configuration

SEARch:TRIGger:WIDTh:POLarity 535

SEARch:TRIGger:WIDTh:LEVel 535

SEARch:TRIGger:WIDTh:LEVel:DELTa 535

SEARch:TRIGger:WIDTh:RANGe 535

SEARch:TRIGger:WIDTh:WIDTh 536

SEARch:TRIGger:WIDTh:DELTa 536

### SEARch:TRIGger:WIDTh:POLarity <Polarity> Indicates the polarity of the pulse to be searched for.

<!-- 来源：RTM2_UserManual_en_10_files\part856.htm -->

### Parameters:

<Polarity> POSitive | NEGative

*RST: POS

Example: Chapter 18.2.2.1, "Searching for a Pulse of Specified Width", on page 407

### Firmware/Software: FW 03.400

### SEARch:TRIGger:WIDTh:LEVel <Level>

Sets the voltage level on which the pulse width is measured.

<!-- 来源：RTM2_UserManual_en_10_files\part857.htm -->

### Parameters:

<Level> *RST: 500 mV

### Firmware/Software: FW 03.400

### SEARch:TRIGger:WIDTh:LEVel:DELTa <DeltaLevel>

Sets a hysteresis range above and below the search level to avoid unwanted search results caused by noise oscillation around the level.

<!-- 来源：RTM2_UserManual_en_10_files\part858.htm -->

### Parameters:

<DeltaLevel> Range: Lower limit depends on vertical scale and other set-

tings, no upper limit

*RST: 200 mV

### Firmware/Software: FW 03.400

### SEARch:TRIGger:WIDTh:RANGe <Range>

```text
Sets how the measured pulse width is compared with the given limit(s). To set the width, use SEARch:TRIGger:WIDTh:WIDTh.
To set the range ± Δt, use SEARch:TRIGger:WIDTh:DELTa.
```

<!-- 来源：RTM2_UserManual_en_10_files\part859.htm -->

### Parameters:

<Range> WITHin | OUTSide | SHORter | LONGer

<!-- 来源：RTM2_UserManual_en_10_files\part860.htm -->

### WITHin

Finds pulses inside the range width ± Δt.

<!-- 来源：RTM2_UserManual_en_10_files\part861.htm -->

### OUTSide

Finds pulses outside the range width ± Δt.

<!-- 来源：RTM2_UserManual_en_10_files\part862.htm -->

### SHORter

Finds pulses shorter than the given width.

<!-- 来源：RTM2_UserManual_en_10_files\part863.htm -->

### LONGer

Finds pulses longer than the given width.

*RST: WITH

Example: Chapter 18.2.2.1, "Searching for a Pulse of Specified Width", on page 407

### Firmware/Software: FW 03.400

### SEARch:TRIGger:WIDTh:WIDTh <Width>

Sets the reference pulse width, the nominal value for comparisons.

<!-- 来源：RTM2_UserManual_en_10_files\part864.htm -->

### Parameters:

<Width> Default unit: s

Example: Chapter 18.2.2.1, "Searching for a Pulse of Specified Width", on page 407

### Firmware/Software: FW 03.400

### SEARch:TRIGger:WIDTh:DELTa <DeltaWidth>

```text
Sets a range Δt to the reference pulse width set with SEARch:TRIGger:WIDTh: WIDTh if SEARch:TRIGger:WIDTh:RANGe is set to WITHin or OUTSide
```

<!-- 来源：RTM2_UserManual_en_10_files\part865.htm -->

### Parameters:

<DeltaWidth> Range: Lower limit depends on the resolution, practically no

upper limit

Example: Chapter 18.2.2.1, "Searching for a Pulse of Specified Width", on page 407

### Firmware/Software: FW 03.400

<!-- 来源：RTM2_UserManual_en_10_files\part866.htm -->

### 18.12.4 Peak Search Configuration

SEARch:MEASure:PEAK:POLarity 536

SEARch:MEASure:LEVel:PEAK:MAGNitude 537

### SEARch:MEASure:PEAK:POLarity <Polarity>

Indicates the polarity of a the pulse to be searched for a peak.

<!-- 来源：RTM2_UserManual_en_10_files\part867.htm -->

### Parameters:

<Polarity> POSitive | NEGative | EITHer

*RST: POS

### Firmware/Software: FW 03.400

### SEARch:MEASure:LEVel:PEAK:MAGNitude <Magnitude> Sets the amplitude limit.

<!-- 来源：RTM2_UserManual_en_10_files\part868.htm -->

### Parameters:

<Magnitude> Default unit: V

### Firmware/Software: FW 03.400

<!-- 来源：RTM2_UserManual_en_10_files\part869.htm -->

### 18.12.5 Rise/Fall Time Search Configuration

SEARch:TRIGger:RISetime:SLOPe 537

SEARch:TRIGger:LEVel:RISetime:LOWer 537

SEARch:TRIGger:LEVel:RISetime:UPPer 538

SEARch:TRIGger:RISetime:RANGe 538

SEARch:TRIGger:RISetime:TIME 538

SEARch:TRIGger:RISetime:DELTa 538

### SEARch:TRIGger:RISetime:SLOPe <Polarity> Sets the slope to be found.

<!-- 来源：RTM2_UserManual_en_10_files\part870.htm -->

### Parameters:

<Polarity> POSitive | NEGative | EITHer

POSitive: to search for rise time. NEGative to search for fall time. EITHer: to search for rise and fall time

*RST: POS

### Firmware/Software: FW 03.700

### SEARch:TRIGger:LEVel:RISetime:LOWer <LowerLevel>

Sets the lower voltage threshold. When the signal crosses this level, the rise time mea- surement starts or stops depending on the selected slope.

<!-- 来源：RTM2_UserManual_en_10_files\part871.htm -->

### Parameters:

<LowerLevel> *RST: 400 mV

Default unit: V

### Firmware/Software: FW 03.700

### SEARch:TRIGger:LEVel:RISetime:UPPer <UpperLevel>

Sets the upper voltage threshold. When the signal crosses this level, the rise/fall time measurement starts or stops depending on the selected slope.

<!-- 来源：RTM2_UserManual_en_10_files\part872.htm -->

### Parameters:

<UpperLevel> *RST: 600 mV

Default unit: V

### Firmware/Software: FW 03.700

<!-- 来源：RTM2_UserManual_en_10_files\part873.htm -->

### SEARch:TRIGger:RISetime:RANGe <Range>

```text
Sets how the measured rise or fall time is compared with the given limit(s). To set the rise/fall time, use SEARch:TRIGger:RISetime:TIME.
To set the range ± Δt, use SEARch:TRIGger:RISetime:DELTa.
```

<!-- 来源：RTM2_UserManual_en_10_files\part874.htm -->

### Parameters:

<Range> LONGer | SHORter | WITHin | OUTSide

<!-- 来源：RTM2_UserManual_en_10_files\part875.htm -->

### LONGer

Finds rise/fall times longer than the given time.

<!-- 来源：RTM2_UserManual_en_10_files\part876.htm -->

### SHORter

Finds rise/fall times shorter than the given time.

<!-- 来源：RTM2_UserManual_en_10_files\part877.htm -->

### WITHin

Finds rise/fall times inside the range time ± Δt.

<!-- 来源：RTM2_UserManual_en_10_files\part878.htm -->

### OUTSide

Finds rise/fall times outside the range time ± Δt.

*RST: LONG

### Firmware/Software: FW 03.700

<!-- 来源：RTM2_UserManual_en_10_files\part879.htm -->

### SEARch:TRIGger:RISetime:TIME <Time>

Sets the reference rise or fall time, the nominal value for comparisons.

<!-- 来源：RTM2_UserManual_en_10_files\part880.htm -->

### Parameters:

<Time> Range: Depends on various settings, mainly time base and

sample rate

*RST: 200e-6

Default unit: s

### Firmware/Software: FW 03.700

### SEARch:TRIGger:RISetime:DELTa <DeltaTime>

Sets a range Δt to the reference rise/fall time set with SEARch:TRIGger:RISetime: TIME if SEARch:TRIGger:RISetime:RANGe on page 538 is set to Within or Outside. The instrument finds rise/fall times inside or outside the range time ± Δt.

<!-- 来源：RTM2_UserManual_en_10_files\part881.htm -->

### Parameters:

<DeltaTime> Range: Depends on various settings, mainly time base and

sample rate

*RST: 50e-6

Default unit: s

### Firmware/Software: FW 03.700

<!-- 来源：RTM2_UserManual_en_10_files\part882.htm -->

### 18.12.6 Runt Search Configuration

SEARch:TRIGger:RUNT:POLarity 539

SEARch:TRIGger:LEVel:RUNT:LOWer 539

SEARch:TRIGger:LEVel:RUNT:UPPer 539

SEARch:TRIGger:RUNT:RANGe 540

SEARch:TRIGger:RUNT:WIDTh 540

SEARch:TRIGger:RUNT:DELTa 540

### SEARch:TRIGger:RUNT:POLarity <Polarity> Indicates the polarity of a the runt to be searched for.

<!-- 来源：RTM2_UserManual_en_10_files\part883.htm -->

### Parameters:

<Polarity> POSitive | NEGative | EITHer

*RST: POS

### Firmware/Software: FW 03.700

### SEARch:TRIGger:LEVel:RUNT:LOWer <LowerLevel>

Sets the lower voltage threshold for runt detection. A positive runt crosses the lower level twice without crossing the upper level.

<!-- 来源：RTM2_UserManual_en_10_files\part884.htm -->

### Parameters:

<LowerLevel> *RST: 400 mV

Default unit: V

### Firmware/Software: FW 03.700

### SEARch:TRIGger:LEVel:RUNT:UPPer <UpperLevel>

Sets the upper voltage threshold for runt detection. A negative runt crosses the upper level twice without crossing the lower level.

<!-- 来源：RTM2_UserManual_en_10_files\part885.htm -->

### Parameters:

<UpperLevel> *RST: 600 mV

Default unit: V

### Firmware/Software: FW 03.700

### SEARch:TRIGger:RUNT:RANGe <Range>

```text
Sets how the measured pulse width is compared with the given limit(s). To set the width, use SEARch:TRIGger:RUNT:WIDTh.
To set the range ± Δt, use SEARch:TRIGger:RUNT:DELTa.
```

<!-- 来源：RTM2_UserManual_en_10_files\part886.htm -->

### Parameters:

<Range> LONGer | SHORter | WITHin | OUTSide

<!-- 来源：RTM2_UserManual_en_10_files\part887.htm -->

### LONGer

Finds pulses longer than the given width.

<!-- 来源：RTM2_UserManual_en_10_files\part888.htm -->

### SHORter

Finds pulses shorter than the given width.

<!-- 来源：RTM2_UserManual_en_10_files\part889.htm -->

### WITHin

Finds pulses inside the range width ± Δt.

<!-- 来源：RTM2_UserManual_en_10_files\part890.htm -->

### OUTSide

Finds pulses outside the range width ± Δt.

*RST: LONG

### Firmware/Software: FW 03.700

### SEARch:TRIGger:RUNT:WIDTh <Width>

Sets the reference runt pulse width, the nominal value for comparisons.

<!-- 来源：RTM2_UserManual_en_10_files\part891.htm -->

### Parameters:

<Width> Range: Depends on various settings, mainly time base and

sample rate

*RST: 200e-6

Default unit: s

### Firmware/Software: FW 03.700

### SEARch:TRIGger:RUNT:DELTa <DeltaWidth>

Sets a range Δt to the reference pulse width set with SEARch:TRIGger:RUNT:WIDTh

if SEARch:TRIGger:RUNT:RANGe on page 540 is set to WITHin or OUTSide.

<!-- 来源：RTM2_UserManual_en_10_files\part892.htm -->

### Parameters:

<DeltaWidth> Range: Depends on various settings, mainly time base and

sample rate

*RST: 50e-6

Default unit: s

### Firmware/Software: FW 03.700

<!-- 来源：RTM2_UserManual_en_10_files\part893.htm -->

### 18.12.7 Data2Clock Search Configuration

SEARch:TRIGger:DATatoclock:CSOurce 541

SEARch:TRIGger:DATatoclock:CLEVel 541

SEARch:TRIGger:DATatoclock:DLEVel 541

SEARch:TRIGger:DATatoclock:CLEVel:DELTa 541

SEARch:TRIGger:DATatoclock:DLEVel:DELTa 541

SEARch:TRIGger:DATatoclock:CEDGe 542

SEARch:TRIGger:DATatoclock:HTIMe 542

SEARch:TRIGger:DATatoclock:STIMe 542

### SEARch:TRIGger:DATatoclock:CSOurce <ClockSource> Selects the input channel of the clock signal.

<!-- 来源：RTM2_UserManual_en_10_files\part894.htm -->

### Parameters:

<ClockSource> CH1 | CH2 | CH3 | CH4 | MA1 | MA2 | MA3 | MA4 | MA5 | RE1 | RE2 | RE3 | RE4

*RST: CH1

### Firmware/Software: FW 03.800

### SEARch:TRIGger:DATatoclock:CLEVel <ClockLevel>

Sets the voltage level for the clock signal. Clock level and clock edge define the refer- ence point for setup and hold time.

<!-- 来源：RTM2_UserManual_en_10_files\part895.htm -->

### Parameters:

<ClockLevel> Range: depends on vertical scale

### Firmware/Software: FW 03.800

### SEARch:TRIGger:DATatoclock:DLEVel <DataLevel>

Sets the voltage level for the data signal. The data lavel defines the point of data tran- sition.

<!-- 来源：RTM2_UserManual_en_10_files\part896.htm -->

### Parameters:

<DataLevel> Range: depends on vertical scale

### Firmware/Software: FW 03.800

### SEARch:TRIGger:DATatoclock:CLEVel:DELTa <LevelDelta>

### SEARch:TRIGger:DATatoclock:DLEVel:DELTa <LevelDelta>

Set a hysteresis range to the clock and data levels in order to avoid unwanted search results caused by noise oscillation around the level. For a rising edge, the hysteresis is below the search level. Otherwise, for a falling edge the hysteresis is above the level.

<!-- 来源：RTM2_UserManual_en_10_files\part897.htm -->

### Parameters:

<LevelDelta> Range: Lower limit depends on vertical scale and other set-

tings, no upper limit

### Firmware/Software: FW 03.800

### SEARch:TRIGger:DATatoclock:CEDGe <ClockEdge>

Sets the edge of the clock signal to define the time reference point for the setup and hold time.

<!-- 来源：RTM2_UserManual_en_10_files\part898.htm -->

### Parameters:

<ClockEdge> POSitive | NEGative | EITHer

*RST: POS

### Firmware/Software: FW 03.800

### SEARch:TRIGger:DATatoclock:HTIMe <HoldTime>

Sets the minimum time after the clock edge while the data signal must stay steady above or below the data level. The hold time can be negative. In this case, the hold time ends before the clock edge, and the setup time must be positive and longer than the absolute value of the hold time.

<!-- 来源：RTM2_UserManual_en_10_files\part899.htm -->

### Parameters:

<HoldTime> Range: depends on time base and sample interval

### Firmware/Software: FW 03.800

### SEARch:TRIGger:DATatoclock:STIMe <SetupTime>

Sets the minimum time before the clock edge while the data signal must stay steady above or below the data level. The setup time can be negative. In this case, the setup interval starts after the clock edge, and the hold time must be positive and longer than the absolute value of the setup time.

<!-- 来源：RTM2_UserManual_en_10_files\part900.htm -->

### Parameters:

<SetupTime> Range: depends on time base and sample interval

### Firmware/Software: FW 03.800

<!-- 来源：RTM2_UserManual_en_10_files\part901.htm -->

### 18.12.8 Pattern Search Configuration

SEARch:TRIGger:PATTern:SOURce 542

SEARch:TRIGger:PATTern:FUNCtion 543

SEARch:TRIGger:PATTern:LEVel<n> 543

SEARch:TRIGger:PATTern:LEVel<n>:DELTa 543

SEARch:TRIGger:PATTern:WIDTh:RANGe 544

SEARch:TRIGger:PATTern:WIDTh[:WIDTh] 544

SEARch:TRIGger:PATTern:WIDTh:DELTa 544

### SEARch:TRIGger:PATTern:SOURce <Pattern> Specifies the search pattern - the state for each channel.

<!-- 来源：RTM2_UserManual_en_10_files\part902.htm -->

### Parameters:

<Pattern> String parameter

String containing 0, 1, X|x for each channel. The order of chan- nels is fixed: CH1 CH2 [CH3 CH4].

### Example: SEAR:TRIG:PATT:SOUR '1X10'

```text
CH1, CH3 are high, CH4 is low. These states are logically com- bined with SEARch:TRIGger:PATTern:FUNCtion. CH2 does not matter (don't care).
```

### SEARch:TRIGger:PATTern:FUNCtion <Function> Sets the logical combination of the channel states.

<!-- 来源：RTM2_UserManual_en_10_files\part903.htm -->

### Parameters:

<Function> AND | OR | NAND | NOR

<!-- 来源：RTM2_UserManual_en_10_files\part904.htm -->

### AND

The required states of all channels must appear in the input sig- nal at the same time.

<!-- 来源：RTM2_UserManual_en_10_files\part905.htm -->

### OR

At least one of the channels must have the required state.

<!-- 来源：RTM2_UserManual_en_10_files\part906.htm -->

### NAND

"Not and" operator, at least one of the channels does not have the required state.

<!-- 来源：RTM2_UserManual_en_10_files\part907.htm -->

### NOR

"Not or" operator, none of the channels has the required state.

*RST: AND

### SEARch:TRIGger:PATTern:LEVel<n> <ThresholdLevel>

Sets the threshold value for each specified source channel. You can set different levels for the channels

<!-- 来源：RTM2_UserManual_en_10_files\part908.htm -->

### Suffix:

<n> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part909.htm -->

### Parameters:

<ThresholdLevel> Range: Depends on vertical scale

### SEARch:TRIGger:PATTern:LEVel<n>:DELTa <LevelDelta>

Sets a hysteresis range to the level of the specified source channel in order to avoid unwanted search results caused by noise oscillation around the level. For a rising edge, the hysteresis is below the search level. Otherwise, for a falling edge the hyste- resis is above the level.

<!-- 来源：RTM2_UserManual_en_10_files\part910.htm -->

### Suffix:

<n> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part911.htm -->

### Parameters:

<LevelDelta> Range: Lower limit depends on vertical scale and other set-

tings, no upper limit

<!-- 来源：RTM2_UserManual_en_10_files\part912.htm -->

### SEARch:TRIGger:PATTern:WIDTh:RANGe <Range>

Sets the condition how the duration of a steady pattern is compared with the given ref- erence time.

To set the reference value width, use SEARch:TRIGger:PATTern:WIDTh[:WIDTh]

on page 544.

To set a range Δt, use SEARch:TRIGger:PATTern:WIDTh:DELTa on page 544

<!-- 来源：RTM2_UserManual_en_10_files\part913.htm -->

### Parameters:

<Range> WITHin | OUTSide | LONGer | SHORter

<!-- 来源：RTM2_UserManual_en_10_files\part914.htm -->

### WITHin

Finds patterns steady for a time range width ± Δt.

<!-- 来源：RTM2_UserManual_en_10_files\part915.htm -->

### OUTSide

Finds patterns outside a time range width ± Δt.

<!-- 来源：RTM2_UserManual_en_10_files\part916.htm -->

### LONGer

Finds patterns steady for at least the given width.

<!-- 来源：RTM2_UserManual_en_10_files\part917.htm -->

### SHORter

Finds patterns shorter than the given width.

*RST: LONG

<!-- 来源：RTM2_UserManual_en_10_files\part918.htm -->

### SEARch:TRIGger:PATTern:WIDTh[:WIDTh] <Width>

Sets the reference time of a steady pattern, the nominal value for comparisons.

<!-- 来源：RTM2_UserManual_en_10_files\part919.htm -->

### Parameters:

<Width> Default unit: s

### SEARch:TRIGger:PATTern:WIDTh:DELTa <DeltaTime>

Sets a range Δt to the reference pattern duration set with SEARch:TRIGger: PATTern:WIDTh[:WIDTh] if SEARch:TRIGger:PATTern:WIDTh:RANGe is set to WITHin or OUTSide.

<!-- 来源：RTM2_UserManual_en_10_files\part920.htm -->

### Parameters:

<DeltaTime> Default unit: s

<!-- 来源：RTM2_UserManual_en_10_files\part921.htm -->

### 18.12.9 Search Results

SEARch:RESult:BCOunt? 545

SEARch:RESDiagram:SHOW 545

SEARch:RESult:ALL? 545

SEARch:RESult<n>? 546

SEARch:RCOunt? 546

EXPort:SEARch:NAME 547

EXPort:SEARch:SAVE 547

<!-- 来源：RTM2_UserManual_en_10_files\part922.htm -->

### SEARch:RESult:BCOunt?

Returns the maximum number of search results which the instrument can store.

<!-- 来源：RTM2_UserManual_en_10_files\part923.htm -->

### Return values:

<BufferedCount> Number of search results

### Usage: Query only

### SEARch:RESDiagram:SHOW <ResultShow> Shows or hides the table of search results.

<!-- 来源：RTM2_UserManual_en_10_files\part924.htm -->

### Parameters:

<ResultShow> ON | OFF

*RST: OFF

Example: Chapter 18.2.2.1, "Searching for a Pulse of Specified Width", on page 407

### Firmware/Software: FW 03.400

<!-- 来源：RTM2_UserManual_en_10_files\part925.htm -->

### SEARch:RESult:ALL?

Returns all result values of the search.

<!-- 来源：RTM2_UserManual_en_10_files\part926.htm -->

### Return values:

<AllResults> List of results items seperated by comma

For each result, six values are returned:

1. Result number as indicated in the search results table

2. X-position (time) of the search result

3. Y-position of the search result, currently not relevant

4. Type of the search result (Edge, Peak,...)

5. Slope or polarity of the search result

6. For peak searches, the value contains the peak voltage. For width searches, it contains the pulse width. For edge searches, the value is not relevant.

### Example: SEARch:RESult:ALL?

Returns all four results of a peak search:

```text
1,-4.7750e-04,0,PEAK,NEGATIVE,-1.530e-02,2,
-4.4630e-04,0,PEAK,NEGATIVE,-1.530e-02,3,
-4.1660e-04,0,PEAK,NEGATIVE,-1.530e-02,4,
-3.8690e-04,0,PEAK,NEGATIVE,-1.530e-02
```

Example: Chapter 18.2.2.1, "Searching for a Pulse of Specified Width", on page 407

### Usage: Query only

### Firmware/Software: FW 03.400

<!-- 来源：RTM2_UserManual_en_10_files\part927.htm -->

### SEARch:RESult<n>?

Returns the result values of the specified search result. See also: SEARch:RESult:ALL?

<!-- 来源：RTM2_UserManual_en_10_files\part928.htm -->

### Suffix:

<n> *

Number of the search result

<!-- 来源：RTM2_UserManual_en_10_files\part929.htm -->

### Return values:

<Result> Comma-separated value list

Meaning of the values:

Result number, time value, y-position (not relevant), search type, slope or polarity, optional value: voltage for peak search, pulse width for width search.

### Example: SEARch:RESult3?

Returns the result values of the third search result.

```text
3,-4.1660e-04,0,PEAK,NEGATIVE,-1.530e-02
```

### Usage: Query only

### Firmware/Software: FW 03.400

<!-- 来源：RTM2_UserManual_en_10_files\part930.htm -->

### SEARch:RCOunt?

Returns the number of search results.

<!-- 来源：RTM2_UserManual_en_10_files\part931.htm -->

### Return values:

<ResultCount> *RST: 0

Example: Chapter 18.2.2.1, "Searching for a Pulse of Specified Width", on page 407

### Usage: Query only

### Firmware/Software: FW 03.400

### EXPort:SEARch:NAME <FileName>

```text
Defines the path and filename for search results that will be saved with EXPort: SEARch:SAVE. The file format is CSV, the filename is incremented automatically
```

You can change the storage location and the file name manually in the SEARCH > "Events" > "Save" menu. Remote control uses the recent settings.

<!-- 来源：RTM2_UserManual_en_10_files\part932.htm -->

### Parameters:

<FileName> String parameter

### Example: EXPort:SEARch:NAME "/USB_FRONT/SEARCH/RESULT"

On first save, the search results are saved to RESULT.CSV, on second save to RESULT01.CSV, the third to RESULT02.CSV...

<!-- 来源：RTM2_UserManual_en_10_files\part933.htm -->

### EXPort:SEARch:SAVE

### Usage: Setting only

<!-- 来源：RTM2_UserManual_en_10_files\part934.htm -->

## 18.13 Protocol Analysis

- General 547

- SPI 551

- SSPI 561

- I²C 565

- UART 576

- CAN 584

- LIN 601

- Audio Signals (Option R&S RTM-K5) 615

- MIL_STD-1553 (Option R&S RTM-K6) 631

- ARINC 429 (Option R&S RTM-K7) 653

<!-- 来源：RTM2_UserManual_en_10_files\part935.htm -->

### 18.13.1 General

Note: SPI/SSPI and UART protocols occupy two bus lines (bus 1 and 2 or bus 3 and 4). If one of these buses is configured, the number of buses (suffix <b>) is reduced. Bus 2 and/or bus 4 is not available.

BUS<b>:STATe 548

BUS<b>:TYPE 548

BUS<b>:FORMat 548

BUS<b>:DSIGnals 548

BUS<b>:LABel 549

BUS<b>:LABel:STATe 549

BUS<b>:DSIZe 549

BUS<b>:POSition 550

BUS<b>:RESult 550

BUS<b>:LIST? 550

BUS<b>:LIST:SAVE 551

### BUS<b>:STATe <State>

Switches the protocol display on or off.

<!-- 来源：RTM2_UserManual_en_10_files\part936.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part937.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### BUS<b>:TYPE <Type>

Defines the bus or interface type for analysis. For most types, a special option to the instrument is required.

<!-- 来源：RTM2_UserManual_en_10_files\part938.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI, UART and I2S protocols occupy two bus lines (bus 1 and 2 or bus 3 and 4).

<!-- 来源：RTM2_UserManual_en_10_files\part939.htm -->

### Parameters:

<Type> PARallel | CPARallel | I2C | SPI | SSPI | UART | CAN | LIN | I2S | MILStd | ARINc

*RST: PARallel

### BUS<b>:FORMat <Format>

Sets the decoding format for the display on the screen.

<!-- 来源：RTM2_UserManual_en_10_files\part940.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part941.htm -->

### Parameters:

<Format> ASCii | HEXadecimal | BINary | DECimal | OCTal

*RST: HEX

### BUS<b>:DSIGnals <BitsSignals>

Displays the individual bit lines above the decoded bus line.

<!-- 来源：RTM2_UserManual_en_10_files\part942.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part943.htm -->

### Parameters:

<BitsSignals> ON | OFF

*RST: ON

### BUS<b>:LABel <Label>

Defines an additional name label for the selected bus.

<!-- 来源：RTM2_UserManual_en_10_files\part944.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part945.htm -->

### Parameters:

<Label> String value

The maximum name length is 8 characters, and only ASCII characters provided on the on-screen keyboard can be used.

### BUS<b>:LABel:STATe <State>

Displays or hides the bus label. The bus label is shown on the the right side of the dis- play.

<!-- 来源：RTM2_UserManual_en_10_files\part946.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part947.htm -->

### Parameters:

<State> ON | OFF

*RST: ON

### BUS<b>:DSIZe <DisplaySize>

Sets the height of the decoded bus signal on the sreen.

<!-- 来源：RTM2_UserManual_en_10_files\part948.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part949.htm -->

### Parameters:

<DisplaySize> SMALl | MEDium | LARGe | DIV2 | DIV4

<!-- 来源：RTM2_UserManual_en_10_files\part950.htm -->

### DIV2 | DIV4

2 or 4 divisions

<!-- 来源：RTM2_UserManual_en_10_files\part951.htm -->

### SMALl | MEDium | LARGe

Size of indicated bus is smaller than 2 div.

*RST: MEDium

### BUS<b>:POSition <Position>

Sets the vertical position of the decoded bus signal in divisions on the sreen.

<!-- 来源：RTM2_UserManual_en_10_files\part952.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

| Parameters: |  |  |
| --- | --- | --- |
| <Position> | Range: | 4 to -4 |
|  | Increment: | 0.02 |
|  | *RST: | -3.5 |

Default unit: DIV

### BUS<b>:RESult <ShowResultTable> Displays or hides the table of decode results.

<!-- 来源：RTM2_UserManual_en_10_files\part953.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part954.htm -->

### Parameters:

<ShowResultTable> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part955.htm -->

### BUS<b>:LIST?

Returns the contents of the frame table in block data format.

<!-- 来源：RTM2_UserManual_en_10_files\part956.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part957.htm -->

### Return values:

<DataTable> Block data

### Usage: Query only

### BUS<b>:LIST:SAVE <FilePath>

Saves the decoded data (frame table) to the specified CSV file (comma-separated list).

<!-- 来源：RTM2_UserManual_en_10_files\part958.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part959.htm -->

### Setting parameters:

<FilePath> String containing the storage device, path, and file name

### Example: BUS:LIST:SAVE "/USB_FRONT/MYTABLE.CSV"

Saves the frame table data to the MYTABLE.CSV file on a USB flash device connected to the front panel.

### Usage: Setting only

<!-- 来源：RTM2_UserManual_en_10_files\part960.htm -->

### 18.13.2 SPI

The Serial Peripheral Interface SPI is used for communication with slow peripheral devices, in particular, for transmission of data streams. A 4-channel instrument is required for full support of the SPI protocol.

The SPI/SSPI protocol require two bus lines (bus 1 and 2 or bus 3 and 4), so the num- ber of buses (suffix <b>) is reduced. Bus 2 and/or bus 4 is not available.

- SPI - Configuration 551

- SPI - Trigger 555

- SPI - Decode Results 557

### 18.13.2.1 SPI - Configuration

BUS<b>:SPI:CS:SOURce 551

BUS<b>:SPI:CS:POLarity 552

BUS<b>:SPI:CLOCk:SOURce 552

BUS<b>:SPI:CLOCk:POLarity 552

BUS<b>:SPI:MOSI:SOURce 553

BUS<b>:SPI:DATA:SOURce 553

BUS<b>:SPI:MISO:SOURce 553

BUS<b>:SPI:MOSI:POLarity 553

BUS<b>:SPI:DATA:POLarity 553

BUS<b>:SPI:MISO:POLarity 554

BUS<b>:SPI:BORDer 554

BUS<b>:SPI:SSIZe 554

CHANnel<m>:THReshold:FINDlevel 555

### BUS<b>:SPI:CS:SOURce <Source>

Selects the input channel of the chip select line.

<!-- 来源：RTM2_UserManual_en_10_files\part961.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part962.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | D0..D15

*RST: CH1

### BUS<b>:SPI:CS:POLarity <Polarity>

Selects whether the chip select signal is high active (high = 1) or low active (low = 1).

<!-- 来源：RTM2_UserManual_en_10_files\part963.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part964.htm -->

### Parameters:

<Polarity> POSitive | NEGative

POSitive = high active NEGative = low active

*RST: POSitive

### BUS<b>:SPI:CLOCk:SOURce <Source>

Selects the input channel of the clock line.

<!-- 来源：RTM2_UserManual_en_10_files\part965.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part966.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | D0..D15

*RST: CH1

### BUS<b>:SPI:CLOCk:POLarity <Polarity>

Selects if data is stored with the rising or falling slope of the clock. The slope marks the begin of a new bit.

<!-- 来源：RTM2_UserManual_en_10_files\part967.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part968.htm -->

### Parameters:

<Polarity> POSitive | NEGative

POSitive: rising slope NEGative: falling slope

*RST: NEGative

### BUS<b>:SPI:MOSI:SOURce <Source>

### BUS<b>:SPI:DATA:SOURce <Source>

Selects the input channel of the MOSI line, or of the data line if only one data line is used.

<!-- 来源：RTM2_UserManual_en_10_files\part969.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI protocols occupy two bus lines (1 and 2 or 3 and 4).

<!-- 来源：RTM2_UserManual_en_10_files\part970.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | D0..D15

D0..D15: requires MSO option R&S RTM-B1

*RST: CH1

### BUS<b>:SPI:MISO:SOURce <MisoSource> Selects the input channel of the optional MISO line.

<!-- 来源：RTM2_UserManual_en_10_files\part971.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part972.htm -->

### Parameters:

<MisoSource> CH1 | CH2 | CH3 | CH4 | NONE | D0..D15

*RST: NONE

### BUS<b>:SPI:MOSI:POLarity <Polarity>

### BUS<b>:SPI:DATA:POLarity <Polarity>

Selects whether transmitted data is high active (high = 1) or low active (low = 1) on the data line.

<!-- 来源：RTM2_UserManual_en_10_files\part973.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part974.htm -->

### Parameters:

<Polarity> POSitive | NEGative

POSitive = high active NEGative = low active

*RST: POSitive

### BUS<b>:SPI:MISO:POLarity <MisoPolarity>

Selects whether transmitted data is high active (high = 1) or low active (low = 1) on the MISO line.

<!-- 来源：RTM2_UserManual_en_10_files\part975.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part976.htm -->

### Parameters:

<MisoPolarity> ACTLow | ACTHigh

*RST: ACTH

### BUS<b>:SPI:BORDer <BitOrder>

Defines if the data of the messages starts with MSB (most significant bit) or LSB (least significant bit).

<!-- 来源：RTM2_UserManual_en_10_files\part977.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part978.htm -->

### Parameters:

<BitOrder> MSBFirst | LSBFirst

*RST: MSBFirst

### BUS<b>:SPI:SSIZe <SymbolSize>

Sets the word length, the number of bits in a message.

<!-- 来源：RTM2_UserManual_en_10_files\part979.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

| Parameters: |  |  |
| --- | --- | --- |
| <SymbolSize> | Range: | 4 to 32 |
|  | Increment: | 1 |
|  | *RST: | 8 |

Default unit: Bit

<!-- 来源：RTM2_UserManual_en_10_files\part980.htm -->

### CHANnel<m>:THReshold:FINDlevel

Executes the analysis of all analog channels that are configured for the selected bus and sets the threshold for digitization of analog signals for each channel.

<!-- 来源：RTM2_UserManual_en_10_files\part981.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

### Usage: Event

### 18.13.2.2 SPI - Trigger

TRIGger:A:SOURce 555

TRIGger:A:SPI:MODE 555

TRIGger:A:SPI:PATTern 556

TRIGger:A:SPI:PLENgth 556

TRIGger:A:SPI:POFFset 557

### TRIGger:A:SOURce <Source>

Sets the trigger source for the selected A trigger type.

<!-- 来源：RTM2_UserManual_en_10_files\part982.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | EXTernanalog | LINE | SBUS1.. SBUS4 | D0. D15

<!-- 来源：RTM2_UserManual_en_10_files\part983.htm -->

### CH1 | CH2 | CH3 | CH4

One of the input channels is the trigger source. Available chan- nels depend on the instrument type.

<!-- 来源：RTM2_UserManual_en_10_files\part984.htm -->

### EXTernanalog

External trigger input on the rear panel

<!-- 来源：RTM2_UserManual_en_10_files\part985.htm -->

### LINE

AC line for the edge trigger

<!-- 来源：RTM2_UserManual_en_10_files\part986.htm -->

### SBUS1 SBUS4

Serial buses 1 to 4

The UART, SPI, SSPI and audio protocols require two bus lines (bus 1 and 2 or bus 3 and 4). Bus 2 and/or bus 4 is not available if one of these protocols is selected.

<!-- 来源：RTM2_UserManual_en_10_files\part987.htm -->

### D0. D15

If MSO option R&S RTM-B1 is installed, the digital channels D0 to D15 can be used as trigger sources for edge, width and pat- tern trigger.

### TRIGger:A:SPI:MODE <Mode>

Specifies the trigger mode for SPI/SSPI protocols.

<!-- 来源：RTM2_UserManual_en_10_files\part988.htm -->

### Parameters:

<Mode> BSTart | BEND | NTHBit | PATTern

<!-- 来源：RTM2_UserManual_en_10_files\part989.htm -->

### BSTart

Burst start, sets the trigger event to the start of the frame. The frame starts when the chip select signal CS changes to the active state.

<!-- 来源：RTM2_UserManual_en_10_files\part990.htm -->

### BEND

Burst end, sets the trigger event to the end of the message.

<!-- 来源：RTM2_UserManual_en_10_files\part991.htm -->

### NTHBit

```text
Sets the trigger event to the specified bit number. To define the bit number, use TRIGger:A:SPI:POFFset.
```

<!-- 来源：RTM2_UserManual_en_10_files\part992.htm -->

### PATTern

```text
Sets the trigger event to a serial pattern. To define the pattern, use TRIGger:A:SPI:PATTern.
For a complete configuration of the pattern mode, you also have to set TRIGger:A:SPI:PLENgth and TRIGger:A:SPI: POFFset.
```

*RST: BSTart

### TRIGger:A:SPI:PATTern <DataPattern>

Defines the bit pattern as trigger condition. The pattern length is adjusted to the num- ber of bits defined in the pattern.

<!-- 来源：RTM2_UserManual_en_10_files\part993.htm -->

### Parameters:

<DataPattern> String with max. 32 characters (4 byte + 8 bit). Characters 0, 1, and X are allowed.

### Example: TRIG:A:SPI:PATT "0011XXXX0110"

Sets a 12bit pattern.

### TRIGger:A:SPI:PLENgth <PatternLength>

```text
Returns the number of bits in the previously defined bit pattern ( TRIGger:A:SPI: PATTern ). The command can also be used to shorten a previously defined bit pattern.
```

<!-- 来源：RTM2_UserManual_en_10_files\part994.htm -->

### Parameters:

<PatternLength> Range: 1 to 32

Increment: 1

*RST: 4

### Example: TRIG:A:SPI:PATT "0011XXXX0110"

```text
TRIG:A:SPI:PLEN? 12
TRIG:A:SPI:PLEN 4 TRIG:A:SPI:PATT? "0011"
```

### TRIGger:A:SPI:POFFset <PatternBitOffset>

Sets the number of bits before the first bit of the pattern.

<!-- 来源：RTM2_UserManual_en_10_files\part995.htm -->

### Parameters:

<PatternBitOffset> Number of ignored bits

Range: 0 to 4095

Increment: 1

*RST: 0

### 18.13.2.3 SPI - Decode Results

BUS<b>:SPI:FCOunt? 557

BUS<b>:SPI:FRAME<n>:STATus? 557

BUS<b>:SPI:FRAME<n>:STARt? 558

BUS<b>:SPI:FRAME<n>:STOP? 558

BUS<b>:SPI:FRAME<n>:DATA:MOSI? 558

BUS<b>:SPI:FRAME<n>:DATA:MISO? 559

BUS<b>:SPI:FRAME<n>:WCOunt? 559

BUS<b>:SPI:FRAME<n>:WORD<o>:STARt? 560

BUS<b>:SPI:FRAME<n>:WORD<o>:STOP? 560

BUS<b>:SPI:FRAME<n>:WORD<o>:MOSI? 560

BUS<b>:SPI:FRAME<n>:WORD<o>:MISO? 561

<!-- 来源：RTM2_UserManual_en_10_files\part996.htm -->

### BUS<b>:SPI:FCOunt?

Returns the number of decoded frames.

<!-- 来源：RTM2_UserManual_en_10_files\part997.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part998.htm -->

### Return values:

<FrameCount> Total number of decoded frames.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part999.htm -->

### BUS<b>:SPI:FRAME<n>:STATus?

Returns the overall state of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1000.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1001.htm -->

### Return values:

<Status> OK | INCFirst | INCLast | INSufficient

<!-- 来源：RTM2_UserManual_en_10_files\part1002.htm -->

### INCFirst

First frame is incomplete

<!-- 来源：RTM2_UserManual_en_10_files\part1003.htm -->

### INCLast

Last frame is incomplete

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1004.htm -->

### BUS<b>:SPI:FRAME<n>:STARt?

Returns the start time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1005.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1006.htm -->

### Return values:

<StartTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1007.htm -->

### BUS<b>:SPI:FRAME<n>:STOP?

Returns the end time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1008.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1009.htm -->

### Return values:

<StopTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1010.htm -->

### BUS<b>:SPI:FRAME<n>:DATA:MOSI?

Returns the data words of the specified frame of the MOSI line.

<!-- 来源：RTM2_UserManual_en_10_files\part1011.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1012.htm -->

### Return values:

<DataMosi> List of decimal values of data bytes

### Example: BUS:SPI:FRAM3:DATA:MOSI?

```text
-> 94,177,171,60,242,219,100,0
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1013.htm -->

### BUS<b>:SPI:FRAME<n>:DATA:MISO?

Returns the data words of the specified frame of the MISO line.

<!-- 来源：RTM2_UserManual_en_10_files\part1014.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1015.htm -->

### Return values:

<DataMiso> List of decimal values of data bytes

### Example: BUS:SPI:FRAM3:DATA:MISO?

```text
-> 94,177,171,60,242,219,100,0
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1016.htm -->

### BUS<b>:SPI:FRAME<n>:WCOunt?

Returns the number of words in the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1017.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1018.htm -->

### Return values:

<WordCount> Number of words

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1019.htm -->

### BUS<b>:SPI:FRAME<n>:WORD<o>:STARt?

Returns the start time of the specified data word.

<!-- 来源：RTM2_UserManual_en_10_files\part1020.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<o> *

Selects the word number.

<!-- 来源：RTM2_UserManual_en_10_files\part1021.htm -->

### Return values:

<StartTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1022.htm -->

### BUS<b>:SPI:FRAME<n>:WORD<o>:STOP?

Returns the end time of the specified data word.

<!-- 来源：RTM2_UserManual_en_10_files\part1023.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<o> *

Selects the word number.

<!-- 来源：RTM2_UserManual_en_10_files\part1024.htm -->

### Return values:

<StopTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1025.htm -->

### BUS<b>:SPI:FRAME<n>:WORD<o>:MOSI?

Returns the data value of the specified word on the MOSI line. Use this command if only one line is defined.

<!-- 来源：RTM2_UserManual_en_10_files\part1026.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame (1...n)

<o> *

Selects the word number (1...m)

<!-- 来源：RTM2_UserManual_en_10_files\part1027.htm -->

### Return values:

<Data> Decimal value of the data word

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1028.htm -->

### BUS<b>:SPI:FRAME<n>:WORD<o>:MISO?

Returns the data value of the specified word on the optional MISO line.

<!-- 来源：RTM2_UserManual_en_10_files\part1029.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame (1...n)

<o> *

Selects the word number (1...m)

<!-- 来源：RTM2_UserManual_en_10_files\part1030.htm -->

### Return values:

<Data> Decimal value of the data word

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1031.htm -->

### 18.13.3 SSPI

BUS<b>:SSPI:CLOCk:SOURce 562

BUS<b>:SSPI:CLOCk:POLarity 562

BUS<b>:SSPI:MOSI:SOURce 562

BUS<b>:SSPI:DATA:SOURce 562

BUS<b>:SSPI:MISO:SOURce 562

BUS<b>:SSPI:MOSI:POLarity 563

BUS<b>:SSPI:DATA:POLarity 563

BUS<b>:SSPI:MISO:POLarity 563

BUS<b>:SSPI:BITime 563

BUS<b>:SSPI:BORDer 564

BUS<b>:SSPI:SSIZe 564

CHANnel<m>:THReshold:FINDlevel 564

### BUS<b>:SSPI:CLOCk:SOURce <Source>

Selects the input channel of the clock line.

<!-- 来源：RTM2_UserManual_en_10_files\part1032.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1033.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | D0..D15

CH3 and CH4 are only available with 4-channel R&S RTM oscil- loscopes.

*RST: CH1

### BUS<b>:SSPI:CLOCk:POLarity <Polarity>

Selects if data is stored with the rising or falling slope of the clock. The slope marks the begin of a new bit.

<!-- 来源：RTM2_UserManual_en_10_files\part1034.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1035.htm -->

### Parameters:

<Polarity> POSitive | NEGative

POSitive: rising slope NEGative: falling slope

*RST: POSitive

### BUS<b>:SSPI:MOSI:SOURce <MosiSource>

### BUS<b>:SSPI:DATA:SOURce <Source>

Selects the input channel of the data line.

<!-- 来源：RTM2_UserManual_en_10_files\part1036.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1037.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | D0..D15

CH3 and CH4 are only available with 4-channel R&S RTM oscil- loscopes.

*RST: CH1

### BUS<b>:SSPI:MISO:SOURce <MisoSource> Selects the input channel of the optional MISO line.

<!-- 来源：RTM2_UserManual_en_10_files\part1038.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1039.htm -->

### Parameters:

<MisoSource> CH1 | CH2 | CH3 | CH4 | NONE | D0..D15

*RST: NONE

### BUS<b>:SSPI:MOSI:POLarity <MosiPolarity>

### BUS<b>:SSPI:DATA:POLarity <Polarity>

Selects whether transmitted data is high active (high = 1) or low active (low = 1) on the data line.

<!-- 来源：RTM2_UserManual_en_10_files\part1040.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1041.htm -->

### Parameters:

<Polarity> POSitive | NEGative

POSitive = high active NEGative = low active

*RST: POSitive

### BUS<b>:SSPI:MISO:POLarity <MisoPolarity>

Selects whether transmitted data is high active (high = 1) or low active (low = 1) on the MISO line.

<!-- 来源：RTM2_UserManual_en_10_files\part1042.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1043.htm -->

### Parameters:

<MisoPolarity> ACTLow | ACTHigh

*RST: ACTH

### BUS<b>:SSPI:BITime <BurstIdleTime>

Within the idle time the data and clock lines are low. A new frame begins when the idle time has expired and the clock line has been inactive during that time. If the time inter- val between the data words is shorter than the idle time, the words are part of the same frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1044.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

| Parameters: |  |  |
| --- | --- | --- |
| <BurstIdleTime> | Range: | 16e-9 to 838.832e-6 |
|  | Increment: | 16e-9 |
|  | *RST: | 100e-6 |

Default unit: s

### BUS<b>:SSPI:BORDer <BitOrder>

Defines if the data of the messages starts with MSB (most significant bit) or LSB (least significant bit).

<!-- 来源：RTM2_UserManual_en_10_files\part1045.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1046.htm -->

### Parameters:

<BitOrder> MSBFirst | LSBFirst

*RST: MSBFirst

### BUS<b>:SSPI:SSIZe <SymbolSize>

Sets the word length, the number of bits in a message.

<!-- 来源：RTM2_UserManual_en_10_files\part1047.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

| Parameters: |  |  |
| --- | --- | --- |
| <SymbolSize> | Range: | 4 to 32 |
|  | Increment: | 1 |
|  | *RST: | 8 |

Default unit: Bit

<!-- 来源：RTM2_UserManual_en_10_files\part1048.htm -->

### CHANnel<m>:THReshold:FINDlevel

Executes the analysis of all analog channels that are configured for the selected bus and sets the threshold for digitization of analog signals for each channel.

<!-- 来源：RTM2_UserManual_en_10_files\part1049.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1050.htm -->

### 18.13.4 I²C

The Inter-Integrated Circuit is a simple, lowbandwidth, low-speed protocol used for communication between on-board devices, for example, in LCD and LED drivers, RAM, EEPROM, and others.

Note: SPI/SSPI and UART protocols occupy two bus lines (bus 1 and 2 or bus 3 and 4). If one of these buses is configured, the number of buses (suffix <b>) is reduced. Bus 2 and/or bus 4 is not available.

- I²C - Configuration 565

- I²C - Trigger 566

- I²C - Decode Results 569

### 18.13.4.1 I²C - Configuration

BUS<b>:I2C:CLOCk:SOURce 565

BUS<b>:I2C:DATA:SOURce 565

CHANnel<m>:THReshold:FINDlevel 566

### BUS<b>:I2C:CLOCk:SOURce <Source>

Sets the input channel to which the clock line is connected.

<!-- 来源：RTM2_UserManual_en_10_files\part1051.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1052.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | D0..D15

CH3 and CH4 are only available with 4-channel R&S RTM oscil- loscopes.

*RST: CH1

### BUS<b>:I2C:DATA:SOURce <Source>

Sets the input channel to which the data line is connected.

<!-- 来源：RTM2_UserManual_en_10_files\part1053.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1054.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | D0..D15

CH3 and CH4 are only available with 4-channel R&S RTM oscil- loscopes.

*RST: CH1

<!-- 来源：RTM2_UserManual_en_10_files\part1055.htm -->

### CHANnel<m>:THReshold:FINDlevel

Executes the analysis of all analog channels that are configured for the selected bus and sets the threshold for digitization of analog signals for each channel.

<!-- 来源：RTM2_UserManual_en_10_files\part1056.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

### Usage: Event

### 18.13.4.2 I²C - Trigger

TRIGger:A:SOURce 566

TRIGger:A:I2C:MODE 567

TRIGger:A:I2C:ACCess 567

TRIGger:A:I2C:AMODe 567

TRIGger:A:I2C:ADDRess 568

TRIGger:A:I2C:PATTern 568

TRIGger:A:I2C:PLENgth 568

TRIGger:A:I2C:POFFset 569

### TRIGger:A:SOURce <Source>

Sets the trigger source for the selected A trigger type.

<!-- 来源：RTM2_UserManual_en_10_files\part1057.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | EXTernanalog | LINE | SBUS1.. SBUS4 | D0. D15

<!-- 来源：RTM2_UserManual_en_10_files\part1058.htm -->

### CH1 | CH2 | CH3 | CH4

One of the input channels is the trigger source. Available chan- nels depend on the instrument type.

<!-- 来源：RTM2_UserManual_en_10_files\part1059.htm -->

### EXTernanalog

External trigger input on the rear panel

<!-- 来源：RTM2_UserManual_en_10_files\part1060.htm -->

### LINE

AC line for the edge trigger

<!-- 来源：RTM2_UserManual_en_10_files\part1061.htm -->

### SBUS1 SBUS4

Serial buses 1 to 4

The UART, SPI, SSPI and audio protocols require two bus lines (bus 1 and 2 or bus 3 and 4). Bus 2 and/or bus 4 is not available if one of these protocols is selected.

<!-- 来源：RTM2_UserManual_en_10_files\part1062.htm -->

### D0. D15

If MSO option R&S RTM-B1 is installed, the digital channels D0 to D15 can be used as trigger sources for edge, width and pat- tern trigger.

### TRIGger:A:I2C:MODE <Mode>

Specifies the trigger mode for I²C.

<!-- 来源：RTM2_UserManual_en_10_files\part1063.htm -->

### Parameters:

<Mode> STARt | RESTart | STOP | MACKnowledge | PATTern

<!-- 来源：RTM2_UserManual_en_10_files\part1064.htm -->

### STARt

Start of the message. The start condition is a falling slope on SDA while SCL is high.

<!-- 来源：RTM2_UserManual_en_10_files\part1065.htm -->

### RESTart

Restarted message. The restart is a repeated start condition.

<!-- 来源：RTM2_UserManual_en_10_files\part1066.htm -->

### STOP

End of the message. The stop condition is a rising slope on SDA while SCL is high.

<!-- 来源：RTM2_UserManual_en_10_files\part1067.htm -->

### MACKnowledge

Missing acknowledge. If the transfer failed, at the moment of the acknowledge bit the SCL and the SDA lines are both on high level.

<!-- 来源：RTM2_UserManual_en_10_files\part1068.htm -->

### PATTern

Triggers on a set of trigger conditions: read or write access of the master, to an address, or/and to a bit pattern in the mes- sage.

For a complete configuration of the pattern mode, you have to set:

```text
TRIGger:A:I2C:ACCess (read/write access), and TRIGger:A:I2C:AMODe and TRIGger:A:I2C:ADDRess (address), and/or
TRIGger:A:I2C:POFFset and TRIGger:A:I2C:PLENgth
and TRIGger:A:I2C:PATTern (pattern)
```

*RST: STARt

### TRIGger:A:I2C:ACCess <Access>

Toggles the trigger condition between Read and Write access of the master.

<!-- 来源：RTM2_UserManual_en_10_files\part1069.htm -->

### Parameters:

<Access> READ | WRITe

*RST: READ

### TRIGger:A:I2C:AMODe <AdrMode> Sets the lenght of the slave address.

<!-- 来源：RTM2_UserManual_en_10_files\part1070.htm -->

### Parameters:

<AdrMode> NORMal | EXTended

NORMal: 7 bit address EXTended: 10 bit address

*RST: NORMal

### TRIGger:A:I2C:ADDRess <AddressString>

Sets the address of the slave device. The address can have 7 bits or 10 bits.

<!-- 来源：RTM2_UserManual_en_10_files\part1071.htm -->

### Parameters:

<AddressString> String with max. 7 or 10 characters, depending on the address length. Characters 0, 1, and X are allowed, but X cannot be assigned to a specified bit. If at least one X occurs in the address, the complete address is set to X.

### Example: TRIG:A:I2C:AMOD NORM TRIG:A:I2C:ADDR "1011" TRIG:A:I2C:ADDR?

Return value (7bit address): "0001011"

### Example: TRIG:A:I2C:AMOD EXT TRIG:A:I2C:ADDR "10X1" TRIG:A:I2C:ADDR?

Return value (10bit address): "XXXXXXXXXX"

### TRIGger:A:I2C:PATTern <DataPattern>

```text
Defines the bit pattern as trigger condition. Make sure that the correct pattern length has been defined before with TRIGger:A:I2C:PLENgth.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1072.htm -->

### Parameters:

<DataPattern> String with max. 24 characters (3 byte + 8 bit). Characters 0, 1, and X are allowed. X can be assigned to a specified bit. If you define a pattern shorter than the pattern length, the missing LSB are filled with X. If you define a pattern longer than the pattern length, the pattern string is not valid

### Example: TRIG:A:I2C:PLEN 2

```text
TRIG:A:I2C:PATT "10X10000XXXX1111" TRIG:A:I2C:PATT?
```

Return value (2 bytes): "10X10000XXXX1111"

### Example: TRIG:A:I2C:PLEN 1

```text
TRIG:A:I2C:PATT "110" TRIG:A:I2C:PATT?
```

Return value (1 byte): "110XXXXX"

### TRIGger:A:I2C:PLENgth <PatternLength>

```text
Defines how many bytes are considered in the trigger condition. To set the pattern for these bytes, use TRIGger:A:I2C:PATTern.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1073.htm -->

### Parameters:

<PatternLength> Number of bytes

Range: 1 to 3

Increment: 1

*RST: 1

### TRIGger:A:I2C:POFFset <PatternByteOffset>

Sets the number of bytes before the first byte of interest, relating to the end of the address bytes.

<!-- 来源：RTM2_UserManual_en_10_files\part1074.htm -->

### Parameters:

<PatternByteOffset> Number of ignored bytes

Range: 0 to 4095

Increment: 1

*RST: 0

### 18.13.4.3 I²C - Decode Results

BUS<b>:I2C:FCOunt? 569

BUS<b>:I2C:FRAMe<n>:DATA? 569

BUS<b>:I2C:FRAMe<n>:STATus? 570

BUS<b>:I2C:FRAMe<n>:STARt? 570

BUS<b>:I2C:FRAMe<n>:STOP? 571

BUS<b>:I2C:FRAMe<n>:AACCess? 571

BUS<b>:I2C:FRAMe<n>:ACCess? 571

BUS<b>:I2C:FRAMe<n>:ACOMplete? 572

BUS<b>:I2C:FRAMe<n>:ADBStart? 572

BUS<b>:I2C:FRAMe<n>:ADDRess? 572

BUS<b>:I2C:FRAMe<n>:ADEVice? 573

BUS<b>:I2C:FRAMe<n>:AMODe? 573

BUS<b>:I2C:FRAMe<n>:ASTart? 573

BUS<b>:I2C:FRAMe<n>:BCOunt? 574

BUS<b>:I2C:FRAMe<n>:BYTE<o>:ACCess? 574

BUS<b>:I2C:FRAMe<n>:BYTE<o>:ACKStart? 574

BUS<b>:I2C:FRAMe<n>:BYTE<o>:COMPlete? 575

BUS<b>:I2C:FRAMe<n>:BYTE<o>:STARt? 575

BUS<b>:I2C:FRAMe<n>:BYTE<o>:VALue? 575

<!-- 来源：RTM2_UserManual_en_10_files\part1075.htm -->

### BUS<b>:I2C:FCOunt?

Returns the number of received frames.

<!-- 来源：RTM2_UserManual_en_10_files\part1076.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1077.htm -->

### Return values:

<FrameCount> Total number of decoded frames.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1078.htm -->

### BUS<b>:I2C:FRAMe<n>:DATA?

Returns the data words of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1079.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1080.htm -->

### Return values:

<DataWordsInFrame>Comma-separated list of decimal values of the data bytes.

### Example: BUS:I2C:FRAM2:DATA?

returns four data bytes:

```text
-> 69,158,174,161
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1081.htm -->

### BUS<b>:I2C:FRAMe<n>:STATus?

Returns the overall state of the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1082.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1083.htm -->

### Return values:

<State> INComplete | OK | UNEXpstop | INSufficient | ADDifferent

<!-- 来源：RTM2_UserManual_en_10_files\part1084.htm -->

### INComplete

The frame is not completely contained in the acquisition.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1085.htm -->

### BUS<b>:I2C:FRAMe<n>:STARt?

Returns the start time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1086.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1087.htm -->

### Return values:

<StartTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1088.htm -->

### BUS<b>:I2C:FRAMe<n>:STOP?

Returns the end time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1089.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1090.htm -->

### Return values:

<EndTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1091.htm -->

### BUS<b>:I2C:FRAMe<n>:AACCess?

Returns the address acknowledge bit value for the indicated frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1092.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1093.htm -->

### Return values:

<Acknowledge> INComplete | ACK | NACK | EITHer

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1094.htm -->

### BUS<b>:I2C:FRAMe<n>:ACCess?

Returns the transfer direction - read or write access from master to slave.

<!-- 来源：RTM2_UserManual_en_10_files\part1095.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1096.htm -->

### Return values:

<Access> INComplete | READ | WRITE | EITHer | UNDF

<!-- 来源：RTM2_UserManual_en_10_files\part1097.htm -->

### INComplete

The frame is not completely contained in the acquisition.

<!-- 来源：RTM2_UserManual_en_10_files\part1098.htm -->

### UNDF

Access is not defined.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1099.htm -->

### BUS<b>:I2C:FRAMe<n>:ACOMplete?

Returns the state of the address.

<!-- 来源：RTM2_UserManual_en_10_files\part1100.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1101.htm -->

### Return values:

<AddressComplete> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part1102.htm -->

### ON

Address was received completely.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1103.htm -->

### BUS<b>:I2C:FRAMe<n>:ADBStart?

Returns the start time of the address acknowledge bit.

<!-- 来源：RTM2_UserManual_en_10_files\part1104.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1105.htm -->

### Return values:

<AckStartTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1106.htm -->

### BUS<b>:I2C:FRAMe<n>:ADDRess?

Returns the decimal address value of the indicated frame including the R/W bit.

<!-- 来源：RTM2_UserManual_en_10_files\part1107.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1108.htm -->

### Return values:

<AddressValue> Decimal value

Range: 0 to 2047

Increment: 1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1109.htm -->

### BUS<b>:I2C:FRAMe<n>:ADEVice?

Returns the decimal address value of the indicated frame without R/W bit.

<!-- 来源：RTM2_UserManual_en_10_files\part1110.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1111.htm -->

### Return values:

<SlaveAddress> Decimal value

Range: 0 to 1023

Increment: 1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1112.htm -->

### BUS<b>:I2C:FRAMe<n>:AMODe?

Returns the address length.

<!-- 来源：RTM2_UserManual_en_10_files\part1113.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1114.htm -->

### Return values:

<AddressMode> BIT7 | BIT10

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1115.htm -->

### BUS<b>:I2C:FRAMe<n>:ASTart?

Returns the start time of the address for the indicated frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1116.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1117.htm -->

### Return values:

<StartTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1118.htm -->

### BUS<b>:I2C:FRAMe<n>:BCOunt?

Returns the number of data bytes in the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1119.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1120.htm -->

### Return values:

<ByteCount im Frame>

Number of words (bytes)

### Example: BUS:I2C:FRAM2:BCO?

```text
-> 4
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1121.htm -->

### BUS<b>:I2C:FRAMe<n>:BYTE<o>:ACCess?

Returns the acknowledge bit value of the specified data byte.

<!-- 来源：RTM2_UserManual_en_10_files\part1122.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<o> *

Selects the byte number.

<!-- 来源：RTM2_UserManual_en_10_files\part1123.htm -->

### Return values:

<Acknowledge> INComplete | ACK | NACK | EITHer

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1124.htm -->

### BUS<b>:I2C:FRAMe<n>:BYTE<o>:ACKStart?

Returns the start time of the acknowledge bit of the specified byte.

<!-- 来源：RTM2_UserManual_en_10_files\part1125.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<o> *

Selects the byte number.

<!-- 来源：RTM2_UserManual_en_10_files\part1126.htm -->

### Return values:

<AckStartTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1127.htm -->

### BUS<b>:I2C:FRAMe<n>:BYTE<o>:COMPlete?

Returns the state of the byte.

<!-- 来源：RTM2_UserManual_en_10_files\part1128.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<o> *

Selects the byte number.

<!-- 来源：RTM2_UserManual_en_10_files\part1129.htm -->

### Return values:

<ByteComplete> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part1130.htm -->

### ON

Data byte was received completely.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1131.htm -->

### BUS<b>:I2C:FRAMe<n>:BYTE<o>:STARt?

Returns the start time of the specified data byte.

<!-- 来源：RTM2_UserManual_en_10_files\part1132.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<o> *

Selects the byte number.

<!-- 来源：RTM2_UserManual_en_10_files\part1133.htm -->

### Return values:

<StartTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1134.htm -->

### BUS<b>:I2C:FRAMe<n>:BYTE<o>:VALue?

Returns the decimal value of the specified byte.

<!-- 来源：RTM2_UserManual_en_10_files\part1135.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame.

<o> *

Selects the byte number.

<!-- 来源：RTM2_UserManual_en_10_files\part1136.htm -->

### Return values:

<ByteValue> Decimal value

Range: 0 to 255

Increment: 1

### Example: BUS:I2C:FRAM2:BYTE2:VAL?

```text
-> 158
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1137.htm -->

### 18.13.5 UART

The Universal Asynchronous Receiver/Transmitter (UART) converts a word of data into serial data, and vice versa.

The UART protocol requires two bus lines (bus 1 and 2 or bus 3 and 4), so the number of buses (suffix <b>) is reduced. Bus 2 and/or bus 4 is not available.

- UART - Configuration 576

- UART - Trigger 580

- UART - Decode Results 582

### 18.13.5.1 UART - Configuration

BUS<b>:UART:RX:SOURce 576

BUS<b>:UART:DATA:SOURce 576

BUS<b>:UART:TX:SOURce 577

BUS<b>:UART:POLarity 577

BUS<b>:UART:DATA:POLarity 577

BUS<b>:UART:SSIZe 578

BUS<b>:UART:PARity 578

BUS<b>:UART:SBIT 578

BUS<b>:UART:BAUDrate 579

BUS<b>:UART:BITime 579

CHANnel<m>:THReshold:FINDlevel 579

### BUS<b>:UART:RX:SOURce <RxSource>

### BUS<b>:UART:DATA:SOURce <Source>

Selects the input channel of the data line.

<!-- 来源：RTM2_UserManual_en_10_files\part1138.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1139.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | D0..D15

CH3 and CH4 are only available with 4-channel R&S RTM oscil- loscopes.

*RST: CH1

### BUS<b>:UART:TX:SOURce <TxSource>

Selects the input channel of the optional Tx line.

<!-- 来源：RTM2_UserManual_en_10_files\part1140.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1141.htm -->

### Parameters:

<TxSource> CH1 | CH2 | CH3 | CH4 | NONE | D0..D15

<!-- 来源：RTM2_UserManual_en_10_files\part1142.htm -->

### NONE

Disables the optional Tx line.

*RST: NONE

### BUS<b>:UART:POLarity <IdleState>

Defines the logic levels of the bus. The idle state corresponds to a logic 1, and the start bit to a logic 0.

Alternative command for BUS<b>:UART:DATA:POLarity

<!-- 来源：RTM2_UserManual_en_10_files\part1143.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1144.htm -->

### Parameters:

<IdleState> IDLLow | IDLHigh

IDLLow: idle low, low = 1 IDLHigh: idle high, high = 1

*RST: IDLH

### BUS<b>:UART:DATA:POLarity <Polarity>

```text
Defines if the transmitted data on the bus is high (high = 1) or low (low = 1) active. Alternative command for BUS<b>:UART:POLarity.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1145.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1146.htm -->

### Parameters:

<Polarity> POSitive | NEGative

POSitive = high active NEGative = low active

*RST: POS

### BUS<b>:UART:SSIZe <SymbolSize> Sets the number of data bits in a message.

<!-- 来源：RTM2_UserManual_en_10_files\part1147.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

| Parameters: |  |  |
| --- | --- | --- |
| <SymbolSize> | Range: | 5 to 9 |
|  | Increment: | 1 |
|  | *RST: | 8 |

Default unit: Bit

### BUS<b>:UART:PARity <Parity>

Defines the optional parity bit that is used for error detection.

<!-- 来源：RTM2_UserManual_en_10_files\part1148.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1149.htm -->

### Parameters:

<Parity> ODD | EVEN | NONE See: "Parity" on page 222

*RST: NONE

### BUS<b>:UART:SBIT <StopBitNumber> Sets the stop bits.

<!-- 来源：RTM2_UserManual_en_10_files\part1150.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1151.htm -->

### Parameters:

<StopBitNumber> B1 | B1_5 | B2

1; 1.5 or 2 stop bits are possible.

*RST: B1

### BUS<b>:UART:BAUDrate <Baudrate>

Sets the number of transmitted bits per second.

<!-- 来源：RTM2_UserManual_en_10_files\part1152.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

| Parameters: |  |  |
| --- | --- | --- |
| <Baudrate> | Range: | 100 to 78.1E6 |
|  | Increment: | 100 |
|  | *RST: | 115200 |

Default unit: Bit

### BUS<b>:UART:BITime <BurstIdleTime>

Sets the minimal time between two data frames (packets), that is, between the last stop bit and the start bit of the next frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1153.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1154.htm -->

### Parameters:

<BurstIdleTime> Range: Range depends on the bus configuration, mainly on

bit rate and symbol size.

Default unit: s

<!-- 来源：RTM2_UserManual_en_10_files\part1155.htm -->

### CHANnel<m>:THReshold:FINDlevel

Executes the analysis of all analog channels that are configured for the selected bus and sets the threshold for digitization of analog signals for each channel.

<!-- 来源：RTM2_UserManual_en_10_files\part1156.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

### Usage: Event

### 18.13.5.2 UART - Trigger

TRIGger:A:SOURce 580

TRIGger:A:UART:MODE 580

TRIGger:A:UART:PATTern 581

TRIGger:A:UART:PLENgth 581

TRIGger:A:UART:POFFset 582

### TRIGger:A:SOURce <Source>

Sets the trigger source for the selected A trigger type.

<!-- 来源：RTM2_UserManual_en_10_files\part1157.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | EXTernanalog | LINE | SBUS1.. SBUS4 | D0. D15

<!-- 来源：RTM2_UserManual_en_10_files\part1158.htm -->

### CH1 | CH2 | CH3 | CH4

One of the input channels is the trigger source. Available chan- nels depend on the instrument type.

<!-- 来源：RTM2_UserManual_en_10_files\part1159.htm -->

### EXTernanalog

External trigger input on the rear panel

<!-- 来源：RTM2_UserManual_en_10_files\part1160.htm -->

### LINE

AC line for the edge trigger

<!-- 来源：RTM2_UserManual_en_10_files\part1161.htm -->

### SBUS1 SBUS4

Serial buses 1 to 4

The UART, SPI, SSPI and audio protocols require two bus lines (bus 1 and 2 or bus 3 and 4). Bus 2 and/or bus 4 is not available if one of these protocols is selected.

<!-- 来源：RTM2_UserManual_en_10_files\part1162.htm -->

### D0. D15

If MSO option R&S RTM-B1 is installed, the digital channels D0 to D15 can be used as trigger sources for edge, width and pat- tern trigger.

### TRIGger:A:UART:MODE <Mode>

Specifies the trigger mode for UART/RS-232 interfaces.

<!-- 来源：RTM2_UserManual_en_10_files\part1163.htm -->

### Parameters:

<Mode> BSTart | SBIT | NTHSymbol | SYMBol | PATTern | PRERror | FERRor | BREak

<!-- 来源：RTM2_UserManual_en_10_files\part1164.htm -->

### BSTart

Burst start. Sets the trigger to the begin of a data frame. The frame start is the first start bit after the idle time.

<!-- 来源：RTM2_UserManual_en_10_files\part1165.htm -->

### SBIT

Start bit. The start bit is the first low bit after a stop bit.

<!-- 来源：RTM2_UserManual_en_10_files\part1166.htm -->

### NTHSymbol

Sets the trigger to the n-th symbol of a burst.

<!-- 来源：RTM2_UserManual_en_10_files\part1167.htm -->

### SYMBol

Triggers if a pattern occurs in a symbol at any position in a burst.

<!-- 来源：RTM2_UserManual_en_10_files\part1168.htm -->

### PATTern

```text
Triggers on a serial pattern at a defined position in the burst. To define the pattern, use TRIGger:A:UART:PLENgth and TRIGger:A:UART:PATTern.
```

To define the position, use TRIGger:A:UART:POFFset

on page 582.

<!-- 来源：RTM2_UserManual_en_10_files\part1169.htm -->

### PRERror

Parity Error: Triggers if a bit error occured in transmission.

<!-- 来源：RTM2_UserManual_en_10_files\part1170.htm -->

### FERRor

Triggers on frame error.

<!-- 来源：RTM2_UserManual_en_10_files\part1171.htm -->

### BREak

Triggers if a start bit is not followed by a stop bit within a defined time. During the break the stop bits are at low state.

*RST: SBIT

### TRIGger:A:UART:PATTern <DataPattern> Defines the bit pattern as trigger condition.

<!-- 来源：RTM2_UserManual_en_10_files\part1172.htm -->

### Parameters:

<DataPattern> Binary pattern with max. 32 bit. Characters 0, 1, and X are allowed.

*RST: 1 = "00000001"

### TRIGger:A:UART:PLENgth <PatternLength> Defines how many symbols build up the serial pattern.

<!-- 来源：RTM2_UserManual_en_10_files\part1173.htm -->

### Parameters:

<PatternLength> Number of symbols

Range: 1 to 3

Increment: 1

*RST: 1

### TRIGger:A:UART:POFFset <PatternByteOffset>

Sets the number of symbols before the first symbol of the pattern.

<!-- 来源：RTM2_UserManual_en_10_files\part1174.htm -->

### Parameters:

<PatternByteOffset> Number of ignored symbols

Range: 0 to 4095

Increment: 1

*RST: 0

### 18.13.5.3 UART - Decode Results

BUS<b>:UART:RX:FCOunt? 582

BUS<b>:UART:TX:FCOunt? 582

BUS<b>:UART:RX:FRAMe<n>:WCOunt? 582

BUS<b>:UART:TX:FRAMe<n>:WCOunt? 582

BUS<b>:UART:RX:FRAMe<n>:WORD<o>:STATe? 583

BUS<b>:UART:TX:FRAMe<n>:WORD<o>:STATe? 583

BUS<b>:UART:RX:FRAMe<n>:WORD<o>:STARt? 583

BUS<b>:UART:TX:FRAMe<n>:WORD<o>:STARt? 583

BUS<b>:UART:RX:FRAMe<n>:WORD<o>:STOP? 584

BUS<b>:UART:TX:FRAMe<n>:WORD<o>:STOP? 584

BUS<b>:UART:RX:FRAMe<n>:WORD<o>:VALue? 584

BUS<b>:UART:TX:FRAMe<n>:WORD<o>:VALue? 584

<!-- 来源：RTM2_UserManual_en_10_files\part1175.htm -->

### BUS<b>:UART:RX:FCOunt? BUS<b>:UART:TX:FCOunt?

Returns the number of decoded frames on the RX and TX lines, respectivley.

<!-- 来源：RTM2_UserManual_en_10_files\part1176.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1177.htm -->

### Return values:

<FrameCount> Total number of decoded frames.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1178.htm -->

### BUS<b>:UART:RX:FRAMe<n>:WCOunt? BUS<b>:UART:TX:FRAMe<n>:WCOunt?

Returns the number of symbols in the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1179.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<o> *

<!-- 来源：RTM2_UserManual_en_10_files\part1180.htm -->

### Return values:

<WordCount> Number of words (symbols, characters)

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1181.htm -->

### BUS<b>:UART:RX:FRAMe<n>:WORD<o>:STATe? BUS<b>:UART:TX:FRAMe<n>:WORD<o>:STATe?

Returns the status of the specified symbol (word).

<!-- 来源：RTM2_UserManual_en_10_files\part1182.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<o> *

Selects the word number.

<!-- 来源：RTM2_UserManual_en_10_files\part1183.htm -->

### Return values:

<Status> OK | FRSTart | FRENd | FRMError | STERror | SPERror | PRERror | INSufficient | BREak

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1184.htm -->

### BUS<b>:UART:RX:FRAMe<n>:WORD<o>:STARt? BUS<b>:UART:TX:FRAMe<n>:WORD<o>:STARt?

Returns the start time of the specified symbol (word).

<!-- 来源：RTM2_UserManual_en_10_files\part1185.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<o> *

Selects the word number.

<!-- 来源：RTM2_UserManual_en_10_files\part1186.htm -->

### Return values:

<StartTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1187.htm -->

### BUS<b>:UART:RX:FRAMe<n>:WORD<o>:STOP? BUS<b>:UART:TX:FRAMe<n>:WORD<o>:STOP?

Returns the end time of the specified symbol (word).

<!-- 来源：RTM2_UserManual_en_10_files\part1188.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<o> *

Selects the word number.

<!-- 来源：RTM2_UserManual_en_10_files\part1189.htm -->

### Return values:

<StopTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1190.htm -->

### BUS<b>:UART:RX:FRAMe<n>:WORD<o>:VALue? BUS<b>:UART:TX:FRAMe<n>:WORD<o>:VALue?

Return the value of the specified symbol (word) on the Rx line and Tx line, respec- tively.

<!-- 来源：RTM2_UserManual_en_10_files\part1191.htm -->

### Suffix:

<b> 1..4

Selects the bus.

Note: SPI/SSPI and UART protocols occupy two bus lines.

<n> *

Selects the frame.

<o> *

Selects the word number.

<!-- 来源：RTM2_UserManual_en_10_files\part1192.htm -->

### Return values:

<Value> Decimal value

Range: 0 to 511

Increment: 1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1193.htm -->

### 18.13.6 CAN

CAN is the Controller Area Network, a bus system used within automotive network architecture.

Note: SPI/SSPI and UART protocols occupy two bus lines (bus 1 and 2 or bus 3 and 4). If one of these buses is configured, the number of buses (suffix <b>) is reduced. Bus 2 and/or bus 4 is not available.

- CAN - Configuration 585

- CAN - Trigger 586

- CAN - Decode Results 591

- CAN - Search 597

### 18.13.6.1 CAN - Configuration

BUS<b>:CAN:DATA:SOURce 585

BUS<b>:CAN:TYPE 585

BUS<b>:CAN:SAMPlepoint 585

BUS<b>:CAN:BITRate 586

CHANnel<m>:THReshold:FINDlevel 586

### BUS<b>:CAN:DATA:SOURce <Source>

Sets the source of the data line. All channel waveforms can be used.

<!-- 来源：RTM2_UserManual_en_10_files\part1194.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1195.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | D0..D15

*RST: CH1

### BUS<b>:CAN:TYPE <SignalType>

Selects the CAN-High or CAN-Low line. CAN uses both lines for differential signal transmission.

If you measure with a differential probe, connect the probe to both CAN-H and CAN-L lines, and set the type CANH.

If you use a single-ended probe, connect the probe to either CAN_L or CAN_H, and select the data type accordingly.

<!-- 来源：RTM2_UserManual_en_10_files\part1196.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1197.htm -->

### Parameters:

<SignalType> CANH | CANL

*RST: CANH

### BUS<b>:CAN:SAMPlepoint <SamplePoint>

Sets the position of the sample point within the bit in percent of the nominal bit time.

See also: "Sample point" on page 230

<!-- 来源：RTM2_UserManual_en_10_files\part1198.htm -->

### Suffix:

<b> 1..4

Selects the bus.

| Parameters: |  |  |
| --- | --- | --- |
| <SamplePoint> | Range: | 10 to 90 |
|  | Increment: | 1 |
|  | *RST: | 50 |

Default unit: %

### BUS<b>:CAN:BITRate <BitRate>

Sets the number of transmitted bits per second.

<!-- 来源：RTM2_UserManual_en_10_files\part1199.htm -->

### Suffix:

<b> 1..4

Selects the bus.

| Parameters: |  |  |
| --- | --- | --- |
| <BitRate> | Range: | 100 to 5,04E06, depends on instrument type, ADC |
|  |  | clock rate |
|  | Increment: | depends on the bit rate value |
|  | *RST: | 50E03 |

Default unit: Bit/s

<!-- 来源：RTM2_UserManual_en_10_files\part1200.htm -->

### CHANnel<m>:THReshold:FINDlevel

Executes the analysis of all analog channels that are configured for the selected bus and sets the threshold for digitization of analog signals for each channel.

<!-- 来源：RTM2_UserManual_en_10_files\part1201.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

### Usage: Event

### 18.13.6.2 CAN - Trigger

TRIGger:A:SOURce 587

TRIGger:A:CAN:TYPE 587

TRIGger:A:CAN:FTYPe 588

TRIGger:A:CAN:ITYPe 588

TRIGger:A:CAN:ICONdition 589

TRIGger:A:CAN:IDENtifier 589

TRIGger:A:CAN:DLC 589

TRIGger:A:CAN:DCONdition 589

TRIGger:A:CAN:DATA 590

TRIGger:A:CAN:ACKerror 590

TRIGger:A:CAN:BITSterror 590

TRIGger:A:CAN:CRCerror 590

TRIGger:A:CAN:FORMerror 590

### TRIGger:A:SOURce <Source>

Sets the trigger source for the selected A trigger type.

<!-- 来源：RTM2_UserManual_en_10_files\part1202.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | EXTernanalog | LINE | SBUS1.. SBUS4 | D0. D15

<!-- 来源：RTM2_UserManual_en_10_files\part1203.htm -->

### CH1 | CH2 | CH3 | CH4

One of the input channels is the trigger source. Available chan- nels depend on the instrument type.

<!-- 来源：RTM2_UserManual_en_10_files\part1204.htm -->

### EXTernanalog

External trigger input on the rear panel

<!-- 来源：RTM2_UserManual_en_10_files\part1205.htm -->

### LINE

AC line for the edge trigger

<!-- 来源：RTM2_UserManual_en_10_files\part1206.htm -->

### SBUS1 SBUS4

Serial buses 1 to 4

The UART, SPI, SSPI and audio protocols require two bus lines (bus 1 and 2 or bus 3 and 4). Bus 2 and/or bus 4 is not available if one of these protocols is selected.

<!-- 来源：RTM2_UserManual_en_10_files\part1207.htm -->

### D0. D15

If MSO option R&S RTM-B1 is installed, the digital channels D0 to D15 can be used as trigger sources for edge, width and pat- tern trigger.

### TRIGger:A:CAN:TYPE <TriggerType> Specifies the trigger mode for CAN.

<!-- 来源：RTM2_UserManual_en_10_files\part1208.htm -->

### Parameters:

<TriggerType> STOFrame | EOFrame | ID | IDDT | FTYPe | ERRCondition

<!-- 来源：RTM2_UserManual_en_10_files\part1209.htm -->

### STOFrame

Start of frame

<!-- 来源：RTM2_UserManual_en_10_files\part1210.htm -->

### EOFrame

End of frame

<!-- 来源：RTM2_UserManual_en_10_files\part1211.htm -->

### ID

Sets the trigger to a specific message identifier or an identifier range.

```text
Specify the identifier with TRIGger:A:CAN:ITYPe, TRIGger: A:CAN:ICONdition, and TRIGger:A:CAN:IDENtifier.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1212.htm -->

### IDDT

Sets the trigger to a combination of identifier and data condition. The instrument triggers at the end of the last byte of the speci- fied data pattern.

```text
Specify the identifier (see ID), and the data with TRIGger:A: CAN:DLC, TRIGger:A:CAN:DCONdition, and TRIGger:A: CAN:DATA.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1213.htm -->

### FTYPe

Triggers on a specified frame type. Specify the frame type with

```text
TRIGger:A:CAN:FTYPe.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1214.htm -->

### ERRCondition

Identifies various errors in the frame. Specify the errors with

```text
TRIGger:A:CAN:ACKerror, TRIGger:A:CAN:BITSterror
, TRIGger:A:CAN:CRCerror, and TRIGger:A:CAN: FORMerror.
```

*RST: STOF

### TRIGger:A:CAN:FTYPe <FrameType>

Specifies the frame type to be triggered on if TRIGger:A:CAN:TYPE is set to FTYPe.

<!-- 来源：RTM2_UserManual_en_10_files\part1215.htm -->

### Parameters:

<FrameType> DATA | REMote | ERRor | OVERload | ANY

*RST: ERR

### TRIGger:A:CAN:ITYPe <IdentifierType>

Selects the length of the identifier: 11 bit for CAN base frames, or 29 bits for CAN extended frames.

The command is relevant if TRIGger:A:CAN:TYPE is set to ID or IDDT.

<!-- 来源：RTM2_UserManual_en_10_files\part1216.htm -->

### Parameters:

<IdentifierType> B11 | B29 | ANY

ANY: only available for CAN trigger type IDDT

*RST: B11

### TRIGger:A:CAN:ICONdition <IdentifierCondition>

Sets the comparison condition: If the pattern contains at least one X (don't care), you can trigger on values equal or not equal to the specified value. If the pattern contains only 0 and 1, you can also trigger on a range greater than or lower than the specified value.

The command is relevant if TRIGger:A:CAN:TYPE is set to ID or IDDT.

<!-- 来源：RTM2_UserManual_en_10_files\part1217.htm -->

### Parameters:

<IdentifierCondition> EQUual | NEQual | GTHan | LTHan

*RST: EQ

### TRIGger:A:CAN:IDENtifier <Identifier>

Defines the identifier pattern. The pattern length is defined with TRIGger:A:CAN: ITYPe on page 588.

The command is relevant if TRIGger:A:CAN:TYPE is set to ID or IDDT.

<!-- 来源：RTM2_UserManual_en_10_files\part1218.htm -->

### Parameters:

<Identifier> String containing binary pattern with max. 29 bit. Characters 0, 1, and X are allowed.

### TRIGger:A:CAN:DLC <DataLength>

Defines the length of the data pattern - the number of bytes in the pattern. The command is relevant if TRIGger:A:CAN:TYPE is set to IDDT.

<!-- 来源：RTM2_UserManual_en_10_files\part1219.htm -->

### Parameters:

<DataLength> Range: 0 to 8

Increment: 1

*RST: 1

Default unit: Byte

### TRIGger:A:CAN:DCONdition <DataCondition>

Sets the comparison condition for data: If the pattern contains at least one X (don't care), you can trigger on values equal or not equal to the specified value. If the pattern contains only 0 and 1, you can also trigger on a range greater than or lower than the specified value.

The command is relevant if TRIGger:A:CAN:TYPE is set to IDDT.

<!-- 来源：RTM2_UserManual_en_10_files\part1220.htm -->

### Parameters:

<DataCondition> EQUal | NEQual | GTHan | LTHan

*RST: EQ

### TRIGger:A:CAN:DATA <Data>

Defines the data pattern. The number of bytes in the data pattern is defined with

```text
TRIGger:A:CAN:DLC.
```

The command is relevant if TRIGger:A:CAN:TYPE is set to IDDT.

<!-- 来源：RTM2_UserManual_en_10_files\part1221.htm -->

### Parameters:

<Data> String containing binary pattern with max. 64 bit. Characters 0, 1, and X are allowed. Make sure to enter complete bytes.

### TRIGger:A:CAN:ACKerror <AcknowledgeError>

Triggers on acknowledgement errors. An acknowledgement error occurs when the transmitter does not receive an acknowledgment - a dominant bit during the Ack Slot.

The command is relevant if TRIGger:A:CAN:TYPE is set to ERRCondition.

<!-- 来源：RTM2_UserManual_en_10_files\part1222.htm -->

### Parameters:

<AcknowledgeError> ON | OFF

*RST: OFF

### TRIGger:A:CAN:BITSterror <BitStuffingError> Triggers on bit stuffing errors.

See also: "Stuff bit" on page 232.

The command is relevant if TRIGger:A:CAN:TYPE is set to ERRCondition.

<!-- 来源：RTM2_UserManual_en_10_files\part1223.htm -->

### Parameters:

<BitStuffingError> ON | OFF

*RST: ON

### TRIGger:A:CAN:CRCerror <CRCerror>

Triggers on errors in the Cyclic Redundancy Check.

The command is relevant if TRIGger:A:CAN:TYPE is set to ERRCondition.

<!-- 来源：RTM2_UserManual_en_10_files\part1224.htm -->

### Parameters:

<CRCerror> ON | OFF

*RST: OFF

### TRIGger:A:CAN:FORMerror <FormError>

Triggers on form errors. A form error occurs when a fixed-form bit field contains one or more illegal bits.

The command is relevant if TRIGger:A:CAN:TYPE is set to ERRCondition.

<!-- 来源：RTM2_UserManual_en_10_files\part1225.htm -->

### Parameters:

<FormError> ON | OFF

*RST: OFF

### 18.13.6.3 CAN - Decode Results

BUS<b>:CAN:FCOunt? 591

BUS<b>:CAN:FRAMe<n>:TYPE? 591

BUS<b>:CAN:FRAMe<n>:STATus? 592

BUS<b>:CAN:FRAMe<n>:STARt? 592

BUS<b>:CAN:FRAMe<n>:STOP? 593

BUS<b>:CAN:FRAMe<n>:DATA? 593

BUS<b>:CAN:FRAMe<n>:ACKState? 593

BUS<b>:CAN:FRAMe<n>:ACKValue? 594

BUS<b>:CAN:FRAMe<n>:CSSTate? 594

BUS<b>:CAN:FRAMe<n>:CSValue? 594

BUS<b>:CAN:FRAMe<n>:DLCState? 594

BUS<b>:CAN:FRAMe<n>:DLCValue? 595

BUS<b>:CAN:FRAMe<n>:IDSTate? 595

BUS<b>:CAN:FRAMe<n>:IDTYpe? 595

BUS<b>:CAN:FRAMe<n>:IDValue? 596

BUS<b>:CAN:FRAMe<n>:BSEPosition? 596

BUS<b>:CAN:FRAMe<n>:BCOunt? 596

BUS<b>:CAN:FRAMe<n>:BYTE<o>:STATe? 597

BUS<b>:CAN:FRAMe<n>:BYTE<o>:VALue? 597

<!-- 来源：RTM2_UserManual_en_10_files\part1226.htm -->

### BUS<b>:CAN:FCOunt?

Returns the number of received frames.

<!-- 来源：RTM2_UserManual_en_10_files\part1227.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1228.htm -->

### Return values:

<FrameCount> Total number of decoded frames.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1229.htm -->

### BUS<b>:CAN:FRAMe<n>:TYPE?

Returns the type of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1230.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1231.htm -->

### Return values:

<FrameType> DATA | REMote | ERR | OVLD

Data, remote, error or overload frame

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1232.htm -->

### BUS<b>:CAN:FRAMe<n>:STATus?

Returns the overall state of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1233.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1234.htm -->

### Return values:

<FrameStatus> OK | BTST | CRCD | ACKD | CRC | EOFD | NOACk | INSufficient

OK: frame is valid.

BTST: bit stuffing error occured CRCD: wrong CRC delimiter occured ACKD: Wrong ACK delimiter occured CRC: cyclic redundancy check failed EOFD: wrong end of frame

NOACk: acknowlegde is missing

INSufficient: frame is not completely contained in the acquisition. The acquired part of the frame is valid.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1235.htm -->

### BUS<b>:CAN:FRAMe<n>:STARt?

Returns the start time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1236.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1237.htm -->

### Return values:

<StartTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1238.htm -->

### BUS<b>:CAN:FRAMe<n>:STOP?

Returns the end time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1239.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1240.htm -->

### Return values:

<StopTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1241.htm -->

### BUS<b>:CAN:FRAMe<n>:DATA?

Returns the data words of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1242.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1243.htm -->

### Return values:

<FrameData> Comma-separated list of decimal values of the data bytes.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1244.htm -->

### BUS<b>:CAN:FRAMe<n>:ACKState?

Returns the state of the acknowledge field.

<!-- 来源：RTM2_UserManual_en_10_files\part1245.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1246.htm -->

### Return values:

<AcknowledgeState> OK | UNDF

UNDF: Undefined

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1247.htm -->

### BUS<b>:CAN:FRAMe<n>:ACKValue?

Returns the value of the acknowledge field.

<!-- 来源：RTM2_UserManual_en_10_files\part1248.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1249.htm -->

### Return values:

<AcknowledgeValue> Decimal value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1250.htm -->

### BUS<b>:CAN:FRAMe<n>:CSSTate?

Returns the state of the checksum.

<!-- 来源：RTM2_UserManual_en_10_files\part1251.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1252.htm -->

### Return values:

<ChecksumState> OK | UNDF

UNDF: Undefined

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1253.htm -->

### BUS<b>:CAN:FRAMe<n>:CSValue?

Returns the checksum value.

<!-- 来源：RTM2_UserManual_en_10_files\part1254.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1255.htm -->

### Return values:

<ChecksumValue> Decimal value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1256.htm -->

### BUS<b>:CAN:FRAMe<n>:DLCState?

Returns the state of the data length code.

<!-- 来源：RTM2_UserManual_en_10_files\part1257.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1258.htm -->

### Return values:

<DLCState> OK | UNDF

UNDF: Undefined

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1259.htm -->

### BUS<b>:CAN:FRAMe<n>:DLCValue?

Returns the number of data bytes in the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1260.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1261.htm -->

### Return values:

<DLCValue> non-negative integer

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1262.htm -->

### BUS<b>:CAN:FRAMe<n>:IDSTate?

Returns the state of the identifier.

<!-- 来源：RTM2_UserManual_en_10_files\part1263.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1264.htm -->

### Return values:

<IdentifierState> OK | UNDF

UNDF: Undefined

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1265.htm -->

### BUS<b>:CAN:FRAMe<n>:IDTYpe?

Returns the length of the identifier: 11 bit for CAN base frames, or 29 bits for CAN extended frames.

<!-- 来源：RTM2_UserManual_en_10_files\part1266.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1267.htm -->

### Return values:

<IdentifierType> ANY | B11 | B29

<!-- 来源：RTM2_UserManual_en_10_files\part1268.htm -->

### ANY

No length specified, for example, for triggering on data only.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1269.htm -->

### BUS<b>:CAN:FRAMe<n>:IDValue?

Returns the decimal address value of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1270.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1271.htm -->

### Return values:

<IdentifierValue> Decimal value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1272.htm -->

### BUS<b>:CAN:FRAMe<n>:BSEPosition?

Returns the position of the bit stuffing error in the specified frame (if available).

<!-- 来源：RTM2_UserManual_en_10_files\part1273.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1274.htm -->

### Return values:

<ErrorPosition> *RST: 0

Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1275.htm -->

### BUS<b>:CAN:FRAMe<n>:BCOunt?

Returns the number of data bytes in the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1276.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1277.htm -->

### Return values:

<ByteCount> Number of words (bytes)

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1278.htm -->

### BUS<b>:CAN:FRAMe<n>:BYTE<o>:STATe?

Returns the state of the specified data byte.

<!-- 来源：RTM2_UserManual_en_10_files\part1279.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<o> *

Selects the byte number (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1280.htm -->

### Return values:

<ByteStatus> OK | UNDF UNDF: Undefined

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1281.htm -->

### BUS<b>:CAN:FRAMe<n>:BYTE<o>:VALue?

Returns the decimal value of the specified byte.

<!-- 来源：RTM2_UserManual_en_10_files\part1282.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<o> *

Selects the byte number (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1283.htm -->

### Return values:

<ByteValue> Decimal value

### Usage: Query only

### 18.13.6.4 CAN - Search

SEARch:PROTocol:CAN:CONDition 598

SEARch:PROTocol:CAN:FRAMe 598

SEARch:PROTocol:CAN:ACKerror 599

SEARch:PROTocol:CAN:BITSterror 599

SEARch:PROTocol:CAN:CRCerror 599

SEARch:PROTocol:CAN:FORMerror 600

SEARch:PROTocol:CAN:FTYPe 600

SEARch:PROTocol:CAN:ITYPe 600

SEARch:PROTocol:CAN:ICONdition 600

SEARch:PROTocol:CAN:IDENtifier 600

SEARch:PROTocol:CAN:DLENgth 601

SEARch:PROTocol:CAN:DCONdition 601

SEARch:PROTocol:CAN:DATA 601

### SEARch:PROTocol:CAN:CONDition <SearchCondition>

Sets the event or combination of events to be searched for. Depending on the selected event, further settings are required.

<!-- 来源：RTM2_UserManual_en_10_files\part1284.htm -->

### Parameters:

<SearchCondition> FRAMe | ERRor | IDENtifier | IDData | IDERror

<!-- 来源：RTM2_UserManual_en_10_files\part1285.htm -->

### FRAMe

```text
Search for a frame type. Set the frame type with SEARch: PROTocol:CAN:FRAMe.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1286.htm -->

### ERRor

```text
Search for errors of one or more error types. Set the error types with SEARch:PROTocol:CAN:ACKerror, SEARch: PROTocol:CAN:BITSterror, SEARch:PROTocol:CAN: CRCerror, and SEARch:PROTocol:CAN:FORMerror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1287.htm -->

### IDENtifier

Search for identifier.

```text
Specifiy the identifier with SEARch:PROTocol:CAN:FTYPe, SEARch:PROTocol:CAN:ITYPe, SEARch:PROTocol:CAN:
ICONdition, and SEARch:PROTocol:CAN:IDENtifier.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1288.htm -->

### IDData

Search for identifier and data.

```text
Set the identifier (see IDENtifier) and the data with SEARch: PROTocol:CAN:DLENgth, SEARch:PROTocol:CAN: DCONdition, and SEARch:PROTocol:CAN:DATA.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1289.htm -->

### IDERror

Search for errors that occur with a specified identifier.

Set the identifier (see IDENtifier) and the errors to be found (see ERRor)

*RST: FRAM

### SEARch:PROTocol:CAN:FRAMe <Frame> Selects the frame type to be searched for.

The command is relevant if SEARch:PROTocol:CAN:CONDition is set to FRAMe.

<!-- 来源：RTM2_UserManual_en_10_files\part1290.htm -->

### Parameters:

<Frame> SOF | EOF | OVERload | ERRor | DTA11 | DTA29 | REM11 | REM29

SOF: start of frame EOF: end of frame

OVERload: overload frame ERRor: error frame

DTA11: data frame with 11bit identifier DTA29: data frame with 29bit identifier REM11: remote frame with 11bit identifier REM29: remote frame with 29bit identifier

*RST: SOF

### SEARch:PROTocol:CAN:ACKerror <AcknowledgeError>

Searches for acknowledgement errors. An acknowledgement error occurs when the transmitter does not receive an acknowledgment - a dominant bit during the Ack Slot.

The command is relevant if SEARch:PROTocol:CAN:CONDition is set to ERRor or

```text
IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1291.htm -->

### Parameters:

<AcknowledgeError> ON | OFF

*RST: OFF

### SEARch:PROTocol:CAN:BITSterror <BitStuffingError> Searches for bit stuffing errors.

See also: "Stuff bit" on page 232.

The command is relevant if SEARch:PROTocol:CAN:CONDition is set to ERRor or

```text
IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1292.htm -->

### Parameters:

<BitStuffingError> ON | OFF

*RST: OFF

### SEARch:PROTocol:CAN:CRCerror <CRCerror> Searches for errors in the Cyclic Redundancy Check.

The command is relevant if SEARch:PROTocol:CAN:CONDition is set to ERRor or

```text
IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1293.htm -->

### Parameters:

<CRCerror> ON | OFF

*RST: OFF

### SEARch:PROTocol:CAN:FORMerror <FormError>

Searches for form errors. A form error occurs when a fixed-form bit field contains one or more illegal bits.

The command is relevant if SEARch:PROTocol:CAN:CONDition is set to ERRor or

```text
IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1294.htm -->

### Parameters:

<FormError> ON | OFF

*RST: OFF

### SEARch:PROTocol:CAN:FTYPe <FrameType>

Specifies the frame type to be searched for if SEARch:PROTocol:CAN:CONDition is set to IDENtifier.

<!-- 来源：RTM2_UserManual_en_10_files\part1295.htm -->

### Parameters:

<FrameType> DATA | REMote | ANY

### SEARch:PROTocol:CAN:ITYPe <IdType>

Selects the length of the identifier: 11 bit for CAN base frames, or 29 bits for CAN extended frames.

```text
The command is relevant if SEARch:PROTocol:CAN:CONDition is set to
IDENtifier, IDData, or IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1296.htm -->

### Parameters:

<IdType> B11 | B29

*RST: B11

### SEARch:PROTocol:CAN:ICONdition <IdCondition>

Sets the comparison condition for the identifier: If the pattern contains at least one X (don't care), you can trigger on values equal or not equal to the specified value. If the pattern contains only 0 and 1, you can also trigger on a range greater than or lower than the specified value.

```text
The command is relevant if SEARch:PROTocol:CAN:CONDition is set to
IDENtifier, IDData, or IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1297.htm -->

### Parameters:

<IdCondition> EQUal | NEQual | GTHan | LTHan

*RST: EQU

### SEARch:PROTocol:CAN:IDENtifier <Identifier>

```text
Defines the identifier pattern. The pattern length is defined with SEARch:PROTocol: CAN:ITYPe.
The command is relevant if SEARch:PROTocol:CAN:CONDition is set to
IDENtifier, IDData, or IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1298.htm -->

### Parameters:

<Identifier> String containing binary pattern with max. 29 bit. Characters 0, 1, and X are allowed.

### SEARch:PROTocol:CAN:DLENgth <DataLength>

Defines the length of the data pattern - the number of bytes in the pattern.

The command is relevant if SEARch:PROTocol:CAN:CONDition is set to IDData.

<!-- 来源：RTM2_UserManual_en_10_files\part1299.htm -->

### Parameters:

<DataLength> Range: 0 to 8

Increment: 1

*RST: 1

Default unit: Byte

### SEARch:PROTocol:CAN:DCONdition <DataCondition>

Sets the comparison condition for data: If the pattern contains at least one X (don't care), you can trigger on values equal or not equal to the specified value. If the pattern contains only 0 and 1, you can also trigger on a range greater than or lower than the specified value.

The command is relevant if SEARch:PROTocol:CAN:CONDition is set to IDData.

<!-- 来源：RTM2_UserManual_en_10_files\part1300.htm -->

### Parameters:

<DataCondition> EQUal | NEQual | GTHan | LTHan

*RST: EQU

<!-- 来源：RTM2_UserManual_en_10_files\part1301.htm -->

### SEARch:PROTocol:CAN:DATA <Data>

```text
Defines the data pattern. The pattern length is defined with SEARch:PROTocol:CAN: DLENgth.
```

The command is relevant if SEARch:PROTocol:CAN:CONDition is set to IDData.

<!-- 来源：RTM2_UserManual_en_10_files\part1302.htm -->

### Parameters:

<Data> String containing binary pattern with max. 64 bit. Characters 0, 1, and X are allowed. Make sure to enter complete bytes.

<!-- 来源：RTM2_UserManual_en_10_files\part1303.htm -->

### 18.13.7 LIN

The Local Interconnect Network (LIN) is a simple, low-cost bus system used within automotive network architectures.

Note: SPI/SSPI and UART protocols occupy two bus lines (bus 1 and 2 or bus 3 and 4). If one of these buses is configured, the number of buses (suffix <b>) is reduced. Bus 2 and/or bus 4 is not available.

- LIN - Configuration 602

- LIN - Trigger 603

- LIN - Decode Results 606

- LIN - Search 612

### 18.13.7.1 LIN - Configuration

BUS<b>:LIN:DATA:SOURce 602

BUS<b>:LIN:POLarity 602

BUS<b>:LIN:STANdard 602

BUS<b>:LIN:BITRate 603

CHANnel<m>:THReshold:FINDlevel 603

### BUS<b>:LIN:DATA:SOURce <Source>

Sets the source of the data line. All channel waveforms can be used.

<!-- 来源：RTM2_UserManual_en_10_files\part1304.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1305.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | D0..D15

*RST: CH1

### BUS<b>:LIN:POLarity <Polarity>

Defines the idle state of the bus. The idle state is the rezessive state and corresponds to a logic 1.

<!-- 来源：RTM2_UserManual_en_10_files\part1306.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1307.htm -->

### Parameters:

<Polarity> IDLHigh | IDLLow

IDLHigh: Low active, negative polarity IDLLow: High active, positive polarity

*RST: IDLL

### BUS<b>:LIN:STANdard <Standard>

Selects the version of the LIN standard that is used in the DUT. The setting mainly defines the checksum version used during decoding.

The most common version is LIN 2.x. For mixed networks, or if the standard is unknown, set the LIN standard to AUTO.

<!-- 来源：RTM2_UserManual_en_10_files\part1308.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1309.htm -->

### Parameters:

<Standard> V1X | V2X | J2602 | AUTO

*RST: V1X

### BUS<b>:LIN:BITRate <BitRate>

Sets the number of transmitted bits per second.

<!-- 来源：RTM2_UserManual_en_10_files\part1310.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1311.htm -->

### Parameters:

<BitRate> *RST: 9,6E03 Default unit: Bit/s

<!-- 来源：RTM2_UserManual_en_10_files\part1312.htm -->

### CHANnel<m>:THReshold:FINDlevel

Executes the analysis of all analog channels that are configured for the selected bus and sets the threshold for digitization of analog signals for each channel.

<!-- 来源：RTM2_UserManual_en_10_files\part1313.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

### Usage: Event

### 18.13.7.2 LIN - Trigger

TRIGger:A:SOURce 603

TRIGger:A:LIN:TYPE 604

TRIGger:A:LIN:CHKSerror 605

TRIGger:A:LIN:IPERror 605

TRIGger:A:LIN:SYERror 605

TRIGger:A:LIN:ICONdition 605

TRIGger:A:LIN:IDENtifier 605

TRIGger:A:LIN:DATA 606

TRIGger:A:LIN:DCONdition 606

TRIGger:A:LIN:DLENgth 606

### TRIGger:A:SOURce <Source>

Sets the trigger source for the selected A trigger type.

<!-- 来源：RTM2_UserManual_en_10_files\part1314.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | EXTernanalog | LINE | SBUS1.. SBUS4 | D0..D15

<!-- 来源：RTM2_UserManual_en_10_files\part1315.htm -->

### CH1 | CH2 | CH3 | CH4

One of the input channels is the trigger source. Available chan- nels depend on the instrument type.

<!-- 来源：RTM2_UserManual_en_10_files\part1316.htm -->

### EXTernanalog

External trigger input on the rear panel

<!-- 来源：RTM2_UserManual_en_10_files\part1317.htm -->

### LINE

AC line for the edge trigger

<!-- 来源：RTM2_UserManual_en_10_files\part1318.htm -->

### SBUS1.. SBUS4

Serial buses 1 to 4

The UART, SPI, SSPI and audio protocols require two bus lines (bus 1 and 2 or bus 3 and 4). Bus 2 and/or bus 4 is not available if one of these protocols is selected.

<!-- 来源：RTM2_UserManual_en_10_files\part1319.htm -->

### D0..D15

If MSO option R&S RTM-B1 is installed, the digital channels D0 to D15 can be used as trigger sources for edge, width and pat- tern trigger.

### TRIGger:A:LIN:TYPE <TriggerType> Specifies the trigger mode for LIN.

<!-- 来源：RTM2_UserManual_en_10_files\part1320.htm -->

### Parameters:

<TriggerType> SYNC | WKFRame | ID | IDDT | ERRCondition

<!-- 来源：RTM2_UserManual_en_10_files\part1321.htm -->

### SYNC

Start of frame, triggers on the stop bit of the sync field.

<!-- 来源：RTM2_UserManual_en_10_files\part1322.htm -->

### WKFRame

Triggers after a wakeup frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1323.htm -->

### ID

```text
Sets the trigger to a specific identifier or an identifier range. Set the identifier with TRIGger:A:LIN:ICONdition and TRIGger:A:LIN:IDENtifier.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1324.htm -->

### IDDT

```text
Set the identifier (see ID) and the data with TRIGger:A:LIN: DLENgth, TRIGger:A:LIN:DCONdition, and TRIGger:A: LIN:DATA.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1325.htm -->

### ERRCondition

Identifies various errors in the frame. You can select one or more error types as trigger condition.

```text
Select the error types with TRIGger:A:LIN:CHKSerror, TRIGger:A:LIN:IPERror, and TRIGger:A:LIN:SYERror.
```

*RST: SYNC

### TRIGger:A:LIN:CHKSerror <ChecksumError>

Triggers on a checksum error. The checksum verifies the correct data transmission. It is the last byte of the frame response. The checksum includes not only the data but also the protected identifier (PID).

The command is relevant if TRIGger:A:LIN:TYPE is set to ERRCondition.

<!-- 来源：RTM2_UserManual_en_10_files\part1326.htm -->

### Parameters:

<ChecksumError> ON | OFF

*RST: ON

### TRIGger:A:LIN:IPERror <IdParityError>

Triggers on a parity error. Parity bits are the bits 6 and 7 of the identifier. They verify the correct transmission of the identifier.

The command is relevant if TRIGger:A:LIN:TYPE is set to ERRCondition.

<!-- 来源：RTM2_UserManual_en_10_files\part1327.htm -->

### Parameters:

<IdParityError> ON | OFF

*RST: OFF

### TRIGger:A:LIN:SYERror <SyncError> Triggers if synchronization caused an error.

The command is relevant if TRIGger:A:LIN:TYPE is set to ERRCondition.

<!-- 来源：RTM2_UserManual_en_10_files\part1328.htm -->

### Parameters:

<SyncError> ON | OFF

*RST: OFF

### TRIGger:A:LIN:ICONdition <IdentifierCondition>

Sets the comparison condition for the identifier: If the pattern contains at least one X (don't care), you can trigger on values equal or not equal to the specified value. If the pattern contains only 0 and 1, you can also trigger on a range greater than or lower than the specified value.

The command is relevant if TRIGger:A:LIN:TYPE is set to ID or IDDT.

<!-- 来源：RTM2_UserManual_en_10_files\part1329.htm -->

### Parameters:

<IdentifierCondition> EQUal | NEQual | GTHan | LTHan

*RST: EQ

### TRIGger:A:LIN:IDENtifier <Identifier> Defines the identifier pattern.

The command is relevant if TRIGger:A:LIN:TYPE is set to ID or IDDT.

<!-- 来源：RTM2_UserManual_en_10_files\part1330.htm -->

### Parameters:

<Identifier> String containing binary pattern. Characters 0, 1, and X are allowed. Enter the 6 bit identifier without parity bits, not the pro- tected identifier.

### TRIGger:A:LIN:DATA <Data>

Defines the data pattern. The number of bytes in the data pattern is defined with

```text
TRIGger:A:LIN:DLENgth.
```

The command is relevant if TRIGger:A:LIN:TYPE is set to IDDT.

<!-- 来源：RTM2_UserManual_en_10_files\part1331.htm -->

### Parameters:

<Data> String containing binary pattern with max. 64 bit. Characters 0, 1, and X are allowed. Make sure to enter complete bytes.

### TRIGger:A:LIN:DCONdition <DataCondition>

Sets the comparison condition for data: If the pattern contains at least one X (don't care), you can trigger on values equal or not equal to the specified value. If the pattern contains only 0 and 1, you can also trigger on a range greater than or lower than the specified value.

The command is relevant if TRIGger:A:LIN:TYPE is set to IDDT.

<!-- 来源：RTM2_UserManual_en_10_files\part1332.htm -->

### Parameters:

<DataCondition> EQUal | NEQual | GTHan | LTHan

*RST: EQ

### TRIGger:A:LIN:DLENgth <DataLength>

Defines the length of the data pattern - the number of bytes in the pattern. The command is relevant if TRIGger:A:LIN:TYPE is set to IDDT.

<!-- 来源：RTM2_UserManual_en_10_files\part1333.htm -->

### Parameters:

<DataLength> Range: 1 to 8

Increment: 1

*RST: 1

Default unit: Byte

### 18.13.7.3 LIN - Decode Results

BUS<b>:LIN:FCOunt? 607

BUS<b>:LIN:FRAMe<n>:DATA? 607

BUS<b>:LIN:FRAMe<n>:STATus? 607

BUS<b>:LIN:FRAMe<n>:STARt? 608

BUS<b>:LIN:FRAMe<n>:STOP? 608

BUS<b>:LIN:FRAMe<n>:CSSTate? 608

BUS<b>:LIN:FRAMe<n>:CSValue? 609

BUS<b>:LIN:FRAMe<n>:IDPValue? 609

BUS<b>:LIN:FRAMe<n>:IDSTate? 609

BUS<b>:LIN:FRAMe<n>:IDValue? 610

BUS<b>:LIN:FRAMe<n>:SYSTate? 610

BUS<b>:LIN:FRAMe<n>:SYValue? 610

BUS<b>:LIN:FRAMe<n>:VERSion? 610

BUS<b>:LIN:FRAMe<n>:BCOunt? 611

BUS<b>:LIN:FRAMe<n>:BYTE<o>:STATe? 611

BUS<b>:LIN:FRAMe<n>:BYTE<o>:VALue? 612

<!-- 来源：RTM2_UserManual_en_10_files\part1334.htm -->

### BUS<b>:LIN:FCOunt?

Returns the number of received frames of the active LIN bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1335.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1336.htm -->

### Return values:

<FrameCount> Total number of decoded frames.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1337.htm -->

### BUS<b>:LIN:FRAMe<n>:DATA?

Returns the data bytes of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1338.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1339.htm -->

### Return values:

<FrameData> Comma-separated list of decimal values of the data bytes.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1340.htm -->

### BUS<b>:LIN:FRAMe<n>:STATus?

### Suffix:

<b> 1..4

Selects the bus.

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1341.htm -->

### Return values:

<FrameStatus> OK | UART | CHCKsum | PRERror | SYERror | WAKeup | INSufficient | ERR | LENer

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1342.htm -->

### BUS<b>:LIN:FRAMe<n>:STARt?

Returns the start time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1343.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1344.htm -->

### Return values:

<StartTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1345.htm -->

### BUS<b>:LIN:FRAMe<n>:STOP?

Returns the end time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1346.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1347.htm -->

### Return values:

<StopTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1348.htm -->

### BUS<b>:LIN:FRAMe<n>:CSSTate?

Returns the checksum state of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1349.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1350.htm -->

### Return values:

<ChecksumState> OK | ERR | UNDF

ERR: error UNDF: undefined

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1351.htm -->

### BUS<b>:LIN:FRAMe<n>:CSValue?

Returns the checksum value.

<!-- 来源：RTM2_UserManual_en_10_files\part1352.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1353.htm -->

### Return values:

<ChecksumValue> Decimal value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1354.htm -->

### BUS<b>:LIN:FRAMe<n>:IDPValue?

Returns the parity value.

<!-- 来源：RTM2_UserManual_en_10_files\part1355.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1356.htm -->

### Return values:

<IdentifierParityValue>Decimal value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1357.htm -->

### BUS<b>:LIN:FRAMe<n>:IDSTate?

Returns the identifier state of the selected frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1358.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1359.htm -->

### Return values:

<IdentifierState> OK | PRERror | UVAL | INSufficient

PRERror: parity error UVAL: unexpected value

INSufficient: the frame is not completely contained in the acqui- sition. The decoded part of the frame is valid.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1360.htm -->

### BUS<b>:LIN:FRAMe<n>:IDValue?

Returns the identifier value (address)

<!-- 来源：RTM2_UserManual_en_10_files\part1361.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1362.htm -->

### Return values:

<IdentifierValue> Decimal value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1363.htm -->

### BUS<b>:LIN:FRAMe<n>:SYSTate?

Returns the state of the sync field for the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1364.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1365.htm -->

### Return values:

<SyncFieldState> OK | ERR | UNDF

ERR: error UNDF: undefined

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1366.htm -->

### BUS<b>:LIN:FRAMe<n>:SYValue?

Returns the value of the synchronization field.

<!-- 来源：RTM2_UserManual_en_10_files\part1367.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1368.htm -->

### Return values:

<SyncFieldValue> Decimal value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1369.htm -->

### BUS<b>:LIN:FRAMe<n>:VERSion?

Returns the version of the LIN standard for the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1370.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1371.htm -->

### Return values:

<FrameVersion> V1X | V2X | UNK

UNK: Unknown

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1372.htm -->

### BUS<b>:LIN:FRAMe<n>:BCOunt?

Returns the number of data bytes in the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1373.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1374.htm -->

### Return values:

<ByteCount> Number of words (bytes)

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1375.htm -->

### BUS<b>:LIN:FRAMe<n>:BYTE<o>:STATe?

Returns the state of the specified data byte.

<!-- 来源：RTM2_UserManual_en_10_files\part1376.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<o> *

Selects the byte number (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1377.htm -->

### Return values:

<ByteStatus> OK | INS | UART

The byte is not completely contained in the acquisition

<!-- 来源：RTM2_UserManual_en_10_files\part1378.htm -->

### UART

At least one UART error occured. LIN uses UART words without parity bit.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1379.htm -->

### BUS<b>:LIN:FRAMe<n>:BYTE<o>:VALue?

Returns the decimal value of the specified byte.

<!-- 来源：RTM2_UserManual_en_10_files\part1380.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<o> *

Selects the byte number (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1381.htm -->

### Return values:

<ByteValue> Decimal value

### Usage: Query only

### 18.13.7.4 LIN - Search

SEARch:PROTocol:LIN:CONDition 612

SEARch:PROTocol:LIN:FRAMe 613

SEARch:PROTocol:LIN:IPERror 613

SEARch:PROTocol:LIN:CHKSerror 614

SEARch:PROTocol:LIN:SYERror 614

SEARch:PROTocol:LIN:ICONdition 614

SEARch:PROTocol:LIN:IDENtifier 614

SEARch:PROTocol:LIN:DLENgth 614

SEARch:PROTocol:LIN:DCONdition 615

SEARch:PROTocol:LIN:DATA 615

### SEARch:PROTocol:LIN:CONDition <SearchCondition>

Sets the event or combination of events to be searched for. Depending on the selected event, further settings are required.

<!-- 来源：RTM2_UserManual_en_10_files\part1382.htm -->

### Parameters:

<SearchCondition> FRAMe | ERRor | IDENtifier | IDData | IDERror

<!-- 来源：RTM2_UserManual_en_10_files\part1383.htm -->

### FRAMe

Search for a frame type.

```text
Set the frame type with SEARch:PROTocol:LIN:FRAMe.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1384.htm -->

### ERRor

Search for errors of one or more error types.

```text
Set the error types with SEARch:PROTocol:LIN:CHKSerror, SEARch:PROTocol:LIN:IPERror, and SEARch:PROTocol: LIN:SYERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1385.htm -->

### IDENtifier

Search for identifier.

```text
Specifiy the identifier with SEARch:PROTocol:LIN: ICONdition and SEARch:PROTocol:LIN:IDENtifier.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1386.htm -->

### IDData

Search for identifier and data.

```text
Set the identifier (see IDENtifier) and the data with SEARch: PROTocol:LIN:DLENgth, SEARch:PROTocol:LIN: DCONdition, and SEARch:PROTocol:LIN:DATA.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1387.htm -->

### IDERror

Search for errors that occur with a specified identifier. Set the identifier (see IDENtifier) and the errors to be found (see ERRor).

*RST: FRAM

### SEARch:PROTocol:LIN:FRAMe <Frame> Selects the frame type to be searched for.

The command is relevant if SEARch:PROTocol:LIN:CONDition is set to FRAMe.

<!-- 来源：RTM2_UserManual_en_10_files\part1388.htm -->

### Parameters:

<Frame> SOF | WAKeup

SOF: start of frame WAKeup: Wakeup frame

*RST: SOF

### SEARch:PROTocol:LIN:IPERror <IdParityError> Searches for parity errors.

The command is relevant if SEARch:PROTocol:LIN:CONDition is set to ERRor or

```text
IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1389.htm -->

### Parameters:

<IdParityError> ON | OFF

*RST: OFF

### SEARch:PROTocol:LIN:CHKSerror <ChecksumError> Searches for checksum errors.

The command is relevant if SEARch:PROTocol:LIN:CONDition is set to ERRor or

```text
IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1390.htm -->

### Parameters:

<ChecksumError> ON | OFF

*RST: OFF

### SEARch:PROTocol:LIN:SYERror <SyncError> Searches for synchronization errors.

The command is relevant if SEARch:PROTocol:LIN:CONDition is set to ERRor or

```text
IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1391.htm -->

### Parameters:

<SyncError> ON | OFF

*RST: OFF

### SEARch:PROTocol:LIN:ICONdition <IdCondition>

Sets the comparison condition for the identifier: If the pattern contains at least one X (don't care), you can trigger on values equal or not equal to the specified value. If the pattern contains only 0 and 1, you can also trigger on a range greater than or lower than the specified value.

```text
The command is relevant if SEARch:PROTocol:LIN:CONDition is set to
IDENtifier, IDData or IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1392.htm -->

### Parameters:

<IdCondition> EQUal | NEQual | GTHan | LTHan

*RST: EQU

### SEARch:PROTocol:LIN:IDENtifier <Identifier> Defines the identifier pattern.

```text
The command is relevant if SEARch:PROTocol:LIN:CONDition is set to
IDENtifier, IDData or IDERror.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1393.htm -->

### Parameters:

<Identifier> String containing binary pattern. Characters 0, 1, and X are allowed. Enter the 6 bit identifier without parity bits, not the pro- tected identifier.

### SEARch:PROTocol:LIN:DLENgth <DataLength>

Defines the length of the data pattern - the number of bytes in the pattern.

The command is relevant if SEARch:PROTocol:LIN:CONDition is set to IDData.

<!-- 来源：RTM2_UserManual_en_10_files\part1394.htm -->

### Parameters:

<DataLength> Range: 1 to 8

Increment: 1

*RST: 1

Default unit: Byte

### SEARch:PROTocol:LIN:DCONdition <DataCondition>

Sets the comparison condition for data: If the pattern contains at least one X (don't care), you can trigger on values equal or not equal to the specified value. If the pattern contains only 0 and 1, you can also trigger on a range greater than or lower than the specified value.

The command is relevant if SEARch:PROTocol:LIN:CONDition is set to IDData.

<!-- 来源：RTM2_UserManual_en_10_files\part1395.htm -->

### Parameters:

<DataCondition> EQUal | NEQual | GTHan | LTHan

*RST: EQU

<!-- 来源：RTM2_UserManual_en_10_files\part1396.htm -->

### SEARch:PROTocol:LIN:DATA <Data>

```text
Defines the data pattern. The pattern length is defined with SEARch:PROTocol:LIN: DLENgth.
```

The command is relevant if SEARch:PROTocol:LIN:CONDition is set to IDData.

<!-- 来源：RTM2_UserManual_en_10_files\part1397.htm -->

### Parameters:

<Data> String containing binary pattern with max. 64 bit. Characters 0, 1, and X are allowed. Make sure to enter complete bytes.

<!-- 来源：RTM2_UserManual_en_10_files\part1398.htm -->

### 18.13.8 Audio Signals (Option R&S RTM-K5)

- Audio Signal Configuration 615

- Audio Trigger 621

- Track of Audio Signals 624

- Audio Decode Results 628

### 18.13.8.1 Audio Signal Configuration

BUS<b>:I2S:AVARiant 616

BUS<b>:I2S:CLOCk:SOURce 616

BUS<b>:I2S:CLOCk:POLarity 616

BUS<b>:I2S:WSELect:SOURce 617

BUS<b>:I2S:WSELect:POLarity 617

BUS<b>:I2S:DATA:SOURce 617

BUS<b>:I2S:DATA:POLarity 618

BUS<b>:I2S:CLOCk:THReshold 618

BUS<b>:I2S:DATA:THReshold 618

BUS<b>:I2S:WSELect:THReshold 618

CHANnel<m>:THReshold:FINDlevel 618

BUS<b>:I2S:WLENgth 619

BUS<b>:I2S:BORDer 619

BUS<b>:I2S:CHANnel:ORDer 619

BUS<b>:I2S:CHANnel:TDMCount 620

BUS<b>:I2S:CHANnel:LENGth 620

BUS<b>:I2S:CHANnel:OFFSet 620

BUS<b>:I2S:FOFFset 620

### BUS<b>:I2S:AVARiant <AudioVariant> Selects the protocol variant of the audio signal.

See also: Chapter 11. 7.1, "Audio Protocols", on page 252

<!-- 来源：RTM2_UserManual_en_10_files\part1399.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1400.htm -->

### Parameters:

<AudioVariant> I2S | LJ | RJ | TDM | DSP

I2S: Inter-IC Sound standard audio format. LJ: left justified data format

RJ: right justified data format

TDM: Time Division Multiplexed audio format to transfer up to 8 audio data channels on one line

*RST: I2S

### BUS<b>:I2S:CLOCk:SOURce <ClockSource>

Selects the source of the clock line. All analog channels of the instrument can be used. If MSO option R&S RTM-B1 is installed, you can use also one of the digital channels.

<!-- 来源：RTM2_UserManual_en_10_files\part1401.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1402.htm -->

### Parameters:

<ClockSource> CH1 | CH2 | CH3 | CH4 | D0..15

*RST: CH2

### BUS<b>:I2S:CLOCk:POLarity <ClockSlope>

Sets the clock edge at which the instrument samples the data on the data line. Usually, the rising edge is used. The R&S RTM can also analyze the converse setup.

<!-- 来源：RTM2_UserManual_en_10_files\part1403.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1404.htm -->

### Parameters:

<ClockSlope> RISing | FALLing

*RST: RIS

### BUS<b>:I2S:WSELect:SOURce <WordSelectSource>

Selects the source of the word select line. All analog channels of the instrument can be used. If MSO option R&S RTM-B1 is installed, you can use also one of the digital channels.

<!-- 来源：RTM2_UserManual_en_10_files\part1405.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1406.htm -->

### Parameters:

<WordSelectSource> CH1 | CH2 | CH3 | CH4 | D0..15

*RST: CH1

### BUS<b>:I2S:WSELect:POLarity <WordSelectPolarity>

For I²S, left and right justified signals, the polarity defines the word select values assigned to the left and right channels.

For TDM) signals, the polarity defines the edge of the frame synchronization pulse that identifies the beginning of a frame. The frame starts at the next clock edge following the selected FSYNC edge.

<!-- 来源：RTM2_UserManual_en_10_files\part1407.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1408.htm -->

### Parameters:

<WordSelectPolarity> NORMal | INVert

<!-- 来源：RTM2_UserManual_en_10_files\part1409.htm -->

### NORMal

0 indicates the left channel, and 1 indicates the right channel. This is the usual setting.

TDM: the frame begins with a rising edge. This is the usual set- ting.

<!-- 来源：RTM2_UserManual_en_10_files\part1410.htm -->

### INVert

0 indicates the right channel, and 1 the left channel. TDM: the frame begins with a falling edge.

*RST: NORM

### BUS<b>:I2S:DATA:SOURce <DataSource>

Selects the source of the data line. All analog channels of the instrument can be used. If MSO option R&S RTM-B1 is installed, you can use also one of the digital channels.

<!-- 来源：RTM2_UserManual_en_10_files\part1411.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1412.htm -->

### Parameters:

<DataSource> CH1 | CH2 | CH3 | CH4 | D0..15

*RST: CH3

### BUS<b>:I2S:DATA:POLarity <DataPolarity>

Defines the interpretation of high and low signal states.

<!-- 来源：RTM2_UserManual_en_10_files\part1413.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1414.htm -->

### Parameters:

<DataPolarity> ACTHigh | ACTLow

<!-- 来源：RTM2_UserManual_en_10_files\part1415.htm -->

### ACTHigh

Active high: HIGH (signal level above the threshold level) = 1 and LOW (signal level below the threshold level) = 0

<!-- 来源：RTM2_UserManual_en_10_files\part1416.htm -->

### ACTLow

Active low: HIGH = 0 and LOW = 1

*RST: ACTH

### BUS<b>:I2S:CLOCk:THReshold <Threshold> BUS<b>:I2S:DATA:THReshold <Threshold> BUS<b>:I2S:WSELect:THReshold <Threshold>

Sets the threshold for the indicated audio line.

```text
The commands have the same effect as CHANnel<m>:THReshold for analog chan- nels. For digital channels, the threshold can be also set with DIGital<m>: TECHnology or DIGital<m>:THReshold
```

<!-- 来源：RTM2_UserManual_en_10_files\part1417.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1418.htm -->

### Parameters:

<Threshold> Threshold voltage

*RST: 1.4

<!-- 来源：RTM2_UserManual_en_10_files\part1419.htm -->

### CHANnel<m>:THReshold:FINDlevel

Executes the analysis of all analog channels that are configured for the selected bus and sets the threshold for digitization of analog signals for each channel.

<!-- 来源：RTM2_UserManual_en_10_files\part1420.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

### Usage: Event

### BUS<b>:I2S:WLENgth <WordLength>

Defines the number of bits in an audio data word (receiver length).

<!-- 来源：RTM2_UserManual_en_10_files\part1421.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1422.htm -->

### Parameters:

<WordLength> Range: The minimum length is 1bit, the maximum length is

the channel length.

*RST: 8

Default unit: Bit

### BUS<b>:I2S:BORDer <BitOrder>

Sets the bit order in the audio data words. Usually, the MSB is transmitted first.

<!-- 来源：RTM2_UserManual_en_10_files\part1423.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1424.htm -->

### Parameters:

<BitOrder> MSBFirst | LSBFirst

MSBFirst: most significant bit is transmitted first LSBFirst: least significant bit is transmitted first

*RST: MSBF

### BUS<b>:I2S:CHANnel:ORDer <ChannelOrder>

Defines if the left or the right channel is the first channel in the frame.

The setting is available for I²S standard, left and right justified audio signals.

<!-- 来源：RTM2_UserManual_en_10_files\part1425.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1426.htm -->

### Parameters:

<ChannelOrder> LFIRst | RFIRst

LFIRst: left channel first RFIRst: right channel first

*RST: LFIR

### BUS<b>:I2S:CHANnel:TDMCount <ChannelCount>

Sets the number of channels transmitted on the TDM audio line.

<!-- 来源：RTM2_UserManual_en_10_files\part1427.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1428.htm -->

### Parameters:

<ChannelCount> Range: 1 to 8

*RST: 8

### BUS<b>:I2S:CHANnel:LENGth <ChannelLength>

Sets the number of bits in a channel block for TDM audio signals (transmitter length). The setting is available only for TDM signals.

<!-- 来源：RTM2_UserManual_en_10_files\part1429.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1430.htm -->

### Parameters:

<ChannelLength> *RST: 8

Default unit: Bit

### BUS<b>:I2S:CHANnel:OFFSet <ChannelOffset>

Sets the number of bits between the channel start and the start of the audio word. The setting is available for left justified data format and TDM audio signals.

<!-- 来源：RTM2_UserManual_en_10_files\part1431.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1432.htm -->

### Parameters:

<ChannelOffset> For TDM, possible values depend on the channel lenght and the word length. The maximum offset is Channel length - Word length. If you change the channel lenght or the word length, the channel offset is adjusted automatically.

For left justified data format, the maximum offset is 31.

*RST: 1

Default unit: Bit

### BUS<b>:I2S:FOFFset <FrameOffset>

Sets a delay of the channel blocks after the frame start (word select edge). Thus, all channels are shifted.

The setting is available only for TDM signals.

<!-- 来源：RTM2_UserManual_en_10_files\part1433.htm -->

### Suffix:

<b> 1..4

Selects the bus.

| Parameters: |  |  |
| --- | --- | --- |
| <FrameOffset> | Range: | 0 to 31 |
|  | *RST: | 0 |
|  | Default unit: | Bit |

### 18.13.8.2 Audio Trigger

TRIGger:A:SOURce 621

TRIGger:A:I2S:TYPE 622

TRIGger:A:I2S:CHANnel:LEFT:CONDition 623

TRIGger:A:I2S:CHANnel:RIGHt:CONDition 623

TRIGger:A:I2S:CHANnel:TDM<n>:CONDition 623

TRIGger:A:I2S:CHANnel:LEFT:DMIN 623

TRIGger:A:I2S:CHANnel:RIGHt:DMIN 623

TRIGger:A:I2S:CHANnel:TDM<n>:DMIN 623

TRIGger:A:I2S:CHANnel:LEFT:DMAX 623

TRIGger:A:I2S:CHANnel:RIGHt:DMAX 623

TRIGger:A:I2S:CHANnel:TDM<n>:DMAX 623

TRIGger:A:I2S:FUNCtion 624

TRIGger:A:I2S:SOWords 624

TRIGger:A:I2S:WINDow:LENGth 624

TRIGger:A:I2S:WSELect:SLOPe 624

TRIGger:A:I2S:WSSLope 624

### TRIGger:A:SOURce <Source>

Sets the trigger source for the selected A trigger type.

<!-- 来源：RTM2_UserManual_en_10_files\part1434.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4 | EXTernanalog | LINE | SBUS1.. SBUS4 | D0..D15

<!-- 来源：RTM2_UserManual_en_10_files\part1435.htm -->

### CH1 | CH2 | CH3 | CH4

One of the input channels is the trigger source. Available chan- nels depend on the instrument type.

<!-- 来源：RTM2_UserManual_en_10_files\part1436.htm -->

### EXTernanalog

External trigger input on the rear panel

<!-- 来源：RTM2_UserManual_en_10_files\part1437.htm -->

### LINE

AC line for the edge trigger

<!-- 来源：RTM2_UserManual_en_10_files\part1438.htm -->

### SBUS1.. SBUS4

Serial buses 1 to 4

The UART, SPI, SSPI and audio protocols require two bus lines (bus 1 and 2 or bus 3 and 4). Bus 2 and/or bus 4 is not available if one of these protocols is selected.

<!-- 来源：RTM2_UserManual_en_10_files\part1439.htm -->

### D0..D15

If MSO option R&S RTM-B1 is installed, the digital channels D0 to D15 can be used as trigger sources for edge, width and pat- tern trigger.

### TRIGger:A:I2S:TYPE <TriggerMode> Specifies the trigger mode for audio signals.

<!-- 来源：RTM2_UserManual_en_10_files\part1440.htm -->

### Parameters:

<TriggerMode> DATA | WINDow | WSELect | ERRCondition

<!-- 来源：RTM2_UserManual_en_10_files\part1441.htm -->

### DATA

Triggers on a data word or a data range that occurs on a speci- fied channel. You can also trigger on an AND combination of data conditions on different channels.

Use the TRIG:A:I2S:CHANnel... commands to define the data condition.

```text
To set the logical combination to trigger on data words on differ- ent channels, use TRIGger:A:I2S:FUNCtion.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1442.htm -->

### WINDow

```text
Triggers if the data conditions are fulfilled at least for the given number of subsequent frames. Ues the data trigger commands to define the data condition. Use TRIGger:A:I2S:WINDow: LENGth to set the time limit.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1443.htm -->

### WSELect

Sets the edge of the word select signal as trigger condition. Use

```text
TRIGger:A:I2S:WSSLope to set the edge.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1444.htm -->

### ERRCondition

An error is detected when two consecutive frames have different length. The instrument triggers on the first clock edge after error detection.

### TRIGger:A:I2S:CHANnel:LEFT:CONDition <Comparison> TRIGger:A:I2S:CHANnel:RIGHt:CONDition <Comparison> TRIGger:A:I2S:CHANnel:TDM<n>:CONDition <Comparison>

Define the operators for comparison of the decoded data words with the specified data words on the specified channel.

<!-- 来源：RTM2_UserManual_en_10_files\part1445.htm -->

### Parameters:

<Comparison> OFF | EQUal | NEQual | GTHan | LTHan | INRange | OORange

INRange: in range OORange: out of range

<!-- 来源：RTM2_UserManual_en_10_files\part1446.htm -->

### OFF

No range is defined.

<!-- 来源：RTM2_UserManual_en_10_files\part1447.htm -->

### EQUal | NEQual | GTHan | LTHan

```text
Equal, not equal, greater than, less than. These conditions require one data word to be set with TRIGger:A:I2S: CHANnel:LEFT:DMIN, TRIGger:A:I2S:CHANnel:RIGHt: DMIN, or TRIGger:A:I2S:CHANnel:TDM<n>:DMIN.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1448.htm -->

### INRange | OORange

In range / Out of range: Set the minimum and maximum value of the range with TRIGger:A:I2S:CHANnel:LEFT:DMIN TRIG:A:I2S:CHANnel:...:DMIN and TRIGger:A:I2S: CHANnel:TDM<n>:DMAX TRIG:A:I2S:CHANnel:...:DMAX.

### TRIGger:A:I2S:CHANnel:LEFT:DMIN <MinimumValue> TRIGger:A:I2S:CHANnel:RIGHt:DMIN <MinimumValue> TRIGger:A:I2S:CHANnel:TDM<n>:DMIN <MinimumValue>

```text
Specifies the data word to be found, or the minimum value of a data range. The meaning depends on TRIGger:A:I2S:CHANnel:TDM<n>:CONDition.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1449.htm -->

### Parameters:

<MinimumValue> The data format is decimal. The maximum value is limited by the word length. Consider that audio words are signed numbers in 2's complement format. For example, an 8-bit data word has a value range from -128 to 127.

### TRIGger:A:I2S:CHANnel:LEFT:DMAX <MaximumValue> TRIGger:A:I2S:CHANnel:RIGHt:DMAX <MaximumValue> TRIGger:A:I2S:CHANnel:TDM<n>:DMAX <MaximumValue>

Specifies the maximum data value to be found.

```text
The settin gis valid if TRIGger:A:I2S:CHANnel:TDM<n>:CONDition is set to
INRange or OORange.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1450.htm -->

### Parameters:

<MaximumValue> The data format is decimal. The maximum value is limited by the word length. Consider that audio words are signed numbers in 2's complement format. For example, an 8-bit data word has a value range from -128 to 127.

### TRIGger:A:I2S:FUNCtion <Function>

Sets the logical combination to trigger on data words on different channels. The instru- ment triggers if all conditions are met inside one frame.

The setting is relevant for trigger types data and window.

<!-- 来源：RTM2_UserManual_en_10_files\part1451.htm -->

### Parameters:

<Function> AND | OR

AND: the instrument triggers if the data conditions on all selected channels are fulfilled.

OR: The instrument triggers if one of the specified data condi- tions is fulfilled.

### TRIGger:A:I2S:SOWords <WindowLength>

### TRIGger:A:I2S:WINDow:LENGth <WindowLength>

Sets the number of subsequent frames (audio samples) for which the data conditions are fulfilled.

<!-- 来源：RTM2_UserManual_en_10_files\part1452.htm -->

### Parameters:

<WindowLength> Number of frames

### TRIGger:A:I2S:WSELect:SLOPe <WordSelectSlope>

### TRIGger:A:I2S:WSSLope <WordSelectSlope>

```text
Sets the edge of the word select signal as trigger condition. Consider the polarity set- ting of the word select line ( BUS<b>:I2S:WSELect:POLarity ).
```

<!-- 来源：RTM2_UserManual_en_10_files\part1453.htm -->

### Parameters:

<WordSelectSlope> POS | NEG

POS: rising edge of the WS signal NEG: falling edge of the WS signal

### 18.13.8.3 Track of Audio Signals

BUS<b>:I2S:DISPlay 625

BUS<b>:I2S:TRACk:LEFT:POSition 625

BUS<b>:I2S:TRACk:LEFT:SCALe 626

BUS<b>:I2S:TRACk:RIGHt:POSition 626

BUS<b>:I2S:TRACk:RIGHt:SCALe 626

BUS<b>:I2S:TRACk:TDM<o>:STATe 627

BUS<b>:I2S:TRACk:TDM<o>:POSition 627

BUS<b>:I2S:TRACk:TDM<o>:SCALe 627

BUS<b>:I2S:TRACk:SET:DEFault 628

BUS<b>:I2S:TRACk:SET:SCReen 628

### BUS<b>:I2S:DISPlay <DisplayMode>

Defines how the decoded bus, the bit lines of the channels, and the track waveforms are displayed.

<!-- 来源：RTM2_UserManual_en_10_files\part1454.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1455.htm -->

### Parameters:

<DisplayMode> SEQuential | PARallel | STRack | PTRack | TRACk | SDSignal

<!-- 来源：RTM2_UserManual_en_10_files\part1456.htm -->

### SEQuential

The decoded data words of the channels are shown in sequen- tial, horizontal order.

<!-- 来源：RTM2_UserManual_en_10_files\part1457.htm -->

### PARallel

The decoded data words of the channels are arranged vertically.

<!-- 来源：RTM2_UserManual_en_10_files\part1458.htm -->

### STRack

Sequential order of data words, and tracks

<!-- 来源：RTM2_UserManual_en_10_files\part1459.htm -->

### PTRack

Parallel order of data words, and tracks

<!-- 来源：RTM2_UserManual_en_10_files\part1460.htm -->

### TRACk

Only tracks

<!-- 来源：RTM2_UserManual_en_10_files\part1461.htm -->

### SDSignal

Sequential order of data words, and bit lines of the channels

### BUS<b>:I2S:TRACk:LEFT:POSition <Position>

Sets the vertical positiion of the track waveform for the left channel in divisions. The command is relevant for I²S standard, left justified and right justified audio formats.

The virtual screen is available also for tracks. Thus, 20 divisions can be used to arrange all lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1462.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<o> 1

Not relevant

<!-- 来源：RTM2_UserManual_en_10_files\part1463.htm -->

### Parameters:

<Position> Range: -10 to 10

Increment: 0.05

<!-- 来源：RTM2_UserManual_en_10_files\part1464.htm -->

### BUS<b>:I2S:TRACk:LEFT:SCALe <Scale>

Sets the vertical scale of the track waveform for the left channel in bits per division.

<!-- 来源：RTM2_UserManual_en_10_files\part1465.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<o> 1

Not relevant

<!-- 来源：RTM2_UserManual_en_10_files\part1466.htm -->

### Parameters:

<Scale> Non-negative integer

Range: 2 to 4294967296 Increment: 2^n

### BUS<b>:I2S:TRACk:RIGHt:POSition <Position>

Sets the vertical positiion of the track waveform for the right channel in divisions. The command is relevant for I²S standard, left justified and right justified audio formats.

The virtual screen is available also for tracks. Thus, 20 divisions can be used to arrange all lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1467.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<o> 1

Not relevant

<!-- 来源：RTM2_UserManual_en_10_files\part1468.htm -->

### Parameters:

<Position> Range: -10 to 10

Increment: 0.05

<!-- 来源：RTM2_UserManual_en_10_files\part1469.htm -->

### BUS<b>:I2S:TRACk:RIGHt:SCALe <Scale>

Sets the vertical scale of the track waveform for the right channel in bits per division.

<!-- 来源：RTM2_UserManual_en_10_files\part1470.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<o> 1

Not relevant

<!-- 来源：RTM2_UserManual_en_10_files\part1471.htm -->

### Parameters:

<Scale> Non-negative integer

Range: 2 to 4294967296 Increment: 2^n

### BUS<b>:I2S:TRACk:TDM<o>:STATe <VisibleState>

Defines if the indicated track waveform is visible on the display.

<!-- 来源：RTM2_UserManual_en_10_files\part1472.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<o> 1..8

Selects the TDM channel to be tracked.

<!-- 来源：RTM2_UserManual_en_10_files\part1473.htm -->

### Parameters:

<VisibleState> ON | OFF

*RST: OFF

### BUS<b>:I2S:TRACk:TDM<o>:POSition <Position>

Sets the vertical positiion of the selected track waveform in divisions.

The virtual screen is available also for tracks. Thus, 20 divisions can be used to arrange all lines.

<!-- 来源：RTM2_UserManual_en_10_files\part1474.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<o> 1..8

Selects the TDM channel to be tracked.

<!-- 来源：RTM2_UserManual_en_10_files\part1475.htm -->

### Parameters:

<Position> Range: -10 to 10

Increment: 0.05

<!-- 来源：RTM2_UserManual_en_10_files\part1476.htm -->

### BUS<b>:I2S:TRACk:TDM<o>:SCALe <Scale>

Sets the vertical scale of the indicated track waveform in count of decimal values per division: Scale = Maximum data value / Number of used divisions.

For example, the maximum decimal value of an 8-bit data word is 256. If all 8 divisions of the display are used, the scale is 256 / 8 = 32 /div. If you want to display the track in 1/4 of the display height (2 divisions), the scale is 256 / 2= 128 /div. If the word length is 10 bit, and 4 division are used for the track, the scale is 1024 / 4 = 256/div.

The resulting zoom factor is Word length / Scale. In the first example, the zoom factor is 32 /32 = 1. In the second example, the zoom factor is 32 / 128 = 0.25. In the third example, it is 10 / 256 = 0.0390625.

<!-- 来源：RTM2_UserManual_en_10_files\part1477.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<o> 1..8

Selects the TDM channel to be tracked.

<!-- 来源：RTM2_UserManual_en_10_files\part1478.htm -->

### Parameters:

<Scale> Non-negative integer

Range: 2 to 4294967296 Increment: 2^n

<!-- 来源：RTM2_UserManual_en_10_files\part1479.htm -->

### BUS<b>:I2S:TRACk:SET:DEFault

Sets all selected tracks to the middle of the display and scales them to full height of the display (8 dovisions). The track waveforms overlap.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1480.htm -->

### BUS<b>:I2S:TRACk:SET:SCReen

Arranges the selected tracks vertically, one above the other. The track waveforms do not overlap.

### Usage: Event

### 18.13.8.4 Audio Decode Results

BUS<b>:I2S:FCOunt? 628

BUS<b>:I2S:FRAMe<n>:STATe? 628

BUS<b>:I2S:FRAMe<n>:STARt? 629

BUS<b>:I2S:FRAMe<n>:STOP? 629

BUS<b>:I2S:FRAMe<n>:LEFT:STATe? 630

BUS<b>:I2S:FRAMe<n>:RIGHt:STATe? 630

BUS<b>:I2S:FRAMe<n>:LEFT:VALue? 630

BUS<b>:I2S:FRAMe<n>:RIGHt:VALue? 630

BUS<b>:I2S:FRAMe<n>:TDM<o>:STATe? 630

BUS<b>:I2S:FRAMe<n>:TDM<o>:VALue? 631

<!-- 来源：RTM2_UserManual_en_10_files\part1481.htm -->

### BUS<b>:I2S:FCOunt?

Returns the number of acquired frames.

<!-- 来源：RTM2_UserManual_en_10_files\part1482.htm -->

### Suffix:

<b> 1. 4

Selects the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1483.htm -->

### Return values:

<FrameCount> Total number of decoded frames.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1484.htm -->

### BUS<b>:I2S:FRAMe<n>:STATe?

Returns the overall state of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1485.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1486.htm -->

### Return values:

<FrameState> ERRor | OK | INSufficient

ERRor: an error occured in the frame. OK: frame is valid.

INSufficient: frame is not completely contained in the acquisition. The acquired part of the frame is valid.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1487.htm -->

### BUS<b>:I2S:FRAMe<n>:STARt?

Returns the start time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1488.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1489.htm -->

### Return values:

<StartTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1490.htm -->

### BUS<b>:I2S:FRAMe<n>:STOP?

Returns the end time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1491.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1492.htm -->

### Return values:

<StopTime> Range: depends on sample rate, record length, and time

base

Increment: depends on the time base Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1493.htm -->

### BUS<b>:I2S:FRAMe<n>:LEFT:STATe? BUS<b>:I2S:FRAMe<n>:RIGHt:STATe?

Returns the state of the specified frame on the right or left audio channel.

<!-- 来源：RTM2_UserManual_en_10_files\part1494.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1495.htm -->

### Return values:

<State> ERRor | OK | INSufficient

ERRor: an error occured in the frame. OK: frame is valid.

INSufficient: frame is not completely contained in the acquisition. The acquired part of the frame is valid.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1496.htm -->

### BUS<b>:I2S:FRAMe<n>:LEFT:VALue? BUS<b>:I2S:FRAMe<n>:RIGHt:VALue?

Returns the data word of the specified frame on the right or left audio channel.

<!-- 来源：RTM2_UserManual_en_10_files\part1497.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<!-- 来源：RTM2_UserManual_en_10_files\part1498.htm -->

### Return values:

<Value> Signed decimal value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1499.htm -->

### BUS<b>:I2S:FRAMe<n>:TDM<o>:STATe?

Returns the state of the specified TDM channel and frame.

<!-- 来源：RTM2_UserManual_en_10_files\part1500.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<o> 1..8

Selects the TDM channel

<!-- 来源：RTM2_UserManual_en_10_files\part1501.htm -->

### Return values:

<State> ERRor | OK | INSufficient

ERRor: an error occured in the frame. OK: frame is valid.

INSufficient: frame is not completely contained in the acquisition. The acquired part of the frame is valid.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1502.htm -->

### BUS<b>:I2S:FRAMe<n>:TDM<o>:VALue?

Returns the data word of the specified frame on the selected TDM channel.

<!-- 来源：RTM2_UserManual_en_10_files\part1503.htm -->

### Suffix:

<b> 1..4

Selects the bus.

<n> *

Selects the frame (1...n).

<o> 1..8

Selects the TDM channel

<!-- 来源：RTM2_UserManual_en_10_files\part1504.htm -->

### Return values:

<Value> Signed decimal value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1505.htm -->

### 18.13.9 MIL_STD-1553 (Option R&S RTM-K6)

The MIL-STD-1553 defines the characteristics of a serial data bus originally designed for the use in the millitary avionics. Nowadays it is also used in spacecraft on-board data handling.

- MIL_STD-1553 Configuration 631

- MIL_STD-1553 Trigger 633

- MIL_STD-1553 Decode Results 640

- MIL-STD-1553 Search 646

### 18.13.9.1 MIL_STD-1553 Configuration

BUS<b>:MILStd:POLarity 631

BUS<b>:MILStd:RESPonsetime:MAXimum 632

BUS<b>:MILStd:SOURce 632

BUS<b>:MILStd:THReshold:HIGH 632

BUS<b>:MILStd:THReshold:LOW 632

### BUS<b>:MILStd:POLarity <Polarity> Sets the polarity of the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1506.htm -->

### Suffix:

<b> 1..4

<!-- 来源：RTM2_UserManual_en_10_files\part1507.htm -->

### Parameters:

<Polarity> POSitive | NEGative

*RST: POS

### BUS<b>:MILStd:RESPonsetime:MAXimum <MaximumTime> Sets a value for the maximum response time.

<!-- 来源：RTM2_UserManual_en_10_files\part1508.htm -->

### Suffix:

<b> 1..4

<!-- 来源：RTM2_UserManual_en_10_files\part1509.htm -->

### Parameters:

<MaximumTime>

### BUS<b>:MILStd:SOURce <Source> Sets the channel for the signal source.

<!-- 来源：RTM2_UserManual_en_10_files\part1510.htm -->

### Suffix:

<b> 1..4

<!-- 来源：RTM2_UserManual_en_10_files\part1511.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4

*RST: CH1

### BUS<b>:MILStd:THReshold:HIGH <UpperLevel> Sets the upper threshold level of the signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1512.htm -->

### Suffix:

<b> 1..4

<!-- 来源：RTM2_UserManual_en_10_files\part1513.htm -->

### Parameters:

<UpperLevel>

### BUS<b>:MILStd:THReshold:LOW <LowerLevel> Sets the lower threshold level of the signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1514.htm -->

### Suffix:

<b> 1..4

<!-- 来源：RTM2_UserManual_en_10_files\part1515.htm -->

### Parameters:

<LowerLevel>

### 18.13.9.2 MIL_STD-1553 Trigger

- General commands 633

- Error Trigger 633

- Command Word Trigger 634

- Satus Word Trigger 637

- Data Word Triggger 638

- Command and Data Trigger 639

### General commands TRIGger:A:MILStd:SYNC <SyncMode>

Triggers on a sync impulse. You can select to trigger on comando/status, on data or on either syncs.

<!-- 来源：RTM2_UserManual_en_10_files\part1516.htm -->

### Parameters:

<SyncMode> CSTatus | DATA | EITHer

*RST: CST

### TRIGger:A:MILStd:TYPE <TriggerMode> Selects the type of trigger.

<!-- 来源：RTM2_UserManual_en_10_files\part1517.htm -->

### Parameters:

<TriggerMode> SYNChronization | FRAME | ERRor | COMMand | STATus | DATA

*RST: SYNC

### TRIGger:A:MILStd:WORD <WordTyoe> Selects the word type to be triggered on.

<!-- 来源：RTM2_UserManual_en_10_files\part1518.htm -->

### Parameters:

<WordTyoe> COMMand | STATus | DATA | ALL

*RST: CST

<!-- 来源：RTM2_UserManual_en_10_files\part1519.htm -->

### Error Trigger

### TRIGger:A:MILStd:ERRor:MANChester <ErrorEnable>

Enables/disables triggering if there is an error in the Manchester coding of the signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1520.htm -->

### Parameters:

<ErrorEnable> ON | OFF

*RST: ON

### TRIGger:A:MILStd:ERRor:PARity <ErrorEnable> Enables/disables triggering when the parity is even.

<!-- 来源：RTM2_UserManual_en_10_files\part1521.htm -->

### Parameters:

<ErrorEnable> ON | OFF

*RST: ON

### TRIGger:A:MILStd:ERRor:SYNC <ErrorEnable>

Enables/disables triggering when a sync impulse doesn't fulfil the technical require- ments or when the transmission is not valid.

<!-- 来源：RTM2_UserManual_en_10_files\part1522.htm -->

### Parameters:

<ErrorEnable> ON | OFF

*RST: ON

### TRIGger:A:MILStd:ERRor:TIMeout <ErrorEnable>

Enables/ disables triggering when the timeout is out of the set range.

<!-- 来源：RTM2_UserManual_en_10_files\part1523.htm -->

### Parameters:

<ErrorEnable> ON | OFF

*RST: ON

<!-- 来源：RTM2_UserManual_en_10_files\part1524.htm -->

### Command Word Trigger

### TRIGger:A:MILStd:COMMand:TYPE <CommandType> Triggers on a command type.

<!-- 来源：RTM2_UserManual_en_10_files\part1525.htm -->

### Parameters:

<CommandType> AWORd | MCODe

<!-- 来源：RTM2_UserManual_en_10_files\part1526.htm -->

### AWORd

Triggers on an address or word count

<!-- 来源：RTM2_UserManual_en_10_files\part1527.htm -->

### MCODe

Triggers on a mode code

*RST: AWOR

### TRIGger:A:MILStd:MCODe:CODE <ModeCode> Sets a function for the mode code to be triggered on.

<!-- 来源：RTM2_UserManual_en_10_files\part1528.htm -->

### Parameters:

<ModeCode> DBControl | TSYNchronize | TSTatus | ISELftest | TSHutdown | OTSHutdown | ITERminal | OITerminal | RESet | VECTor | RSYNchronize | TLAStcmmand | BITWord | STSHutdown | OSTShutdown | ANY

DBControl: dynamic bus control TSYNchronize: synchronize without data TSTatus: transmit status word

ISELftest: initiate self test TSHutdown: transmitter shutdown

OTSHutdown: override transmitter shutdown ITERminal: inhibit terminal flag

OITerminal: override inhibit terminal flag RESet: reset remote terminal

VECTor: transmit vector word RSYNchronize: synchronize with data TLAStcmmand: transmit last command word BITWord: transmit bit word

STSHutdown: selected transmitter shutdown OSTShutdown: override selected transmitter shutdown

*RST: ANY

### TRIGger:A:MILStd:MCODe:VALue <ModeCode> Sets the value of the mode code to be triggered on.

<!-- 来源：RTM2_UserManual_en_10_files\part1529.htm -->

### Parameters:

<ModeCode>

<!-- 来源：RTM2_UserManual_en_10_files\part1530.htm -->

### TRIGger:A:MILStd:RTADdress:CONDition <Compare>

For the RT address, sets the triggering condition for the comparison of the decoded value to the defined range.

<!-- 来源：RTM2_UserManual_en_10_files\part1531.htm -->

### Parameters:

<Compare> EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### TRIGger:A:MILStd:RTADdress:MAXimum <AddressMaximum> Sets the maximum RT address.

<!-- 来源：RTM2_UserManual_en_10_files\part1532.htm -->

### Parameters:

<AddressMaximum> 01X-string

### TRIGger:A:MILStd:RTADdress:MINimum <AddressMinimum> Sets the minimum RT address.

<!-- 来源：RTM2_UserManual_en_10_files\part1533.htm -->

### Parameters:

<AddressMinimum> 01X-string

<!-- 来源：RTM2_UserManual_en_10_files\part1534.htm -->

### TRIGger:A:MILStd:SADDress:CONDition <Compare>

For the subaddress, sets the triggering condition for the comparison of the decoded value to the defined range.

<!-- 来源：RTM2_UserManual_en_10_files\part1535.htm -->

### Parameters:

<Compare> EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### TRIGger:A:MILStd:SADDress:MAXimum <AddressMaximum> Sets the maximum subaddress.

<!-- 来源：RTM2_UserManual_en_10_files\part1536.htm -->

### Parameters:

<AddressMaximum> 01X-string

### TRIGger:A:MILStd:SADDress:MCADdress <ModeCodeAddress>

```text
Triggers on the value of the subaddress, if TRIGger:A:MILStd:COMMand:TYPE is set to mode code.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1537.htm -->

### Parameters:

<ModeCodeAddress> A0 | A31 | EITHer

*RST: EITH

### TRIGger:A:MILStd:SADDress:MINimum <AddressMinimum> Sets the minimum subaddress.

<!-- 来源：RTM2_UserManual_en_10_files\part1538.htm -->

### Parameters:

<AddressMinimum> 01X-string

### TRIGger:A:MILStd:TRMode <DataDirection> Triggers on a transmission mode.

<!-- 来源：RTM2_UserManual_en_10_files\part1539.htm -->

### Parameters:

<DataDirection> TRANsmit | RECeive | EITHer

*RST: EITH

### TRIGger:A:MILStd:WCOunt:CONDition <Compare>

For a command word, triggers on a word comparison condition.

<!-- 来源：RTM2_UserManual_en_10_files\part1540.htm -->

### Parameters:

<Compare> EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### TRIGger:A:MILStd:WCOunt:MAXimum <WordCountMaximum> For a command word, triggers on a maximum word count.

<!-- 来源：RTM2_UserManual_en_10_files\part1541.htm -->

### Parameters:

<WordCountMaximum>

### TRIGger:A:MILStd:WCOunt:MINimum <WordCountMinimum> For a command word, triggers on a minimum word count.

<!-- 来源：RTM2_UserManual_en_10_files\part1542.htm -->

### Parameters:

<WordCountMinimum>

<!-- 来源：RTM2_UserManual_en_10_files\part1543.htm -->

### Satus Word Trigger TRIGger:A:MILStd:STATus:BCReceived <StatusBit>

Triggers on the state of the broadcast command received bit of the status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1544.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### TRIGger:A:MILStd:STATus:BUSY <StatusBit> Triggers on the state of the busy bit of the status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1545.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### TRIGger:A:MILStd:STATus:DBCaccept <StatusBit>

Triggers on the state of the dynamic bus control accept bit of the status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1546.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### TRIGger:A:MILStd:STATus:INSTrument <StatusBit>

Triggers on the state of the instrumentation bit of the status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1547.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### TRIGger:A:MILStd:STATus:MERRor <StatusBit>

Triggers on the state of the message error bit of the status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1548.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### TRIGger:A:MILStd:STATus:SREQuest <StatusBit>

Triggers on the state of the service request bit of the status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1549.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### TRIGger:A:MILStd:STATus:SUBSystem <StatusBit>

Triggers on the state of the subsystem flag bit of the status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1550.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### TRIGger:A:MILStd:STATus:TERMinal <StatusBit>

Triggers on the state of the terminal flag bit of the status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1551.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

<!-- 来源：RTM2_UserManual_en_10_files\part1552.htm -->

### Data Word Triggger TRIGger:A:MILStd:DATA:CONDition <Compare>

For a data word, sets the triggering condition for the comparison of the decoded value to the defined range.

<!-- 来源：RTM2_UserManual_en_10_files\part1553.htm -->

### Parameters:

<Compare> EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### TRIGger:A:MILStd:DATA:MAXimum <DataMinimum> For a data word, sets the maximum data value.

<!-- 来源：RTM2_UserManual_en_10_files\part1554.htm -->

### Parameters:

<DataMinimum> 01X-string

### TRIGger:A:MILStd:DATA:MINimum <DataMinimum> For a data word, sets the minimum data value.

<!-- 来源：RTM2_UserManual_en_10_files\part1555.htm -->

### Parameters:

<DataMinimum> 01X-string

### TRIGger:A:MILStd:DATA:OFFSet <DataOffset>

For a data word sets the word offset to be triggered on.

<!-- 来源：RTM2_UserManual_en_10_files\part1556.htm -->

### Parameters:

<DataOffset> *RST: 0

### TRIGger:A:MILStd:DATA:OFFSet:CONDition <DataOffset>

For a data offset, sets the triggering condition for the comparison of the decoded value to the defined range.

<!-- 来源：RTM2_UserManual_en_10_files\part1557.htm -->

### Parameters:

<DataOffset> EQUal | NEQual | GTHan | GEQual | LEQual | LTHan

*RST: 0

### TRIGger:A:MILStd:DATA:WORDs <DataWords>

For a data word sets the number of words to be triggered on.

<!-- 来源：RTM2_UserManual_en_10_files\part1558.htm -->

### Parameters:

<DataWords> *RST: 1

<!-- 来源：RTM2_UserManual_en_10_files\part1559.htm -->

### Command and Data Trigger

### TRIGger:A:MILStd:TTYPe <TransmissionType> Sets the transmission type to be triggered on.

<!-- 来源：RTM2_UserManual_en_10_files\part1560.htm -->

### Parameters:

<TransmissionType> BCRT | RTBC | RTRT | MCData

<!-- 来源：RTM2_UserManual_en_10_files\part1561.htm -->

### BCRT

bus controller to remote terminal transmission

<!-- 来源：RTM2_UserManual_en_10_files\part1562.htm -->

### RTBC

remote terminal to bus controller transmission

<!-- 来源：RTM2_UserManual_en_10_files\part1563.htm -->

### RTRT

remote terminal to remote terminal transmission

<!-- 来源：RTM2_UserManual_en_10_files\part1564.htm -->

### MCData

mode code data

*RST: BCRT

### 18.13.9.3 MIL_STD-1553 Decode Results

BUS<b>:MILStd:WCOunt? 640

BUS<b>:MILStd:WORD<n>:COMMand:MCODe:CODE? 641

BUS<b>:MILStd:WORD<n>:COMMand:MCODe:VALue? 641

BUS<b>:MILStd:WORD<n>:COMMand:RTADdress? 641

BUS<b>:MILStd:WORD<n>:COMMand:SADDress? 641

BUS<b>:MILStd:WORD<n>:COMMand:WCOunt? 642

BUS<b>:MILStd:WORD<n>:DATA? 642

BUS<b>:MILStd:WORD<n>:IMGTime? 642

BUS<b>:MILStd:WORD<n>:PARity? 642

BUS<b>:MILStd:WORD<n>:RTIMe? 643

BUS<b>:MILStd:WORD<n>:STARt? 643

BUS<b>:MILStd:WORD<n>:STATus? 643

BUS<b>:MILStd:WORD<n>:STATus:BCReceived? 643

BUS<b>:MILStd:WORD<n>:STATus:BUSY? 644

BUS<b>:MILStd:WORD<n>:STATus:DBCaccept? 644

BUS<b>:MILStd:WORD<n>:STATus:INSTrument? 644

BUS<b>:MILStd:WORD<n>:STATus:MERRor? 644

BUS<b>:MILStd:WORD<n>:STATus:RTADdress? 645

BUS<b>:MILStd:WORD<n>:STATus:SREQuest? 645

BUS<b>:MILStd:WORD<n>:STATus:SUBSystem? 645

BUS<b>:MILStd:WORD<n>:STATus:TERMinal? 645

BUS<b>:MILStd:WORD<n>:STOP? 646

BUS<b>:MILStd:WORD<n>:TRMode? 646

BUS<b>:MILStd:WORD<n>:TYPE? 646

<!-- 来源：RTM2_UserManual_en_10_files\part1565.htm -->

### BUS<b>:MILStd:WCOunt?

Returns the number of received words.

<!-- 来源：RTM2_UserManual_en_10_files\part1566.htm -->

### Suffix:

<b> 1. 4

<!-- 来源：RTM2_UserManual_en_10_files\part1567.htm -->

### Return values:

<WordCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1568.htm -->

### BUS<b>:MILStd:WORD<n>:COMMand:MCODe:CODE?

For the sepcified command word, returns the type of mode code.

<!-- 来源：RTM2_UserManual_en_10_files\part1569.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1570.htm -->

### Return values:

<ModeCode> DBControl | TSYNchronize | TSTatus | ISELftest | TSHutdown | OTSHutdown | ITERminal | OITerminal | RESet | VECTor | RSYNchronize | TLAStcmmand | BITWord | STSHutdown | OSTShutdown

*RST: ANY

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1571.htm -->

### BUS<b>:MILStd:WORD<n>:COMMand:MCODe:VALue?

For the specified command word, returns the value of the mode code.

<!-- 来源：RTM2_UserManual_en_10_files\part1572.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1573.htm -->

### Return values:

<ModeCodeValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1574.htm -->

### BUS<b>:MILStd:WORD<n>:COMMand:RTADdress?

Returns the RT address of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1575.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1576.htm -->

### Return values:

<RTAddress>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1577.htm -->

### BUS<b>:MILStd:WORD<n>:COMMand:SADDress?

For a command word, returns the subaddress of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1578.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1579.htm -->

### Return values:

<SubAddress>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1580.htm -->

### BUS<b>:MILStd:WORD<n>:COMMand:WCOunt?

For a command word, returns the word count.

<!-- 来源：RTM2_UserManual_en_10_files\part1581.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1582.htm -->

### Return values:

<WordCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1583.htm -->

### BUS<b>:MILStd:WORD<n>:DATA?

Returns the value of the specified data word.

<!-- 来源：RTM2_UserManual_en_10_files\part1584.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1585.htm -->

### Return values:

<DataValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1586.htm -->

### BUS<b>:MILStd:WORD<n>:IMGTime?

Returns the intermessage gate time of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1587.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1588.htm -->

### Return values:

<InterMessageGapTime>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1589.htm -->

### BUS<b>:MILStd:WORD<n>:PARity?

Returns the parity of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1590.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1591.htm -->

### Return values:

<ParityValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1592.htm -->

### BUS<b>:MILStd:WORD<n>:RTIMe?

Return the response time of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1593.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1594.htm -->

### Return values:

<ResponseTime>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1595.htm -->

### BUS<b>:MILStd:WORD<n>:STARt?

Returns the start time of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1596.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1597.htm -->

### Return values:

<StartTime>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1598.htm -->

### BUS<b>:MILStd:WORD<n>:STATus?

For a status word returns the value and if there are errors.

<!-- 来源：RTM2_UserManual_en_10_files\part1599.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1600.htm -->

### Parameters:

<WordState> OK | INSufficient | PERRor | MERRor | TERRor | SERRor

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1601.htm -->

### BUS<b>:MILStd:WORD<n>:STATus:BCReceived?

Returns the state of the broadcast command received bit of the specified status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1602.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1603.htm -->

### Return values:

<BitState>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1604.htm -->

### BUS<b>:MILStd:WORD<n>:STATus:BUSY?

Returns the state of the busy bit of the specified status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1605.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1606.htm -->

### Return values:

<BitState>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1607.htm -->

### BUS<b>:MILStd:WORD<n>:STATus:DBCaccept?

Returns the state of the dynamic bus control bit of the specified status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1608.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1609.htm -->

### Return values:

<BitState>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1610.htm -->

### BUS<b>:MILStd:WORD<n>:STATus:INSTrument?

Returns the state of the instrumentation bit of the specified status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1611.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1612.htm -->

### Return values:

<BitState>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1613.htm -->

### BUS<b>:MILStd:WORD<n>:STATus:MERRor?

Returns the state of the message error bit of the specified status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1614.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1615.htm -->

### Return values:

<BitState>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1616.htm -->

### BUS<b>:MILStd:WORD<n>:STATus:RTADdress?

Returns the RT address of the specified status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1617.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1618.htm -->

### Return values:

<RTAddress>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1619.htm -->

### BUS<b>:MILStd:WORD<n>:STATus:SREQuest?

Returns the state of the service request bit of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1620.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1621.htm -->

### Return values:

<BitState>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1622.htm -->

### BUS<b>:MILStd:WORD<n>:STATus:SUBSystem?

Returns the state of the subsystem bit of the specified status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1623.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1624.htm -->

### Return values:

<BitState>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1625.htm -->

### BUS<b>:MILStd:WORD<n>:STATus:TERMinal?

Returns the state of the terminal flag bit of the specified status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1626.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1627.htm -->

### Return values:

<BitState>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1628.htm -->

### BUS<b>:MILStd:WORD<n>:STOP?

Returns the stop time of the word of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1629.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1630.htm -->

### Return values:

<StopTime>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1631.htm -->

### BUS<b>:MILStd:WORD<n>:TRMode?

Returns the transmission direction of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1632.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1633.htm -->

### Return values:

<DataDirection> TRANsmit | RECeive

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1634.htm -->

### BUS<b>:MILStd:WORD<n>:TYPE?

Returns the type of word of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1635.htm -->

### Suffix:

<b> 1..4

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part1636.htm -->

### Return values:

<WordType> COMMand | STATus | DATA | CMCode

### Usage: Query only

### 18.13.9.4 MIL-STD-1553 Search

SEARch:PROTocol:MILStd:CONDition 647

SEARch:PROTocol:MILStd:DATA:COMPare 647

SEARch:PROTocol:MILStd:DATA:CONDition 648

SEARch:PROTocol:MILStd:DATA:MAXimum 648

SEARch:PROTocol:MILStd:DATA:MINimum 648

SEARch:PROTocol:MILStd:DATA:OFFSet 648

SEARch:PROTocol:MILStd:DATA:WORDs 648

SEARch:PROTocol:MILStd:ERRor 648

SEARch:PROTocol:MILStd:MCODe 648

SEARch:PROTocol:MILStd:RTADdress:COMPare 649

SEARch:PROTocol:MILStd:RTADdress:CONDition 649

SEARch:PROTocol:MILStd:RTADdress:MAXimum 649

SEARch:PROTocol:MILStd:RTADdress:MINimum 649

SEARch:PROTocol:MILStd:SADDress:COMPare 649

SEARch:PROTocol:MILStd:SADDress:CONDition 650

SEARch:PROTocol:MILStd:SADDress:MAXimum 650

SEARch:PROTocol:MILStd:SADDress:MCADdress 650

SEARch:PROTocol:MILStd:SADDress:MINimum 650

SEARch:PROTocol:MILStd:STATus:BCReceived 650

SEARch:PROTocol:MILStd:STATus:BUSY 650

SEARch:PROTocol:MILStd:STATus:DBCaccept 651

SEARch:PROTocol:MILStd:STATus:INSTrument 651

SEARch:PROTocol:MILStd:STATus:MERRor 651

SEARch:PROTocol:MILStd:STATus:SREQuest 651

SEARch:PROTocol:MILStd:STATus:SUBSystem 651

SEARch:PROTocol:MILStd:STATus:TERMinal 651

SEARch:PROTocol:MILStd:TRMode 652

SEARch:PROTocol:MILStd:TTYPe 652

SEARch:PROTocol:MILStd:WSTart 652

SEARch:PROTocol:MILStd:WCOunt:COMPare 652

SEARch:PROTocol:MILStd:WCOunt:CONDition 652

SEARch:PROTocol:MILStd:WCOunt:MAXimum 653

SEARch:PROTocol:MILStd:WCOunt:MINimum 653

### SEARch:PROTocol:MILStd:CONDition <SearchCondition> Selects the condition to be searched for.

<!-- 来源：RTM2_UserManual_en_10_files\part1637.htm -->

### Parameters:

<SearchCondition> WSTart | ERRor | STATus | DATA | COMMand | MCODe | CDATa

*RST: WST

### SEARch:PROTocol:MILStd:DATA:COMPare <Comparison> For a data word, searches for a comparison condition.

<!-- 来源：RTM2_UserManual_en_10_files\part1638.htm -->

### Parameters:

<Comparison> OFF | EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### SEARch:PROTocol:MILStd:DATA:CONDition <Comparison> For a data word, searches for a comparison condition.

<!-- 来源：RTM2_UserManual_en_10_files\part1639.htm -->

### Parameters:

<Comparison> OFF | EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### SEARch:PROTocol:MILStd:DATA:MAXimum <DataMaximum> For a data word, searches for a maximum value.

<!-- 来源：RTM2_UserManual_en_10_files\part1640.htm -->

### Parameters:

<DataMaximum> 01X-string

### SEARch:PROTocol:MILStd:DATA:MINimum <DataMinimum> For a data word, searches for a minimum value.

<!-- 来源：RTM2_UserManual_en_10_files\part1641.htm -->

### Parameters:

<DataMinimum> 01X-string

### SEARch:PROTocol:MILStd:DATA:OFFSet <DataOffset> For a data word, searches for a data offset.

<!-- 来源：RTM2_UserManual_en_10_files\part1642.htm -->

### Parameters:

<DataOffset> *RST: 0

### SEARch:PROTocol:MILStd:DATA:WORDs <DataWords> For a data word, searches for a number of words.

<!-- 来源：RTM2_UserManual_en_10_files\part1643.htm -->

### Parameters:

<DataWords> *RST: 1

### SEARch:PROTocol:MILStd:ERRor <ErrorType> Selects the error type to be searched for.

<!-- 来源：RTM2_UserManual_en_10_files\part1644.htm -->

### Parameters:

<ErrorType> SYNChronization | PARity | TIMeout | MANChester | ANY

### SEARch:PROTocol:MILStd:MCODe <ModeCode> Searches for a mode code type.

<!-- 来源：RTM2_UserManual_en_10_files\part1645.htm -->

### Parameters:

<ModeCode> DBControl | TSYNchronize | TSTatus | ISELftest | TSHutdown | OTSHutdown | ITERminal | OITerminal | RESet | VECTor | RSYNchronize | TLAStcmmand | BITWord | STSHutdown | OSTShutdown | ANY

*RST: ANY

### SEARch:PROTocol:MILStd:RTADdress:COMPare <Comparison> For an RT address, searches for a comparison condition.

<!-- 来源：RTM2_UserManual_en_10_files\part1646.htm -->

### Parameters:

<Comparison> OFF | EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### SEARch:PROTocol:MILStd:RTADdress:CONDition <Comparison> For an RT address, searches for a comparison condition.

<!-- 来源：RTM2_UserManual_en_10_files\part1647.htm -->

### Parameters:

<Comparison> OFF | EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### SEARch:PROTocol:MILStd:RTADdress:MAXimum <AddressMaximum> For an RT address, searches for the maximum address.

<!-- 来源：RTM2_UserManual_en_10_files\part1648.htm -->

### Parameters:

<AddressMaximum> 01X-string

### SEARch:PROTocol:MILStd:RTADdress:MINimum <AddressMinimum> For an RT address, searches for the minimum address.

<!-- 来源：RTM2_UserManual_en_10_files\part1649.htm -->

### Parameters:

<AddressMinimum> 01X-string

### SEARch:PROTocol:MILStd:SADDress:COMPare <Comparison> For a subaddress, searches for a comparison condition.

<!-- 来源：RTM2_UserManual_en_10_files\part1650.htm -->

### Parameters:

<Comparison> OFF | EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### SEARch:PROTocol:MILStd:SADDress:CONDition <Comparison> For a subaddress, searches for a comparison condition.

<!-- 来源：RTM2_UserManual_en_10_files\part1651.htm -->

### Parameters:

<Comparison> OFF | EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### SEARch:PROTocol:MILStd:SADDress:MAXimum <AddressMaximum> For a subaddress, searches for the maximum address.

<!-- 来源：RTM2_UserManual_en_10_files\part1652.htm -->

### Parameters:

<AddressMaximum> 01X-string

### SEARch:PROTocol:MILStd:SADDress:MCADdress <ModeCodeAddress> Searches for a mode code address.

<!-- 来源：RTM2_UserManual_en_10_files\part1653.htm -->

### Parameters:

<ModeCodeAddress> A0 | A31 | EITHer

*RST: EITH

### SEARch:PROTocol:MILStd:SADDress:MINimum <AddressMinimum> For a subaddress, searches for the minimum address.

<!-- 来源：RTM2_UserManual_en_10_files\part1654.htm -->

### Parameters:

<AddressMinimum> 01X-string

### SEARch:PROTocol:MILStd:STATus:BCReceived <StatusBit> Searches for a broadcast received bit of a status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1655.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### SEARch:PROTocol:MILStd:STATus:BUSY <StatusBit> Searches for a busy bit of a status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1656.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### SEARch:PROTocol:MILStd:STATus:DBCaccept <StatusBit> Searches for a dynamic bus control accept bit of a status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1657.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### SEARch:PROTocol:MILStd:STATus:INSTrument <StatusBit> Searches for an instrument bit of a status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1658.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### SEARch:PROTocol:MILStd:STATus:MERRor <StatusBit> Searches for a message error bit of a status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1659.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### SEARch:PROTocol:MILStd:STATus:SREQuest <StatusBit> Searches for a service request bit of a status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1660.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### SEARch:PROTocol:MILStd:STATus:SUBSystem <StatusBit> Searches for a subsystem bit of a status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1661.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### SEARch:PROTocol:MILStd:STATus:TERMinal <StatusBit> Searches for a terminal bit of a status word.

<!-- 来源：RTM2_UserManual_en_10_files\part1662.htm -->

### Parameters:

<StatusBit> 0 | 1 | X

*RST: X

### SEARch:PROTocol:MILStd:TRMode <DataDirection> Selects the transmission mode to be searched for.

<!-- 来源：RTM2_UserManual_en_10_files\part1663.htm -->

### Parameters:

<DataDirection> TRANsmit | RECeive | EITHer

*RST: EITH

### SEARch:PROTocol:MILStd:TTYPe <TransmissionType> Selects the transmission type to be searched for.

<!-- 来源：RTM2_UserManual_en_10_files\part1664.htm -->

### Parameters:

<TransmissionType> BCRT | RTBC | RTRT | MCData

<!-- 来源：RTM2_UserManual_en_10_files\part1665.htm -->

### BCRT

bus controller to remote terminal transmission

<!-- 来源：RTM2_UserManual_en_10_files\part1666.htm -->

### RTBC

remote terminal to bus controller transmission

<!-- 来源：RTM2_UserManual_en_10_files\part1667.htm -->

### RTRT

remote terminal to remote terminal transmission

<!-- 来源：RTM2_UserManual_en_10_files\part1668.htm -->

### MCData

mde code with data

*RST: BCRT

### SEARch:PROTocol:MILStd:WSTart <WordStart> Selects a word start to be searched for.

<!-- 来源：RTM2_UserManual_en_10_files\part1669.htm -->

### Parameters:

<WordStart> COMMand | STATus | DATA

*RST: COMM

### SEARch:PROTocol:MILStd:WCOunt:COMPare <Compare> Searches for a comparison condition of the word count.

<!-- 来源：RTM2_UserManual_en_10_files\part1670.htm -->

### Parameters:

<Compare> OFF | EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### SEARch:PROTocol:MILStd:WCOunt:CONDition <Compare> Searches for a comparison condition of the word count.

<!-- 来源：RTM2_UserManual_en_10_files\part1671.htm -->

### Parameters:

<Compare> OFF | EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

*RST: OFF

### SEARch:PROTocol:MILStd:WCOunt:MAXimum <WordCountMaximum> Searches for the maximum word count.

<!-- 来源：RTM2_UserManual_en_10_files\part1672.htm -->

### Parameters:

<WordCountMaximum>

### SEARch:PROTocol:MILStd:WCOunt:MINimum <WordCountMinimum> Searches for the minimum word count.

<!-- 来源：RTM2_UserManual_en_10_files\part1673.htm -->

### Parameters:

<WordCountMinimum>

<!-- 来源：RTM2_UserManual_en_10_files\part1674.htm -->

### 18.13.10 ARINC 429 (Option R&S RTM-K7)

### 18.13.10.1 ARINC 429 - Configuration

BUS<b>:ARINc:BRMode 653

BUS<b>:ARINc:BRValue 653

BUS<b>:ARINc:POLarity 654

BUS<b>:ARINc:SOURce 654

BUS<b>:ARINc:THReshold:HIGH 654

BUS<b>:ARINc:THReshold:LOW 654

### BUS<b>:ARINc:BRMode <BitRateMode>

Sets the bit rate mode to high speed, low speed or a user defined mode.

If USER mode is selected, you can set the bit rate value with BUS<b>:ARINc: BRValue.

<!-- 来源：RTM2_UserManual_en_10_files\part1675.htm -->

### Parameters:

<BitRateMode> HIGH | LOW | USER

### BUS<b>:ARINc:BRValue <BitRateValue> Sets the number of transmitted bits per second.

If you set a value with this command, the mode of BUS<b>:ARINc:BRMode will be automatically set to USER.

<!-- 来源：RTM2_UserManual_en_10_files\part1676.htm -->

### Parameters:

<BitRateValue>

### BUS<b>:ARINc:POLarity <Polarity>

Sets the wire on which the bus signal is measured.

<!-- 来源：RTM2_UserManual_en_10_files\part1677.htm -->

### Parameters:

<Polarity> ALEG | BLEG | NORMal | INVerted

*RST: ALEG

### BUS<b>:ARINc:SOURce <Source> Sets the channel for the signal source.

<!-- 来源：RTM2_UserManual_en_10_files\part1678.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4

*RST: CH1

### BUS<b>:ARINc:THReshold:HIGH <ThresholdHigh> Sets the high threshold level of the signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1679.htm -->

### Parameters:

<ThresholdHigh>

### BUS<b>:ARINc:THReshold:LOW <ThresholdLow> Sets the low threshold level of the signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1680.htm -->

### Parameters:

<ThresholdLow>

### 18.13.10.2 ARINC 429 - Trigger

TRIGger:A:ARINc:DATA:CONDition 655

TRIGger:A:ARINc:DATA:MAXimum 655

TRIGger:A:ARINc:DATA:MINimum 655

TRIGger:A:ARINc:DATA:OFFSet 655

TRIGger:A:ARINc:DATA:SIZE 656

TRIGger:A:ARINc:ERRor:CODing 656

TRIGger:A:ARINc:ERRor:GAP 656

TRIGger:A:ARINc:ERRor:PARity 656

TRIGger:A:ARINc:FORMat 656

TRIGger:A:ARINc:LABel:CONDition 656

TRIGger:A:ARINc:LABel:MAXimum 657

TRIGger:A:ARINc:LABel:MINimum 657

TRIGger:A:ARINc:SDI 657

TRIGger:A:ARINc:SSM 657

TRIGger:A:ARINc:TTIMe:CONDition 658

TRIGger:A:ARINc:TTIMe:MAXimum 658

TRIGger:A:ARINc:TTIMe:MINimum 658

TRIGger:A:ARINc:TYPE 658

TRIGger:A:ARINc:WORD:TYPE 658

### TRIGger:A:ARINc:DATA:CONDition <Compare>

Define the operators for comparison of the decoded data condition with the specified data.

<!-- 来源：RTM2_UserManual_en_10_files\part1681.htm -->

### Parameters:

<Compare> EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

INRange: in range OORange: out of range

<!-- 来源：RTM2_UserManual_en_10_files\part1682.htm -->

### OFF

No range is defined.

<!-- 来源：RTM2_UserManual_en_10_files\part1683.htm -->

### EQUal | NEQual | GTHan | LTHan

```text
Equal, not equal, greater than, less than. These conditions require one data word to be set with TRIGger:A:ARINc: DATA:MINimum.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1684.htm -->

### INRange | OORange

```text
In range / Out of range: Set the minimum and maximum value of the range with TRIGger:A:ARINc:DATA:MINimum and TRIGger:A:ARINc:DATA:MAXimum.
```

### TRIGger:A:ARINc:DATA:MAXimum <DataMaximum>

Specifies the maximum value of the data if TRIGger:A:ARINc:DATA:CONDition is set to INRange or OORange.

<!-- 来源：RTM2_UserManual_en_10_files\part1685.htm -->

### Parameters:

<DataMaximum> 01X-string

### TRIGger:A:ARINc:DATA:MINimum <DataMinimum> Sets the minimum condition for the data.

<!-- 来源：RTM2_UserManual_en_10_files\part1686.htm -->

### Parameters:

<DataMinimum> 01X-string

### TRIGger:A:ARINc:DATA:OFFSet <DataOffset> Sets a data offset.

<!-- 来源：RTM2_UserManual_en_10_files\part1687.htm -->

### Parameters:

<DataOffset>

### TRIGger:A:ARINc:DATA:SIZE <DataSize>

Sets the data size.

<!-- 来源：RTM2_UserManual_en_10_files\part1688.htm -->

### Parameters:

<DataSize>

### TRIGger:A:ARINc:ERRor:CODing <ErrorEnable> Enables triggering when a coding error occurs.

<!-- 来源：RTM2_UserManual_en_10_files\part1689.htm -->

### Parameters:

<ErrorEnable> ON | OFF

*RST: ON

### TRIGger:A:ARINc:ERRor:GAP <ErrorEnable> Enables triggering when a gap error occurs.

<!-- 来源：RTM2_UserManual_en_10_files\part1690.htm -->

### Parameters:

<ErrorEnable> ON | OFF

*RST: ON

### TRIGger:A:ARINc:ERRor:PARity <ErrorEnable> Enables triggering when a parity error occurs.

<!-- 来源：RTM2_UserManual_en_10_files\part1691.htm -->

### Parameters:

<ErrorEnable> ON | OFF

*RST: ON

### TRIGger:A:ARINc:FORMat <DataFormat>

Sets the the transmission format to be triggered on.

<!-- 来源：RTM2_UserManual_en_10_files\part1692.htm -->

### Parameters:

<DataFormat> DATA | DSSM | DSDI | DSSSm

```text
DSSM: SSM+Data
DSDI: SDI+Data
DSSSm: SSM+Data +SDI
```

### TRIGger:A:ARINc:LABel:CONDition <Compare>

Define the operators for comparison of the decoded label condition with the specified label.

<!-- 来源：RTM2_UserManual_en_10_files\part1693.htm -->

### Parameters:

<Compare> EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

```text
INRange: in range
OORange: out of range
```

<!-- 来源：RTM2_UserManual_en_10_files\part1694.htm -->

### OFF

No range is defined.

<!-- 来源：RTM2_UserManual_en_10_files\part1695.htm -->

### EQUal | NEQual | GTHan | LTHan

```text
Equal, not equal, greater than, less than. These conditions require one label to be set with TRIGger:A:ARINc:LABel: MINimum.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1696.htm -->

### INRange | OORange

```text
In range / Out of range: Set the minimum and maximum value of the range with TRIGger:A:ARINc:LABel:MINimum and TRIGger:A:ARINc:LABel:MAXimum.
```

### TRIGger:A:ARINc:LABel:MAXimum <LabelMaximum>

Specifies the maximum value of the label if TRIGger:A:ARINc:LABel:CONDition

is set to INRange or OORange.

<!-- 来源：RTM2_UserManual_en_10_files\part1697.htm -->

### Parameters:

<LabelMaximum> 01X-string

### TRIGger:A:ARINc:LABel:MINimum <LabelMinimum> Sets the minimum value of the label to be triggerd on.

<!-- 来源：RTM2_UserManual_en_10_files\part1698.htm -->

### Parameters:

<LabelMinimum> 01X-string

### TRIGger:A:ARINc:SDI <SDIvalue>

Sets the source/destination identifier (SDI) bits to be triggered on.

<!-- 来源：RTM2_UserManual_en_10_files\part1699.htm -->

### Parameters:

<SDIvalue> ANY | S00 | S01 | S10 | S11

### TRIGger:A:ARINc:SSM <SSMvalue>

Sets the sign/status matrix (SSM) bits to be triggered on.

<!-- 来源：RTM2_UserManual_en_10_files\part1700.htm -->

### Parameters:

<SSMvalue> ANY | S00 | S01 | S10 | S11

### TRIGger:A:ARINc:TTIMe:CONDition <Compare>

Define the operators for comparison of the decoded transmission time condition with the specified data.

<!-- 来源：RTM2_UserManual_en_10_files\part1701.htm -->

### Parameters:

<Compare> GTHan | LTHan | WITHin | OUTSide

*RST: GTH

### TRIGger:A:ARINc:TTIMe:MAXimum <TransmissionTimeMax> Sets the maximum value of the transmission time.

<!-- 来源：RTM2_UserManual_en_10_files\part1702.htm -->

### Parameters:

<TransmissionTimeMax>

### TRIGger:A:ARINc:TTIMe:MINimum <TransmissionTimeMin> Sets the minimum value of the transmission time.

<!-- 来源：RTM2_UserManual_en_10_files\part1703.htm -->

### Parameters:

<TransmissionTimeMin>

### TRIGger:A:ARINc:TYPE <TriggerType> Selects the type of trigger.

<!-- 来源：RTM2_UserManual_en_10_files\part1704.htm -->

### Parameters:

<TriggerType> WORD | ERRor | LABel | LDATa | TTIMe

### TRIGger:A:ARINc:WORD:TYPE <WordType>

Sets the word type to be triggered on.

<!-- 来源：RTM2_UserManual_en_10_files\part1705.htm -->

### Parameters:

<WordType> STARt | STOP

### 18.13.10.3 ARINC 429 - Decode Results

BUS<b>:ARINc:WCOunt? 659

BUS<b>:ARINc:DATA:FORMat 659

BUS<b>:ARINc:WORD<n>:DATA? 659

BUS<b>:ARINc:WORD<n>:DATA[:VALue]? 659

BUS<b>:ARINc:WORD<n>:FORMat? 659

BUS<b>:ARINc:WORD<n>:LABel? 660

BUS<b>:ARINc:WORD<n>:LABel[:VALue]? 660

BUS<b>:ARINc:WORD<n>:PARity? 660

BUS<b>:ARINc:WORD<n>:PATTern? 660

BUS<b>:ARINc:WORD<n>:SDI? 660

BUS<b>:ARINc:WORD<n>:SSM? 661

BUS<b>:ARINc:WORD<n>:STARt? 661

BUS<b>:ARINc:WORD<n>:STOP? 661

BUS<b>:ARINc:WORD<n>:STATus? 661

<!-- 来源：RTM2_UserManual_en_10_files\part1706.htm -->

### BUS<b>:ARINc:WCOunt?

Returns the number of decoded words.

<!-- 来源：RTM2_UserManual_en_10_files\part1707.htm -->

### Return values:

<WordCount>

### Usage: Query only

### BUS<b>:ARINc:DATA:FORMat <StandardDecodeFormat> Sets the decoding data format for the specified ARINC 429 bus.

<!-- 来源：RTM2_UserManual_en_10_files\part1708.htm -->

### Parameters:

<StandardDecodeFormDaAt>TA | DSSM | DSDI | DSSSm

```text
SSMData: SSM+Data SDIData: SDI+Data SSData: SSM+Data +SDI
```

<!-- 来源：RTM2_UserManual_en_10_files\part1709.htm -->

### BUS<b>:ARINc:WORD<n>:DATA?

Returns the data bytes of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1710.htm -->

### Suffix:

<b> 1..4

<n> *

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1711.htm -->

### BUS<b>:ARINc:WORD<n>:DATA[:VALue]?

Returns the decimal value of the data of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1712.htm -->

### Return values:

<DataValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1713.htm -->

### BUS<b>:ARINc:WORD<n>:FORMat?

Returns the format of the sepcified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1714.htm -->

### Return values:

<DataFormat> DATA | DSSM | DSDI | DSSSm

```text
SSMData: SSM+Data SDIData: SDI+Data SSData: SSM+Data +SDI
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1715.htm -->

### BUS<b>:ARINc:WORD<n>:LABel?

Returns the label of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1716.htm -->

### Suffix:

<b> 1..4

<n> *

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1717.htm -->

### BUS<b>:ARINc:WORD<n>:LABel[:VALue]?

Returns the decimal value of the label of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1718.htm -->

### Return values:

<LabelValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1719.htm -->

### BUS<b>:ARINc:WORD<n>:PARity?

Returns the parity of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1720.htm -->

### Return values:

<Parity>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1721.htm -->

### BUS<b>:ARINc:WORD<n>:PATTern?

Returns all 32 bits of a data word as decimal value.

<!-- 来源：RTM2_UserManual_en_10_files\part1722.htm -->

### Return values:

<PatternValue> Integer value

Range: 0 to 2 32 -1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1723.htm -->

### BUS<b>:ARINc:WORD<n>:SDI?

Returns the source/destination identifier (SDI) bits of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1724.htm -->

### Return values:

<SDI>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1725.htm -->

### BUS<b>:ARINc:WORD<n>:SSM?

Returns the sign/status matrix(SSM) bits of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1726.htm -->

### Return values:

<SSM>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1727.htm -->

### BUS<b>:ARINc:WORD<n>:STARt?

Returns the start time of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1728.htm -->

### Return values:

<StartTime>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1729.htm -->

### BUS<b>:ARINc:WORD<n>:STOP?

Returns the end time of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1730.htm -->

### Return values:

<StopTime>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1731.htm -->

### BUS<b>:ARINc:WORD<n>:STATus?

Returns the status of the specified word.

<!-- 来源：RTM2_UserManual_en_10_files\part1732.htm -->

### Return values:

<WordStatus> OK | INSufficient | INComplete | PRERror | GERRor | CERRor

### Usage: Query only

### 18.13.10.4 ARINC 429 - Search

SEARch:PROTocol:ARINc:CONDition 662

SEARch:PROTocol:ARINc:DATA:CONDition 662

SEARch:PROTocol:ARINc:DATA:MAXimum 662

SEARch:PROTocol:ARINc:DATA:MINimum 663

SEARch:PROTocol:ARINc:DATA:OFFSet 663

SEARch:PROTocol:ARINc:DATA:SIZE 663

SEARch:PROTocol:ARINc:ERRor 663

SEARch:PROTocol:ARINc:FORMat 663

SEARch:PROTocol:ARINc:LABel:CONDition 664

SEARch:PROTocol:ARINc:LABel:MAXimum 664

SEARch:PROTocol:ARINc:LABel:MINimum 664

SEARch:PROTocol:ARINc:SDI 664

SEARch:PROTocol:ARINc:SSM 664

SEARch:PROTocol:ARINc:WORD[:TYPE] 665

<!-- 来源：RTM2_UserManual_en_10_files\part1733.htm -->

### SEARch:PROTocol:ARINc:CONDition

Sets the event or combination of events to be searched for. Depending on the selected event, further settings are required.

<!-- 来源：RTM2_UserManual_en_10_files\part1734.htm -->

### Parameters:

<SearchCondition> WORD | ERRor | LABel | LDATa

<!-- 来源：RTM2_UserManual_en_10_files\part1735.htm -->

### WORD

Search for a word type.

```text
Set the word type with SEARch:PROTocol:ARINc:WORD[: TYPE].
```

<!-- 来源：RTM2_UserManual_en_10_files\part1736.htm -->

### ERROr

Search for errors of one or more error types.

Set the error types with SEARch:PROTocol:ARINc:ERRor

<!-- 来源：RTM2_UserManual_en_10_files\part1737.htm -->

### LABel

Searches for label.

```text
Set the label with SEARch:PROTocol:ARINc:LABel: CONDition, SEARch:PROTocol:ARINc:LABel:MAXimum and SEARch:PROTocol:ARINc:LABel:MINimum
```

<!-- 来源：RTM2_UserManual_en_10_files\part1738.htm -->

### LDATa

Searches for label and data.

```text
Set the label with SEARch:PROTocol:ARINc:LABel: CONDition, SEARch:PROTocol:ARINc:LABel:MAXimum and SEARch:PROTocol:ARINc:LABel:MINimum.
Set the data with SEARch:PROTocol:ARINc:DATA: CONDition, SEARch:PROTocol:ARINc:DATA:MAXimum, SEARch:PROTocol:ARINc:DATA:MINimum, SEARch: PROTocol:ARINc:DATA:OFFSet, SEARch:PROTocol: ARINc:DATA:SIZE, SEARch:PROTocol:ARINc:SDI and SEARch:PROTocol:ARINc:SSM
```

<!-- 来源：RTM2_UserManual_en_10_files\part1739.htm -->

### SEARch:PROTocol:ARINc:DATA:CONDition

Sets the comparison condition for data: If the pattern contains at least one X (don't care), you can trigger on values equal or not equal to the specified value. If the pattern contains only 0 and 1, you can also trigger on a range greater than or lower than the specified value.

The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to LDATa.

<!-- 来源：RTM2_UserManual_en_10_files\part1740.htm -->

### Parameters:

<DataCondition> EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

<!-- 来源：RTM2_UserManual_en_10_files\part1741.htm -->

### SEARch:PROTocol:ARINc:DATA:MAXimum

Searches for a maximum value of the data if SEARch:PROTocol:ARINc:DATA: CONDition is set to INRange or OORange.

The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to LDATa.

<!-- 来源：RTM2_UserManual_en_10_files\part1742.htm -->

### Parameters:

<DataMaximum> 01X-string

<!-- 来源：RTM2_UserManual_en_10_files\part1743.htm -->

### SEARch:PROTocol:ARINc:DATA:MINimum

Searches for a minimum value of the data.

The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to LDATa.

<!-- 来源：RTM2_UserManual_en_10_files\part1744.htm -->

### Parameters:

<DataMinimum> 01X-string

<!-- 来源：RTM2_UserManual_en_10_files\part1745.htm -->

### SEARch:PROTocol:ARINc:DATA:OFFSet

Searches for specified data offset.

The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to LDATa.

<!-- 来源：RTM2_UserManual_en_10_files\part1746.htm -->

### Parameters:

<DataOffset>

<!-- 来源：RTM2_UserManual_en_10_files\part1747.htm -->

### SEARch:PROTocol:ARINc:DATA:SIZE

Searches for specified data size.

The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to LDATa.

<!-- 来源：RTM2_UserManual_en_10_files\part1748.htm -->

### Parameters:

<DataSize>

<!-- 来源：RTM2_UserManual_en_10_files\part1749.htm -->

### SEARch:PROTocol:ARINc:ERRor

Searches for an error condition.

The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to ERRor.

<!-- 来源：RTM2_UserManual_en_10_files\part1750.htm -->

### Parameters:

<ErrorCondition> ANY | PARity | GAP | CODing

<!-- 来源：RTM2_UserManual_en_10_files\part1751.htm -->

### SEARch:PROTocol:ARINc:FORMat

Searches for a data format.

The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to LDATa.

<!-- 来源：RTM2_UserManual_en_10_files\part1752.htm -->

### Parameters:

<DataFormat> DATA | DSSM | DSDI | DSSSm

```text
SSMData: SSM+Data SDIData: SDI+Data SSData: SSM+Data +SDI
```

<!-- 来源：RTM2_UserManual_en_10_files\part1753.htm -->

### SEARch:PROTocol:ARINc:LABel:CONDition

Sets the comparison condition for label: If the pattern contains at least one X (don't care), you can trigger on values equal or not equal to the specified value. If the pattern contains only 0 and 1, you can also trigger on a range greater than or lower than the specified value.

```text
The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to LABel
```

or LDAta.

<!-- 来源：RTM2_UserManual_en_10_files\part1754.htm -->

### Parameters:

<LabelCondition> EQUal | NEQual | GTHan | GEQual | LEQual | LTHan | WITHin | OUTSide

<!-- 来源：RTM2_UserManual_en_10_files\part1755.htm -->

### SEARch:PROTocol:ARINc:LABel:MAXimum

Searches for a maximum value of the label if SEARch:PROTocol:ARINc:LABel: CONDition is set to INRange or OORange.

```text
The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to LABel
```

or LDATa.

<!-- 来源：RTM2_UserManual_en_10_files\part1756.htm -->

### Parameters:

<LabelMaximum> 01X-string

<!-- 来源：RTM2_UserManual_en_10_files\part1757.htm -->

### SEARch:PROTocol:ARINc:LABel:MINimum

Searches for a minimum value of the label.

```text
The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to LABel
```

or LDATa.

<!-- 来源：RTM2_UserManual_en_10_files\part1758.htm -->

### Parameters:

<LabelMinimum> 01X-string

<!-- 来源：RTM2_UserManual_en_10_files\part1759.htm -->

### SEARch:PROTocol:ARINc:SDI

Searches for the specified source/destination identifier (SDI) bits.

The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to LDATa.

<!-- 来源：RTM2_UserManual_en_10_files\part1760.htm -->

### Parameters:

<SDIvalue> ANY | S00 | S01 | S10 | S11

<!-- 来源：RTM2_UserManual_en_10_files\part1761.htm -->

### SEARch:PROTocol:ARINc:SSM

Searches for specified sign/status matrix (SSM) bits.

The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to LDATa.

<!-- 来源：RTM2_UserManual_en_10_files\part1762.htm -->

### Parameters:

<SSMvalue> ANY | S00 | S01 | S10 | S11

<!-- 来源：RTM2_UserManual_en_10_files\part1763.htm -->

### SEARch:PROTocol:ARINc:WORD[:TYPE]

Selects the word type to be searched for.

The command is relevant if SEARch:PROTocol:ARINc:CONDition is set to WORD.

<!-- 来源：RTM2_UserManual_en_10_files\part1764.htm -->

### Parameters:

<WordType> STARt | STOP

<!-- 来源：RTM2_UserManual_en_10_files\part1765.htm -->

## 18.14 Power Analysis (Option R&S RTM-K31)

- Measurement Selection and General Settings 665

- Probe Adjustment 667

- Report 667

- Statistical Results 668

- Power Quality 670

- Consumption 675

- Current Harmonics 676

- Inrush Current 683

- Ripple 685

- Spectrum 690

- Transient Response 693

- Slew Rate 695

- Modulation Analysis 697

- Dynamic ON Resistance 700

- Efficiency 701

- Switching Loss 703

- Turn ON/OFF 707

- Safe Operating Area (S.O.A.) 708

- S.O.A. Results 710

<!-- 来源：RTM2_UserManual_en_10_files\part1766.htm -->

### 18.14.1 Measurement Selection and General Settings

POWer:ATYPe 665

POWer:ENABle 666

POWer:SOURce:CURRent<n> 666

POWer:SOURce:VOLTage<n> 666

POWer:RESult:TABLe 666

POWer:STATistics:RESet 667

POWer:STATistics:VISible 667

<!-- 来源：RTM2_UserManual_en_10_files\part1767.htm -->

### POWer:ATYPe

Sets the type of power analysis measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part1768.htm -->

### Parameters:

<AnalysisType> OFF | QUALity | CONSumption | HARMonicsINRushcurrent | RIPPle | SPECtrumSWITchingloss | SLEWrateMODulation | DONResistance | EFFiciencySWITchingloss | TURNonoff | TRANsient

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part1769.htm -->

### POWer:ENABle

Enables/disables the power analysis measurements.

<!-- 来源：RTM2_UserManual_en_10_files\part1770.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part1771.htm -->

### POWer:SOURce:CURRent<n>

Sets the channel for the current source. Connect the current probe in flow direction of the current.

<!-- 来源：RTM2_UserManual_en_10_files\part1772.htm -->

### Suffix:

<n> 1..2

Only relevant if two current sources are used: 1 = In, 2 = Out

<!-- 来源：RTM2_UserManual_en_10_files\part1773.htm -->

### Parameters:

<CurrentSource> CH1 | CH2 | CH3 | CH4 | RE1 | RE2 | RE3 | RE4

<!-- 来源：RTM2_UserManual_en_10_files\part1774.htm -->

### POWer:SOURce:VOLTage<n>

Sets the channel for the voltage source input..

<!-- 来源：RTM2_UserManual_en_10_files\part1775.htm -->

### Suffix:

<n> 1..4

Only relevant if several current sources are used: 1 = In, 2 = Out, 3 and 4 = Out for Turn ON/OFF measurement

<!-- 来源：RTM2_UserManual_en_10_files\part1776.htm -->

### Parameters:

<VoltageSource> CH1 | CH2 | CH3 | CH4 | RE1 | RE2 | RE3 | RE4

<!-- 来源：RTM2_UserManual_en_10_files\part1777.htm -->

### POWer:RESult:TABLe

Displays or hides the result table.

Tha command is available for harmonic and spectrum power measurements.

<!-- 来源：RTM2_UserManual_en_10_files\part1778.htm -->

### Parameters:

<Visible> ON | OFF

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part1779.htm -->

### POWer:STATistics:RESet

Deletes the statistical results for the current measurement or all measurements, respectivley, and starts a new statistical evaluation.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1780.htm -->

### POWer:STATistics:VISible

Shows/ hides the statistical evaluation of the measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part1781.htm -->

### Parameters:

<Visible> ON | OFF

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part1782.htm -->

### 18.14.2 Probe Adjustment

<!-- 来源：RTM2_UserManual_en_10_files\part1783.htm -->

### POWer:DESKew[:EXECute]

Starts the automatic deskew procedure to align the waveforms of all visible channels. It is necessary to deskew if a current and a voltage probe is used in the measurment.

Use the R&S RT-ZF20 power deskew fixture to deskew the probes.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1784.htm -->

### POWer:ZOFFset[:EXECute]

Executes a zero offset for all visible channels.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1785.htm -->

### 18.14.3 Report

POWer:REPort:ADD 667

POWer:REPort:DESCription 668

POWer:REPort:DUT 668

POWer:REPort:OUTPut 668

POWer:REPort:SITE 668

POWer:REPort:TEMPerature 668

POWer:REPort:USER 668

<!-- 来源：RTM2_UserManual_en_10_files\part1786.htm -->

### POWer:REPort:ADD

Adds a power report.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1787.htm -->

### POWer:REPort:DESCription

Sets a description that can be shown at the titel page of a report.

<!-- 来源：RTM2_UserManual_en_10_files\part1788.htm -->

### Parameters:

<DescriptionString> String parameter

<!-- 来源：RTM2_UserManual_en_10_files\part1789.htm -->

### POWer:REPort:DUT

Sets a device under test (DUT) value that can be shown at the titel page of a report.

<!-- 来源：RTM2_UserManual_en_10_files\part1790.htm -->

### Parameters:

<DeviceString> String parameter

<!-- 来源：RTM2_UserManual_en_10_files\part1791.htm -->

### POWer:REPort:OUTPut

Sets the directory for the output folder, where the reports are stored.

<!-- 来源：RTM2_UserManual_en_10_files\part1792.htm -->

### Parameters:

<OutputFolderPath> String parameter

<!-- 来源：RTM2_UserManual_en_10_files\part1793.htm -->

### POWer:REPort:SITE

Sets a site value that can be shown at the titel page of a report.

<!-- 来源：RTM2_UserManual_en_10_files\part1794.htm -->

### Parameters:

<SiteString> String parameter

### POWer:REPort:TEMPerature <Temperature>

Sets a temperature value that can be shown at the titel page of a report.

<!-- 来源：RTM2_UserManual_en_10_files\part1795.htm -->

### Parameters:

<Temperature> Range: -273 to 32767

Increment: 1

*RST: 20

<!-- 来源：RTM2_UserManual_en_10_files\part1796.htm -->

### POWer:REPort:USER

Sets a user value that can be shown at the titel page of a report.

<!-- 来源：RTM2_UserManual_en_10_files\part1797.htm -->

### Parameters:

<UserString> String parameter

<!-- 来源：RTM2_UserManual_en_10_files\part1798.htm -->

### 18.14.4 Statistical Results

Some power measurements deliver also statistical results, which can be exported to CSV files.

Power measurements use the measurement places ≥ 5. The number of the measure- ment places are shown in the result table on the display, and they are listed in the result files of EXPort:MEASurement<m>:STATistics:ALL commands.

EXPort:MEASurement<m>:STATistics:NAME 669

EXPort:MEASurement<m>:STATistics:SAVE 669

EXPort:MEASurement<m>:STATistics:ALL:NAME 669

EXPort:MEASurement<m>:STATistics:ALL:SAVE 669

<!-- 来源：RTM2_UserManual_en_10_files\part1799.htm -->

### EXPort:MEASurement<m>:STATistics:NAME

Defines the path and filename of the statistics file. The file format is CSV. If the file already exists, it will be overwritten.

<!-- 来源：RTM2_UserManual_en_10_files\part1800.htm -->

### Suffix:

<m> 1. 15

1..4: measurement places of automatic measurements

5..15: measurement places for power measurements.

<!-- 来源：RTM2_UserManual_en_10_files\part1801.htm -->

### Parameters:

<FileName> String parameter

<!-- 来源：RTM2_UserManual_en_10_files\part1802.htm -->

### EXPort:MEASurement<m>:STATistics:SAVE

```text
Saves statistical results of the indicated measurement place to the file that is defined by the EXPort:MEASurement<m>:STATistics:NAME command.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1803.htm -->

### Suffix:

<m> 1..15

1..4: measurement places of automatic measurements

5..15: measurement places for power measurements.

### Usage: Event

See also: EXPort:MEASurement<m>:STATistics:ALL:SAVE on page 494.

<!-- 来源：RTM2_UserManual_en_10_files\part1804.htm -->

### EXPort:MEASurement<m>:STATistics:ALL:NAME

Defines the path and filename of the statistics file. The file format is CSV. If the file already exists, it will be overwritten.

<!-- 来源：RTM2_UserManual_en_10_files\part1805.htm -->

### Suffix:

<m> 1..4

The suffix is irrelevant, all results are returned.

<!-- 来源：RTM2_UserManual_en_10_files\part1806.htm -->

### Parameters:

<FileName> String parameter

<!-- 来源：RTM2_UserManual_en_10_files\part1807.htm -->

### EXPort:MEASurement<m>:STATistics:ALL:SAVE

Saves statistical results of all measurement places to the file that is defined by the

```text
EXPort:MEASurement<m>:STATistics:ALL:NAME command.
```

<!-- 来源：RTM2_UserManual_en_10_files\part1808.htm -->

### Suffix:

<m> 1..4

The suffix is irrelevant, all results are returned.

### Example: The file contains general information, statistical results, long term statistics, and the individual values that are used to calcu- late the statistics. The number of values is "Average No." "Vendor","Rohde&Schwarz",

```text
"Device/Mat.-No.","RTM2022 / 5710.0999k22", "Serial No.","900001",
"Firmware Version","Beta 05.601",
"Date","2014-11-18 / 16:40:27",
"Meas. Place",,"1",,"2",,"3",,
"Type",,"Frequency",,"Mean Value",,"Frequency",,
"Source 1",,"CH1",,"CH1",,"CH2",,
"Source 2",,,,,,,,,,
"Wave count",,42,,39,,37,, "Current",,4.998250e+05,,5.648727e-01,,4.998250e+05,, "Average No.",,1.000000e+03,,1.000000e+03,,1.000000e+03,, "Minimum",,4.997501e+05,,5.633875e-01,,4.997501e+05,, "Maximum",,4.998250e+05,,5.650349e-01,,4.998250e+05,, "Mean",,4.998179e+05,,5.642045e-01,,4.998169e+05,,
"σ-Deviation",,2.199706e+01,,3.677224e-04,,2.326898e+01,,
"Time of first value",,,,,,,,,,
"Time of last value",,,,,,,,,,
"Long term Minimum",,4.997501e+05,,5.633875e-01,,4.997501e+05,, "Long term Maximum",,4.998250e+05,,5.650349e-01,,4.998250e+05,, "Long term Mittelwert",,4.998179e+05,,5.642045e-01,,4.998169e+05,, "Long term σ-Deviation",,2.226370e+01,,3.725295e-04,,2.358995e+01,,
"Long term start time",,,,,,,,,,
"Long term end Time",,,,,,,,,,
"Index","Time Offset","Value","Time Offset","Value", "Time Offset","Value",
1,,4.998250e+05,,5.649274e-01,,4.997501e+05,
2,,4.998250e+05,,5.649072e-01,,4.998250e+05,
3,,4.998250e+05,,5.650349e-01,,4.998250e+05,
4,,4.998250e+05,,5.641094e-01,,4.998250e+05,
5,,4.998250e+05,,5.640586e-01,,4.998250e+05,
6,,4.997501e+05,,5.642784e-01,,4.998250e+05,
7,,4.998250e+05,,5.637245e-01,,4.998250e+05,...
```

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1809.htm -->

### 18.14.5 Power Quality

POWer:QUALity:EXECute 672

POWer:QUALity:REPort:ADD 672

POWer:QUALity:RESult:VOLTage:RMS[:ACTual]? 672

POWer:QUALity:RESult:VOLTage:CREStfactor[:ACTual]? 672

POWer:QUALity:RESult:VOLTage:FREQuency[:ACTual]? 672

POWer:QUALity:RESult:CURRent:RMS[:ACTual]? 672

POWer:QUALity:RESult:CURRent:CREStfactor[:ACTual]? 672

POWer:QUALity:RESult:CURRent:FREQuency[:ACTual]? 672

POWer:QUALity:RESult:VOLTage:RMS:AVG? 672

POWer:QUALity:RESult:VOLTage:CREStfactor:AVG? 672

POWer:QUALity:RESult:VOLTage:FREQuency:AVG? 672

POWer:QUALity:RESult:CURRent:RMS:AVG? 672

POWer:QUALity:RESult:CURRent:CREStfactor:AVG? 672

POWer:QUALity:RESult:CURRent:FREQuency:AVG? 672

POWer:QUALity:RESult:VOLTage:RMS:NPEak? 673

POWer:QUALity:RESult:VOLTage:CREStfactor:NPEak? 673

POWer:QUALity:RESult:VOLTage:FREQuency:NPEak? 673

POWer:QUALity:RESult:CURRent:RMS:NPEak? 673

POWer:QUALity:RESult:CURRent:CREStfactor:NPEak? 673

POWer:QUALity:RESult:CURRent:FREQuency:NPEak? 673

POWer:QUALity:RESult:VOLTage:RMS:PPEak? 673

POWer:QUALity:RESult:VOLTage:CREStfactor:PPEak? 673

POWer:QUALity:RESult:VOLTage:FREQuency:PPEak? 673

POWer:QUALity:RESult:CURRent:RMS:PPEak? 673

POWer:QUALity:RESult:CURRent:CREStfactor:PPEak? 673

POWer:QUALity:RESult:CURRent:FREQuency:PPEak? 673

POWer:QUALity:RESult:VOLTage:RMS:STDDev? 673

POWer:QUALity:RESult:VOLTage:CREStfactor:STDDev? 673

POWer:QUALity:RESult:VOLTage:FREQuency:STDDev? 673

POWer:QUALity:RESult:CURRent:RMS:STDDev? 673

POWer:QUALity:RESult:CURRent:CREStfactor:STDDev? 673

POWer:QUALity:RESult:CURRent:FREQuency:STDDev? 673

POWer:QUALity:RESult:VOLTage:RMS:WFMCount? 673

POWer:QUALity:RESult:VOLTage:CREStfactor:WFMCount? 673

POWer:QUALity:RESult:VOLTage:FREQuency:WFMCount? 673

POWer:QUALity:RESult:CURRent:RMS:WFMCount? 673

POWer:QUALity:RESult:CURRent:CREStfactor:WFMCount? 674

POWer:QUALity:RESult:CURRent:FREQuency:WFMCount? 674

POWer:QUALity:RESult:POWer:REALpower[:ACTual]? 674

POWer:QUALity:RESult:POWer:REACtive[:ACTual]? 674

POWer:QUALity:RESult:POWer:APParent[:ACTual]? 674

POWer:QUALity:RESult:POWer:PFACtor[:ACTual]? 674

POWer:QUALity:RESult:POWer:PHASe[:ACTual]? 674

POWer:QUALity:RESult:POWer:REALpower:AVG? 674

POWer:QUALity:RESult:POWer:REACtive:AVG? 674

POWer:QUALity:RESult:POWer:APParent:AVG? 674

POWer:QUALity:RESult:POWer:PFACtor:AVG? 674

POWer:QUALity:RESult:POWer:PHASe:AVG? 674

POWer:QUALity:RESult:POWer:REALpower:NPEak? 674

POWer:QUALity:RESult:POWer:REACtive:NPEak? 674

POWer:QUALity:RESult:POWer:APParent:NPEak? 674

POWer:QUALity:RESult:POWer:PFACtor:NPEak? 674

POWer:QUALity:RESult:POWer:PHASe:NPEak? 674

POWer:QUALity:RESult:POWer:REALpower:PPEak? 674

POWer:QUALity:RESult:POWer:REACtive:PPEak? 674

POWer:QUALity:RESult:POWer:APParent:PPEak? 674

POWer:QUALity:RESult:POWer:PFACtor:PPEak? 675

POWer:QUALity:RESult:POWer:PHASe:PPEak? 675

POWer:QUALity:RESult:POWer:REALpower:STDDev? 675

POWer:QUALity:RESult:POWer:REACtive:STDDev? 675

POWer:QUALity:RESult:POWer:APParent:STDDev? 675

POWer:QUALity:RESult:POWer:PFACtor:STDDev? 675

POWer:QUALity:RESult:POWer:PHASe:STDDev? 675

POWer:QUALity:RESult:POWer:REALpower:WFMCount? 675

POWer:QUALity:RESult:POWer:REACtive:WFMCount? 675

POWer:QUALity:RESult:POWer:APParent:WFMCount? 675

POWer:QUALity:RESult:POWer:PFACtor:WFMCount? 675

POWer:QUALity:RESult:POWer:PHASe:WFMCount? 675

<!-- 来源：RTM2_UserManual_en_10_files\part1810.htm -->

### POWer:QUALity:EXECute

Starts the power quality measurement.

### Usage: Event

### POWer:QUALity:REPort:ADD Adds the result to the report list. Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1811.htm -->

### POWer:QUALity:RESult:VOLTage:RMS[:ACTual]? POWer:QUALity:RESult:VOLTage:CREStfactor[:ACTual]? POWer:QUALity:RESult:VOLTage:FREQuency[:ACTual]? POWer:QUALity:RESult:CURRent:RMS[:ACTual]?

### POWer:QUALity:RESult:CURRent:CREStfactor[:ACTual]? POWer:QUALity:RESult:CURRent:FREQuency[:ACTual]?

Returns the instantenious result of the specified measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part1812.htm -->

### Return values:

<ActualValue> Measurement result. If no measurement was executed, no value (NAN) is returned.

### Usage: Query only

### POWer:QUALity:RESult:VOLTage:RMS:AVG?

### POWer:QUALity:RESult:VOLTage:CREStfactor:AVG? POWer:QUALity:RESult:VOLTage:FREQuency:AVG? POWer:QUALity:RESult:CURRent:RMS:AVG?

### POWer:QUALity:RESult:CURRent:CREStfactor:AVG? POWer:QUALity:RESult:CURRent:FREQuency:AVG?

Returns the average value of the specified measurement series.

<!-- 来源：RTM2_UserManual_en_10_files\part1813.htm -->

### Return values:

<AverageValue> Statistic value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1814.htm -->

### POWer:QUALity:RESult:VOLTage:RMS:NPEak? POWer:QUALity:RESult:VOLTage:CREStfactor:NPEak? POWer:QUALity:RESult:VOLTage:FREQuency:NPEak? POWer:QUALity:RESult:CURRent:RMS:NPEak?

### POWer:QUALity:RESult:CURRent:CREStfactor:NPEak? POWer:QUALity:RESult:CURRent:FREQuency:NPEak?

Returns the minimum value of the specified measurement series.

<!-- 来源：RTM2_UserManual_en_10_files\part1815.htm -->

### Return values:

<MinimumValue> Statistic value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1816.htm -->

### POWer:QUALity:RESult:VOLTage:RMS:PPEak? POWer:QUALity:RESult:VOLTage:CREStfactor:PPEak? POWer:QUALity:RESult:VOLTage:FREQuency:PPEak? POWer:QUALity:RESult:CURRent:RMS:PPEak?

### POWer:QUALity:RESult:CURRent:CREStfactor:PPEak? POWer:QUALity:RESult:CURRent:FREQuency:PPEak?

Returns the maximum value of the specified measurement series.

<!-- 来源：RTM2_UserManual_en_10_files\part1817.htm -->

### Return values:

<MaximumValue> Statistic value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1818.htm -->

### POWer:QUALity:RESult:VOLTage:RMS:STDDev? POWer:QUALity:RESult:VOLTage:CREStfactor:STDDev? POWer:QUALity:RESult:VOLTage:FREQuency:STDDev? POWer:QUALity:RESult:CURRent:RMS:STDDev?

### POWer:QUALity:RESult:CURRent:CREStfactor:STDDev? POWer:QUALity:RESult:CURRent:FREQuency:STDDev?

Returns the statistical standard deviation of the specified measurement series.

<!-- 来源：RTM2_UserManual_en_10_files\part1819.htm -->

### Return values:

<DeviationValue> Statistic value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1820.htm -->

### POWer:QUALity:RESult:VOLTage:RMS:WFMCount? POWer:QUALity:RESult:VOLTage:CREStfactor:WFMCount? POWer:QUALity:RESult:VOLTage:FREQuency:WFMCount? POWer:QUALity:RESult:CURRent:RMS:WFMCount?

### POWer:QUALity:RESult:CURRent:CREStfactor:WFMCount? POWer:QUALity:RESult:CURRent:FREQuency:WFMCount?

Returns the current number of measured waveforms.

<!-- 来源：RTM2_UserManual_en_10_files\part1821.htm -->

### Return values:

<WaveformCount> Statistic value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1822.htm -->

### POWer:QUALity:RESult:POWer:REALpower[:ACTual]? POWer:QUALity:RESult:POWer:REACtive[:ACTual]?

### POWer:QUALity:RESult:POWer:APParent[:ACTual]? POWer:QUALity:RESult:POWer:PFACtor[:ACTual]? POWer:QUALity:RESult:POWer:PHASe[:ACTual]?

Returns the instantenious result of the specified measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part1823.htm -->

### Return values:

<ActualValue> Measurement result. If no measurement was executed, no value (NAN) is returned.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1824.htm -->

### POWer:QUALity:RESult:POWer:REALpower:AVG? POWer:QUALity:RESult:POWer:REACtive:AVG?

### POWer:QUALity:RESult:POWer:APParent:AVG? POWer:QUALity:RESult:POWer:PFACtor:AVG? POWer:QUALity:RESult:POWer:PHASe:AVG?

Returns the average value of the specified measurement series.

<!-- 来源：RTM2_UserManual_en_10_files\part1825.htm -->

### Return values:

<AverageValue> Statistic value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1826.htm -->

### POWer:QUALity:RESult:POWer:REALpower:NPEak? POWer:QUALity:RESult:POWer:REACtive:NPEak?

### POWer:QUALity:RESult:POWer:APParent:NPEak? POWer:QUALity:RESult:POWer:PFACtor:NPEak? POWer:QUALity:RESult:POWer:PHASe:NPEak?

Returns the minimum value of the specified measurement series.

<!-- 来源：RTM2_UserManual_en_10_files\part1827.htm -->

### Return values:

<MinimumValue> Statistic value

### Usage: Query only

### POWer:QUALity:RESult:POWer:REALpower:PPEak? POWer:QUALity:RESult:POWer:REACtive:PPEak?

### POWer:QUALity:RESult:POWer:APParent:PPEak?

### POWer:QUALity:RESult:POWer:PFACtor:PPEak? POWer:QUALity:RESult:POWer:PHASe:PPEak?

Returns the maximum value of the specified measurement series.

<!-- 来源：RTM2_UserManual_en_10_files\part1828.htm -->

### Return values:

<MaximumValue> Statistic value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1829.htm -->

### POWer:QUALity:RESult:POWer:REALpower:STDDev? POWer:QUALity:RESult:POWer:REACtive:STDDev?

### POWer:QUALity:RESult:POWer:APParent:STDDev? POWer:QUALity:RESult:POWer:PFACtor:STDDev? POWer:QUALity:RESult:POWer:PHASe:STDDev?

Returns the statistical standard deviation of the specified measurement series.

<!-- 来源：RTM2_UserManual_en_10_files\part1830.htm -->

### Return values:

<DeviationValue> Statistic value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1831.htm -->

### POWer:QUALity:RESult:POWer:REALpower:WFMCount? POWer:QUALity:RESult:POWer:REACtive:WFMCount?

### POWer:QUALity:RESult:POWer:APParent:WFMCount? POWer:QUALity:RESult:POWer:PFACtor:WFMCount? POWer:QUALity:RESult:POWer:PHASe:WFMCount?

Returns the current number of measured waveforms.

<!-- 来源：RTM2_UserManual_en_10_files\part1832.htm -->

### Return values:

<WaveformCount> Statistic value

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1833.htm -->

### 18.14.6 Consumption

POWer:CONSumption:EXECute 675

POWer:CONSumption:REPort:ADD 676

POWer:CONSumption:RESTart 676

POWer:CONSumption:RESult:DURation? 676

POWer:CONSumption:RESult:ENERgy? 676

POWer:CONSumption:RESult:REALpower? 676

### POWer:CONSumption:EXECute <State> Starts the consumption measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part1834.htm -->

### Parameters:

<State> ON | OFF

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1835.htm -->

### POWer:CONSumption:REPort:ADD

Adds the result to the report list.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1836.htm -->

### POWer:CONSumption:RESTart

Restarts the measurement.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1837.htm -->

### POWer:CONSumption:RESult:DURation?

Queries the duration of the measurement. The result is displayed in seconds.

<!-- 来源：RTM2_UserManual_en_10_files\part1838.htm -->

### Return values:

<Duration>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1839.htm -->

### POWer:CONSumption:RESult:ENERgy?

Queries the energy.

<!-- 来源：RTM2_UserManual_en_10_files\part1840.htm -->

### Return values:

<Energy>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1841.htm -->

### POWer:CONSumption:RESult:REALpower?

Queries the real power.

<!-- 来源：RTM2_UserManual_en_10_files\part1842.htm -->

### Return values:

<RealPower>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1843.htm -->

### 18.14.7 Current Harmonics

### 18.14.7.1 Current Harmonics - Settings

POWer:HARMonics:ENFRequency 677

POWer:HARMonics:DOFRequency 677

POWer:HARMonics:MIFRequency 677

POWer:HARMonics:STANdard 677

POWer:HARMonics:EXECute 677

POWer:HARMonics:REPort:ADD 677

POWer:HARMonics:RESult<n>:RESet 677

### POWer:HARMonics:ENFRequency <ENFrequency>

Selects the frequency of the input signal when POWer:HARMonics:STANdard

on page 677 is set to ENA/ENB/ENC/END.

<!-- 来源：RTM2_UserManual_en_10_files\part1844.htm -->

### Parameters:

<ENFrequency> AUTO | F50 | F60

### POWer:HARMonics:DOFRequency <DoFrequency>

Selects the frequency of the input signal when POWer:HARMonics:STANdard is set to RTC.

<!-- 来源：RTM2_UserManual_en_10_files\part1845.htm -->

### Parameters:

<DoFrequency> F400 | NVF | WVF

### POWer:HARMonics:MIFRequency <MILFrequency>

Selects the frequency of the input signal when POWer:HARMonics:STANdard is set to MIL.

<!-- 来源：RTM2_UserManual_en_10_files\part1846.htm -->

### Parameters:

<MILFrequency> F60 | F400

### POWer:HARMonics:STANdard <Standard>

Sets a standard for the current harmonic measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part1847.htm -->

### Parameters:

<Standard> ENA | ENB | ENC | END | MIL | RTC

<!-- 来源：RTM2_UserManual_en_10_files\part1848.htm -->

### POWer:HARMonics:EXECute

Starts the current harmonics measurement.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1849.htm -->

### POWer:HARMonics:REPort:ADD

Adds the result to the report list.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1850.htm -->

### POWer:HARMonics:RESult<n>:RESet

Resets the count of the measurements.

<!-- 来源：RTM2_UserManual_en_10_files\part1851.htm -->

### Suffix:

<n> 1..40

### Usage: Event

### 18.14.7.2 Current Harmonics - Results

POWer:HARMonics:AVAilable? 678

POWer:HARMonics:MEASurement:DURation? 678

POWer:HARMonics:MEASurement:FREQuency:AVG? 678

POWer:HARMonics:MEASurement:FREQuency:NPEak? 679

POWer:HARMonics:MEASurement:FREQuency:PPeak? 679

POWer:HARMonics:MEASurement:FREQuency:STDDev? 679

POWer:HARMonics:MEASurement:FREQuency[:ACTual]? 679

POWer:HARMonics:MEASurement:REALpower[:ACTual]? 679

POWer:HARMonics:MEASurement:THDistortion:AVG? 679

POWer:HARMonics:MEASurement:THDistortion:NPEak? 680

POWer:HARMonics:MEASurement:THDistortion:PPeak? 680

POWer:HARMonics:MEASurement:THDistortion:STDDev? 680

POWer:HARMonics:MEASurement:THDistortion[:ACTual]? 680

POWer:HARMonics:RESult<n>:FREQency? 680

POWer:HARMonics:RESult<n>:LEVel:LIMit? 680

POWer:HARMonics:RESult<n>:LEVel[:VALue]? 681

POWer:HARMonics:RESult<n>:MAXimum? 681

POWer:HARMonics:RESult<n>:MEAN? 681

POWer:HARMonics:RESult<n>:MINimum? 681

POWer:HARMonics:RESult<n>:VALid? 682

POWer:HARMonics:RESult<n>:VCOunt? 682

POWer:HARMonics:RESult<n>:WFMCount? 682

EXPort:POWer:NAME 682

EXPort:POWer:SAVE 682

<!-- 来源：RTM2_UserManual_en_10_files\part1852.htm -->

### POWer:HARMonics:AVAilable?

Returns the number of measured harmonics.

<!-- 来源：RTM2_UserManual_en_10_files\part1853.htm -->

### Return values:

<HarmonicsCount> Number of harmonics

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1854.htm -->

### POWer:HARMonics:MEASurement:DURation?

Returns the time duration of the measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part1855.htm -->

### Return values:

<Duration> Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1856.htm -->

### POWer:HARMonics:MEASurement:FREQuency:AVG?

Returns the average frequency of the measured signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1857.htm -->

### Return values:

<AverageValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1858.htm -->

### POWer:HARMonics:MEASurement:FREQuency:NPEak?

Returns the minimum frequency of the measured signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1859.htm -->

### Return values:

<MinimumValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1860.htm -->

### POWer:HARMonics:MEASurement:FREQuency:PPeak?

Returns the maximum frequency of the measured signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1861.htm -->

### Return values:

<MaximumValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1862.htm -->

### POWer:HARMonics:MEASurement:FREQuency:STDDev?

Returns the standard deviation of frequencies of the measured signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1863.htm -->

### Return values:

<DeviationValue> Standard deviation

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1864.htm -->

### POWer:HARMonics:MEASurement:FREQuency[:ACTual]?

Returns the current frequency value.

<!-- 来源：RTM2_UserManual_en_10_files\part1865.htm -->

### Return values:

<ActualValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1866.htm -->

### POWer:HARMonics:MEASurement:REALpower[:ACTual]?

Returns the measured total power, which is used for dynamic calculation of the limits.

<!-- 来源：RTM2_UserManual_en_10_files\part1867.htm -->

### Return values:

<RealPower>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1868.htm -->

### POWer:HARMonics:MEASurement:THDistortion:AVG?

Returns the average total harmonic disortion of the measured signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1869.htm -->

### Return values:

<AverageValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1870.htm -->

### POWer:HARMonics:MEASurement:THDistortion:NPEak?

Returns the minimum total harmonic disortion of the measured signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1871.htm -->

### Return values:

<MinimumValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1872.htm -->

### POWer:HARMonics:MEASurement:THDistortion:PPeak?

Returns the maximum total harmonic disortion of the measured signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1873.htm -->

### Return values:

<MaximumValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1874.htm -->

### POWer:HARMonics:MEASurement:THDistortion:STDDev?

Returns the standard deviation of total harmonic disortions of the measured signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1875.htm -->

### Return values:

<DeviationValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1876.htm -->

### POWer:HARMonics:MEASurement:THDistortion[:ACTual]?

Returns the current total harmonic disortion value.

<!-- 来源：RTM2_UserManual_en_10_files\part1877.htm -->

### Return values:

<ActualValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1878.htm -->

### POWer:HARMonics:RESult<n>:FREQency?

Queries the frequency of the n-th harmonic.

<!-- 来源：RTM2_UserManual_en_10_files\part1879.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1880.htm -->

### Return values:

<Frequency>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1881.htm -->

### POWer:HARMonics:RESult<n>:LEVel:LIMit?

Queries the limit for the level of the n-th harmonic.

<!-- 来源：RTM2_UserManual_en_10_files\part1882.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1883.htm -->

### Return values:

<LevelLimit>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1884.htm -->

### POWer:HARMonics:RESult<n>:LEVel[:VALue]?

Queries the level of the n-th harmonic.

<!-- 来源：RTM2_UserManual_en_10_files\part1885.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1886.htm -->

### Return values:

<Level>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1887.htm -->

### POWer:HARMonics:RESult<n>:MAXimum?

Queries the maximum level of the n-th harmonic.

<!-- 来源：RTM2_UserManual_en_10_files\part1888.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1889.htm -->

### Return values:

<LevelMaximum>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1890.htm -->

### POWer:HARMonics:RESult<n>:MEAN?

Queries the average level of the n-th harmonic.

<!-- 来源：RTM2_UserManual_en_10_files\part1891.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1892.htm -->

### Return values:

<LevelAverage>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1893.htm -->

### POWer:HARMonics:RESult<n>:MINimum?

Queries the minimum level of the n-th harmonic.

<!-- 来源：RTM2_UserManual_en_10_files\part1894.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1895.htm -->

### Return values:

<LevelMinimum>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1896.htm -->

### POWer:HARMonics:RESult<n>:VALid?

Queries whether the value of n-th harmonic is within the limit for the current measur- ment.

<!-- 来源：RTM2_UserManual_en_10_files\part1897.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1898.htm -->

### Return values:

<Valid> PASS | FAIL

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1899.htm -->

### POWer:HARMonics:RESult<n>:VCOunt?

Queries the number of waveforms, for which the limit value of at least one harmonic was violated.

<!-- 来源：RTM2_UserManual_en_10_files\part1900.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1901.htm -->

### Parameters:

<ViolateCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1902.htm -->

### POWer:HARMonics:RESult<n>:WFMCount?

Queries the number of waveforms, for which the harmonics were measured.

<!-- 来源：RTM2_UserManual_en_10_files\part1903.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1904.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

### EXPort:POWer:NAME <ExportPath>

Defines the path and filename of the results file, available for current harmonics and spectrum power measurements. The file format is CSV. If the file already exists, it will be overwritten.

<!-- 来源：RTM2_UserManual_en_10_files\part1905.htm -->

### Parameters:

<ExportPath> string

String parameter

<!-- 来源：RTM2_UserManual_en_10_files\part1906.htm -->

### EXPort:POWer:SAVE

```text
Saves statistical results of the indicated measurement place to the file that is defined by the EXPort:POWer:NAME command.
```

### Example: Current harmonics measurement: EXPort:POWer:NAME "/USB_FRONT/POWER/HARMONIC" EXPort:POWer:SAVE

The file contains the following data:

```text
"Power Analysis Results: Harmonics (CH2), 50 Hz, EN61000-3-2 A" "Current: Fail (1 / 40)"
"Total Pass: 0; Total Fail: 2" Order,Frequency[Hz],Level[V],Minimum[V],Maximum[V],Average[V], Limit[V],State 1,5.0049E+01,8.06691E+00,8.06691E+00,2.43617E+01,1.62143E+01,
1.60000E+01,Fail
2,1.0010E+02,9.52154E-03,7.72160E-03,9.52154E-03,8.62157E-03,
1.08000E+00,Pass
3,1.5015E+02,3.51324E-03,3.51324E-03,5.07817E-02,2.71475E-02,
2.30000E+00,Pass
4,1.9958E+02,2.47575E-03,2.47575E-03,3.74720E-03,3.11148E-03,
4.30000E-01,Pass
5,2.5024E+02,5.88447E-03,5.88447E-03,3.02487E-02,1.80666E-02,
1.14000E+00,Pass
6,2.9968E+02,7.02598E-03,1.27264E-03,7.02598E-03,4.14931E-03,
3.00000E-01,Pass
...
```

### Example: Spectrum measurement:

```text
EXPort:POWer:NAME "/USB_FRONT/POWER/SPECTRUM" EXPort:POWer:SAVE
```

The file contains the following data:

```text
"Power Analysis Results: Spectrum (CH1), 100kHz" "Total: 67"
Order,Frequency[Hz],Level[dBV],Minimum[dBV],Maximum[dBV],Average[dBV] 1,1.0009766E+05,-1.11840E+02,-1.19960E+02,-8.39799E+01,-1.03205E+02
2,1.9897461E+05,-1.03860E+02,-1.21000E+02,-8.97199E+01,-1.03222E+02
3,2.9907227E+05,-1.02660E+02,-1.22520E+02,-9.12399E+01,-1.03858E+02
4,4.0039062E+05,-1.08660E+02,-1.17400E+02,-9.24199E+01,-1.04547E+02
5,4.9926758E+05,-1.00340E+02,-1.11500E+02,-7.78199E+01,-9.44799E+01
6,6.0058594E+05,-1.10040E+02,-1.16040E+02,-9.39199E+01,-1.03913E+02
...
```

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1907.htm -->

### 18.14.8 Inrush Current

POWer:INRushcurrent:EXECute 684

POWer:INRushcurrent:GATE<n>:STARt 684

POWer:INRushcurrent:GATE<n>:STOP 684

POWer:INRushcurrent:GCOunt 684

POWer:INRushcurrent:REPort:ADD 684

POWer:INRushcurrent:RESult<n>:AREA? 684

POWer:INRushcurrent:RESult<n>:MAXCurrent? 685

### POWer:INRushcurrent:EXECute Starts the inrush current measurement. Usage: Event

### POWer:INRushcurrent:GATE<n>:STARt <StartTime> Sets the start measuring time for the selected gate.

<!-- 来源：RTM2_UserManual_en_10_files\part1908.htm -->

### Suffix:

<n> 1..3

<!-- 来源：RTM2_UserManual_en_10_files\part1909.htm -->

### Parameters:

<StartTime>

### POWer:INRushcurrent:GATE<n>:STOP <StopTime> Sets the stop measuring time for the selected gate.

<!-- 来源：RTM2_UserManual_en_10_files\part1910.htm -->

### Suffix:

<n> 1..3

<!-- 来源：RTM2_UserManual_en_10_files\part1911.htm -->

### Parameters:

<StopTime>

### POWer:INRushcurrent:GCOunt <GateCount> Sets the number of inrush current gates.

<!-- 来源：RTM2_UserManual_en_10_files\part1912.htm -->

### Parameters:

<GateCount> *RST: 1

<!-- 来源：RTM2_UserManual_en_10_files\part1913.htm -->

### POWer:INRushcurrent:REPort:ADD

Adds the result to the report list.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1914.htm -->

### POWer:INRushcurrent:RESult<n>:AREA?

Queries the area of the corresponding gate.

<!-- 来源：RTM2_UserManual_en_10_files\part1915.htm -->

### Suffix:

<n> 1..3

<!-- 来源：RTM2_UserManual_en_10_files\part1916.htm -->

### Return values:

<AreaValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1917.htm -->

### POWer:INRushcurrent:RESult<n>:MAXCurrent?

Queires the maximum current for the corresponding gate.

<!-- 来源：RTM2_UserManual_en_10_files\part1918.htm -->

### Suffix:

<n> 1..3

<!-- 来源：RTM2_UserManual_en_10_files\part1919.htm -->

### Return values:

<MaxCurrentValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1920.htm -->

### 18.14.9 Ripple

POWer:RIPPle:EXECute 686

POWer:RIPPle:REPort:ADD 686

POWer:RIPPle:RESult:FREQuency[:ACTual]? 686

POWer:RIPPle:RESult:FREQuency:AVG? 686

POWer:RIPPle:RESult:FREQuency:NPEak? 686

POWer:RIPPle:RESult:FREQuency:PPEak? 686

POWer:RIPPle:RESult:FREQuency:STDDev? 686

POWer:RIPPle:RESult:FREQuency:WFMCount? 686

POWer:RIPPle:RESult:LPEak[:ACTual]? 687

POWer:RIPPle:RESult:LPEak:AVG? 687

POWer:RIPPle:RESult:LPEak:NPEak? 687

POWer:RIPPle:RESult:LPEak:PPEak? 687

POWer:RIPPle:RESult:LPEak:STDDev? 687

POWer:RIPPle:RESult:LPEak:WFMCount? 687

POWer:RIPPle:RESult:MEAN[:ACTual]? 687

POWer:RIPPle:RESult:MEAN:AVG? 687

POWer:RIPPle:RESult:MEAN:NPEak? 687

POWer:RIPPle:RESult:MEAN:PPEak? 687

POWer:RIPPle:RESult:MEAN:STDDev? 687

POWer:RIPPle:RESult:MEAN:WFMCount? 687

POWer:RIPPle:RESult:NDCYcle[:ACTual]? 687

POWer:RIPPle:RESult:NDCYcle:AVG? 687

POWer:RIPPle:RESult:NDCYcle:NPEak? 688

POWer:RIPPle:RESult:NDCYcle:PPEak? 688

POWer:RIPPle:RESult:NDCYcle:STDDev? 688

POWer:RIPPle:RESult:NDCYcle:WFMCount? 688

POWer:RIPPle:RESult:PDCYcle[:ACTual]? 688

POWer:RIPPle:RESult:PDCYcle:AVG? 688

POWer:RIPPle:RESult:PDCYcle:NPEak? 688

POWer:RIPPle:RESult:PDCYcle:PPEak? 688

POWer:RIPPle:RESult:PDCYcle:STDDev? 688

POWer:RIPPle:RESult:PDCYcle:WFMCount? 688

POWer:RIPPle:RESult:PEAK[:ACTual]? 688

POWer:RIPPle:RESult:PEAK:AVG? 688

POWer:RIPPle:RESult:PEAK:NPEak? 688

POWer:RIPPle:RESult:PEAK:PPEak? 688

POWer:RIPPle:RESult:PEAK:STDDev? 688

POWer:RIPPle:RESult:PEAK:WFMCount? 688

POWer:RIPPle:RESult:PERiod[:ACTual]? 689

POWer:RIPPle:RESult:PERiod:AVG? 689

POWer:RIPPle:RESult:PERiod:NPEak? 689

POWer:RIPPle:RESult:PERiod:PPEak? 689

POWer:RIPPle:RESult:PERiod:STDDev? 689

POWer:RIPPle:RESult:PERiod:WFMCount? 689

POWer:RIPPle:RESult:STDDev[:ACTual]? 689

POWer:RIPPle:RESult:STDDev:AVG? 689

POWer:RIPPle:RESult:STDDev:NPEak? 689

POWer:RIPPle:RESult:STDDev:PPEak? 689

POWer:RIPPle:RESult:STDDev:STDDev? 689

POWer:RIPPle:RESult:STDDev:WFMCount? 689

POWer:RIPPle:RESult:UPEak[:ACTual]? 689

POWer:RIPPle:RESult:UPEak:AVG? 689

POWer:RIPPle:RESult:UPEak:NPEak? 689

POWer:RIPPle:RESult:UPEak:PPEak? 689

POWer:RIPPle:RESult:UPEak:STDDev? 690

POWer:RIPPle:RESult:UPEak:WFMCount? 690

### POWer:RIPPle:EXECute Starts the ripple measurement. Usage: Event

### POWer:RIPPle:REPort:ADD Adds the result to the report list. Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1921.htm -->

### POWer:RIPPle:RESult:FREQuency[:ACTual]? POWer:RIPPle:RESult:FREQuency:AVG?

### POWer:RIPPle:RESult:FREQuency:NPEak? POWer:RIPPle:RESult:FREQuency:PPEak? POWer:RIPPle:RESult:FREQuency:STDDev? POWer:RIPPle:RESult:FREQuency:WFMCount?

Returns the corresponding statistic result for the frequency.

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1922.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1923.htm -->

### POWer:RIPPle:RESult:LPEak[:ACTual]? POWer:RIPPle:RESult:LPEak:AVG?

### POWer:RIPPle:RESult:LPEak:NPEak? POWer:RIPPle:RESult:LPEak:PPEak? POWer:RIPPle:RESult:LPEak:STDDev? POWer:RIPPle:RESult:LPEak:WFMCount?

Returns the corresponding statistic result for "Vp-".

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1924.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

### POWer:RIPPle:RESult:MEAN[:ACTual]? POWer:RIPPle:RESult:MEAN:AVG?

### POWer:RIPPle:RESult:MEAN:NPEak? POWer:RIPPle:RESult:MEAN:PPEak? POWer:RIPPle:RESult:MEAN:STDDev?

### POWer:RIPPle:RESult:MEAN:WFMCount?

Returns the corresponding statistic result for "Mean".

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1925.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1926.htm -->

### POWer:RIPPle:RESult:NDCYcle[:ACTual]? POWer:RIPPle:RESult:NDCYcle:AVG?

### POWer:RIPPle:RESult:NDCYcle:NPEak? POWer:RIPPle:RESult:NDCYcle:PPEak? POWer:RIPPle:RESult:NDCYcle:STDDev? POWer:RIPPle:RESult:NDCYcle:WFMCount?

Returns the corresponding statistic result for the negative duty cycle.

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1927.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1928.htm -->

### POWer:RIPPle:RESult:PDCYcle[:ACTual]? POWer:RIPPle:RESult:PDCYcle:AVG?

### POWer:RIPPle:RESult:PDCYcle:NPEak? POWer:RIPPle:RESult:PDCYcle:PPEak? POWer:RIPPle:RESult:PDCYcle:STDDev? POWer:RIPPle:RESult:PDCYcle:WFMCount?

Returns the corresponding statistic result for the positive duty cycle.

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1929.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

### POWer:RIPPle:RESult:PEAK[:ACTual]? POWer:RIPPle:RESult:PEAK:AVG?

### POWer:RIPPle:RESult:PEAK:NPEak? POWer:RIPPle:RESult:PEAK:PPEak? POWer:RIPPle:RESult:PEAK:STDDev?

### POWer:RIPPle:RESult:PEAK:WFMCount?

Returns the corresponding statistic result for "Vpp".

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1930.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1931.htm -->

### POWer:RIPPle:RESult:PERiod[:ACTual]? POWer:RIPPle:RESult:PERiod:AVG?

### POWer:RIPPle:RESult:PERiod:NPEak? POWer:RIPPle:RESult:PERiod:PPEak? POWer:RIPPle:RESult:PERiod:STDDev? POWer:RIPPle:RESult:PERiod:WFMCount? Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1932.htm -->

### POWer:RIPPle:RESult:STDDev[:ACTual]? POWer:RIPPle:RESult:STDDev:AVG?

### POWer:RIPPle:RESult:STDDev:NPEak? POWer:RIPPle:RESult:STDDev:PPEak? POWer:RIPPle:RESult:STDDev:STDDev? POWer:RIPPle:RESult:STDDev:WFMCount?

Returns the corresponding statistic result for the standard deviation.

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1933.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

### POWer:RIPPle:RESult:UPEak[:ACTual]? POWer:RIPPle:RESult:UPEak:AVG?

### POWer:RIPPle:RESult:UPEak:NPEak? POWer:RIPPle:RESult:UPEak:PPEak?

### POWer:RIPPle:RESult:UPEak:STDDev? POWer:RIPPle:RESult:UPEak:WFMCount?

Returns the corresponding statistic result for "Vp+".

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1934.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1935.htm -->

### 18.14.10 Spectrum

POWer:SPECtrum:EXECute 690

POWer:SPECtrum:FREQuency 690

POWer:SPECtrum:REPort:ADD 690

POWer:SPECtrum:RESult<n>:FREQuency? 691

POWer:SPECtrum:RESult<n>:LEVel[:VALue]? 691

POWer:SPECtrum:RESult<n>:MAXimum? 691

POWer:SPECtrum:RESult<n>:MEAN? 691

POWer:SPECtrum:RESult<n>:MINimum? 691

POWer:SPECtrum:RESult<n>:RESet 692

POWer:SPECtrum:RESult<n>:WFMCount? 692

EXPort:POWer:NAME 692

EXPort:POWer:SAVE 692

### POWer:SPECtrum:EXECute Starts the spectrum measurement. Usage: Event

### POWer:SPECtrum:FREQuency <SwitchingFrequency> Sets the frequency of the input signal.

<!-- 来源：RTM2_UserManual_en_10_files\part1936.htm -->

### Parameters:

<SwitchingFrequency>

### POWer:SPECtrum:REPort:ADD Adds the result to the report list. Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1937.htm -->

### POWer:SPECtrum:RESult<n>:FREQuency?

Queries the frequency of the n-th order.

<!-- 来源：RTM2_UserManual_en_10_files\part1938.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1939.htm -->

### Return values:

<FrequencyValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1940.htm -->

### POWer:SPECtrum:RESult<n>:LEVel[:VALue]?

Queries the level of the n-th order.

<!-- 来源：RTM2_UserManual_en_10_files\part1941.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1942.htm -->

### Return values:

<LevelValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1943.htm -->

### POWer:SPECtrum:RESult<n>:MAXimum?

Queries the maximum level of the n-th order.

<!-- 来源：RTM2_UserManual_en_10_files\part1944.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1945.htm -->

### Return values:

<LevelMaximum>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1946.htm -->

### POWer:SPECtrum:RESult<n>:MEAN?

Queries the average level of the n-th order.

<!-- 来源：RTM2_UserManual_en_10_files\part1947.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1948.htm -->

### Return values:

<LevelAverage>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1949.htm -->

### POWer:SPECtrum:RESult<n>:MINimum?

Queries the minimum level of the n-th order.

<!-- 来源：RTM2_UserManual_en_10_files\part1950.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1951.htm -->

### Return values:

<LevelMinimum>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1952.htm -->

### POWer:SPECtrum:RESult<n>:RESet

Resets the count of the measurements.

<!-- 来源：RTM2_UserManual_en_10_files\part1953.htm -->

### Suffix:

<n> 1..40

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1954.htm -->

### POWer:SPECtrum:RESult<n>:WFMCount?

Queries the number of waveforms, for which the spectrum was measured.

<!-- 来源：RTM2_UserManual_en_10_files\part1955.htm -->

### Suffix:

<n> 1..40

<!-- 来源：RTM2_UserManual_en_10_files\part1956.htm -->

### Return values:

<VaveformCount>

### Usage: Query only

### EXPort:POWer:NAME <ExportPath>

Defines the path and filename of the results file, available for current harmonics and spectrum power measurements. The file format is CSV. If the file already exists, it will be overwritten.

<!-- 来源：RTM2_UserManual_en_10_files\part1957.htm -->

### Parameters:

<ExportPath> string

String parameter

<!-- 来源：RTM2_UserManual_en_10_files\part1958.htm -->

### EXPort:POWer:SAVE

```text
Saves statistical results of the indicated measurement place to the file that is defined by the EXPort:POWer:NAME command.
```

### Example: Current harmonics measurement: EXPort:POWer:NAME "/USB_FRONT/POWER/HARMONIC" EXPort:POWer:SAVE

The file contains the following data:

```text
"Power Analysis Results: Harmonics (CH2), 50 Hz, EN61000-3-2 A" "Current: Fail (1 / 40)"
"Total Pass: 0; Total Fail: 2" Order,Frequency[Hz],Level[V],Minimum[V],Maximum[V],Average[V], Limit[V],State 1,5.0049E+01,8.06691E+00,8.06691E+00,2.43617E+01,1.62143E+01,
1.60000E+01,Fail
2,1.0010E+02,9.52154E-03,7.72160E-03,9.52154E-03,8.62157E-03,
1.08000E+00,Pass
3,1.5015E+02,3.51324E-03,3.51324E-03,5.07817E-02,2.71475E-02,
2.30000E+00,Pass
4,1.9958E+02,2.47575E-03,2.47575E-03,3.74720E-03,3.11148E-03,
4.30000E-01,Pass
5,2.5024E+02,5.88447E-03,5.88447E-03,3.02487E-02,1.80666E-02,
1.14000E+00,Pass
6,2.9968E+02,7.02598E-03,1.27264E-03,7.02598E-03,4.14931E-03,
3.00000E-01,Pass
...
```

### Example: Spectrum measurement:

```text
EXPort:POWer:NAME "/USB_FRONT/POWER/SPECTRUM" EXPort:POWer:SAVE
```

The file contains the following data:

```text
"Power Analysis Results: Spectrum (CH1), 100kHz" "Total: 67"
Order,Frequency[Hz],Level[dBV],Minimum[dBV],Maximum[dBV],Average[dBV] 1,1.0009766E+05,-1.11840E+02,-1.19960E+02,-8.39799E+01,-1.03205E+02
2,1.9897461E+05,-1.03860E+02,-1.21000E+02,-8.97199E+01,-1.03222E+02
3,2.9907227E+05,-1.02660E+02,-1.22520E+02,-9.12399E+01,-1.03858E+02
4,4.0039062E+05,-1.08660E+02,-1.17400E+02,-9.24199E+01,-1.04547E+02
5,4.9926758E+05,-1.00340E+02,-1.11500E+02,-7.78199E+01,-9.44799E+01
6,6.0058594E+05,-1.10040E+02,-1.16040E+02,-9.39199E+01,-1.03913E+02
...
```

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1959.htm -->

### 18.14.11 Transient Response

POWer:TRANsient:EXECute 694

POWer:TRANsient:REPort:ADD 694

POWer:TRANsient:RESult:DELay? 694

POWer:TRANsient:RESult:OVERshoot? 694

POWer:TRANsient:RESult:PEAK:TIME? 694

POWer:TRANsient:RESult:PEAK:VALue? 694

POWer:TRANsient:RESult:RTIMe? 695

POWer:TRANsient:RESult:SETTlingtime? 695

POWer:TRANsient:SIGHigh 695

POWer:TRANsient:SIGLow 695

POWer:TRANsient:STARt 695

POWer:TRANsient:STOP 695

<!-- 来源：RTM2_UserManual_en_10_files\part1960.htm -->

### POWer:TRANsient:EXECute

Starts the transient response measurement.

### Usage: Event

### POWer:TRANsient:REPort:ADD Adds the result to the report list. Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1961.htm -->

### POWer:TRANsient:RESult:DELay?

Queries the delay time.

<!-- 来源：RTM2_UserManual_en_10_files\part1962.htm -->

### Return values:

<DeleayTime>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1963.htm -->

### POWer:TRANsient:RESult:OVERshoot?

Queries the overshoot.

<!-- 来源：RTM2_UserManual_en_10_files\part1964.htm -->

### Return values:

<Overshoot>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1965.htm -->

### POWer:TRANsient:RESult:PEAK:TIME?

Queries the peak time.

<!-- 来源：RTM2_UserManual_en_10_files\part1966.htm -->

### Return values:

<PeakTime>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1967.htm -->

### POWer:TRANsient:RESult:PEAK:VALue?

Queries the peak value.

<!-- 来源：RTM2_UserManual_en_10_files\part1968.htm -->

### Return values:

<PeakValue>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1969.htm -->

### POWer:TRANsient:RESult:RTIMe?

Queries the rise time.

<!-- 来源：RTM2_UserManual_en_10_files\part1970.htm -->

### Return values:

<RiseTime>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1971.htm -->

### POWer:TRANsient:RESult:SETTlingtime?

Queries the settling time.

<!-- 来源：RTM2_UserManual_en_10_files\part1972.htm -->

### Return values:

<SettlingTime>

### Usage: Query only

### POWer:TRANsient:SIGHigh <SignalHigh> Sets the expected signal high voltage value.

<!-- 来源：RTM2_UserManual_en_10_files\part1973.htm -->

### Parameters:

<SignalHigh>

### POWer:TRANsient:SIGLow <SignalLow> Sets the expected signal low voltage value.

<!-- 来源：RTM2_UserManual_en_10_files\part1974.htm -->

### Parameters:

<SignalLow>

### POWer:TRANsient:STARt <StartTime> Sets the start time.

<!-- 来源：RTM2_UserManual_en_10_files\part1975.htm -->

### Parameters:

<StartTime>

### POWer:TRANsient:STOP <StopTime> Sets the stop time.

<!-- 来源：RTM2_UserManual_en_10_files\part1976.htm -->

### Parameters:

<StopTime>

<!-- 来源：RTM2_UserManual_en_10_files\part1977.htm -->

### 18.14.12 Slew Rate

POWer:SLEWrate:DSAMple 696

POWer:SLEWrate:DTIMe 696

POWer:SLEWrate:EXECute 696

POWer:SLEWrate:REPort:ADD 696

POWer:SLEWrate:RESult:LPEak[:ACTual]? 696

POWer:SLEWrate:RESult:LPEak:AVG? 696

POWer:SLEWrate:RESult:LPEak:NPEak? 696

POWer:SLEWrate:RESult:LPEak:PPEak? 696

POWer:SLEWrate:RESult:LPEak:STDDev? 696

POWer:SLEWrate:RESult:LPEak:WFMCount? 696

POWer:SLEWrate:RESult:UPEak[:ACTual]? 697

POWer:SLEWrate:RESult:UPEak:AVG? 697

POWer:SLEWrate:RESult:UPEak:NPEak? 697

POWer:SLEWrate:RESult:UPEak:PPEak? 697

POWer:SLEWrate:RESult:UPEak:STDDev? 697

POWer:SLEWrate:RESult:UPEak:WFMCount? 697

### POWer:SLEWrate:DSAMple <DeltaSample>

Sets the number of samples that are used for the calculation of the slope.

<!-- 来源：RTM2_UserManual_en_10_files\part1978.htm -->

### Parameters:

<DeltaSample>

### POWer:SLEWrate:DTIMe <DeltaTime> Sets the delta time.

<!-- 来源：RTM2_UserManual_en_10_files\part1979.htm -->

### Parameters:

<DeltaTime>

### POWer:SLEWrate:EXECute Starts the slew rate measurement. Usage: Event

### POWer:SLEWrate:REPort:ADD Adds the result to the report list. Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1980.htm -->

### POWer:SLEWrate:RESult:LPEak[:ACTual]? POWer:SLEWrate:RESult:LPEak:AVG?

### POWer:SLEWrate:RESult:LPEak:NPEak? POWer:SLEWrate:RESult:LPEak:PPEak? POWer:SLEWrate:RESult:LPEak:STDDev? POWer:SLEWrate:RESult:LPEak:WFMCount?

Returns the corresponding statistic result for "Vp-".

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1981.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1982.htm -->

### POWer:SLEWrate:RESult:UPEak[:ACTual]? POWer:SLEWrate:RESult:UPEak:AVG?

### POWer:SLEWrate:RESult:UPEak:NPEak? POWer:SLEWrate:RESult:UPEak:PPEak? POWer:SLEWrate:RESult:UPEak:STDDev? POWer:SLEWrate:RESult:UPEak:WFMCount?

Returns the corresponding statistic result for "Vp+".

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1983.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1984.htm -->

### 18.14.13 Modulation Analysis

POWer:MODulation:TYPE 698

POWer:MODulation:EXECute 698

POWer:MODulation:REPort:ADD 698

POWer:MODulation:RESult:LPEak[:ACTual]? 698

POWer:MODulation:RESult:LPEak:AVG? 698

POWer:MODulation:RESult:LPEak:NPEak? 698

POWer:MODulation:RESult:LPEak:PPEak? 698

POWer:MODulation:RESult:LPEak:STDDev? 698

POWer:MODulation:RESult:LPEak:WFMCount? 698

POWer:MODulation:RESult:MEAN[:ACTual]? 699

POWer:MODulation:RESult:MEAN:AVG? 699

POWer:MODulation:RESult:MEAN:NPEak? 699

POWer:MODulation:RESult:MEAN:PPEak? 699

POWer:MODulation:RESult:MEAN:STDDev? 699

POWer:MODulation:RESult:MEAN:WFMCount? 699

POWer:MODulation:RESult:RMS[:ACTual]? 699

POWer:MODulation:RESult:RMS:AVG? 699

POWer:MODulation:RESult:RMS:NPEak? 699

POWer:MODulation:RESult:RMS:PPEak? 699

POWer:MODulation:RESult:RMS:STDDev? 699

POWer:MODulation:RESult:RMS:WFMCount? 699

POWer:MODulation:RESult:STDDev[:ACTual]? 700

POWer:MODulation:RESult:STDDev:AVG? 700

POWer:MODulation:RESult:STDDev:NPEak? 700

POWer:MODulation:RESult:STDDev:PPEak? 700

POWer:MODulation:RESult:STDDev:STDDev? 700

POWer:MODulation:RESult:STDDev:WFMCount? 700

POWer:MODulation:RESult:UPEak[:ACTual]? 700

POWer:MODulation:RESult:UPEak:AVG? 700

POWer:MODulation:RESult:UPEak:NPEak? 700

POWer:MODulation:RESult:UPEak:PPEak? 700

POWer:MODulation:RESult:UPEak:STDDev? 700

POWer:MODulation:RESult:UPEakWFMCount? 700

### POWer:MODulation:TYPE <ModulationType> Sets the modulation type.

<!-- 来源：RTM2_UserManual_en_10_files\part1985.htm -->

### Parameters:

<ModulationType> PERiod | FREQuencyPDCYcle | NDCYclePPWidth | NPWidth

<!-- 来源：RTM2_UserManual_en_10_files\part1986.htm -->

### POWer:MODulation:EXECute

Starts the modulation analysis measurement.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1987.htm -->

### POWer:MODulation:REPort:ADD

Adds the result to the report list.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part1988.htm -->

### POWer:MODulation:RESult:LPEak[:ACTual]? POWer:MODulation:RESult:LPEak:AVG?

### POWer:MODulation:RESult:LPEak:NPEak? POWer:MODulation:RESult:LPEak:PPEak? POWer:MODulation:RESult:LPEak:STDDev? POWer:MODulation:RESult:LPEak:WFMCount?

Returns the corresponding statistic result for "Vp-".

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1989.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1990.htm -->

### POWer:MODulation:RESult:MEAN[:ACTual]? POWer:MODulation:RESult:MEAN:AVG?

### POWer:MODulation:RESult:MEAN:NPEak? POWer:MODulation:RESult:MEAN:PPEak? POWer:MODulation:RESult:MEAN:STDDev? POWer:MODulation:RESult:MEAN:WFMCount?

Returns the corresponding statistic result for "Mean".

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1991.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1992.htm -->

### POWer:MODulation:RESult:RMS[:ACTual]? POWer:MODulation:RESult:RMS:AVG?

### POWer:MODulation:RESult:RMS:NPEak? POWer:MODulation:RESult:RMS:PPEak? POWer:MODulation:RESult:RMS:STDDev? POWer:MODulation:RESult:RMS:WFMCount?

Returns the corresponding statistic result for RMS.

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1993.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1994.htm -->

### POWer:MODulation:RESult:STDDev[:ACTual]? POWer:MODulation:RESult:STDDev:AVG?

### POWer:MODulation:RESult:STDDev:NPEak? POWer:MODulation:RESult:STDDev:PPEak? POWer:MODulation:RESult:STDDev:STDDev? POWer:MODulation:RESult:STDDev:WFMCount?

Returns the corresponding statistic result for the standard deviation.

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1995.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1996.htm -->

### POWer:MODulation:RESult:UPEak[:ACTual]? POWer:MODulation:RESult:UPEak:AVG?

### POWer:MODulation:RESult:UPEak:NPEak? POWer:MODulation:RESult:UPEak:PPEak? POWer:MODulation:RESult:UPEak:STDDev? POWer:MODulation:RESult:UPEakWFMCount?

Returns the corresponding statistic result for "Vp+".

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part1997.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part1998.htm -->

### 18.14.14 Dynamic ON Resistance

POWer:DONResistance:EXECute 701

POWer:DONResistance:GATE<n>:START 701

POWer:DONResistance:GATE<n>STOP 701

POWer:DONResistance:RESult:DONResistance? 701

POWer:DONResistance:REPort:ADD 701

<!-- 来源：RTM2_UserManual_en_10_files\part1999.htm -->

### POWer:DONResistance:EXECute

Starts the dynamic ON resistance measurement.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2000.htm -->

### POWer:DONResistance:GATE<n>:START

Sets the start time for the corresponding gate.

<!-- 来源：RTM2_UserManual_en_10_files\part2001.htm -->

### Suffix:

<n> 1..2

<!-- 来源：RTM2_UserManual_en_10_files\part2002.htm -->

### Return values:

<StartTime>

<!-- 来源：RTM2_UserManual_en_10_files\part2003.htm -->

### POWer:DONResistance:GATE<n>STOP

Sets the stop time for the corresponding gate.

<!-- 来源：RTM2_UserManual_en_10_files\part2004.htm -->

### Suffix:

<n> 1..2

<!-- 来源：RTM2_UserManual_en_10_files\part2005.htm -->

### Return values:

<StopTime>

<!-- 来源：RTM2_UserManual_en_10_files\part2006.htm -->

### POWer:DONResistance:RESult:DONResistance?

Queries the dynamic ON resistance value.

<!-- 来源：RTM2_UserManual_en_10_files\part2007.htm -->

### Return values:

<Value>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2008.htm -->

### POWer:DONResistance:REPort:ADD

Adds the result to the report list.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2009.htm -->

### 18.14.15 Efficiency

POWer:EFFiciency:EXECute 702

POWer:EFFiciency:REPort:ADD 702

POWer:EFFiciency:RESult:EFFiciency[:ACTual]? 702

POWer:EFFiciency:RESult:EFFiciency:AVG? 702

POWer:EFFiciency:RESult:EFFiciency:NPEak? 702

POWer:EFFiciency:RESult:EFFiciency:PPEak? 702

POWer:EFFiciency:RESult:EFFiciency:STDDev? 702

POWer:EFFiciency:RESult:EFFiciency:WFMCount? 702

POWer:EFFiciency:RESult:INPut:REALpower[:ACTual]? 702

POWer:EFFiciency:RESult:INPut:REALpower:AVG? 702

POWer:EFFiciency:RESult:INPut:REALpower:NPEak? 702

POWer:EFFiciency:RESult:INPut:REALpower:PPEak? 703

POWer:EFFiciency:RESult:INPut:REALpower:STDDev? 703

POWer:EFFiciency:RESult:INPut:REALpower:WFMCount? 703

POWer:EFFiciency:RESult:OUTPut:REALpower[:ACTual]? 703

POWer:EFFiciency:RESult:OUTPut:REALpower:AVG? 703

POWer:EFFiciency:RESult:OUTPut:REALpower:NPEak? 703

POWer:EFFiciency:RESult:OUTPut:REALpower:PPEak? 703

POWer:EFFiciency:RESult:OUTPut:REALpower:STDDev? 703

POWer:EFFiciency:RESult:OUTPut:REALpower:WFMCount? 703

### POWer:EFFiciency:EXECute Starts the efficiency measurement. Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2010.htm -->

### POWer:EFFiciency:REPort:ADD

Adds the result to the report list.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2011.htm -->

### POWer:EFFiciency:RESult:EFFiciency[:ACTual]? POWer:EFFiciency:RESult:EFFiciency:AVG?

### POWer:EFFiciency:RESult:EFFiciency:NPEak? POWer:EFFiciency:RESult:EFFiciency:PPEak? POWer:EFFiciency:RESult:EFFiciency:STDDev? POWer:EFFiciency:RESult:EFFiciency:WFMCount?

Returns the corresponding statistic result for the efficiency.

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part2012.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

### POWer:EFFiciency:RESult:INPut:REALpower[:ACTual]? POWer:EFFiciency:RESult:INPut:REALpower:AVG?

### POWer:EFFiciency:RESult:INPut:REALpower:NPEak?

### POWer:EFFiciency:RESult:INPut:REALpower:PPEak? POWer:EFFiciency:RESult:INPut:REALpower:STDDev? POWer:EFFiciency:RESult:INPut:REALpower:WFMCount?

Returns the corresponding statistic result for the input real power.

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part2013.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2014.htm -->

### POWer:EFFiciency:RESult:OUTPut:REALpower[:ACTual]? POWer:EFFiciency:RESult:OUTPut:REALpower:AVG?

### POWer:EFFiciency:RESult:OUTPut:REALpower:NPEak? POWer:EFFiciency:RESult:OUTPut:REALpower:PPEak? POWer:EFFiciency:RESult:OUTPut:REALpower:STDDev? POWer:EFFiciency:RESult:OUTPut:REALpower:WFMCount?

Returns the corresponding statistic result for the output real power.

- [:ACTual]: current measurement result

- AVG: average of the long-term measurement results

- NPEak: negative peak value of the long-term measurement results

- PPEak: positive peak value of the long-term measurement results

- STDDev: standard deviation of the long-term measurement results

- WFMCount: the number of waveforms used for the displayed results

<!-- 来源：RTM2_UserManual_en_10_files\part2015.htm -->

### Return values:

<WaveformCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2016.htm -->

### 18.14.16 Switching Loss

POWer:SWITching:TYPE 704

POWer:SWITching:EXECute 704

POWer:SWITching:GATE:CONDuction:STARt 704

POWer:SWITching:GATE:CONDuction:STOP 704

POWer:SWITching:GATE:NCONduction:STARt 704

POWer:SWITching:GATE:NCONduction:STOP 705

POWer:SWITching:GATE:SWAVe 705

POWer:SWITching:GATE:TOFF:STARt 705

POWer:SWITching:GATE:TOFF:STOP 705

POWer:SWITching:GATE:TON:STARt 705

POWer:SWITching:GATE:TON:STOP 705

POWer:SWITching:REPort:ADD 705

POWer:SWITching:RESult:CONDuction:ENERgy? 706

POWer:SWITching:RESult:CONDuction:POWer? 706

POWer:SWITching:RESult:NCONduction:ENERgy? 706

POWer:SWITching:RESult:NCONduction:POWer? 706

POWer:SWITching:RESult:TOFF:ENERgy? 706

POWer:SWITching:RESult:TOFF:POWer? 706

POWer:SWITching:RESult:TON:ENERgy? 707

POWer:SWITching:RESult:TON:POWer? 707

POWer:SWITching:RESult:TOTal:ENERgy? 707

POWer:SWITching:RESult:TOTal:POWer? 707

### POWer:SWITching:TYPE <MeasureType>

Sets the measurement type for the switching loss maesurment.

<!-- 来源：RTM2_UserManual_en_10_files\part2017.htm -->

### Parameters:

<MeasureType> ENERgy | POWer

<!-- 来源：RTM2_UserManual_en_10_files\part2018.htm -->

### POWer:SWITching:EXECute

Starts the switching loss measurement.

### Usage: Event

### POWer:SWITching:GATE:CONDuction:STARt <StartTime>

Sets the start time for the conduction gate. This value is simultaneously the stop time for the turn on gate.

<!-- 来源：RTM2_UserManual_en_10_files\part2019.htm -->

### Parameters:

<StartTime>

### POWer:SWITching:GATE:CONDuction:STOP <StopTime>

Sets the stop time for the conduction gate. This value is simultaneously the start time for the turn off gate.

<!-- 来源：RTM2_UserManual_en_10_files\part2020.htm -->

### Parameters:

<StopTime>

### POWer:SWITching:GATE:NCONduction:STARt <StartTime>

Sets the start time for the non conduction gate. This value is simultaneously the stop time for the turn off gate.

<!-- 来源：RTM2_UserManual_en_10_files\part2021.htm -->

### Parameters:

<StartTime>

### POWer:SWITching:GATE:NCONduction:STOP <StopTime> Sets the stop time for the non conduction gate.

<!-- 来源：RTM2_UserManual_en_10_files\part2022.htm -->

### Parameters:

<StopTime>

<!-- 来源：RTM2_UserManual_en_10_files\part2023.htm -->

### POWer:SWITching:GATE:SWAVe

Sets the cursor on the waveform.

### Usage: Event

### POWer:SWITching:GATE:TOFF:STARt <StartTime>

Sets the start time for the turn off gate. This value is simultaneously the stop time for the conduction gate.

<!-- 来源：RTM2_UserManual_en_10_files\part2024.htm -->

### Parameters:

<StartTime>

### POWer:SWITching:GATE:TOFF:STOP <StopTime> Sets the stop time for the turn off gate.

<!-- 来源：RTM2_UserManual_en_10_files\part2025.htm -->

### Parameters:

<StopTime>

### POWer:SWITching:GATE:TON:STARt <StartTime> Sets the start time for the turn on gate.

<!-- 来源：RTM2_UserManual_en_10_files\part2026.htm -->

### Parameters:

<StartTime>

### POWer:SWITching:GATE:TON:STOP <StopTime> Sets the stop time for the turn on gate.

<!-- 来源：RTM2_UserManual_en_10_files\part2027.htm -->

### Parameters:

<StopTime>

### POWer:SWITching:REPort:ADD Adds the result to the report list. Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2028.htm -->

### POWer:SWITching:RESult:CONDuction:ENERgy?

Queries the conduction energy.

<!-- 来源：RTM2_UserManual_en_10_files\part2029.htm -->

### Return values:

<ConductionEnergy>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2030.htm -->

### POWer:SWITching:RESult:CONDuction:POWer?

Queries the conduction power.

<!-- 来源：RTM2_UserManual_en_10_files\part2031.htm -->

### Return values:

<ConductionPower>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2032.htm -->

### POWer:SWITching:RESult:NCONduction:ENERgy?

Queries the non conduction energy.

<!-- 来源：RTM2_UserManual_en_10_files\part2033.htm -->

### Return values:

<NonConductionEnergy>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2034.htm -->

### POWer:SWITching:RESult:NCONduction:POWer?

Queries the non conduction power.

<!-- 来源：RTM2_UserManual_en_10_files\part2035.htm -->

### Return values:

<NonConductionPower>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2036.htm -->

### POWer:SWITching:RESult:TOFF:ENERgy?

Queries the turn off energy.

<!-- 来源：RTM2_UserManual_en_10_files\part2037.htm -->

### Return values:

<TurnOffEnergy>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2038.htm -->

### POWer:SWITching:RESult:TOFF:POWer?

Queries the turn off power.

<!-- 来源：RTM2_UserManual_en_10_files\part2039.htm -->

### Return values:

<TurnOffPower>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2040.htm -->

### POWer:SWITching:RESult:TON:ENERgy?

Queries the turn on energy.

<!-- 来源：RTM2_UserManual_en_10_files\part2041.htm -->

### Return values:

<TurnOnEnergy>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2042.htm -->

### POWer:SWITching:RESult:TON:POWer?

Queries the turn on power.

<!-- 来源：RTM2_UserManual_en_10_files\part2043.htm -->

### Return values:

<TurnOnPower>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2044.htm -->

### POWer:SWITching:RESult:TOTal:ENERgy?

Queries the total energy.

<!-- 来源：RTM2_UserManual_en_10_files\part2045.htm -->

### Return values:

<TotalEnergy>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2046.htm -->

### POWer:SWITching:RESult:TOTal:POWer?

Queries the total power.

<!-- 来源：RTM2_UserManual_en_10_files\part2047.htm -->

### Return values:

<TotalPower>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2048.htm -->

### 18.14.17 Turn ON/OFF

POWer:ONOFf:EXECute 707

POWer:ONOFf:MEASurement 707

POWer:ONOFf:REPort:ADD 708

POWer:ONOFf:RESult<n>:TIME? 708

<!-- 来源：RTM2_UserManual_en_10_files\part2049.htm -->

### POWer:ONOFf:EXECute

Starts the turn on/off measurement.

### Usage: Event

### POWer:ONOFf:MEASurement <MeasureType> Selects the turn on or the turn off measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part2050.htm -->

### Parameters:

<MeasureType> TON | TOFF

*RST: TON

<!-- 来源：RTM2_UserManual_en_10_files\part2051.htm -->

### POWer:ONOFf:REPort:ADD

Adds the result to the report list.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2052.htm -->

### POWer:ONOFf:RESult<n>:TIME?

Queries the turn on/ turn off time.

<!-- 来源：RTM2_UserManual_en_10_files\part2053.htm -->

### Suffix:

<n> 1..3

<!-- 来源：RTM2_UserManual_en_10_files\part2054.htm -->

### Return values:

<Value>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2055.htm -->

### 18.14.18 Safe Operating Area (S.O.A.)

### 18.14.18.1 S.O.A. Settings

POWer:SOA:EXECute 708

POWer:SOA:RESTart 709

POWer:SOA:SCALe:MASK 709

POWer:SOA:SCALe:DISPlay 709

POWer:SOA:LINear:ADD 709

POWer:SOA:LOGarithmic:ADD 709

POWer:SOA:LINear:INSert 709

POWer:SOA:LOGarithmic:INSert 709

POWer:SOA:LINear:POINt<m>:CURRent 709

POWer:SOA:LOGarithmic:POINt<m>:CURRent 709

POWer:SOA:LINear:POINt<m>:CURRent:MAXimum 710

POWer:SOA:LOGarithmic:POINt<m>:CURRent:MAXimum 710

POWer:SOA:LINear:POINt<m>:CURRent:MINimum 710

POWer:SOA:LOGarithmic:POINt<m>:CURRent:MINimum 710

POWer:SOA:LINear:POINt<m>:VOLTage 710

POWer:SOA:LOGarithmic:POINt<m>:VOLTage 710

POWer:SOA:LINear:REMove 710

POWer:SOA:LOGarithmic:REMove 710

<!-- 来源：RTM2_UserManual_en_10_files\part2056.htm -->

### POWer:SOA:EXECute

Starts the safe operating area (S.O.A.) measurement.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2057.htm -->

### POWer:SOA:RESTart

Restarts the measurement.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2058.htm -->

### POWer:SOA:SCALe:MASK <>

Sets the scale for the mask, linear or logarithmic.

<!-- 来源：RTM2_UserManual_en_10_files\part2059.htm -->

### POWer:SOA:SCALe:DISPlay <>

Sets a linear or a logarithmic scaled for the displayed results.

<!-- 来源：RTM2_UserManual_en_10_files\part2060.htm -->

### POWer:SOA:LINear:ADD

### POWer:SOA:LOGarithmic:ADD

Adds a point to the safe operation area definition list.

### Usage: Event

### POWer:SOA:LINear:INSert <InsertIndex>

### POWer:SOA:LOGarithmic:INSert <InsertIndex>

Inserts a point with the selected insert index in the list of the safe operating area mask definition.

<!-- 来源：RTM2_UserManual_en_10_files\part2061.htm -->

### Setting parameters:

<InsertIndex>

### Usage: Setting only

### POWer:SOA:LINear:POINt<m>:CURRent <Current>

<!-- 来源：RTM2_UserManual_en_10_files\part2062.htm -->

### POWer:SOA:LOGarithmic:POINt<m>:CURRent <Current>

Sets the maximum current for the indicated mask point. The minimum current is set to 0.

<!-- 来源：RTM2_UserManual_en_10_files\part2063.htm -->

### Suffix:

<m> *

Index of the mask point

<!-- 来源：RTM2_UserManual_en_10_files\part2064.htm -->

### Parameters:

<Current> Imax value

### POWer:SOA:LINear:POINt<m>:CURRent:MAXimum <MinimumCurrent>

### POWer:SOA:LOGarithmic:POINt<m>:CURRent:MAXimum <MinimumCurrent> Sets the maximum current for the corresponding point.

<!-- 来源：RTM2_UserManual_en_10_files\part2065.htm -->

### Suffix:

<m> *

<!-- 来源：RTM2_UserManual_en_10_files\part2066.htm -->

### Parameters:

<MinimumCurrent>

### POWer:SOA:LINear:POINt<m>:CURRent:MINimum <MaximumCurrent>

### POWer:SOA:LOGarithmic:POINt<m>:CURRent:MINimum <MaximumCurrent> Sets the minimum current for the corresponding point.

<!-- 来源：RTM2_UserManual_en_10_files\part2067.htm -->

### Suffix:

<m> *

<!-- 来源：RTM2_UserManual_en_10_files\part2068.htm -->

### Parameters:

<MaximumCurrent>

### POWer:SOA:LINear:POINt<m>:VOLTage <Voltage>

### POWer:SOA:LOGarithmic:POINt<m>:VOLTage <Voltage> Sets the voltage for the corresponding point.

<!-- 来源：RTM2_UserManual_en_10_files\part2069.htm -->

### Suffix:

<m> *

<!-- 来源：RTM2_UserManual_en_10_files\part2070.htm -->

### Parameters:

<Voltage>

### POWer:SOA:LINear:REMove <RemoveIndex>

### POWer:SOA:LOGarithmic:REMove <RemoveIndex>

Removes the point with the selcted index from the list of the safe operating area mask definition.

<!-- 来源：RTM2_UserManual_en_10_files\part2071.htm -->

### Setting parameters:

<RemoveIndex>

### Usage: Setting only

<!-- 来源：RTM2_UserManual_en_10_files\part2072.htm -->

### 18.14.19 S.O.A. Results

POWer:SOA:RESult:ACQuisition:TOLerance 711

POWer:SOA:RESult:TOTal:TOLerance 711

POWer:SOA:LINear:COUNt? 712

POWer:SOA:LOGarithmic:COUNt? 712

POWer:SOA:RESult:ACQuisition:FAILed? 712

POWer:SOA:RESult:ACQuisition:FRATe? 712

POWer:SOA:RESult:ACQuisition:PASSed? 712

POWer:SOA:RESult:ACQuisition:POINts? 712

POWer:SOA:RESult:ACQuisition:STATe? 712

POWer:SOA:RESult:ACQuisition:VCOunt? 713

POWer:SOA:RESult:ACQuisition:VIOLation<n>? 713

POWer:SOA:RESult:ACQuisition:VIOLation<n>:VOLTage? 713

POWer:SOA:RESult:ACQuisition:VIOLation<n>:CURRent? 713

POWer:SOA:RESult:TOTal:SAMPle:COUNt? 713

POWer:SOA:RESult:TOTal:SAMPle:FAILed? 714

POWer:SOA:RESult:TOTal:SAMPle:PASSed? 714

POWer:SOA:RESult:TOTal:COUNt? 714

POWer:SOA:RESult:TOTal:FAILed? 714

POWer:SOA:RESult:TOTal:FRATe? 714

POWer:SOA:RESult:TOTal:PASSed? 714

POWer:SOA:RESult:TOTal:STATe? 715

POWer:SOA:RESult:TOTal:VCOunt? 715

POWer:SOA:RESult:TOTal:VIOLation<n>? 715

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent? 715

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage? 715

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:HEADer? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:HEADer? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:XINCrement? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:XINCrement? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:XORigin? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:XORigin? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:YINCrement? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:YINCrement? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:YORigin? 717

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:YORigin? 717

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:YRESolution? 717

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:YRESolution? 717

### POWer:SOA:RESult:ACQuisition:TOLerance <Tolerance> Sets acquisition tolerance in percent.

<!-- 来源：RTM2_UserManual_en_10_files\part2073.htm -->

### Parameters:

<Tolerance>

### POWer:SOA:RESult:TOTal:TOLerance <Tolerance> Sets total tolerance in percent.

<!-- 来源：RTM2_UserManual_en_10_files\part2074.htm -->

### Parameters:

<Tolerance>

<!-- 来源：RTM2_UserManual_en_10_files\part2075.htm -->

### POWer:SOA:LINear:COUNt?

### POWer:SOA:LOGarithmic:COUNt?

Queries the number of points that included in the safe operating area mask description.

<!-- 来源：RTM2_UserManual_en_10_files\part2076.htm -->

### Return values:

<PointsCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2077.htm -->

### POWer:SOA:RESult:ACQuisition:FAILed?

Returns the number of points that failed, i.e they are not within the defined safe operat- ing area.

<!-- 来源：RTM2_UserManual_en_10_files\part2078.htm -->

### Return values:

<FailedPoints>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2079.htm -->

### POWer:SOA:RESult:ACQuisition:FRATe?

Returns the total point fail rate, i.e the ratio of point hits to the number of tested points for the current acquisition.

<!-- 来源：RTM2_UserManual_en_10_files\part2080.htm -->

### Return values:

<FailRate>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2081.htm -->

### POWer:SOA:RESult:ACQuisition:PASSed?

Returns the number of passed points, i.e they are within the defined safe operating area.

<!-- 来源：RTM2_UserManual_en_10_files\part2082.htm -->

### Return values:

<PassedPoints>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2083.htm -->

### POWer:SOA:RESult:ACQuisition:POINts?

Returns the number of points, considered for the current acquisition.

<!-- 来源：RTM2_UserManual_en_10_files\part2084.htm -->

### Return values:

<Points>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2085.htm -->

### POWer:SOA:RESult:ACQuisition:STATe?

Returns the result, passed or failed, of the current aqcuisition measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part2086.htm -->

### Return values:

<AcquisitionState> 0 | 1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2087.htm -->

### POWer:SOA:RESult:ACQuisition:VCOunt?

Returns the acquisition violation count.

<!-- 来源：RTM2_UserManual_en_10_files\part2088.htm -->

### Return values:

<ViolationCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2089.htm -->

### POWer:SOA:RESult:ACQuisition:VIOLation<n>?

Returns the current and voltage value for the corresponding acquisition violation.

<!-- 来源：RTM2_UserManual_en_10_files\part2090.htm -->

### Return values:

<Current>

<Voltage>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2091.htm -->

### POWer:SOA:RESult:ACQuisition:VIOLation<n>:VOLTage?

Returns the voltage value for the corresponding acquisition violation point.

<!-- 来源：RTM2_UserManual_en_10_files\part2092.htm -->

### Suffix:

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part2093.htm -->

### Return values:

<Voltage>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2094.htm -->

### POWer:SOA:RESult:ACQuisition:VIOLation<n>:CURRent?

Returns the current value for the corresponding acquisition violation point.

<!-- 来源：RTM2_UserManual_en_10_files\part2095.htm -->

### Suffix:

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part2096.htm -->

### Return values:

<Current>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2097.htm -->

### POWer:SOA:RESult:TOTal:SAMPle:COUNt?

Returns the total number of samples used to determine the total result.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2098.htm -->

### POWer:SOA:RESult:TOTal:SAMPle:FAILed?

Returns the total number of failed samples, i.e they are not within the defined safe operating area.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2099.htm -->

### POWer:SOA:RESult:TOTal:SAMPle:PASSed?

Returns the number of passed samples, i.e they are within the defined safe operating area.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2100.htm -->

### POWer:SOA:RESult:TOTal:COUNt?

Returns the total number of acquisitions used to determine the total result.

<!-- 来源：RTM2_UserManual_en_10_files\part2101.htm -->

### Return values:

<AcquisitionCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2102.htm -->

### POWer:SOA:RESult:TOTal:FAILed?

Returns the total number of failed acquisitions, i.e they are not within the defined safe operating area.

<!-- 来源：RTM2_UserManual_en_10_files\part2103.htm -->

### Return values:

<FailedAcquisitions>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2104.htm -->

### POWer:SOA:RESult:TOTal:FRATe?

Returns the total acquisition fail rate, i.e the ratio of acquisition hits to the number of tested acquisitions.

<!-- 来源：RTM2_UserManual_en_10_files\part2105.htm -->

### Return values:

<FailRate>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2106.htm -->

### POWer:SOA:RESult:TOTal:PASSed?

Returns the number of passed acquisitions, i.e they are within the defined safe operat- ing area.

<!-- 来源：RTM2_UserManual_en_10_files\part2107.htm -->

### Return values:

<PassedAcquisitions>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2108.htm -->

### POWer:SOA:RESult:TOTal:STATe?

Returns the result, passed or failed, of the total measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part2109.htm -->

### Return values:

<TotalState> 0 | 1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2110.htm -->

### POWer:SOA:RESult:TOTal:VCOunt?

Returns the total violation count.

<!-- 来源：RTM2_UserManual_en_10_files\part2111.htm -->

### Return values:

<ViolationCount>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2112.htm -->

### POWer:SOA:RESult:TOTal:VIOLation<n>?

Returns the current and voltage value for the corresponding total violation.

<!-- 来源：RTM2_UserManual_en_10_files\part2113.htm -->

### Return values:

<Current>

<Voltage>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2114.htm -->

### POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent?

Returns the current of the total violation.

<!-- 来源：RTM2_UserManual_en_10_files\part2115.htm -->

### Suffix:

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part2116.htm -->

### Return values:

<Current>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2117.htm -->

### POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage?

Returns the voltage of the total violation.

<!-- 来源：RTM2_UserManual_en_10_files\part2118.htm -->

### Suffix:

<n> *

<!-- 来源：RTM2_UserManual_en_10_files\part2119.htm -->

### Return values:

<Voltage>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2120.htm -->

### POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA? POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA?

Returns the data of the total voltage violation waveform in the same way as

```text
CHANnel<m>:DATA?.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2121.htm -->

### Return values:

<Header> StringData

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2122.htm -->

### POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:HEADer? POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:HEADer?

Returns information on the total violation current.

<!-- 来源：RTM2_UserManual_en_10_files\part2123.htm -->

### Return values:

<Header> StringData

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2124.htm -->

### POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:XINCrement? POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:XINCrement?

Return the time difference between two adjacent samples of the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part2125.htm -->

### Return values:

<Xincrement>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2126.htm -->

### POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:XORigin? POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:XORigin?

Return the time of the first sample of the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part2127.htm -->

### Return values:

<Xorigin>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2128.htm -->

### POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:YINCrement? POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:YINCrement?

Return the voltage value per bit of the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part2129.htm -->

### Return values:

<Yincrement>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2130.htm -->

### POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:YORigin? POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:YORigin?

Return the voltage value for binary value 0 of the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part2131.htm -->

### Return values:

<Yorigin>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2132.htm -->

### POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:YRESolution? POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:YRESolution?

Return the vertical bit resolution of the indicated waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part2133.htm -->

### Return values:

<Yresolution>

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2134.htm -->

## 18.15 Mixed Signal Option (MSO, R&S RTM-B1)

- Digital Channels - Activity Display 717

- Digital Channels - Configuration 718

- Waveform Data 721

- Parallel Buses 723

<!-- 来源：RTM2_UserManual_en_10_files\part2135.htm -->

### 18.15.1 Digital Channels - Activity Display

<!-- 来源：RTM2_UserManual_en_10_files\part2136.htm -->

### DIGital<m>:CURRent:STATe:MAXimum? DIGital<m>:CURRent:STATe:MINimum?

Both commands together return the current status of the indicated digital channel regardless of the trigger settings, and even without any acquisition.

| DIG:CURR:STAT:MIN returns | DIG:CURR:STAT:MAX returns | Signal |
| --- | --- | --- |
| 0 | 0 | Low |
| 1 | 1 | High |
| 0 | 1 | Toggle |

<!-- 来源：RTM2_UserManual_en_10_files\part2137.htm -->

### Suffix:

<m> 0. 15

Selects the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2138.htm -->

### Return values:

<CurrentState> Range: 0 | 1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2139.htm -->

### 18.15.2 Digital Channels - Configuration

DIGital<m>:DISPlay 718

DIGital<m>:TECHnology 718

DIGital<m>:THReshold 718

DIGital<m>:THCoupling 719

DIGital<m>:Hysteresis 719

DIGital<m>:DESKew 719

DIGital<m>:SIZE 719

DIGital<m>:POSition 720

DIGital<m>:LABel 720

DIGital<m>:LABel:STATe 720

### DIGital<m>:DISPlay <State>

Enables and displays the indicated digital channel, or disables it.

<!-- 来源：RTM2_UserManual_en_10_files\part2140.htm -->

### Suffix:

<m> 0. 15

Number of the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2141.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

### DIGital<m>:TECHnology <ThresholdMode>

Selects the threshold voltage for various types of integrated circuits and applies it to the channel group to which the indicated digital channel belongs.

<!-- 来源：RTM2_UserManual_en_10_files\part2142.htm -->

### Suffix:

<m> 0..15

Number of the digital channel.

Channel groups: 0..3; 4..7; 8..11; 12..15

<!-- 来源：RTM2_UserManual_en_10_files\part2143.htm -->

### Parameters:

<ThresholdMode> TTL | ECL | CMOS | MANual

TTL: 1.4 V

ECL: -1.3 V

CMOS: 2.5 V

MANual: Set a user-defined threshold value with DIGital<m>: THReshold

*RST: MAN

### DIGital<m>:THReshold <ThresholdLevel>

Sets the logical threshold for the channel group to which the indicated digital channel belongs.

<!-- 来源：RTM2_UserManual_en_10_files\part2144.htm -->

### Suffix:

<m> 0..15

Number of the digital channel.

Channel groups: 0..3; 4..7; 8..11; 12..15

<!-- 来源：RTM2_UserManual_en_10_files\part2145.htm -->

### Parameters:

<ThresholdLevel> *RST: 1.4

Default unit: V

### DIGital<m>:THCoupling <ThresholdCoupling>

Applies the last defined threshold and hysteresis values to all digital channels.

<!-- 来源：RTM2_UserManual_en_10_files\part2146.htm -->

### Suffix:

<m> 0. 15

Number of the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2147.htm -->

### Parameters:

<ThresholdCoupling> ON | OFF

<!-- 来源：RTM2_UserManual_en_10_files\part2148.htm -->

### DIGital<m>:Hysteresis

Defines the size of the hysteresis to avoid the change of signal states due to noise. The setting applied to the channel group to which the indicated digital channel belongs.

<!-- 来源：RTM2_UserManual_en_10_files\part2149.htm -->

### Suffix:

<m> 0..15

Number of the digital channel.

Channel groups: 0..3; 4..7; 8..11; 12..15

<!-- 来源：RTM2_UserManual_en_10_files\part2150.htm -->

### Parameters:

<Hysteresis> MAXimum | ROBust | NORMal

### DIGital<m>:DESKew <Deskew>

Sets the deskew value for the specified logic channel. The deskew value compensates delays that are known from the circuit specifics or caused by the different length of cables. The skew between the probe boxes of the digital channels and the probe con- nectors of the analog channels is automatically aligned by the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part2151.htm -->

### Suffix:

<m> 0..15

Selects the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2152.htm -->

### Parameters:

<Deskew> *RST: 0

Default unit: s

### DIGital<m>:SIZE <Size>

Sets the size of the indicated vertical channel.

<!-- 来源：RTM2_UserManual_en_10_files\part2153.htm -->

### Suffix:

<m> 0..15

Number of the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2154.htm -->

### Parameters:

<Size> SMALl | MEDium | LARGe | DIV1 | DIV2 | DIV4 | DIV8

<!-- 来源：RTM2_UserManual_en_10_files\part2155.htm -->

### DIV1 | DIV2 | DIV4 | DIV8

1, 2, 4, or 8 divisions per digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2156.htm -->

### SMALl | MEDium | LARGe

Size of the indicated digital channel is smaller than 1 div, about 1/4, 1/3, or 1/2 division, respectively.

*RST: SMAL

### DIGital<m>:POSition <Position>

Sets the vertical position of the indicated vertical channel.

<!-- 来源：RTM2_UserManual_en_10_files\part2157.htm -->

### Suffix:

<m> 0..15

Number of the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2158.htm -->

### Parameters:

<Position> Vertical position in divisions Default unit: DIV

### DIGital<m>:LABel <Label>

Defines a label for the indicated digital channel.

<!-- 来源：RTM2_UserManual_en_10_files\part2159.htm -->

### Suffix:

<m> 0..15

Number of the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2160.htm -->

### Parameters:

<Label> String value String parameter

### Example: DIGital4:LABel "Data"

Defines the label "Data" dor digital channel D4.

### DIGital<m>:LABel:STATe <State>

Displays or hides the label of the indicated digital channel.

<!-- 来源：RTM2_UserManual_en_10_files\part2161.htm -->

### Suffix:

<m> 0..15

Number of the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2162.htm -->

### Parameters:

<State> ON | OFF

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part2163.htm -->

### 18.15.3 Waveform Data

For data queries and conversion, consider also the following commands:

- FORMat[:DATA] on page 731

- DIGital<m>:DATA:XINCrement? on page 742

- DIGital<m>:DATA:XORigin? on page 742

- DIGital<m>:DATA:YINCrement? on page 743

- DIGital<m>:DATA:YORigin? on page 743

- DIGital<m>:DATA:YRESolution? on page 743

DIGital<m>:DATA? 721

DIGital<m>:DATA:HEADer? 721

DIGital<m>:DATA:POINts 722

<!-- 来源：RTM2_UserManual_en_10_files\part2164.htm -->

### DIGital<m>:DATA?

Returns the data of the specified digital channel for transmission from the instrument to the controlling computer. The waveforms data can be used in MATLAB, for example.

To set the export format, use FORMat[:DATA] on page 731.

```text
To set the range of samples to be returned, use DIGital<m>:DATA:POINts.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2165.htm -->

### Suffix:

<m> 0. 15

Selects the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2166.htm -->

### Parameters:

<WaveformData> List of values according to the format settings.

### Example: FORM ASC,0 DIG1:DATA?

```text
1,1,1,1,1,1,0,0,0,0,0,0,...
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2167.htm -->

### DIGital<m>:DATA:HEADer?

Returns information on the specified digital channel waveform.

#### Table 18-8: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Record length of the waveform in Samples | 200000 |
| 4 | Number of values per sample interval, usually 1. | 1 |

<!-- 来源：RTM2_UserManual_en_10_files\part2168.htm -->

### Suffix:

<m> 0..15

Selects the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2169.htm -->

### Parameters:

<Header> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,1

### Usage: Query only

### DIGital<m>:DATA:POINts <PointSelection>

```text
As a setting, the command selects a range of samples that will be returned with DIGital<m>:DATA?. As a query, it returns the number of returned samples for the selected range.
```

If ACQuire:WRATe is set to MSAMples (maximum sample rate), the memory usually contains more data samples than the screen can display. In this case, you can decide which data will be saved: samples stored in the memory or only the displayed samples.

### Note: The sample range can be changed only in STOP mode. If the acquisition is run- ning, DEF is always used automatically. If the acquisition has been stopped, data can be read from the memory, and all settings are available.

<!-- 来源：RTM2_UserManual_en_10_files\part2170.htm -->

### Suffix:

<m> 0..15

Selects the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2171.htm -->

### Setting parameters:

<PointSelection> DEFault | MAXimum | DMAXimum

Sets the range for data queries.

<!-- 来源：RTM2_UserManual_en_10_files\part2172.htm -->

### DEFault

Waveform samples that are visible as waveform points on the screen.

<!-- 来源：RTM2_UserManual_en_10_files\part2173.htm -->

### MAXimum

All waveform samples that are stored in the memory. Only avail- able if acquisition is stopped.

<!-- 来源：RTM2_UserManual_en_10_files\part2174.htm -->

### DMAXimum

Display maximum: Waveform samples stored in the current waveform record but only for the displayed time range. At maxi- mum waveform rate, the instrument stores more samples than visible on the screen, and DMAX returns more values than DEF. Only available if acquisition is stopped.

*RST: DEFault

<!-- 来源：RTM2_UserManual_en_10_files\part2175.htm -->

### Return values:

<Points> Number of data points in the selected range.

Default unit: Samples See also: CHANnel<m>:DATA:POINts

<!-- 来源：RTM2_UserManual_en_10_files\part2176.htm -->

### 18.15.4 Parallel Buses

- Parallel Bus - Line Configuration 723

- Parallel Clocked Bus - Control Wires Configuration 724

- Parallel Buses - Decode Results 725

### 18.15.4.1 Parallel Bus - Line Configuration

### BUS<b>:PARallel:WIDTh <BusWidth> Sets the number of lines to be analyzed.

<!-- 来源：RTM2_UserManual_en_10_files\part2177.htm -->

### Suffix:

<b> 1. 4

Selects the parallel bus.

<!-- 来源：RTM2_UserManual_en_10_files\part2178.htm -->

### Parameters:

<BusWidth> Range: 1 to 16

Increment: 1

*RST: 8

Default unit: Bit

### BUS<b>:CPARallel:WIDTh <BusWidth> Sets the number of lines to be analyzed.

<!-- 来源：RTM2_UserManual_en_10_files\part2179.htm -->

### Suffix:

<b> 1..4

Selects the parallel bus.

| Parameters: |  |  |
| --- | --- | --- |
| <BusWidth> | Range: | 1 to 15 (clock only) or 14 (clock and CS) |
|  | Increment: | 1 |
|  | *RST: | 4 |

Default unit: Bit

### BUS<b>:PARallel:DATA<m>:SOURce <DataSource>

### BUS<b>:CPARallel:DATA<m>:SOURce <DataSource> Defines the digital channel that is assigned to the selected bit.

Use the command for each bit of the bus.

<!-- 来源：RTM2_UserManual_en_10_files\part2180.htm -->

### Suffix:

<b> 1..4

Selects the parallel bus.

<m> Sets the bit number.

<!-- 来源：RTM2_UserManual_en_10_files\part2181.htm -->

### Parameters:

<DataSource> D0..D15

### Example: BUS:PARallel:Width 4 BUS:PARallel:DATA0:SOURce D8 BUS:PARallel:DATA1:SOURce D9 BUS:PARallel:DATA2:SOURce D10 BUS:PARallel:DATA3:SOURce D11

### 18.15.4.2 Parallel Clocked Bus - Control Wires Configuration

BUS<b>:CPARallel:CLOCk:SOURce 724

BUS<b>:CPARallel:CLOCK:SLOPe 724

BUS<b>:CPARallel:CS:ENABle 724

BUS<b>:CPARallel:CS:SOURce 725

BUS<b>:CPARallel:CS:POLarity 725

### BUS<b>:CPARallel:CLOCk:SOURce <ClockSource> Selects the digital channel that is used as clock line.

<!-- 来源：RTM2_UserManual_en_10_files\part2182.htm -->

### Suffix:

<b> 1. 4

Selects the parallel bus.

<!-- 来源：RTM2_UserManual_en_10_files\part2183.htm -->

### Parameters:

<ClockSource> D0..D15

*RST: D0

### BUS<b>:CPARallel:CLOCK:SLOPe <ClockSlope>

Selects if the data is sampled on the rising or falling slope of the clock, or on both edges (EITHer). The clock slope marks the begin of a new bit.

<!-- 来源：RTM2_UserManual_en_10_files\part2184.htm -->

### Suffix:

<b> 1..4

Selects the parallel bus.

<!-- 来源：RTM2_UserManual_en_10_files\part2185.htm -->

### Parameters:

<ClockSlope> POSitive | NEGative | EITHer

### BUS<b>:CPARallel:CS:ENABle <ChipSelectEnable> Enables and disables the chip select line.

<!-- 来源：RTM2_UserManual_en_10_files\part2186.htm -->

### Suffix:

<b> 1..4

Selects the parallel bus.

<!-- 来源：RTM2_UserManual_en_10_files\part2187.htm -->

### Parameters:

<ChipSelectEnable> ON | OFF

*RST: ON

### BUS<b>:CPARallel:CS:SOURce <ChipSelectSource> Selects the digital channel that is used as chip select line.

<!-- 来源：RTM2_UserManual_en_10_files\part2188.htm -->

### Suffix:

<b> 1..4

Selects the parallel bus.

<!-- 来源：RTM2_UserManual_en_10_files\part2189.htm -->

### Parameters:

<ChipSelectSource> D0..D15

*RST: D1

### BUS<b>:CPARallel:CS:POLarity <Polarity>

Selects wether the chip select signal is high active (high = 1) or low active (low = 1).

<!-- 来源：RTM2_UserManual_en_10_files\part2190.htm -->

### Suffix:

<b> 1..4

Selects the parallel bus.

<!-- 来源：RTM2_UserManual_en_10_files\part2191.htm -->

### Parameters:

<Polarity> POSitive | NEGative

POSitive = high active NEGative = low active

### 18.15.4.3 Parallel Buses - Decode Results

The commands to query results of decoded parallel clocked and unclocked buses are similar and described together in this chapter..

BUS<b>:PARallel:FCOunt? 725

BUS<b>:CPARallel:FCOunt? 725

BUS<b>:PARallel:FRAMe<n>:DATA? 726

BUS<b>:CPARallel:FRAMe<n>:DATA? 726

BUS<b>:PARallel:FRAMe<n>:STATe? 726

BUS<b>:CPARallel:FRAMe<n>:STATe? 726

BUS<b>:PARallel:FRAMe<n>:STARt? 726

BUS<b>:CPARallel:FRAMe<n>:STARt? 726

BUS<b>:PARallel:FRAMe<n>:STOP? 727

BUS<b>:CPARallel:FRAMe<n>:STOP? 727

<!-- 来源：RTM2_UserManual_en_10_files\part2192.htm -->

### BUS<b>:PARallel:FCOunt? BUS<b>:CPARallel:FCOunt?

Returns the number of decoded frames.

<!-- 来源：RTM2_UserManual_en_10_files\part2193.htm -->

### Suffix:

<b> 1. 4

Selects the parallel bus.

<!-- 来源：RTM2_UserManual_en_10_files\part2194.htm -->

### Return values:

<FrameCount> Total number of decoded frames.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2195.htm -->

### BUS<b>:PARallel:FRAMe<n>:DATA? BUS<b>:CPARallel:FRAMe<n>:DATA?

Returns the data words of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part2196.htm -->

### Suffix:

<b> 1..4

Selects the parallel bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part2197.htm -->

### Return values:

<FrameData> List of decimal values of data words

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2198.htm -->

### BUS<b>:PARallel:FRAMe<n>:STATe? BUS<b>:CPARallel:FRAMe<n>:STATe?

Returns the overall state of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part2199.htm -->

### Suffix:

<b> 1..4

Selects the parallel bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part2200.htm -->

### Return values:

<FrameStatus> OK | ERRor | INSufficient

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2201.htm -->

### BUS<b>:PARallel:FRAMe<n>:STARt? BUS<b>:CPARallel:FRAMe<n>:STARt?

Returns the start time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part2202.htm -->

### Suffix:

<b> 1..4

Selects the parallel bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part2203.htm -->

### Return values:

<StartTime> Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2204.htm -->

### BUS<b>:PARallel:FRAMe<n>:STOP? BUS<b>:CPARallel:FRAMe<n>:STOP?

Returns the end time of the specified frame.

<!-- 来源：RTM2_UserManual_en_10_files\part2205.htm -->

### Suffix:

<b> 1..4

Selects the parallel bus.

<n> *

Selects the frame.

<!-- 来源：RTM2_UserManual_en_10_files\part2206.htm -->

### Return values:

<StopTime> Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2207.htm -->

## 18.16 Digital Voltmeter and Counter (Option R&S RTM-K32)

<!-- 来源：RTM2_UserManual_en_10_files\part2208.htm -->

### 18.16.1 Counter Settings and Results

TCOunter<t>:ENAB 727

TCOunter<t>:RESult[:ACTual]:FREQuency? 727

TCOunter<t>:RESult[:ACTual]:PERiod? 728

### TCOunter<t>:ENAB <Enable>

Enables or disables the trigger counter measurements.

<!-- 来源：RTM2_UserManual_en_10_files\part2209.htm -->

### Suffix:

<t> 1. 2

The suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part2210.htm -->

### Parameters:

<Enable> ON | OFF

*RST: OFF

<!-- 来源：RTM2_UserManual_en_10_files\part2211.htm -->

### TCOunter<t>:RESult[:ACTual]:FREQuency?

Returns the frequency of the trigger source.

<!-- 来源：RTM2_UserManual_en_10_files\part2212.htm -->

### Suffix:

<t> 1..2

1 = A-trigger source, 2 = B-trigger source

<!-- 来源：RTM2_UserManual_en_10_files\part2213.htm -->

### Return values:

<FrequencyValue> Default unit: Hz

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2214.htm -->

### TCOunter<t>:RESult[:ACTual]:PERiod?

Returns the period of the trigger source.

<!-- 来源：RTM2_UserManual_en_10_files\part2215.htm -->

### Suffix:

<t> 1..2

1 = A-trigger source, 2 = B-trigger source

<!-- 来源：RTM2_UserManual_en_10_files\part2216.htm -->

### Return values:

<PeriodValue> Default unit: s

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2217.htm -->

### 18.16.2 Digital Voltmeter Settings and Results

The DVM suffix <m> sets the number of the DVM measurement (measurement place).

DVM<m>:ENABle 728

DVM<m>:SOURce 728

DVM<m>:TYPE 728

DVM<m>:POSition 729

DVM<m>:RESult[:ACTual]? 729

DVM<m>:RESult[:ACTual]:STATus? 729

### DVM<m>:ENABle <VoltmeterEnable>

Enables and disables all configured voltmeter measurements.

<!-- 来源：RTM2_UserManual_en_10_files\part2218.htm -->

### Parameters:

<VoltmeterEnable> ON | OFF

*RST: OFF

### DVM<m>:SOURce <Source>

Sets the measurement source for the indicated DVM measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part2219.htm -->

### Parameters:

<Source> CH1 | CH2 | CH3 | CH4

CH3 and CH4 are only available with 4-channel instruments.

### DVM<m>:TYPE <MeasurementType>

Sets the measurement type for the indicated DVM measurement. Set OFF to disable the measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part2220.htm -->

### Parameters:

<MeasurementType> DC | ACDCrms | ACRMs | UPEakvalue | LPEakvalue | PEAK | CRESt | OFF

DC: mean value of the signal ACDCrms: RMS value of the signal

ACRMs: RMS value of the signal's AC component UPEakvalue: maximum value

LPEakvalue: minimum value

PEAK: peak-to-peak value (maximum - minimum) CRESt: crest factor (|X| max /X RMS )

OFF - disables the measurement.

*RST: DC for <m> = 1; for other measurements OFF

### DVM<m>:POSition <Position>

Sets the corner of the screen in which the measurement results are displayed.

<!-- 来源：RTM2_UserManual_en_10_files\part2221.htm -->

### Parameters:

<Position> TLEFt | TRIGht | BLEFt | BRIGht

TLEFt - top left corner TRIGht - top right corner BLEFt - bottom left corner BRIGht - bottom right corner

*RST: TLEF

<!-- 来源：RTM2_UserManual_en_10_files\part2222.htm -->

### DVM<m>:RESult[:ACTual]?

Returns the current value of the indicated measurement.

<!-- 来源：RTM2_UserManual_en_10_files\part2223.htm -->

### Return values:

<CurrentValue> Numeric value

### Example: DVM2:SOUR CH2 DVM2:TYPE DCRMs DVM2:RES?

```text
<-- 7.089E-01
```

An RMS measurement is performed on measurement place 2, on channel 2. The result is 708,9 mV.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2224.htm -->

### DVM<m>:RESult[:ACTual]:STATus?

Returns the result value and the status of the result.

The status is the decimal representation of a 4-bit register value:

- Bit 0 = 1: result is valid

- Bit 1 = 1: no result available

- Bit 2 = 1: clipping occurs

- Bit 3 = 1: no period found

<!-- 来源：RTM2_UserManual_en_10_files\part2225.htm -->

### Return values:

<ResultAndStatus> <Value>,Status

### Example: DVM:SOUR CH1 DVM:TYPE MEAN DVM:RES:STAT?

```text
<-- 4.968E-01,5
```

The result value of the mean measurement on channel 1 is

496.1 mV. The result status is 5 (decimal) = 0101 (binary). That means, the result is valid (bit 0 = 1), and the signal is clipped by the limits of the ADC range (bit 3 = 1).

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2226.htm -->

## 18.17 Data and File Management

This chapter describes commands on how to transfer data from the instrument to a computer, how to print and save screenshots, and how to manage measurement set- tings.

- Waveform Data Transfer 730

- Waveform Data Export to File 744

- Instrument Settings 745

- Screenshots 751

<!-- 来源：RTM2_UserManual_en_10_files\part2227.htm -->

### 18.17.1 Waveform Data Transfer

This chapter describes data transfer commands that have effect on other commands in different applications of the instrument, and transfer commands that work in the same way.

FORMat[:DATA] 731

FORMat:BORDer 733

CHANnel<m>:DATA? 733

CHANnel<m>:DATA:HEADer? 734

CHANnel<m>:DATA:POINts 734

CHANnel<m>:DATA:ENVelope? 735

CHANnel<m>:DATA:ENVelope:HEADer? 736

CALCulate:MATH<m>:DATA? 736

CALCulate:MATH<m>:DATA:HEADer? 737

CALCulate:MATH<m>:DATA:POINts? 737

CALCulate:MATH<m>:DATA:ENVelope? 737

CALCulate:MATH<m>:DATA:ENVelope:HEADer? 738

CALCulate:MATH<m>:DATA:ENVelope:POINts? 738

DIGital<m>:DATA? 738

DIGital<m>:DATA:HEADer? 739

DIGital<m>:DATA:POINts 739

MASK:DATA? 740

MASK:DATA:HEADer? 740

REFCurve<m>:DATA? 741

REFCurve<m>:DATA:HEADer? 741

REFCurve<m>:DATA:POINts? 742

CHANnel<m>:DATA:XORigin? 742

CHANnel<m>:DATA:ENVelope:XORigin? 742

CALCulate:MATH<m>:DATA:XORigin? 742

CALCulate:MATH<m>:DATA:ENVelope:XORigin? 742

MASK:DATA:XORigin? 742

DIGital<m>:DATA:XORigin? 742

REFCurve<m>:DATA:XORigin? 742

CHANnel<m>:DATA:XINCrement? 742

CHANnel<m>:DATA:ENVelope:XINCrement? 742

CALCulate:MATH<m>:DATA:XINCrement? 742

CALCulate:MATH<m>:DATA:ENVelope:XINCrement? 742

MASK:DATA:XINCrement? 742

DIGital<m>:DATA:XINCrement? 742

REFCurve<m>:DATA:XINCrement? 742

CHANnel<m>:DATA:YORigin? 743

CHANnel<m>:DATA:ENVelope:YORigin? 743

CALCulate:MATH<m>:DATA:YORigin? 743

CALCulate:MATH<m>:DATA:ENVelope:YORigin? 743

MASK:DATA:YORigin? 743

DIGital<m>:DATA:YORigin? 743

REFCurve<m>:DATA:YORigin? 743

CHANnel<m>:DATA:YINCrement? 743

CHANnel<m>:DATA:ENVelope:YINCrement? 743

CALCulate:MATH<m>:DATA:YINCrement? 743

CALCulate:MATH<m>:DATA:ENVelope:YINCrement? 743

MASK:DATA:YINCrement? 743

DIGital<m>:DATA:YINCrement? 743

REFCurve<m>:DATA:YINCrement? 743

CHANnel<m>:DATA:YRESolution? 743

CHANnel<m>:DATA:ENVelope:YRESolution? 743

CALCulate:MATH<m>:DATA:YRESolution? 743

CALCulate:MATH<m>:DATA:ENVelope:YRESolution? 743

MASK:DATA:YRESolution? 743

DIGital<m>:DATA:YRESolution? 743

REFCurve<m>:DATA:YRESolution? 743

### FORMat[:DATA] <DataFormat>,<Accuracy> Defines the format for data export with

- CHANnel<m>:DATA? on page 428

- CHANnel<m>:DATA:ENVelope? on page 429

- CALCulate:MATH<m>:DATA? on page 499

- REFCurve<m>:DATA? on page 474

- MASK:DATA? on page 529

<!-- 来源：RTM2_UserManual_en_10_files\part2228.htm -->

### Parameters:

<DataFormat> ASCii | REAL | UINTeger

<!-- 来源：RTM2_UserManual_en_10_files\part2229.htm -->

### ASCii

List of values, for example, 1.23,1.22,1.24,..

<Accuracy> is 0 which means that the instrument selects the number of digits to be returned. The query returns ASC,0.

<!-- 来源：RTM2_UserManual_en_10_files\part2230.htm -->

### REAL

Binary format. <Accuracy> is 32. The query returns REAL,32. The data is stored as binary data (Definite Length Block Data according to IEEE 488.2). Each waveform value is formatted in 32 Bit IEEE 754 Floating-Point-Format.

The schema of the result string is as follows:

```text
#41024<value1><value2>…<value n> with:
#4 = number of digits of the following number (= 4 in the exam- ple)
1024 = number of following data bytes (= 1024 in the example)
<value> = 4-byte floating point values
```

<!-- 来源：RTM2_UserManual_en_10_files\part2231.htm -->

### UINTeger

Unsigned integer format, binary values with length 8 bit (1 byte per sample), 16 bit (2 bytes per sample) or 32 bit (4 bytes per sample): UINT,8 or UINT,16 or UINT,32.

The data range for UINT,8 is 0 to 255, the data range for

UINT,16 is 0 to 65.535 and for UINT,32 is 2 32 - 1.

The schema of the result string is the same as for REAL format. For data conversion, you need the results of following com- mands:

```text
...:DATA:XORigin?;...:DATA:XINCrement?;..:DATA:
Yorigin?;...:DATA:YINCrement?;...:DATA: YRESolution?. They are described below in this chapter. The way of data conversion is described in Chapter 18.2.1.2, "Read- ing Waveform Data in Unsigned Integer Format", on page 406. 32 bit data is relevant for average waveforms if averaging 512 or 1024 waveforms. The resulting data is 17 bits long (512 wave- forms) or 18 bit (1024 waveforms).
```

*RST: ASC

<Accuracy> 0 | 8 | 16 | 32

Length of a data value in bit 0 - for ASC only

32 - for REAL

8 | 16 | 32 - for UINT

*RST: 0

### Example: Set the ASCII data format:

```text
FORM ASC
```

### Example: Query for data format:

```text
FORM?
-> ASC,0
```

### Example: Set the unsigned integer format, 16 bit data length:

```text
FORM UINT,16
```

### FORMat:BORDer <ByteOrder>

Defines the byte order for binary data export if FORMat[:DATA] is set to REAL or

```text
UINT,16|32.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2232.htm -->

### Parameters:

<ByteOrder> MSBFirst | LSBFirst

<!-- 来源：RTM2_UserManual_en_10_files\part2233.htm -->

### MSBFirst

Big endian, most significant byte first

<!-- 来源：RTM2_UserManual_en_10_files\part2234.htm -->

### LSBFirst

Little endian, least significant byte first

*RST: MSBF

### Example: See Chapter 18.2.1.1, "Reading Waveform Data in Real For- mat", on page 405

| ByteOrder | 8 bit | 16 bit | 32 bit |
| --- | --- | --- | --- |
| MSBF | 0xab | 0xAB CD | 0xAB CD 00 00 |
| LSBF | not relevant | 0xCD AB | 0x00 00 CD AB |

<!-- 来源：RTM2_UserManual_en_10_files\part2235.htm -->

### CHANnel<m>:DATA?

Returns the data of the analog channel waveform for transmission from the instrument to the controlling computer. The waveforms data can be used in MATLAB, for example.

To set the export format, use FORMat[:DATA] on page 731.

```text
To set the range of samples to be returned, use CHANnel<m>:DATA:POINts. For envelope waveforms, use the CHANnel<m>:DATA:ENVelope? command. Suffix:
```

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part2236.htm -->

### Return values:

<Data> List of values according to the format settings - the voltages of recorded waveform samples.

### Example: FORM ASC CHAN1:DATA?

```text
-0.125000,-0.123016,-0.123016,-0.123016,
-0.123016,-0.123016,...
```

### Example: See Chapter 18.2.1, "Data Export", on page 405

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2237.htm -->

### CHANnel<m>:DATA:HEADer?

Returns information on the channel waveform. For envelope waveforms, use the

```text
CHANnel<m>:DATA:ENVelope:HEADer? command.
```

#### Table 18-9: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Record length of the waveform in Samples | 200000 |
| 4 | Number of values per sample interval, usually 1. | 1 |

<!-- 来源：RTM2_UserManual_en_10_files\part2238.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part2239.htm -->

### Return values:

<DataHeader> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,1

### Usage: Query only

### CHANnel<m>:DATA:POINts <Points>

```text
As a setting, the command selects a range of samples that will be returned with CHANnel<m>:DATA? and CHANnel<m>:DATA:ENVelope?. As a query, it returns the number of returned samples for the selected range.
```

If ACQuire:WRATe is set to MSAMples (maximum sample rate), the memory usually contains more data samples than the screen can display. In this case, you can decide which data will be saved: samples stored in the memory or only the displayed samples.

### Note: The sample range can only be changed in STOP mode. If the acquisition is run- ning, DEF is always used automatically. If the acquisition has been stopped, data can be read from the memory, and all settings are available.

<!-- 来源：RTM2_UserManual_en_10_files\part2240.htm -->

### Suffix:

<m> 1..4

The command affects all channels, and the suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part2241.htm -->

### Setting parameters:

<Points> DEFault | MAXimum | DMAXimum Sets the range for data queries.

<!-- 来源：RTM2_UserManual_en_10_files\part2242.htm -->

### DEFault

Waveform points that are visible on the screen. At maximum waveform rate, the instrument stores more samples than visible on the screen, and DEF returns less values than acquired.

<!-- 来源：RTM2_UserManual_en_10_files\part2243.htm -->

### MAXimum

All waveform samples that are stored in the memory. Only avail- able if acquisition is stopped.

<!-- 来源：RTM2_UserManual_en_10_files\part2244.htm -->

### DMAXimum

Display maximum: Waveform samples stored in the current waveform record but only for the displayed time range. At maxi- mum waveform rate, the instrument stores more samples than visible on the screen, and DMAX returns more values than DEF. Only available if acquisition is stopped.

*RST: DEFault

<!-- 来源：RTM2_UserManual_en_10_files\part2245.htm -->

### Return values:

<Points> Number of data points in the selected range.

Default unit: Samples

### Example: CHAN:DATA:POIN DEF CHAN:DATA:POIN?;:CHAN2:DATA:POIN?

Returned values: 10416;10416 CHAN:DATA:POIN DMAX CHAN:DATA:POIN?;:CHAN2:DATA:POIN?

Returned values: 124992;124992 CHAN:DATA:POIN MAX CHAN:DATA:POIN?;:CHAN2:DATA:POIN?

Returned values: 4194302;4194302

### Example: See Chapter 18.2.1.1, "Reading Waveform Data in Real For- mat", on page 405

<!-- 来源：RTM2_UserManual_en_10_files\part2246.htm -->

### CHANnel<m>:DATA:ENVelope?

Returns the data of the envelope. The envelope consists of two waveforms. The wave- forms data can be used in MATLAB, for example.

Use this command only for envelope waveforms. For other channel waveforms use

```text
CHANnel<m>:DATA?.
```

To set the export format, use FORMat[:DATA] on page 731.

```text
To set the range of samples to be returned, use CHANnel<m>:DATA:POINts.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2247.htm -->

### Suffix:

<m> 1..4

Selects the input channel. The number of channels depends on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part2248.htm -->

### Return values:

<Data> List of values according to the format settings - the voltages of the envelope points. The list contains two values for each sam- ple interval.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2249.htm -->

### CHANnel<m>:DATA:ENVelope:HEADer?

Returns information on the envelope waveform.

Use this command only for envelope waveforms. for all other channel waveforms use

```text
CHANnel<m>:DATA:HEADer?.
```

#### Table 18-10: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Number of samples | 200000 |
| 4 | Number of values per sample interval. For envelope waveforms the value is 2. | 2 |

<!-- 来源：RTM2_UserManual_en_10_files\part2250.htm -->

### Suffix:

<m> 1..4

<!-- 来源：RTM2_UserManual_en_10_files\part2251.htm -->

### Return values:

<DataHeader> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,2

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2252.htm -->

### CALCulate:MATH<m>:DATA?

Returns the data of the math waveform points for transmission from the instrument to the controlling computer. The waveforms data can be used in MATHLAB, for example.

To set the export format, use FORMat[:DATA] on page 731.

<!-- 来源：RTM2_UserManual_en_10_files\part2253.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part2254.htm -->

### Return values:

<Data> List of values according to the format settings - voltages, or magnitudes of a spectrum.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2255.htm -->

### CALCulate:MATH<m>:DATA:HEADer?

Returns information on the math waveform.

#### Table 18-11: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Record length of the waveform in Samples | 200000 |
| 4 | Number of values per sample interval, usually 1. | 1 |

<!-- 来源：RTM2_UserManual_en_10_files\part2256.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part2257.htm -->

### Return values:

<Header> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2258.htm -->

### CALCulate:MATH<m>:DATA:POINts?

```text
Returns the number of data samples that are returned with CALCulate:MATH<m>: DATA?.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2259.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part2260.htm -->

### Return values:

<DataPoints> Amount of data points

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2261.htm -->

### CALCulate:MATH<m>:DATA:ENVelope?

Returns the data of FFT envelope waveforms ( CALCulate:MATH<m>:ARIThmetics is set to ENV ). The envelope consists of two waveforms. The data of the two wave- forms is written into one data stream in interleaved order.

Use this command only for envelope waveforms. For other FFT and math waveforms, use CALCulate:MATH<m>:DATA? on page 499.

To set the export format, use FORMat[:DATA] on page 731.

<!-- 来源：RTM2_UserManual_en_10_files\part2262.htm -->

### Suffix:

<m> 1..4

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part2263.htm -->

### Return values:

<Data> List of values according to the format settings - the voltages of the envelope points. The list contains two values for each sam- ple interval.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2264.htm -->

### CALCulate:MATH<m>:DATA:ENVelope:HEADer?

Returns information on the envelope waveform.

Use this command only for envelope waveforms. For all other FFT waveforms, use

```text
CALCulate:MATH<m>:DATA:HEADer?.
```

#### Table 18-12: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Number of samples | 200000 |
| 4 | Number of values per sample interval. For envelope waveforms the value is 2. | 2 |

<!-- 来源：RTM2_UserManual_en_10_files\part2265.htm -->

### Suffix:

<m> 1..4

The numeric suffix is irrelevant.

<!-- 来源：RTM2_UserManual_en_10_files\part2266.htm -->

### Return values:

<Header> Comma-separated value list, string data

Example: -9.477E-008,9.477E-008,200000,2

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2267.htm -->

### CALCulate:MATH<m>:DATA:ENVelope:POINts?

```text
Returns the number of data samples that are returned with CALCulate:MATH<m>: DATA:ENVelope?.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2268.htm -->

### Suffix:

<m> 1..4

Selects the math waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part2269.htm -->

### Return values:

<DataPoints> Amount of data points

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2270.htm -->

### DIGital<m>:DATA?

Returns the data of the specified digital channel for transmission from the instrument to the controlling computer. The waveforms data can be used in MATLAB, for example.

To set the export format, use FORMat[:DATA] on page 731.

```text
To set the range of samples to be returned, use DIGital<m>:DATA:POINts.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2271.htm -->

### Suffix:

<m> 0..15

Selects the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2272.htm -->

### Parameters:

<WaveformData> List of values according to the format settings.

### Example: FORM ASC,0 DIG1:DATA?

```text
1,1,1,1,1,1,0,0,0,0,0,0,...
```

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2273.htm -->

### DIGital<m>:DATA:HEADer?

Returns information on the specified digital channel waveform.

#### Table 18-13: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Record length of the waveform in Samples | 200000 |
| 4 | Number of values per sample interval, usually 1. | 1 |

<!-- 来源：RTM2_UserManual_en_10_files\part2274.htm -->

### Suffix:

<m> 0..15

Selects the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2275.htm -->

### Parameters:

<Header> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,1

### Usage: Query only

### DIGital<m>:DATA:POINts <PointSelection>

```text
As a setting, the command selects a range of samples that will be returned with DIGital<m>:DATA?. As a query, it returns the number of returned samples for the selected range.
```

If ACQuire:WRATe is set to MSAMples (maximum sample rate), the memory usually contains more data samples than the screen can display. In this case, you can decide which data will be saved: samples stored in the memory or only the displayed samples.

### Note: The sample range can be changed only in STOP mode. If the acquisition is run- ning, DEF is always used automatically. If the acquisition has been stopped, data can be read from the memory, and all settings are available.

<!-- 来源：RTM2_UserManual_en_10_files\part2276.htm -->

### Suffix:

<m> 0..15

Selects the digital channel

<!-- 来源：RTM2_UserManual_en_10_files\part2277.htm -->

### Setting parameters:

<PointSelection> DEFault | MAXimum | DMAXimum

Sets the range for data queries.

<!-- 来源：RTM2_UserManual_en_10_files\part2278.htm -->

### DEFault

Waveform samples that are visible as waveform points on the screen.

<!-- 来源：RTM2_UserManual_en_10_files\part2279.htm -->

### MAXimum

All waveform samples that are stored in the memory. Only avail- able if acquisition is stopped.

<!-- 来源：RTM2_UserManual_en_10_files\part2280.htm -->

### DMAXimum

Display maximum: Waveform samples stored in the current waveform record but only for the displayed time range. At maxi- mum waveform rate, the instrument stores more samples than visible on the screen, and DMAX returns more values than DEF. Only available if acquisition is stopped.

*RST: DEFault

<!-- 来源：RTM2_UserManual_en_10_files\part2281.htm -->

### Return values:

<Points> Number of data points in the selected range.

Default unit: Samples See also: CHANnel<m>:DATA:POINts

<!-- 来源：RTM2_UserManual_en_10_files\part2282.htm -->

### MASK:DATA?

Returns the data of the mask. The mask consists of two limit curves. To set the export format, use FORMat[:DATA] on page 731.

<!-- 来源：RTM2_UserManual_en_10_files\part2283.htm -->

### Return values:

<Data> List of values according to the format settings - the y-values of the mask points. The list contains two values for each sample interval.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2284.htm -->

### MASK:DATA:HEADer?

```text
Returns information on the mask data that is delivered with MASK:DATA?.
```

#### Table 18-14: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |

| Position | Meaning | Example |
| --- | --- | --- |
| 3 | Number of samples | 200000 |
| 4 | Number of values per sample interval. For masks the value is 2. | 2 |

<!-- 来源：RTM2_UserManual_en_10_files\part2285.htm -->

### Return values:

<DataHeader> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,2

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2286.htm -->

### REFCurve<m>:DATA?

Returns the data of the reference waveform for transmission from the instrument to the controlling computer. The waveforms data can be used in MATLAB, for example.

To set the export format, use FORMat[:DATA] on page 731.

<!-- 来源：RTM2_UserManual_en_10_files\part2287.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part2288.htm -->

### Return values:

<Data> List of values according to the format settings.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2289.htm -->

### REFCurve<m>:DATA:HEADer?

Returns information on the reference waveform.

#### Table 18-15: Header data

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | XStart in s | -9.477E-008 = - 94,77 ns |
| 2 | XStop in s | 9.477E-008 = 94,77 ns |
| 3 | Record length of the waveform in Samples | 200000 |
| 4 | Number of values per sample interval, usually 1. | 1 |

<!-- 来源：RTM2_UserManual_en_10_files\part2290.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform, the internal reference storage.

<!-- 来源：RTM2_UserManual_en_10_files\part2291.htm -->

### Parameters:

<Header> Comma-separated value list

Example: -9.477E-008,9.477E-008,200000,1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2292.htm -->

### REFCurve<m>:DATA:POINts?

```text
Returns the number of data samples that are returned with REFCurve<m>:DATA?.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2293.htm -->

### Suffix:

<m> 1..4

Selects the reference waveform.

<!-- 来源：RTM2_UserManual_en_10_files\part2294.htm -->

### Return values:

<DataPoints> Amount of data points

### Usage: Query only

### CHANnel<m>:DATA:XORigin? CHANnel<m>:DATA:ENVelope:XORigin? CALCulate:MATH<m>:DATA:XORigin?

### CALCulate:MATH<m>:DATA:ENVelope:XORigin? MASK:DATA:XORigin?

### DIGital<m>:DATA:XORigin? REFCurve<m>:DATA:XORigin?

Return the time of the first sample of the indicated waveform.

The commands are relevant for data conversion if binary data format is defined ( FORM UINT, 8|16|32 ).

<!-- 来源：RTM2_UserManual_en_10_files\part2295.htm -->

### Return values:

<Xorigin> Time in s

### Example: See Chapter 18.2.1.2, "Reading Waveform Data in Unsigned Integer Format", on page 406

### Usage: Query only

### CHANnel<m>:DATA:XINCrement? CHANnel<m>:DATA:ENVelope:XINCrement? CALCulate:MATH<m>:DATA:XINCrement?

### CALCulate:MATH<m>:DATA:ENVelope:XINCrement? MASK:DATA:XINCrement?

### DIGital<m>:DATA:XINCrement? REFCurve<m>:DATA:XINCrement?

Return the time difference between two adjacent samples of the indicated waveform.

The commands are relevant for data conversion if binary data format is defined ( FORM UINT, 8|16|32 ).

<!-- 来源：RTM2_UserManual_en_10_files\part2296.htm -->

### Return values:

<Xincrement> Time in s

### Example: See Chapter 18.2.1.2, "Reading Waveform Data in Unsigned Integer Format", on page 406

### Usage: Query only

### CHANnel<m>:DATA:YORigin? CHANnel<m>:DATA:ENVelope:YORigin? CALCulate:MATH<m>:DATA:YORigin?

### CALCulate:MATH<m>:DATA:ENVelope:YORigin? MASK:DATA:YORigin?

### DIGital<m>:DATA:YORigin? REFCurve<m>:DATA:YORigin?

Return the voltage value for binary value 0 of the indicated waveform.

The commands are relevant for data conversion if binary data format is defined ( FORM UINT, 8|16|32 ).

<!-- 来源：RTM2_UserManual_en_10_files\part2297.htm -->

### Return values:

<Yorigin> Voltage in V

### Example: See Chapter 18.2.1.2, "Reading Waveform Data in Unsigned Integer Format", on page 406

### Usage: Query only

### CHANnel<m>:DATA:YINCrement? CHANnel<m>:DATA:ENVelope:YINCrement? CALCulate:MATH<m>:DATA:YINCrement?

### CALCulate:MATH<m>:DATA:ENVelope:YINCrement? MASK:DATA:YINCrement?

### DIGital<m>:DATA:YINCrement? REFCurve<m>:DATA:YINCrement?

Return the voltage value per bit of the indicated waveform.

The commands are relevant for data conversion if binary data format is defined ( FORM UINT, 8|16|32 ).

<!-- 来源：RTM2_UserManual_en_10_files\part2298.htm -->

### Return values:

<Yincrement> Voltage in V

### Example: See Chapter 18.2.1.2, "Reading Waveform Data in Unsigned Integer Format", on page 406

### Usage: Query only

### CHANnel<m>:DATA:YRESolution? CHANnel<m>:DATA:ENVelope:YRESolution? CALCulate:MATH<m>:DATA:YRESolution?

### CALCulate:MATH<m>:DATA:ENVelope:YRESolution? MASK:DATA:YRESolution?

### DIGital<m>:DATA:YRESolution? REFCurve<m>:DATA:YRESolution?

Return the vertical bit resolution of the indicated waveform.

The commands are relevant for data conversion if binary data format is defined ( FORM UINT, 8|16|32 ).

<!-- 来源：RTM2_UserManual_en_10_files\part2299.htm -->

### Return values:

<Yresolution> For default waveforms, the resolution is 8 bit.

If high resolution, average or filter are set for the waveform, the resolution is 16 bit.

### Example: See Chapter 18.2.1.2, "Reading Waveform Data in Unsigned Integer Format", on page 406

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2300.htm -->

### 18.17.2 Waveform Data Export to File

EXPort:WAVeform:SOURce 744

EXPort:WAVeform:NAME 744

EXPort:WAVeform:SAVE 745

### EXPort:WAVeform:SOURce <WaveformSource> Defines the waveform to be exported.

<!-- 来源：RTM2_UserManual_en_10_files\part2301.htm -->

### Parameters:

<WaveformSource> CH1..4 | D70 | D158 | MA1..5 | RE1. 4

<!-- 来源：RTM2_UserManual_en_10_files\part2302.htm -->

### CH1. 4

Analog channels CH1 | CH2 | CH3 | CH4

<!-- 来源：RTM2_UserManual_en_10_files\part2303.htm -->

### D70

Pod 1, digital channels D0 to D7 are exported together

<!-- 来源：RTM2_UserManual_en_10_files\part2304.htm -->

### D158

Pod 2, digital channels D8 to D15 are exported together.

<!-- 来源：RTM2_UserManual_en_10_files\part2305.htm -->

### MA1. 5

Mathematic waveforms MA1 | MA2 | MA3 | MA4 | MA5

<!-- 来源：RTM2_UserManual_en_10_files\part2306.htm -->

### RE1. 4

Reference waveforms RE1 | RE2 | RE3 | RE4

### EXPort:WAVeform:NAME <FileName>

```text
Defines the path and filename for a waveform data file that will be saved with EXPort: WAVeform:SAVE. The data format and file extension is defined using FORMat[: DATA].
```

Existing files will be overwritten.

You can change the storage location, file name and/or file format manually in the FILE

> "Waveforms" menu. Remote control uses the recent settings.

<!-- 来源：RTM2_UserManual_en_10_files\part2307.htm -->

### Parameters:

<FileName> String parameter

Example: FORMAT CSV

```text
EXPort:WAVeform:NAME "/USB_FRONT/WAVEFORMS/WFM01"
EXPort:WAVeform:SAVE
```

The waveform data is saved to WFM01.CSV.

### EXPort:WAVeform:SAVE Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2308.htm -->

### 18.17.3 Instrument Settings

The Mass MEMomory subsystem provides commands to access the storage media and to save and reload instrument settings and data.

The R&S RTM has three storage devices indicated as drives:

- /INT: internal storage with default directories for each data type

- /USB_FRONT: USB connector on the front panel

- /USB_REAR: USB connector on the rear panel

Common computer and network drives like C:, D:, \\server\share are not availa- ble.

<!-- 来源：RTM2_UserManual_en_10_files\part2309.htm -->

### Name conventions

The names of files and directories have to meet the following rules:

- Only the 8.3 format with ASCI characters is supported.

- No special characters are allowed.

- Use / (slash) instead of \ (backslash).

MMEMory:DRIVes? 745

MMEMory:MSIS 746

MMEMory:CDIRectory 746

MMEMory:MDIRectory 746

MMEMory:RDIRectory 747

MMEMory:DCATalog? 747

MMEMory:DCATalog:LENGth? 748

MMEMory:CATalog? 748

MMEMory:CATalog:LENGth? 749

MMEMory:COPY 749

MMEMory:MOVE 749

MMEMory:DELete 750

MMEMory:DATA 750

MMEMory:STORe:STATe 751

MMEMory:LOAD:STATe 751

<!-- 来源：RTM2_UserManual_en_10_files\part2310.htm -->

### MMEMory:DRIVes?

Returns the storage devices available on the R&S RTM.

<!-- 来源：RTM2_UserManual_en_10_files\part2311.htm -->

### Return values:

<Drive> List of strings, for example, ""/INT"",""/USB_FRONT"",""/ USB_REAR""

/INT: internal storage

/USB_FRONT: USB connector on the front panel

/USB_REAR: USB connector on the rear panel

### Usage: Query only

### MMEMory:MSIS [<MassStorageIS>] Changes the storage device (drive).

<!-- 来源：RTM2_UserManual_en_10_files\part2312.htm -->

### Parameters:

<MassStorageIS> One of the available drives: /INT, /USB_FRONT, or /USB_REAR

### Example: MMEM:MSIS '/USB_FRONT'

Sets the USB flash drive connected to the front panel as storage device to be used.

### MMEMory:CDIRectory [<DirectoryName>] Specifies the current directory for file access.

<!-- 来源：RTM2_UserManual_en_10_files\part2313.htm -->

### Setting parameters:

<DirectoryName> String parameter to specify the directory, including the storage device.

### Example: MMEM:CDIR "/USB_FRONT/DATA"

Example: Chapter 18.2.3.2, "Saving, Copying, and Loading Setup Data", on page 408

### MMEMory:MDIRectory <DirectoryName> Creates a new directory with the specified name.

<!-- 来源：RTM2_UserManual_en_10_files\part2314.htm -->

### Setting parameters:

<DirectoryName> String parameter

Absolute path including the storage device, or relative to the cur- rent directory.

### Example: Create directory DATA on the front USB flash device, with abso- lute path:

```text
MMEM:MDIR "/USB_FRONT/DATA"
```

### Example: Create directory JANUARY in the DATA directory, with relative path:

```text
MMEM:CDIR "/USB_FRONT/DATA/" MMEM:MDIR "JANUARY"
```

### Usage: Setting only

### MMEMory:RDIRectory <DirectoryName> Deletes the specified directory.

### Note: All subdirectories and all files in the specified directory and in the subdirectories will be deleted!

You cannot delete the current directory or a superior directory. In this case, the instru- ment returns an execution error.

<!-- 来源：RTM2_UserManual_en_10_files\part2315.htm -->

### Setting parameters:

<DirectoryName> String parameter, absolute path or relative to the current direc- tory

### Example: MMEM:RDIR "/INT/TEST"

Deletes the directory TEST in the internal storage device, and all files and subdirectories in the directory.

### Usage: Setting only

### MMEMory:DCATalog? <PathName>

Returns the subdirectories of the specified directory. The result corresponds to the number of strings returned by the MMEMory:DCATalog:LENgth? command.

<!-- 来源：RTM2_UserManual_en_10_files\part2316.htm -->

### Query parameters:

<PathName> String parameter Specifies the directory.

<!-- 来源：RTM2_UserManual_en_10_files\part2317.htm -->

### Return values:

<FileEntry> String parameter

List of subdirectory strings separated by commas. If the speci- fied directory does not have any subdirectory, the current and the parent directories are returned ( ".,,0","..,,0" )

### Example: Query for directories with absolute path:

```text
MMEM:DCAT? "/USB_FRONT/*"
received ".,,0","..,,0","DATA,,0","DATA_NEW,, 0","SCREENSHOTS,,0"
MMEM:DCAT:LENG? "/USB_FRONT/*"
received 5
```

### Example: Query for directories in the current directory:

```text
MMEM:CDIR "/USB_FRONT/DATA/" MMEM:DCAT? "*"
received ".,,0","..,,0","JANUARY,,0", "FEBRUARY,,0"
MMEM:DCAT:LENG? "*"
received 4
```

### Example: Query with filter:

```text
MMEM:DCAT? "/USB_FRONT/DA*" received "DATA,,0","DATA_NEW,,0" MMEM:DCAT:LENG? "/USB_FRONT/DA*"
received 2
```

### Usage: Query only

### MMEMory:DCATalog:LENGth? <PathName>

Returns the number of directories in specified directory. The result corresponds to the number of strings returned by the MMEMory:DCATalog? command.

<!-- 来源：RTM2_UserManual_en_10_files\part2318.htm -->

### Query parameters:

<PathName> String parameter Specifies the directory.

<!-- 来源：RTM2_UserManual_en_10_files\part2319.htm -->

### Return values:

<FileEntryCount> Number of directories.

### Example: see MMEMory:DCATalog?

### Usage: Query only

### MMEMory:CATalog? <PathName>[,<Format>]

Returns the a list of files contained in the specified directory. The result corresponds to the number of files returned by the MMEMory:CATalog:LENgth? command.

<!-- 来源：RTM2_UserManual_en_10_files\part2320.htm -->

### Query parameters:

<PathName> String parameter

Specifies the directory. A filter can be used to list, for example, only files of a given file type.

<Format> ALL | WTIMe

ALL: Extended result including file, date, time and attributes WTIMe: Result including file, date, time

<!-- 来源：RTM2_UserManual_en_10_files\part2321.htm -->

### Return values:

<UsedMemory> Total amount of storage currently used in the directory, in bytes.

<FreeMemory> Total amount of storage available in the directory, in bytes.

<FileEntry> String parameter

All files of the directory are listed with their file name, format and size in bytes.

### Example: Query for files in the DATA directory, with absolute path:

```text
MMEM:CAT? "/USB_FRONT/DATA/*.*"
received: 511104,8633856,"MONDAY.TXT,,8", "TUESDAY.CSV,,8"
```

### Example: Query for TXT files in the DATA directory, with relative path:

```text
MMEM:CDIR "/USB_FRONT/DATA"' MMEM:CAT? "*.TXT"
received: 511104,8633856,"MONDAY.TXT,,8" MMEM:CAT:LENGTH? "*.TXT"
received 1
```

Example: Chapter 18.2.3.2, "Saving, Copying, and Loading Setup Data", on page 408

### Usage: Query only

### MMEMory:CATalog:LENGth? <PathName>

Returns the number of files in the specified directory. The result corresponds to the number of files returned by the MMEMory:CATalog? command.

<!-- 来源：RTM2_UserManual_en_10_files\part2322.htm -->

### Query parameters:

<PathName> String parameter

Directory to be queried, absolute or relative path

<!-- 来源：RTM2_UserManual_en_10_files\part2323.htm -->

### Return values:

<Count> Number of files.

### Example: see MMEMory:CATalog?

### Usage: Query only

### MMEMory:COPY <FileSource>,<FileDestination>

Copies data to another directory on the same or different storage device. The file name can be changed, too.

<!-- 来源：RTM2_UserManual_en_10_files\part2324.htm -->

### Setting parameters:

<FileSource> String parameter

Name and path of the file to be copied

<FileDestination> String parameter

Name and path of the new file. If the file already exists, it is over- written without notice.

### Example: MMEM:COPY "/INT/SETTINGS/SET001.SET",

```text
"/USB_FRONT/SETTINGS/TESTSET1.SET"
```

Example: Chapter 18.2.3.2, "Saving, Copying, and Loading Setup Data", on page 408

### Usage: Setting only

### MMEMory:MOVE <FileSource>,<FileDestination> Moves an existing file to a new location.

<!-- 来源：RTM2_UserManual_en_10_files\part2325.htm -->

### Setting parameters:

<FileSource> String parameter

Path and name of the file to be moved

<FileDestination> String parameter

Path and name of the new file

### Example: MMEM:MOVE "/INT/SETTINGS/SET001.SET",

```text
"/USB_FRONT/SETTINGS/SET001.SET"
```

### Usage: Setting only

### MMEMory:DELete <FileSource> Removes a file from the specified directory.

<!-- 来源：RTM2_UserManual_en_10_files\part2326.htm -->

### Setting parameters:

<FileSource> String parameter

File name and path of the file to be removed. If the path is omit- ted, the specified file will be deleted in the current directory. Fil- ters are not allowed.

Example: Chapter 18.2.3.2, "Saving, Copying, and Loading Setup Data", on page 408

### Usage: Setting only

### MMEMory:DATA <FileName>,<Data>

```text
Writes data to the specified file in the current directory MMEMory:CDIRectory, or reads the data.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2327.htm -->

### Parameters:

<Data> 488.2 block data

The block begins with character '#'. The next digit is the length of the length information, followed by this given number of digits providing the number of bytes in the binary data attached.

<!-- 来源：RTM2_UserManual_en_10_files\part2328.htm -->

### Parameters for setting and query:

<FileName> String parameter containing the file name

### Example: MMEM:DATA "abc.txt", #216This is the file

#2: the length infomation has two digits 16: the binary data has 16 bytes.

```text
MMEM:DATA? "abc.txt" received: This is the file
```

Example: Chapter 18.2.3.2, "Saving, Copying, and Loading Setup Data", on page 408

### MMEMory:STORe:STATe <StateNumber>,<FileName>

Saves the current device settings to the specified file in the current directory.

<!-- 来源：RTM2_UserManual_en_10_files\part2329.htm -->

### Setting parameters:

<StateNumber> Range: 1 to 1

Increment: 0

*RST: 1

<FileName> String parameter

File name, with or without file extension

### Example: MMEM:CDIR "/USB_FRONT/DATA"' MMEM:STOR:STAT 1,"MORNING.SET"

Example: Chapter 18.2.3.2, "Saving, Copying, and Loading Setup Data", on page 408

### Usage: Setting only

### MMEMory:LOAD:STATe <StateNumber>,<FileName>

Loads the device settings from the specified file in the current directory.

<!-- 来源：RTM2_UserManual_en_10_files\part2330.htm -->

### Setting parameters:

<StateNumber> Range: 1 to 1

Increment: 0

*RST: 1

<FileName> String parameter

File name, with or without file extension

### Example: MMEM:CDIR "/USB_FRONT/DATA"' MMEM:LOAD:STAT 1,"MORNING"

Example: Chapter 18.2.3.2, "Saving, Copying, and Loading Setup Data", on page 408

### Usage: Setting only

<!-- 来源：RTM2_UserManual_en_10_files\part2331.htm -->

### 18.17.4 Screenshots

This chapter describes remote commands used to print and save screenshots.

HCOPy:DESTination 752

MMEMory:NAME 752

HCOPy[:IMMediate] 752

HCOPy:DATA? 753

HCOPy:LANGuage 753

HCOpy:MENU[:ENABle] 753

HCOPy:PAGE:SIZE 753

HCOPy:PAGE:ORIentation 753

HCOPy:COLor:SCHeme 753

SYSTem:COMMunicate:PRINter:SELect 754

SYSTem:COMMunicate:PRINter:ENUMerate:FIRSt? 754

SYSTem:COMMunicate:PRINter:ENUMerate[:NEXT]? 754

SYSTem:COMMunicate:PRINter:CSET 754

### HCOPy:DESTination <Medium>

Defines whether the screenshot is saved or printed.

<!-- 来源：RTM2_UserManual_en_10_files\part2332.htm -->

### Parameters:

<Medium> MMEM | SYST:COMM:PRIN

String parameter

<!-- 来源：RTM2_UserManual_en_10_files\part2333.htm -->

### MMEM

```text
Saves the screenshot to a file. Specify the file name and location with MMEMory:NAME.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2334.htm -->

### SYST:COMM:PRIN

Prints on the printer specified with SYSTem:COMMunicate: PRINter:SELect. The printer must be specified before the HCOPy:DESTination is sent.

*RST: MMEM

### Example: HCOP:DEST "MMEM"

Chapter 18.2. 3.1, "Saving Screenshots to File", on page 408

### MMEMory:NAME <FileName>

```text
Defines the file name to store an image of the display with HCOPy[:IMMediate].
```

<!-- 来源：RTM2_UserManual_en_10_files\part2335.htm -->

### Parameters:

<FileName> String parameter

Example: Chapter 18.2.3.1, "Saving Screenshots to File", on page 408

<!-- 来源：RTM2_UserManual_en_10_files\part2336.htm -->

### HCOPy[:IMMediate]

```text
Prints an image of the display to the printer or saves an image to a file or the clipboard, depending on the HCOPy:DESTination setting.
```

Before starting the printout, make sure that:

```text
● The printer is defined by SYSTem:COMMunicate:PRINter:SELect.
```

- The path for storage is defined correctly by MMEMory:CDIRectory

```text
● The file name for storage is defined by MMEMory:NAME.
```

Example: Chapter 18.2.3.1, "Saving Screenshots to File", on page 408

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2337.htm -->

### HCOPy:DATA?

Returns the data of the image file. The file format is defined using HCOPy:LANGuage

( BMP | PNG )

<!-- 来源：RTM2_UserManual_en_10_files\part2338.htm -->

### Return values:

<ScreenData> Block data

### Usage: Query only

### HCOPy:LANGuage <Format>

Defines the format of the printed or saved screenshot.

<!-- 来源：RTM2_UserManual_en_10_files\part2339.htm -->

### Parameters:

<Format> GDI | BMP | PNG

<!-- 来源：RTM2_UserManual_en_10_files\part2340.htm -->

### GDI

For output on printer

<!-- 来源：RTM2_UserManual_en_10_files\part2341.htm -->

### BMP | PNG

```text
File formats for saved screenshots. Set also HCOpy:MENU[:ENABle].
```

*RST: PNG

Example: Chapter 18.2.3.1, "Saving Screenshots to File", on page 408

<!-- 来源：RTM2_UserManual_en_10_files\part2342.htm -->

### HCOpy:MENU[:ENABle]

Includes the menu in the screenshot. If OFF (no menu), the menu is clipped off, and date and time are shown instead of the menu name.

<!-- 来源：RTM2_UserManual_en_10_files\part2343.htm -->

### Parameters:

<MenuEnable> ON | OFF

### HCOPy:PAGE:SIZE <Size>

Defines the page size to be used.

<!-- 来源：RTM2_UserManual_en_10_files\part2344.htm -->

### Parameters:

<Size> A4 | A5 | B5 | B6 | EXECutive

### HCOPy:PAGE:ORIentation <Orientation> Defines the page orientation.

<!-- 来源：RTM2_UserManual_en_10_files\part2345.htm -->

### Parameters:

<Orientation> LANDscape | PORTrait

### HCOPy:COLor:SCHeme <ColorScheme>

Defines the color mode for saved and printed screenshots.

<!-- 来源：RTM2_UserManual_en_10_files\part2346.htm -->

### Parameters:

<ColorScheme> COLor | GRAYscale | INVerted

INVerted inverts the colors of the output, i.e. a dark waveform is printed on a white background.

*RST: COLor

Example: Chapter 18.2.3.1, "Saving Screenshots to File", on page 408

### SYSTem:COMMunicate:PRINter:SELect <PrinterName> Selects a configured printer.

<!-- 来源：RTM2_UserManual_en_10_files\part2347.htm -->

### Parameters:

<PrinterName> String parameter

```text
Enter the string as it is returned with SYSTem:COMMunicate: PRINter:ENUMerate:FIRSt? or SYSTem:COMMunicate: PRINter:ENUMerate[:NEXT]?.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2348.htm -->

### SYSTem:COMMunicate:PRINter:ENUMerate:FIRSt?

```text
Queries the name of the first printer in the list of printers. The names of other installed printers can be queried with the SYSTem:COMMunicate:PRINter:ENUMerate[: NEXT]? command.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2349.htm -->

### Return values:

<PrinterName> String parameter

If no printer is configured an empty string is returned.

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2350.htm -->

### SYSTem:COMMunicate:PRINter:ENUMerate[:NEXT]?

```text
Queries the name of the next printer installed. The SYSTem:COMMunicate: PRINter:ENUMerate:FIRSt? command should be sent previously to return to the beginning of the printer list and query the name of the first printer.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2351.htm -->

### Return values:

<PrinterName> String parameter

After all available printer names have been returned, an empty string enclosed by quotation marks (") is returned for the next query. Further queries are answered by a query error.

### Usage: Query only

### SYSTem:COMMunicate:PRINter:CSET <CommandSet> Sets the printer language that is supported by the printer.

<!-- 来源：RTM2_UserManual_en_10_files\part2352.htm -->

### Parameters:

<CommandSet> PCL5 | PCLXl | PS | DESKjet

PCLXl = PCL XL

PS = Postscript

DESKjet = PCL3 for HP Deskjet

<!-- 来源：RTM2_UserManual_en_10_files\part2353.htm -->

## 18.18 General Instrument Setup

DISPlay:LANGuage 755

CALibration 755

CALibration:STATe? 756

TRIGger:OUT:MODE 756

TRIGger:OUT:PLENgth 756

TRIGger:OUT:POLarity 756

SYSTem:NAME 756

SYSTem:DATE 757

SYSTem:TIME 757

SYSTem:BEEPer:CONTrol:STATe 757

SYSTem:BEEPer:ERRor:STATe 757

SYSTem:BEEPer:TRIG:STATe 758

SYSTem:BEEPer[:IMMediate] 758

SYSTem:SET 758

SYSTem:ERRor:[NEXT]? 758

SYSTem:ERRor:ALL? 758

SYST:PRESet 759

SYSTem:EDUCation:PRESet 759

### DISPlay:LANGuage <Language>

Sets the language in which the softkey labels, help and other screen information can be displayed.

<!-- 来源：RTM2_UserManual_en_10_files\part2354.htm -->

### Parameters:

<Language> ENGLish | GERMan | FRENch | SPANishRUSSian | SCHinese | TCHinese | JAPanese | ENGLish | GERMan | FRENch | SPANish | RUSSian | SCHinese | TCHinese | JAPanese | KORean

Supported languages are listed in the "Specifications" data sheet.

*RST: Reset does not change the language

<!-- 来源：RTM2_UserManual_en_10_files\part2355.htm -->

### CALibration

```text
Calibration starts the self-alignment process. It can take several minutes. Consider your timeout settings.
Calibration? returns information on the state of the self-alignment. Return values ≠ 0 indicate an error.
```

Same as *CAL?.

<!-- 来源：RTM2_UserManual_en_10_files\part2356.htm -->

### Return values:

<SelfAlignment> Numeric status indicator

<!-- 来源：RTM2_UserManual_en_10_files\part2357.htm -->

### CALibration:STATe?

Returns the overall state of the self-alignment.

<!-- 来源：RTM2_UserManual_en_10_files\part2358.htm -->

### Return values:

<SelfAlignmentState> NOALignment | RUN | ERRor | OK | ABORt

NOALignment: no self-aligment was performed. Relevant for service operations.

RUN: self-aligment is running ERRor: an error occured.

OK: self-aligment has been performed successfully ABORt: self-aligment has been cancelled

### Usage: Query only

### TRIGger:OUT:MODE <OutputMode>

Defines wether and when a trigger out pulse is generated: never, on trigger event, or on mask violation.

<!-- 来源：RTM2_UserManual_en_10_files\part2359.htm -->

### Parameters:

<OutputMode> OFF | TRIGger | MASK

*RST: OFF

### TRIGger:OUT:PLENgth <PulseLength> Defines the pulse width of the trigger out pulse.

<!-- 来源：RTM2_UserManual_en_10_files\part2360.htm -->

### Parameters:

<PulseLength> *RST: 1E-6

Default unit: s

### TRIGger:OUT:POLarity <Polarity> Sets the polarity of the trigger out pulse.

<!-- 来源：RTM2_UserManual_en_10_files\part2361.htm -->

### Parameters:

<Polarity> POSitive | NEGative

*RST: POS

### SYSTem:NAME <Name>

Defines an instrument name.

<!-- 来源：RTM2_UserManual_en_10_files\part2362.htm -->

### Parameters:

<Name> String with max. 20 characters

### SYSTem:DATE <Year>,<Month>,<Day> Specifies the internal date for the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part2363.htm -->

### Parameters:

<Year> Increment: 1 Default unit: a

<Month> Range: 1 to 12

Increment: 1

<Day> Range: 1 to 31

Increment: 1 Default unit: d

### Usage: SCPI confirmed

| <Hour> | Range: 0 to Increment: 1 Default unit: h | 23 |
| --- | --- | --- |
| <Minute> | Range: 0 to Increment: 1 Default unit: min | 59 |
| <Second> | Range: 0 to Increment: 1 Default unit: s | 59 |
| Usage: | SCPI confirmed |  |

### SYSTem:TIME <Hour>,<Minute>,<Second> Specifies the internal time for the instrument. Parameters:

### SYSTem:BEEPer:CONTrol:STATe <ControlBeep>

Enables or diables a sound for general control events, e.g. reaching the rotary encoder end or changing the measuring mode in the "Automeasure" menu.

<!-- 来源：RTM2_UserManual_en_10_files\part2364.htm -->

### Parameters:

<ControlBeep> ON | OFF

### SYSTem:BEEPer:ERRor:STATe <ErrorBeep> Enables or disables the beep if an error occurs.

<!-- 来源：RTM2_UserManual_en_10_files\part2365.htm -->

### Parameters:

<ErrorBeep> ON | OFF

### SYSTem:BEEPer:TRIG:STATe <TriggerBeep> Enables or disables the beep if a trigger occurs.

<!-- 来源：RTM2_UserManual_en_10_files\part2366.htm -->

### Parameters:

<TriggerBeep> ON | OFF

### SYSTem:BEEPer[:IMMediate] Generates an immediate beep. Usage: Event

### SYSTem:SET <Setup>

Defines or queries the device settings that can be saved and load manually with FILE > "Device Settings".

<!-- 来源：RTM2_UserManual_en_10_files\part2367.htm -->

### Parameters:

<Setup> 488.2 block data

### Usage: SCPI confirmed

<!-- 来源：RTM2_UserManual_en_10_files\part2368.htm -->

### SYSTem:ERRor:[NEXT]?

Queries the error/event queue for the oldest item and removes it from the queue. The response consists of an error number and a short description of the error.

Positive error numbers are instrument-dependent. Negative error numbers are reserved by the SCPI standard.

<!-- 来源：RTM2_UserManual_en_10_files\part2369.htm -->

### Return values:

<Error> Error/event_number,"Error/event_description>[;Device-depend- ent info]"

If the queue is empty, the response is 0,"No error"

### Usage: Query only SCPI confirmed

<!-- 来源：RTM2_UserManual_en_10_files\part2370.htm -->

### SYSTem:ERRor:ALL?

Queries the error/event queue for all unread items and removes them from the queue. The response is a comma separated list of error number and a short description of the error in FIFO order.

Positive error numbers are instrument-dependent. Negative error numbers are reserved by the SCPI standard.

<!-- 来源：RTM2_UserManual_en_10_files\part2371.htm -->

### Return values:

<Error> List of: Error/event_number,"Error/event_description>[;Device- dependent info]"

If the queue is empty, the response is 0,"No error"

### Usage: Query only SCPI confirmed

<!-- 来源：RTM2_UserManual_en_10_files\part2372.htm -->

### SYST:PRESet

Resets the instrument to the default state, has the same effect as *RST.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2373.htm -->

### SYSTem:EDUCation:PRESet

Deletes the password of the education mode.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2374.htm -->

## 18.19 Status Reporting

<!-- 来源：RTM2_UserManual_en_10_files\part2375.htm -->

### 18.19.1 STATus:OPERation Register

The commands of the STATus:OPERation subsystem control the status reporting structures of the STATus:OPERation register:

See also:

- Chapter B.1, "Structure of a SCPI Status Register", on page 780

- Chapter B.3.3, "STATus:OPERation Register", on page 785 The following commands are available:

STATus:OPERation:CONDition? 759

STATus:OPERation:ENABle 760

STATus:OPERation:NTRansition 760

STATus:OPERation:PTRansition 760

STATus:OPERation[:EVENt]? 760

<!-- 来源：RTM2_UserManual_en_10_files\part2376.htm -->

### STATus:OPERation:CONDition?

Returns the of the CONDition part of the operational status register.

<!-- 来源：RTM2_UserManual_en_10_files\part2377.htm -->

### Return values:

<Condition> Condition bits in decimal representation. ALIGnment (bit 0), SELFtest (bit 1), AUToset (bit 2), WTRigger (bit 3).

Range: 1 to 65535

Increment: 1

### Usage: Query only

### STATus:OPERation:ENABle <Enable>

<!-- 来源：RTM2_UserManual_en_10_files\part2378.htm -->

### Parameters:

<Enable> Range: 1 to 65535

Increment: 1

### STATus:OPERation:NTRansition <NegativeTransition>

<!-- 来源：RTM2_UserManual_en_10_files\part2379.htm -->

### Parameters:

<NegativeTransition> Range: 1 to 65535

Increment: 1

### STATus:OPERation:PTRansition <PositiveTransition>

<!-- 来源：RTM2_UserManual_en_10_files\part2380.htm -->

### Parameters:

<PositiveTransition> Range: 1 to 65535

Increment: 1

<!-- 来源：RTM2_UserManual_en_10_files\part2381.htm -->

### STATus:OPERation[:EVENt]? Return values:

<Event> Range: 1 to 65535

Increment: 1

### Usage: Query only

<!-- 来源：RTM2_UserManual_en_10_files\part2382.htm -->

### 18.19.2 STATus:QUEStionable Registers

The commands of the STATus:QUEStionable subsystem control the status reporting structures of the STATus:QUEStionable registers:

#### Figure 18-1: Structure of the STATus:QUEStionable register

See also:

- Chapter B.1, "Structure of a SCPI Status Register", on page 780

- Chapter B.3.4, "STATus:QUEStionable Register", on page 785 The following commands are available:

STATus:PRESet 762

STATus:QUEStionable:CONDition? 762

STATus:QUEStionable:COVerload:CONDition? 762

STATus:QUEStionable:LIMit:CONDition? 762

STATus:QUEStionable:MASK:CONDition? 762

STATus:QUEStionable:ENABle 762

STATus:QUEStionable:COVerload:ENABle 762

STATus:QUEStionable:LIMit:ENABle 762

STATus:QUEStionable:MASK:ENABle 762

STATus:QUEStionable[:EVENt]? 763

STATus:QUEStionable:COVerload[:EVENt]? 763

STATus:QUEStionable:LIMit[:EVENt]? 763

STATus:QUEStionable:MASK[:EVENt]? 763

STATus:QUEStionable:NTRansition 763

STATus:QUEStionable:COVerload:NTRansition 763

STATus:QUEStionable:LIMit:NTRansition 763

STATus:QUEStionable:MASK:NTRansition 763

STATus:QUEStionable:PTRansition 763

STATus:QUEStionable:COVerload:PTRansition 763

STATus:QUEStionable:LIMit:PTRansition 763

STATus:QUEStionable:MASK:PTRansition 763

<!-- 来源：RTM2_UserManual_en_10_files\part2383.htm -->

### STATus:PRESet

Resets all STATUS:QUESTIONALBLE registers.

### Usage: Event

<!-- 来源：RTM2_UserManual_en_10_files\part2384.htm -->

### STATus:QUEStionable:CONDition? STATus:QUEStionable:COVerload:CONDition? STATus:QUEStionable:LIMit:CONDition?

### STATus:QUEStionable:MASK:CONDition?

Returns the contents of the CONDition part of the status register to check for question- able instrument or measurement states. Reading the CONDition registers does not delete the contents.

<!-- 来源：RTM2_UserManual_en_10_files\part2385.htm -->

### Return values:

<Condition> Condition bits in decimal representation

Range: 1 to 65535

Increment: 1

### Usage: Query only

### STATus:QUEStionable:ENABle <Enable> STATus:QUEStionable:COVerload:ENABle <Enable> STATus:QUEStionable:LIMit:ENABle <Enable> STATus:QUEStionable:MASK:ENABle <Enable>

Sets the ENABle part that allows true conditions in the EVENt part to be reported in the summary bit. If a bit is set to 1 in the enable part and its associated event bit transitions to true, a positive transition occurs in the summary bit and is reported to the next higher level.

<!-- 来源：RTM2_UserManual_en_10_files\part2386.htm -->

### Parameters:

<Enable> Bit mask in decimal representation

Range: 1 to 65535

Increment: 1

### Example: STATus:QUEStionable:MASK:ENABle 24

Set bits no. 3 and 4 of the STATus:QUEStiona- ble:MASK:ENABle register part: 24 = 8 + 16 = 2 3 + 2 4

<!-- 来源：RTM2_UserManual_en_10_files\part2387.htm -->

### STATus:QUEStionable[:EVENt]? STATus:QUEStionable:COVerload[:EVENt]? STATus:QUEStionable:LIMit[:EVENt]?

### STATus:QUEStionable:MASK[:EVENt]?

Returns the contents of the EVENt part of the status register to check whether an event has occurred since the last reading. Reading an EVENt register deletes its con- tents.

<!-- 来源：RTM2_UserManual_en_10_files\part2388.htm -->

### Return values:

<Event> Event bits in decimal representation

Range: 1 to 65535

Increment: 1

### Usage: Query only

### STATus:QUEStionable:NTRansition <NegativeTransition> STATus:QUEStionable:COVerload:NTRansition <NegativeTransition> STATus:QUEStionable:LIMit:NTRansition <NegativeTransition> STATus:QUEStionable:MASK:NTRansition <NegativeTransition>

Sets the negative transition filter. If a bit is set, a 1 to 0 transition in the corresponding bit of the condition register causes a 1 to be written in the corresponding bit of the event register.

<!-- 来源：RTM2_UserManual_en_10_files\part2389.htm -->

### Parameters:

<NegativeTransition> Bit mask in decimal representation

Range: 1 to 65535

Increment: 1

### Example: STATus:QUEStionable:MASK:NTRansition 24

Set bits no. 3 and 4 of the STATus:QUEStiona- ble:MASK:NTRansition register part: 24 = 8 + 16 = 2 3 + 2 4

### STATus:QUEStionable:PTRansition <PositiveTransition> STATus:QUEStionable:COVerload:PTRansition <PositiveTransition> STATus:QUEStionable:LIMit:PTRansition <PositiveTransition> STATus:QUEStionable:MASK:PTRansition <PositiveTransition>

Sets the positive transition filter. If a bit is set, a 0 to 1 transition in the corresponding bit of the condition register causes a 1 to be written in the corresponding bit of the event register.

<!-- 来源：RTM2_UserManual_en_10_files\part2390.htm -->

### Parameters:

<PositiveTransition> Bit mask in decimal representation

Range: 1 to 65535

Increment: 1

### Example: STATus:QUEStionable:MASK:PTRansition 24

Set bits no. 3 and 4 of the STATus:QUEStiona- ble:MASK:PTRansition register part: 24 = 8 + 16 = 2 3 + 2 4

<!-- 来源：RTM2_UserManual_en_10_files\part2391.htm -->

### Annex

Annex

A Remote Control Basics

This chapter provides basic information on operating an instrument via remote control.

<!-- 来源：RTM2_UserManual_en_10_files\part2392.htm -->

## A.1 Messages

Instrument messages are employed in the same way for all interfaces, if not indicated otherwise in the description.

See also:

- Structure and syntax of the instrument messages: Chapter A.2, "SCPI Command Structure", on page 767

- Detailed description of all messages: Chapter 18, "Remote Commands Reference", on page 404

There are different types of instrument messages, depending on the direction they are sent:

- Commands

- Instrument responses

<!-- 来源：RTM2_UserManual_en_10_files\part2393.htm -->

### Commands

Commands (program messages) are messages the controller sends to the instrument. They operate the instrument functions and request information. The commands are subdivided according to two criteria:

- According to the effect they have on the instrument:

– Setting commands cause instrument settings such as a reset of the instru- ment or setting the frequency.

– Queries cause data to be provided for remote control, e.g. for identification of the instrument or polling a parameter value. Queries are formed by directly appending a question mark to the command header.

- According to their definition in standards:

– Common commands: their function and syntax are precisely defined in stan- dard IEEE 488.2. They are employed identically on all instruments (if imple- mented). They refer to functions such as management of the standardized sta- tus registers, reset and self test.

– Instrument control commands refer to functions depending on the features of the instrument such as frequency settings. Many of these commands have also been standardized by the SCPI committee. These commands are marked as "SCPI compliant" in the command reference chapters. Commands without this SCPI label are device-specific, however, their syntax follows SCPI rules as per- mitted by the standard.

<!-- 来源：RTM2_UserManual_en_10_files\part2394.htm -->

### Instrument responses

Instrument responses (response messages and service requests) are messages the instrument sends to the controller after a query. They can contain measurement results, instrument settings and information on the instrument status.

<!-- 来源：RTM2_UserManual_en_10_files\part2395.htm -->

## A.1.1 LAN Interface Messages

In the LAN connection, the interface messages are called low–level control messages. These messages can be used to emulate interface messages of the GPIB bus.

| Command | Long term | Effect on the instrument |
| --- | --- | --- |
| &ABO | Abort | Aborts processing of the commands just received. |
| &DCL | Device Clear | Aborts processing of the commands just received and sets the command processing software to a defined initial state. Does not change the instrument setting. |
| >L | Go to Local | Transition to the "local" state (manual control). (The instrument automatically returns to remote state when a remote command is sent UNLESS &NREN was sent before.) |
| >R | Go to Remote | Enables automatic transition from local state to remote state by a subsequent remote command (after &NREN was sent). |
| &GET | Group Execute Trigger | Triggers a previously active instrument function (e.g. a sweep). The effect of the command is the same as with that of a pulse at the external trigger signal input. |
| &LLO | Local Lockout | Disables transition from remote control to manual control by means of the front panel keys. |
| &NREN | Not Remote Enable | Disables automatic transition from local state to remote state by a subsequent remote command. (To re-activate automatic transition use >R.) |
| &POL | Serial Poll | Starts a serial poll. |

<!-- 来源：RTM2_UserManual_en_10_files\part2396.htm -->

## A.1.2 GPIB Interface Messages

Interface messages are transmitted to the instrument on the data lines, with the atten- tion line (ATN) being active (LOW). They are used for communication between the controller and the instrument and can only be sent by a computer which has the func- tion of a GPIB bus controller. GPIB interface messages can be further subdivided into:

- Universal commands: act on all instruments connected to the GPIB bus without previous addressing

- Addressed commands: only act on instruments previously addressed as listeners

### A.1.2.1 Universal Commands

Universal commands are encoded in the range 10 through 1F hex. They affect all instruments connected to the bus and do not require addressing.

| Command | Effect on the instrument |
| --- | --- |
| DCL (Device Clear) | Aborts the processing of the commands just received and sets the com- mand processing software to a defined initial state. Does not change the instrument settings. |
| IFC (Interface Clear) *) | Resets the interfaces to the default setting. |
| LLO (Local Lockout) | The LOC/IEC ADDR key is disabled. |
| SPE (Serial Poll Enable) | Ready for serial poll. |
| SPD (Serial Poll Disable) | End of serial poll. |
| PPU (Parallel Poll Unconfig- ure) | End of the parallel-poll state. |
| *) IFC is not a real universal command, it is sent via a separate line; however, it also affects all instruments connected to the bus and does not require addressing |  |

### A.1.2.2 Addressed Commands

Addressed commands are encoded in the range 00 through 0F hex. They only affect instruments addressed as listeners.

| Command | Effect on the instrument |
| --- | --- |
| GET (Group Execute Trigger) | Triggers a previously active instrument function (e.g. a sweep). The effect of the command is the same as with that of a pulse at the external trigger signal input. |
| GTL (Go to Local) | Transition to the "local" state (manual control). |
| GTR (Go to Remote) | Transition to the "remote" state (remote control). |
| PPC (Parallel Poll Configure) | Configures the instrument for parallel poll. |
| SDC (Selected Device Clear) | Aborts the processing of the commands just received and sets the command processing software to a defined initial state. Does not change the instrument setting. |

<!-- 来源：RTM2_UserManual_en_10_files\part2397.htm -->

## A.2 SCPI Command Structure

SCPI commands consist of a so-called header and, in most cases, one or more param- eters. The header and the parameters are separated by a "white space" (ASCII code 0 to 9, 11 to 32 decimal, e.g. blank). The headers may consist of several mnemonics (keywords). Queries are formed by appending a question mark directly to the header.

The commands can be either device-specific or device-independent (common com- mands). Common and device-specific commands differ in their syntax.

<!-- 来源：RTM2_UserManual_en_10_files\part2398.htm -->

## A.2.1 Syntax for Common Commands

Common (=device-independent) commands consist of a header preceded by an aster- isk (*) and possibly one or more parameters.

### Examples:

| *RST | RESET | Resets the instrument. |
| --- | --- | --- |
| *ESE | EVENT STATUS ENABLE | Sets the bits of the event status enable registers. |
| *ESR? | EVENT STATUS QUERY | Queries the contents of the event status register. |
| *IDN? | IDENTIFICATION QUERY | Queries the instrument identification string. |

<!-- 来源：RTM2_UserManual_en_10_files\part2399.htm -->

## A.2.2 Syntax for Device-Specific Commands

Not all commands used in the following examples are necessarily implemented in the instrument.

For demonstration purposes only, assume the existence of the following commands for this section:

- DISPlay[:WINDow<1...4>]:MAXimize <Boolean>

- FORMat:READings:DATA <type>[,<length>]

- HCOPy:DEVice:COLor <Boolean>

- HCOPy:DEVice:CMAP:COLor:RGB <red>,<green>,<blue>

- HCOPy[:IMMediate]

- HCOPy:ITEM:ALL

- HCOPy:ITEM:LABel <string>

- HCOPy:PAGE:DIMensions:QUADrant[<N>]

- HCOPy:PAGE:ORIentation LANDscape | PORTrait

- HCOPy:PAGE:SCALe <numeric value>

- MMEMory:COPY <file_source>,<file_destination>

- SENSE:BANDwidth|BWIDth[:RESolution] <numeric_value>

- SENSe:FREQuency:STOP <numeric value>

- SENSe:LIST:FREQuency <numeric_value>{,<numeric_value>}

<!-- 来源：RTM2_UserManual_en_10_files\part2400.htm -->

### Long and short form

The mnemonics feature a long form and a short form. The short form is marked by upper case letters, the long form corresponds to the complete word. Either the short form or the long form can be entered; other abbreviations are not permitted.

<!-- 来源：RTM2_UserManual_en_10_files\part2401.htm -->

### Example:

```text
HCOPy:DEVice:COLor ON is equivalent to HCOP:DEV:COL ON.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2402.htm -->

### Case-insensitivity

Upper case and lower case notation only serves to distinguish the two forms in the manual, the instrument itself is case-insensitive.

<!-- 来源：RTM2_UserManual_en_10_files\part2403.htm -->

### Numeric suffixes

If a command can be applied to multiple instances of an object, e.g. specific channels or sources, the required instances can be specified by a suffix added to the command. Numeric suffixes are indicated by angular brackets (<1...4>, <n>, <i>) and are replaced by a single value in the command. Entries without a suffix are interpreted as having the suffix 1.

<!-- 来源：RTM2_UserManual_en_10_files\part2404.htm -->

### Example:

Definition: HCOPy:PAGE:DIMensions:QUADrant[<N>]

Command: HCOP:PAGE:DIM:QUAD2

This command refers to the quadrant 2.

<!-- 来源：RTM2_UserManual_en_10_files\part2405.htm -->

### Different numbering in remote control

For remote control, the suffix may differ from the number of the corresponding selec- tion used in manual operation. SCPI prescribes that suffix counting starts with 1. Suffix 1 is the default state and used when no specific suffix is specified.

<!-- 来源：RTM2_UserManual_en_10_files\part2406.htm -->

### Optional mnemonics

Some command systems permit certain mnemonics to be inserted into the header or omitted. These mnemonics are marked by square brackets in the description. The instrument must recognize the long command to comply with the SCPI standard. Some commands are considerably shortened by these optional mnemonics.

<!-- 来源：RTM2_UserManual_en_10_files\part2407.htm -->

### Example:

Definition: HCOPy[:IMMediate]

Command: HCOP:IMM is equivalent to HCOP

<!-- 来源：RTM2_UserManual_en_10_files\part2408.htm -->

### Optional mnemonics with numeric suffixes

Do not omit an optional mnemonic if it includes a numeric suffix that is relevant for the effect of the command.

<!-- 来源：RTM2_UserManual_en_10_files\part2409.htm -->

### Example:

Definition: DISPlay[:WINDow<1...4>]:MAXimize <Boolean>

Command: DISP:MAX ON refers to window 1.

In order to refer to a window other than 1, you must include the optional WINDow

parameter with the suffix for the required window.

```text
DISP:WIND2:MAX ON refers to window 2.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2410.htm -->

### Parameters

Parameters must be separated from the header by a "white space". If several parame- ters are specified in a command, they are separated by a comma (,). For a description of the parameter types, refer to Chapter A.2.3, "SCPI Parameters", on page 771.

<!-- 来源：RTM2_UserManual_en_10_files\part2411.htm -->

### Example:

Definition: HCOPy:DEVice:CMAP:COLor:RGB <red>,<green>,<blue>

Command: HCOP:DEV:CMAP:COL:RGB 3,32,44

### Special characters

| \| | Parameters A vertical stroke in parameter definitions indicates alternative possibilities in the sense of "or". The effect of the command differs, depending on which parameter is used. Example: Definition: HCOPy:PAGE:ORIentation LANDscape \| PORTrait Command HCOP:PAGE:ORI LAND specifies landscape orientation Command HCOP:PAGE:ORI PORT specifies portrait orientation Mnemonics A selection of mnemonics with an identical effect exists for several commands. These mnemonics are indicated in the same line; they are separated by a vertical stroke. Only one of these mnemonics needs to be included in the header of the command. The effect of the command is independent of which of the mnemonics is used. Example: Definition SENSE:BANDwidth\|BWIDth[:RESolution] <numeric_value> The two following commands with identical meaning can be created: SENS:BAND:RES 1 SENS:BWID:RES 1 |
| --- | --- |
| [ ] | Mnemonics in square brackets are optional and may be inserted into the header or omitted. Example: HCOPy[:IMMediate] HCOP:IMM is equivalent to HCOP |
| { } | Parameters in curly brackets are optional and can be inserted once or several times, or omitted. Example: SENSe:LIST:FREQuency <numeric_value>{,<numeric_value>} The following are valid commands: SENS:LIST:FREQ 10 SENS:LIST:FREQ 10,20 SENS:LIST:FREQ 10,20,30,40 |

<!-- 来源：RTM2_UserManual_en_10_files\part2412.htm -->

## A.2.3 SCPI Parameters

Many commands are supplemented by a parameter or a list of parameters. The parameters must be separated from the header by a "white space" (ASCII code 0 to 9, 11 to 32 decimal, e.g. blank). Allowed parameters are:

- Numeric values

- Special numeric values

- Boolean parameters

- Text

- Character strings

- Block data

The parameters required for each command and the allowed range of values are specified in the command description.

<!-- 来源：RTM2_UserManual_en_10_files\part2413.htm -->

### Numeric values

Numeric values can be entered in any form, i.e. with sign, decimal point and exponent. Values exceeding the resolution of the instrument are rounded up or down. The man- tissa may comprise up to 255 characters, the exponent must lie inside the value range

-32000 to 32000. The exponent is introduced by an "E" or "e". Entry of the exponent alone is not allowed. In the case of physical quantities, the unit can be entered.

Allowed unit prefixes are G (giga), MA (mega), MOHM and MHZ are also allowed), K (kilo), M (milli), U (micro) and N (nano). If the unit is missing, the basic unit is used.

```text
Example: SENS:FREQ:STOP 1.5GHz = SENS:FREQ:STOP 1.5E9
```

<!-- 来源：RTM2_UserManual_en_10_files\part2414.htm -->

### Units

For physical quantities, the unit can be entered. Allowed unit prefixes are:

- G (giga)

- MA (mega), MOHM, MHZ

- K (kilo)

- M (milli)

- U (micro)

- N (nano)

If the unit is missing, the basic unit is used.

<!-- 来源：RTM2_UserManual_en_10_files\part2415.htm -->

### Example:

```text
SENS:FREQ:STOP 1.5GHz = SENS:FREQ:STOP 1.5E9
```

Some settings allow relative values to be stated in percent. According to SCPI, this unit is represented by the PCT string.

<!-- 来源：RTM2_UserManual_en_10_files\part2416.htm -->

### Example:

```text
HCOP:PAGE:SCAL 90PCT
```

<!-- 来源：RTM2_UserManual_en_10_files\part2417.htm -->

### Special numeric values

The texts listed below are interpreted as special numeric values. In the case of a query, the numeric value is provided.

- MIN/MAX

MINimum and MAXimum denote the minimum and maximum value.

<!-- 来源：RTM2_UserManual_en_10_files\part2418.htm -->

### Example:

Setting command: SENSe:LIST:FREQ MAXimum

Query: SENS:LIST:FREQ?, Response: 3.5E9

<!-- 来源：RTM2_UserManual_en_10_files\part2419.htm -->

### Queries for special numeric values

The numeric values associated to MAXimum/MINimum can be queried by adding the corresponding mnemonics to the command. They must be entered following the quota- tion mark.

Example: SENSe:LIST:FREQ? MAXimum

Returns the maximum numeric value as a result.

<!-- 来源：RTM2_UserManual_en_10_files\part2420.htm -->

### Boolean Parameters

Boolean parameters represent two states. The "ON" state (logically true) is represen- ted by "ON" or a numeric value 1. The "OFF" state (logically untrue) is represented by "OFF" or the numeric value 0. The numeric values are provided as the response for a query.

<!-- 来源：RTM2_UserManual_en_10_files\part2421.htm -->

### Example:

Setting command: HCOPy:DEV:COL ON

Query: HCOPy:DEV:COL?

Response: 1

<!-- 来源：RTM2_UserManual_en_10_files\part2422.htm -->

### Text parameters

Text parameters observe the syntactic rules for mnemonics, i.e. they can be entered using a short or long form. Like any parameter, they have to be separated from the header by a white space. In the case of a query, the short form of the text is provided.

<!-- 来源：RTM2_UserManual_en_10_files\part2423.htm -->

### Example:

Setting command: HCOPy:PAGE:ORIentation LANDscape

Query: HCOP:PAGE:ORI?

Response: LAND

<!-- 来源：RTM2_UserManual_en_10_files\part2424.htm -->

### Character strings

Strings must always be entered in quotation marks (' or ").

<!-- 来源：RTM2_UserManual_en_10_files\part2425.htm -->

### Example:

```text
HCOP:ITEM:LABel "Test1" or HCOP:ITEM:LABel 'Test1'
```

<!-- 来源：RTM2_UserManual_en_10_files\part2426.htm -->

### Block data

Block data is a format which is suitable for the transmission of large amounts of data. A command using a block data parameter has the following structure:

<!-- 来源：RTM2_UserManual_en_10_files\part2427.htm -->

### Example:

```text
FORMat:READings:DATA #45168xxxxxxxx
```

The ASCII character # introduces the data block. The next number indicates how many of the following digits describe the length of the data block. In the example the 4 follow- ing digits indicate the length to be 5168 bytes. The data bytes follow. During the trans- mission of these data bytes all end or other control signs are ignored until all bytes are transmitted.

#0 specifies a data block of indefinite length. The use of the indefinite format requires a NL^END message to terminate the data block. This format is useful when the length of the transmission is not known or if speed or other considerations prevent segmentation of the data into blocks of definite length.

<!-- 来源：RTM2_UserManual_en_10_files\part2428.htm -->

## A.2.4 Overview of Syntax Elements

The following table provides an overview of the syntax elements:

| : | The colon separates the mnemonics of a command. In a command line the separating semico- lon marks the uppermost command level. |
| --- | --- |
| ; | The semicolon separates two commands of a command line. It does not alter the path. |
| , | The comma separates several parameters of a command. |
| ? | The question mark forms a query. |
| * | The asterisk marks a common command. |
| ' ' " | Quotation marks introduce a string and terminate it. Both single and double quotation marks are possible. |
| # | The hash symbol introduces binary, octal, hexadecimal and block data. ● Binary: #B10110 ● Octal: #O7612 ● Hexa: #HF3A7 ● Block: #21312 |
|  | A "white space" (ASCII-Code 0 to 9, 11 to 32 decimal, e.g. blank) separates the header from the parameters. |

<!-- 来源：RTM2_UserManual_en_10_files\part2429.htm -->

## A.2.5 Structure of a command line

A command line may consist of one or several commands. It is terminated by one of the following:

- a <New Line>

- a <New Line> with EOI

- an EOI together with the last data byte

Several commands in a command line must be separated by a semicolon ";". If the next command belongs to a different command system, the semicolon is followed by a colon.

<!-- 来源：RTM2_UserManual_en_10_files\part2430.htm -->

### Example:

```text
MMEM:COPY "Test1","MeasurementXY";:HCOP:ITEM ALL
```

This command line contains two commands. The first command belongs to the MMEM system, the second command belongs to the HCOP system.

If the successive commands belong to the same system, having one or several levels in common, the command line can be abbreviated. To this end, the second command after the semicolon starts with the level that lies below the common levels. The colon following the semicolon must be omitted in this case.

<!-- 来源：RTM2_UserManual_en_10_files\part2431.htm -->

### Example:

```text
HCOP:ITEM ALL;:HCOP:IMM
```

This command line contains two commands. Both commands are part of the HCOP

command system, i.e. they have one level in common.

When abbreviating the command line, the second command begins with the level below HCOP. The colon after the semicolon is omitted. The abbreviated form of the command line reads as follows:

```text
HCOP:ITEM ALL;IMM
```

A new command line always begins with the complete path.

<!-- 来源：RTM2_UserManual_en_10_files\part2432.htm -->

### Example:

```text
HCOP:ITEM ALL HCOP:IMM
```

<!-- 来源：RTM2_UserManual_en_10_files\part2433.htm -->

## A.2.6 Responses to Queries

A query is defined for each setting command unless explicitly specified otherwise. It is formed by adding a question mark to the associated setting command. According to SCPI, the responses to queries are partly subject to stricter rules than in standard IEEE 488.2.

- The requested parameter is transmitted without a header.

```text
Example: HCOP:PAGE:ORI?, Response: LAND
```

- Maximum values, minimum values and all other quantities that are requested via a special text parameter are returned as numeric values.

```text
Example: SENSe:FREQuency:STOP? MAX, Response: 3.5E9
```

- Numeric values are output without a unit. Physical quantities are referred to the basic units or to the units set using the Unit command. The response 3.5E9 in the previous example stands for 3.5 GHz.

- Truth values (Boolean values) are returned as 0 (for OFF) and 1 (for ON).

<!-- 来源：RTM2_UserManual_en_10_files\part2434.htm -->

### Example:

Setting command: HCOPy:DEV:COL ON

Query: HCOPy:DEV:COL?

Response: 1

- Text (character data) is returned in a short form.

<!-- 来源：RTM2_UserManual_en_10_files\part2435.htm -->

### Example:

Setting command: HCOPy:PAGE:ORIentation LANDscape

Query: HCOP:PAGE:ORI?

Response: LAND

<!-- 来源：RTM2_UserManual_en_10_files\part2436.htm -->

## A.3 Command Sequence and Synchronization

IEEE 488.2 defines a distinction between overlapped and sequential commands:

- A sequential command is one which finishes executing before the next command starts executing. Commands that are processed quickly are usually implemented as sequential commands.

- An overlapping command is one which does not automatically finish executing before the next command starts executing. Usually, overlapping commands take longer to process and allow the program to do other tasks while being executed. If overlapping commands do have to be executed in a defined order, e.g. in order to avoid wrong measurement results, they must be serviced sequentially. This is called synchronization between the controller and the instrument.

Setting commands within one command line, even though they may be implemented as sequential commands, are not necessarily serviced in the order in which they have been received. In order to make sure that commands are actually carried out in a cer- tain order, each command must be sent in a separate command line.

<!-- 来源：RTM2_UserManual_en_10_files\part2437.htm -->

### Example: Commands and queries in one message

The response to a query combined in a program message with commands that affect the queried value is not predictable.

The following commands always return the specified result:

```text
:FREQ:STAR 1GHZ;SPAN 100:FREQ:STAR?
```

Result:

```text
1000000000 (1 GHz)
```

Whereas the result for the following commands is not specified by SCPI:

```text
:FREQ:STAR 1GHz;STAR?;SPAN 1000000
```

As a general rule, send commands and queries in different program messages.

The result could be the value of STARt before the command was sent since the instru- ment might defer executing the individual commands until a program message termi- nator is received. The result could also be 1 GHz if the instrument executes commands as they are received.

<!-- 来源：RTM2_UserManual_en_10_files\part2438.htm -->

### Example: Overlapping command with *OPC

The instrument implements SINGle as an overlapped (asynchronous) command. Assuming that SINGle takes longer to execute than *OPC, sending the following com- mand sequence results in initiating a sweep and, after some time, setting the OPC bit in the ESR:

```text
SINGle; *OPC.
```

Sending the following commands still initiates a sweep:

```text
SINGle; *OPC; *CLS
```

However, since the operation is still pending when the instrument executes *CLS, forc- ing it into the "Operation Complete Command Idle" State (OCIS), *OPC is effectively skipped. The OPC bit is not set until the instrument executes another *OPC command.

<!-- 来源：RTM2_UserManual_en_10_files\part2439.htm -->

## A.3.1 Preventing Overlapping Execution

To prevent an overlapping execution of commands, one of the commands *OPC,

*OPC? or *WAI can be used. All three commands cause a certain action only to be carried out after the hardware has been set. By suitable programming, the controller can be forced to wait for the corresponding action to occur.

#### Table A-1: Synchronization using *OPC, *OPC? and *WAI

| Com- mand | Action | Programming the controller |
| --- | --- | --- |
| *OPC | Sets the Operation Complete bit in the ESR after all previous commands have been exe- cuted. | ● Setting bit 0 in the ESE ● Setting bit 5 in the SRE ● Waiting for service request (SRQ) |
| *OPC? | Stops command processing until 1 is returned. This is only the case after the Oper- ation Complete bit has been set in the ESR. This bit indicates that the previous setting has been completed. | Sending *OPC? directly after the command whose processing should be terminated before other commands can be executed. |
| *WAI | Stops further command processing until all commands sent before *WAI have been exe- cuted. | Sending *WAI directly after the command whose processing should be terminated before other commands are executed. |

Command synchronization using *WAI or *OPC? is a good choice if the overlapped command takes only little time to process. The two synchronization commands simply block overlapped execution of the command. Append the synchronization command to the overlapping command, for example:

```text
SINGle; *OPC?
```

For time consuming overlapped commands you can allow the controller or the instru- ment to do other useful work while waiting for command execution. Use one of the fol- lowing methods:

<!-- 来源：RTM2_UserManual_en_10_files\part2440.htm -->

### *OPC with a service request

1. Set the OPC mask bit (bit no. 0) in the ESE: *ESE 1

2. Set bit no. 5 in the SRE: *SRE 32 to enable ESB service request.

3. Send the overlapped command with *OPC

4. Wait for a service request

The service request indicates that the overlapped command has finished.

<!-- 来源：RTM2_UserManual_en_10_files\part2441.htm -->

### *OPC? with a service request

1. Set bit no. 4 in the SRE: *SRE 16 to enable MAV service request.

2. Send the overlapped command with *OPC?

3. Wait for a service request

The service request indicates that the overlapped command has finished.

<!-- 来源：RTM2_UserManual_en_10_files\part2442.htm -->

### Event Status Register (ESE)

1. Set the OPC mask bit (bit no. 0) in the ESE: *ESE 1

2. Send the overlapped command without *OPC, *OPC? or *WAI

3. Poll the operation complete state periodically (by means of a timer) using the sequence: *OPC; *ESR?

A return value (LSB) of 1 indicates that the overlapped command has finished.

<!-- 来源：RTM2_UserManual_en_10_files\part2443.htm -->

## A.4 General Programming Recommendations

<!-- 来源：RTM2_UserManual_en_10_files\part2444.htm -->

### Initial instrument status before changing settings

Manual operation is designed for maximum possible operating convenience. In con- trast, the priority of remote control is the "predictability" of the instrument status. Thus, when a command attempts to define incompatible settings, the command is ignored and the instrument status remains unchanged, i.e. other settings are not automatically adapted. Therefore, control programs should always define an initial instrument status (e.g. using the *RST command) and then implement the required settings.

<!-- 来源：RTM2_UserManual_en_10_files\part2445.htm -->

### Command sequence

As a general rule, send commands and queries in different program messages. Other- wise, the result of the query may vary depending on which operation is performed first (see also Preventing Overlapping Execution).

<!-- 来源：RTM2_UserManual_en_10_files\part2446.htm -->

### Reacting to malfunctions

The service request is the only possibility for the instrument to become active on its own. Each controller program should instruct the instrument to initiate a service request in case of malfunction. The program should react appropriately to the service request.

<!-- 来源：RTM2_UserManual_en_10_files\part2447.htm -->

### Error queues

The error queue should be queried after every service request in the controller pro- gram as the entries describe the cause of an error more precisely than the status regis- ters. Especially in the test phase of a controller program the error queue should be queried regularly since faulty commands from the controller to the instrument are recorded there as well.

<!-- 来源：RTM2_UserManual_en_10_files\part2448.htm -->

### B Status Reporting System

B Status Reporting System

Structure of a SCPI Status Register

The status reporting system stores all information on the current operating state of the instrument, and on errors which have occurred. This information is stored in the status registers and in the error queue. Both can be queried via GPIB bus or LAN interface ( STATus... commands).

<!-- 来源：RTM2_UserManual_en_10_files\part2449.htm -->

## B.1 Structure of a SCPI Status Register

Each standard SCPI register consists of 5 parts. Each part has a width of 16 bits and has different functions. The individual bits are independent of each other, i.e. each hardware status is assigned a bit number which is valid for all five parts. Bit 15 (the most significant bit) is set to zero for all parts. Thus the contents of the register parts can be processed by the controller as positive integers.

#### Figure B-1: The status-register model

<!-- 来源：RTM2_UserManual_en_10_files\part2450.htm -->

### Description of the five status register parts

The five parts of a SCPI register have different properties and functions:

<!-- 来源：RTM2_UserManual_en_10_files\part2451.htm -->

### ● CONDition

- CONDition

The CONDition part is written into directly by the hardware or the sum bit of the next lower register. Its contents reflect the current instrument status. This register part can only be read, but not written into or cleared. Its contents are not affected by reading.

<!-- 来源：RTM2_UserManual_en_10_files\part2452.htm -->

### ● PTRansition / NTRansition

- PTRansition / NTRansition

The two transition register parts define which state transition of the CONDition

part (none, 0 to 1, 1 to 0 or both) is stored in the EVENt part.

The Positive-TRansition part acts as a transition filter. When a bit of the CONDition part is changed from 0 to 1, the associated PTR bit decides whether the EVENt bit is set to 1.

– PTR bit =1: the EVENt bit is set.

– PTR bit =0: the EVENt bit is not set.

This part can be written into and read as required. Its contents are not affected by reading.

The Negative-TRansition part also acts as a transition filter. When a bit of the CONDition part is changed from 1 to 0, the associated NTR bit decides whether the EVENt bit is set to 1.

– NTR bit =1: the EVENt bit is set.

– NTR bit =0: the EVENt bit is not set.

This part can be written into and read as required. Its contents are not affected by reading.

- EVENt

The EVENt part indicates whether an event has occurred since the last reading, it is the "memory" of the condition part. It only indicates events passed on by the transition filters. It is permanently updated by the instrument. This part can only be read by the user. Reading the register clears it. This part is often equated with the entire register.

- ENABle

The ENABle part determines whether the associated EVENt bit contributes to the sum bit (see below). Each bit of the EVENt part is "ANDed" with the associated ENABle bit (symbol '&'). The results of all logical operations of this part are passed on to the sum bit via an "OR" function (symbol '+').

```text
ENABle bit = 0: the associated EVENt bit does not contribute to the sum bit ENABle bit = 1: if the associated EVENt bit is "1", the sum bit is set to "1" as well. This part can be written into and read by the user as required. Its contents are not affected by reading.
```

<!-- 来源：RTM2_UserManual_en_10_files\part2453.htm -->

### Sum bit

The sum bit is obtained from the EVENt and ENABle part for each register. The result is then entered into a bit of the CONDition part of the higher-order register.

The instrument automatically generates the sum bit for each register. Thus an event can lead to a service request throughout all levels of the hierarchy.

<!-- 来源：RTM2_UserManual_en_10_files\part2454.htm -->

## B.2 Hierarchy of status registers

As shown in the following figure, the status information is of hierarchical structure.

#### Figure B-2: Overview of the status registers hierarchy

<!-- 来源：RTM2_UserManual_en_10_files\part2455.htm -->

### ● STB, SRE

- STB, SRE

The STatus Byte ( STB ) register and its associated mask register Service Request Enable ( SRE ) form the highest level of the status reporting system. The STB pro- vides a rough overview of the instrument status, collecting the information of the lower-level registers.

<!-- 来源：RTM2_UserManual_en_10_files\part2456.htm -->

### ● ESR, SCPI registers

- ESR, SCPI registers

The STB receives its information from the following registers:

– The Event Status Register ( ESR ) with the associated mask register standard Event Status Enable ( ESE ).

– The STATus:OPERation and STATus:QUEStionable registers which are defined by SCPI and contain detailed information on the instrument.

<!-- 来源：RTM2_UserManual_en_10_files\part2457.htm -->

### ● Output buffer

- Output buffer

The output buffer contains the messages the instrument returns to the controller. It is not part of the status reporting system but determines the value of the MAV bit in the STB and thus is represented in the overview.

All status registers have the same internal structure.

<!-- 来源：RTM2_UserManual_en_10_files\part2458.htm -->

### SRE, ESE

The service request enable register SRE can be used as ENABle part of the STB if the STB is structured according to SCPI. By analogy, the ESE can be used as the ENABle part of the ESR.

<!-- 来源：RTM2_UserManual_en_10_files\part2459.htm -->

## B.3 Contents of the Status Registers

In the following sections, the contents of the status registers are described in more detail.

<!-- 来源：RTM2_UserManual_en_10_files\part2460.htm -->

## B.3.1 Status Byte (STB) and Service Request Enable Register (SRE)

The STatus Byte (STB) is already defined in IEEE 488.2. It provides a rough over- view of the instrument status by collecting the pieces of information of the lower regis- ters. A special feature is that bit 6 acts as the sum bit of the remaining bits of the status byte.

The STB can thus be compared with the CONDition part of an SCPI register and assumes the highest level within the SCPI hierarchy.

```text
The STB is read using the command *STB? or a serial poll.
```

The STatus Byte (STB) is linked to the Service Request Enable (SRE) register. Each bit of the STB is assigned a bit in the SRE. Bit 6 of the SRE is ignored. If a bit is set in the SRE and the associated bit in the STB changes from 0 to 1, a service request (SRQ) is generated. The SRE can be set using the command *SRE and read using the command *SRE?.

#### Table B-1: Meaning of the bits used in the status byte

| Bit No. | Meaning |
| --- | --- |
| 0...1 | Not used |
| 2 | Error Queue not empty The bit is set when an entry is made in the error queue. If this bit is enabled by the SRE, each entry of the error queue generates a service request. Thus an error can be recognized and specified in greater detail by polling the error queue. The poll provides an informative error mes- sage. This procedure is to be recommended since it considerably reduces the problems involved with remote control. |
| 3 | QUEStionable status register summary bit The bit is set if an EVENt bit is set in the QUEStionable status register and the associated ENABle bit is set to 1. A set bit indicates a questionable instrument status, which can be speci- fied in greater detail by querying the STATus:QUEStionable status register. |

| Bit No. | Meaning |
| --- | --- |
| 4 | MAV bit (message available) The bit is set if a message is available in the output queue which can be read. This bit can be used to enable data to be automatically read from the instrument to the controller. |
| 5 | ESB bit Sum bit of the event status register. It is set if one of the bits in the event status register is set and enabled in the event status enable register. Setting of this bit indicates a serious error which can be specified in greater detail by polling the event status register. |
| 6 | MSS bit (master status summary bit) The bit is set if the instrument triggers a service request. This is the case if one of the other bits of this registers is set together with its mask bit in the service request enable register SRE. |
| 7 | STATus:OPERation status register summary bit The bit is set if an EVENt bit is set in the OPERation status register and the associated ENABle bit is set to 1. A set bit indicates that the instrument is just performing an action. The type of action can be determined by querying the STATus:OPERation status register. |

<!-- 来源：RTM2_UserManual_en_10_files\part2461.htm -->

## B.3.2 Event Status Register (ESR) and Event Status Enable Register (ESE)

The ESR is defined in IEEE 488.2. It can be compared with the EVENt part of a SCPI register. The event status register can be read out using command *ESR?.

The ESE corresponds to the ENABle part of a SCPI register. If a bit is set in the ESE and the associated bit in the ESR changes from 0 to 1, the ESB bit in the STB is set. The ESE register can be set using the command *ESE and read using the command

```text
*ESE?.
```

#### Table B-2: Meaning of the bits used in the event status register

| Bit No. | Meaning |
| --- | --- |
| 0 | Operation Complete This bit is set on receipt of the command *OPC exactly when all previous commands have been executed. |
| 1 | Not used |
| 2 | Query Error This bit is set if either the controller wants to read data from the instrument without having sent a query, or if it does not fetch requested data and sends new instructions to the instrument instead. The cause is often a query which is faulty and hence cannot be executed. |
| 3 | Device-dependent Error This bit is set if a device-dependent error occurs. An error message with a number between -300 and -399 or a positive error number, which denotes the error in greater detail, is entered into the error queue. |
| 4 | Execution Error This bit is set if a received command is syntactically correct but cannot be performed for other reasons. An error message with a number between -200 and -300, which denotes the error in greater detail, is entered into the error queue. |

| Bit No. | Meaning |
| --- | --- |
| 5 | Command Error This bit is set if a command is received, which is undefined or syntactically incorrect. An error message with a number between -100 and -200, which denotes the error in greater detail, is entered into the error queue. |
| 6 | User Request This bit is set when the instrument is switched over to manual control. |
| 7 | Power On (supply voltage on) This bit is set on switching on the instrument. |

<!-- 来源：RTM2_UserManual_en_10_files\part2462.htm -->

## B.3.3 STATus:OPERation Register

In the CONDition part, this register contains information on which actions the instru- ment is being executing. In the EVENt part, it contains information on which actions the instrument has executed since the last reading. It can be read using the commands STATus:OPERation:CONDition? or STATus:OPERation[:EVENt]?.

See also: Figure B-2

The remote commands for the STATus:OPERation register are described in Chap- ter 18.19.1, "STATus:OPERation Register", on page 759.

#### Table B-3: Bits in the STATus:OPERation register

| Bit No. | Meaning |
| --- | --- |
| 0 | ALIGnment This bit is set as long as the instrument is performing a self alignment. |
| 1 | SELFtest This bit is set while the selftest is running. |
| 2 | AUToset This bit is set while the instrument is performing an auto setup. |
| 3 | WTRIgger This bit is set while the instrument is waiting for the trigger. |
| 4 to 14 | Not used |
| 15 | This bit is always 0. |

<!-- 来源：RTM2_UserManual_en_10_files\part2463.htm -->

## B.3.4 STATus:QUEStionable Register

This register contains information about indefinite states which may occur if the unit is operated without meeting the specifications. It can be read using the commands STATus:QUEStionable:CONDition? on page 762 and STATus: QUEStionable[:EVENt]? on page 763

| Bit No. | Meaning |
| --- | --- |
| 0 to 2 | not used |
| 3 | COVerload This bit is set if a questionable channel overload occurs (see Chapter B.3.4.1, "STATus:QUES- tionable:COVerload register", on page 787). |
| 4 | TEMPerature This bit is set if a questionable temperature occurs (see Chapter B.3.4.2, "STATus:QUEStiona- ble:TEMPerature register", on page 787). |
| 5 to 7 | Not used |

#### Figure B-3: Overview of the STATus:QUEStionable register Table B-4: Bits in the STATus:QUEStionable register

| Bit No. | Meaning |
| --- | --- |
| 8 | NOALigndata This bit is set if no alignment data is available - the instrument is uncalibrated. |
| 9 | LIMit This bit is set if a limit value is violated (see Chapter B.3.4.3, "STATus:QUEStionable:LIMit reg- ister", on page 787). |
| 10 to 11 | Not used |
| 12 | MASK This bit is set if a mask value is violated (see Chapter B.3.4.4, "STATus:QUEStionable:MASK register", on page 788 |
| 13 to 14 | Not used |
| 15 | This bit is always 0. |

### B.3.4.1 STATus:QUEStionable:COVerload register

This register contains all information about overload of the channels. The bit is set if the assigned channel is overloaded.

#### Table B-5: Bits in the STATus:QUEStionable:COVerload register

| Bit No. | Meaning |
| --- | --- |
| 0 | CHANnel1 |
| 1 | CHANnel2 |
| 2 | CHANnel3 |
| 3 | CHANnel4 |

### B.3.4.2 STATus:QUEStionable:TEMPerature register

This register contains information about the instrument's temperature.

#### Table B-6: Bits in the STATus:QUEStionable:TEMPerature register

| Bit No. | Meaning |
| --- | --- |
| 0 | TEMP WARN This bit is set if a temperature warning on channel 1, 2, 3 or 4 occured. |
| 1 | TEMP ERRor This bit is set if a temperature error on channel 1, 2, 3 or 4 occured. |

### B.3.4.3 STATus:QUEStionable:LIMit register

This register contains information about the observance of the limits of measurements. This bit is set if the limits of the main or additional measurement of the assigned mea- surement are violated.

#### Table B-7: Bits in the STATus:QUEStionable:LIMit register

| Bit No. | Meaning |
| --- | --- |
| 0 | MEAS1 |
| 1 | MEAS2 |
| 2 | MEAS3 |
| 3 | MEAS4 |

### B.3.4.4 STATus:QUEStionable:MASK register

This register contains information about the violation of masks. This bit is set if the assigned mask is violated.

#### Table B-8: Bits in the STATus:QUEStionable:MASK register

| Bit No. | Meaning |
| --- | --- |
| 0 | MASK1 |

<!-- 来源：RTM2_UserManual_en_10_files\part2464.htm -->

## B.4 Application of the Status Reporting System

The purpose of the status reporting system is to monitor the status of one or several devices in a measuring system. To do this and react appropriately, the controller must receive and evaluate the information of all devices. The following standard methods are used:

- Service request (SRQ) initiated by the instrument

- Serial poll of all devices in the bus system, initiated by the controller in order to find out who sent a SRQ and why

- Parallel poll of all devices

- Query of a specific instrument status by means of commands

- Query of the error queue

<!-- 来源：RTM2_UserManual_en_10_files\part2465.htm -->

## B.4.1 Service Request

Under certain circumstances, the instrument can send a service request (SRQ) to the controller. Usually this service request initiates an interrupt at the controller, to which the control program can react appropriately. As evident from Figure B-2, an SRQ is always initiated if one or several of bits 2, 3, 4, 5 or 7 of the status byte are set and enabled in the SRE. Each of these bits combines the information of a further register, the error queue or the output buffer. The ENABle parts of the status registers can be set such that arbitrary bits in an arbitrary status register initiate an SRQ. In order to make use of the possibilities of the service request effectively, all bits should be set to "1" in enable registers SRE and ESE.

The SRQ is the only possibility for the instrument to become active on its own. Each controller program should cause the instrument to initiate a service request if errors occur. The program should react appropriately to the service request.

<!-- 来源：RTM2_UserManual_en_10_files\part2466.htm -->

## B.4.2 Serial Poll

In a serial poll, just as with command *STB, the status byte of an instrument is queried. However, the query is realized via interface messages and is thus clearly faster.

The serial poll method is defined in IEEE 488.1 and used to be the only standard pos- sibility for different instruments to poll the status byte. The method also works for instruments which do not adhere to SCPI or IEEE 488.2.

The serial poll is mainly used to obtain a fast overview of the state of several instru- ments connected to the controller.

<!-- 来源：RTM2_UserManual_en_10_files\part2467.htm -->

## B.4.3 Query of an instrument status

Each part of any status register can be read using queries. There are two types of commands:

- The common commands *ESR?, *IDN?, *IST?, *STB? query the higher-level registers.

- The commands of the STATus system query the SCPI registers ( STATus:QUEStionable...)

The returned value is always a decimal number that represents the bit pattern of the queried register. This number is evaluated by the controller program.

Queries are usually used after an SRQ in order to obtain more detailed information on the cause of the SRQ.

### B.4.3.1 Decimal representation of a bit pattern

The STB and ESR registers contain 8 bits, the SCPI registers 16 bits. The contents of a status register are specified and transferred as a single decimal number. To make this possible, each bit is assigned a weighted value. The decimal number is calculated as the sum of the weighted values of all bits in the register that are set to 1.

<!-- 来源：RTM2_UserManual_en_10_files\part2468.htm -->

### Example:

The decimal value 40 = 32 + 8 indicates that bits no. 3 and 5 in the status register (e.g. the QUEStionable status summary bit and the ESB bit in the STatus Byte ) are set.

<!-- 来源：RTM2_UserManual_en_10_files\part2469.htm -->

## B.4.4 Error Queue

Each error state in the instrument leads to an entry in the error queue. The entries of the error queue are detailed plain text error messages that can be looked up in the Error Log or queried via remote control using SYSTem:ERRor[:NEXT]?. Each call of SYSTem:ERRor[:NEXT]? provides one entry from the error queue. If no error mes- sages are stored there any more, the instrument responds with 0, "No error".

The error queue should be queried after every SRQ in the controller program as the entries describe the cause of an error more precisely than the status registers. Espe- cially in the test phase of a controller program the error queue should be queried regu- larly since faulty commands from the controller to the instrument are recorded there as well.

<!-- 来源：RTM2_UserManual_en_10_files\part2470.htm -->

## B.5 Reset Values of the Status Reporting System

The following table contains the different commands and events causing the status reporting system to be reset. None of the commands, except *RST and SYSTem:PRESet, influence the functional instrument settings. In particular, DCL does not change the instrument settings.

#### Table B-9: Resest of the status reporting system

| Event | Switching on supply voltage Power-On-Status- Clear | DCL, SDC (Device Clear, Selected Device Clear) | *RST or SYS- Tem:PRE- Set | STA- Tus:PRE- Set | *CLS |  |
| --- | --- | --- | --- | --- | --- | --- |
| Effect | 0 | 1 |  |  |  |  |
| Clear STB, ESR | - | yes | - | - | - | yes |
| Clear SRE, ESE | - | yes | - | - | - | - |
| Clear EVENt parts of the regis- ters | - | yes | - | - | - | yes |
| Clear ENABle parts of all OPERation and QUEStionable registers; Fill ENABle parts of all other registers with "1". | - | yes | - | - | yes | - |
| Fill PTRansition parts with "1"; Clear NTRansition parts | - | yes | - | - | yes | - |
| Clear error queue | yes | yes | - | - | - | yes |

| Event | Switching on supply voltage Power-On-Status- Clear | DCL, SDC (Device Clear, Selected Device Clear) | *RST or SYS- Tem:PRE- Set | STA- Tus:PRE- Set | *CLS |  |
| --- | --- | --- | --- | --- | --- | --- |
| Effect | 0 | 1 |  |  |  |  |
| Clear output buffer | yes | yes | yes | 1) | 1) | 1) |
| Clear command processing and input buffer | yes | yes | yes | - | - | - |
| 1) The first command in a command line that immediately follows a <PROGRAM MESSAGE TERMINA- TOR> clears the output buffer. |  |  |  |  |  |  |

<!-- 来源：RTM2_UserManual_en_10_files\part2471.htm -->

### List of Commands

List of Commands

*CAL? 410

*CLS. 410

*ESE. 410

*ESR?. 410

*IDN?. 410

*OPC. 411

*OPT?. 411

*PSC. 411

*RST. 412

*SRE. 412

*STB?. 412

*TRG. 412

*TST?. 412

*WAI. 413

ACQuire:AVAilable? 438

ACQuire:AVERage:COMPlete?. 417

ACQuire:AVERage:COUNt. 417

ACQuire:COUNt? 437

ACQuire:FILTer:FREQuency. 420

ACQuire:INTerpolate 417

ACQuire:MODE. 417

ACQuire:NSINgle:COUNt. 414

ACQuire:NSINgle:MAXimum. 438

ACQuire:POINts:ARATe?. 420

ACQuire:POINts[:VALue]. 418

ACQuire:SEGMented:MAXimum 438

ACQuire:SEGMented:STATe. 438

ACQuire:SRATe:ZOOM?. 469

ACQuire:SRATe? 421

ACQuire:WRATe. 418

AUToscale 416

BUS<b>:ARINc:BRMode 653

BUS<b>:ARINc:BRValue 653

BUS<b>:ARINc:DATA:FORMat. 659

BUS<b>:ARINc:POLarity. 654

BUS<b>:ARINc:SOURce. 654

BUS<b>:ARINc:THReshold:HIGH. 654

BUS<b>:ARINc:THReshold:LOW. 654

BUS<b>:ARINc:WCOunt?. 659

BUS<b>:ARINc:WORD<n>:DATA?. 659

BUS<b>:ARINc:WORD<n>:DATA[:VALue]?. 659

BUS<b>:ARINc:WORD<n>:FORMat?. 659

BUS<b>:ARINc:WORD<n>:LABel? 660

BUS<b>:ARINc:WORD<n>:LABel[:VALue]? 660

BUS<b>:ARINc:WORD<n>:PARity?. 660

BUS<b>:ARINc:WORD<n>:PATTern?. 660

BUS<b>:ARINc:WORD<n>:SDI?. 660

BUS<b>:ARINc:WORD<n>:SSM?. 661

BUS<b>:ARINc:WORD<n>:STARt?. 661

BUS<b>:ARINc:WORD<n>:STATus?. 661

BUS<b>:ARINc:WORD<n>:STOP?. 661

BUS<b>:CAN:BITRate. 586

BUS<b>:CAN:DATA:SOURce. 585

BUS<b>:CAN:FCOunt?. 591

BUS<b>:CAN:FRAMe<n>:ACKState?. 593

BUS<b>:CAN:FRAMe<n>:ACKValue? 594

BUS<b>:CAN:FRAMe<n>:BCOunt?. 596

BUS<b>:CAN:FRAMe<n>:BSEPosition? 596

BUS<b>:CAN:FRAMe<n>:BYTE<o>:STATe?. 597

BUS<b>:CAN:FRAMe<n>:BYTE<o>:VALue?. 597

BUS<b>:CAN:FRAMe<n>:CSSTate?. 594

BUS<b>:CAN:FRAMe<n>:CSValue? 594

BUS<b>:CAN:FRAMe<n>:DATA?. 593

BUS<b>:CAN:FRAMe<n>:DLCState? 594

BUS<b>:CAN:FRAMe<n>:DLCValue? 595

BUS<b>:CAN:FRAMe<n>:IDSTate?. 595

BUS<b>:CAN:FRAMe<n>:IDTYpe?. 595

BUS<b>:CAN:FRAMe<n>:IDValue? 596

BUS<b>:CAN:FRAMe<n>:STARt?. 592

BUS<b>:CAN:FRAMe<n>:STATus?. 592

BUS<b>:CAN:FRAMe<n>:STOP?. 593

BUS<b>:CAN:FRAMe<n>:TYPE?. 591

BUS<b>:CAN:SAMPlepoint 585

BUS<b>:CAN:TYPE. 585

BUS<b>:CPARallel:CLOCK:SLOPe. 724

BUS<b>:CPARallel:CLOCk:SOURce. 724

BUS<b>:CPARallel:CS:ENABle. 724

BUS<b>:CPARallel:CS:POLarity. 725

BUS<b>:CPARallel:CS:SOURce. 725

BUS<b>:CPARallel:DATA<m>:SOURce. 723

BUS<b>:CPARallel:FCOunt?. 725

BUS<b>:CPARallel:FRAMe<n>:DATA?. 726

BUS<b>:CPARallel:FRAMe<n>:STARt?. 726

BUS<b>:CPARallel:FRAMe<n>:STATe?. 726

BUS<b>:CPARallel:FRAMe<n>:STOP?. 727

BUS<b>:CPARallel:WIDTh. 723

BUS<b>:DSIGnals. 548

BUS<b>:DSIZe. 549

BUS<b>:FORMat. 548

BUS<b>:HISTory:CURRent 439

BUS<b>:HISTory:PALL. 439

BUS<b>:HISTory:PLAYer:SPEed. 441

BUS<b>:HISTory:PLAYer:STATe. 442

BUS<b>:HISTory:REPLay. 441

BUS<b>:HISTory:STARt. 440

BUS<b>:HISTory:STOP 440

BUS<b>:HISTory:TSABsolute:ALL?. 444

BUS<b>:HISTory:TSABsolute?. 444

BUS<b>:HISTory:TSDate:ALL?. 445

BUS<b>:HISTory:TSDate?. 444

BUS<b>:HISTory:TSRelative:ALL? 443

BUS<b>:HISTory:TSRelative?. 443

BUS<b>:I2C:CLOCk:SOURce. 565

BUS<b>:I2C:DATA:SOURce. 565

BUS<b>:I2C:FCOunt?. 569

BUS<b>:I2C:FRAMe<n>:AACCess? 571

BUS<b>:I2C:FRAMe<n>:ACCess? 571

BUS<b>:I2C:FRAMe<n>:ACOMplete? 572

BUS<b>:I2C:FRAMe<n>:ADBStart?. 572

BUS<b>:I2C:FRAMe<n>:ADDRess? 572

BUS<b>:I2C:FRAMe<n>:ADEVice? 573

BUS<b>:I2C:FRAMe<n>:AMODe?. 573

BUS<b>:I2C:FRAMe<n>:ASTart?. 573

BUS<b>:I2C:FRAMe<n>:BCOunt?. 574

BUS<b>:I2C:FRAMe<n>:BYTE<o>:ACCess?. 574

BUS<b>:I2C:FRAMe<n>:BYTE<o>:ACKStart?. 574

BUS<b>:I2C:FRAMe<n>:BYTE<o>:COMPlete?. 575

BUS<b>:I2C:FRAMe<n>:BYTE<o>:STARt?. 575

BUS<b>:I2C:FRAMe<n>:BYTE<o>:VALue?. 575

BUS<b>:I2C:FRAMe<n>:DATA?. 569

BUS<b>:I2C:FRAMe<n>:STARt?. 570

BUS<b>:I2C:FRAMe<n>:STATus?. 570

BUS<b>:I2C:FRAMe<n>:STOP?. 571

BUS<b>:I2S:AVARiant. 616

BUS<b>:I2S:BORDer. 619

BUS<b>:I2S:CHANnel:LENGth 620

BUS<b>:I2S:CHANnel:OFFSet. 620

BUS<b>:I2S:CHANnel:ORDer 619

BUS<b>:I2S:CHANnel:TDMCount 620

BUS<b>:I2S:CLOCk:POLarity. 616

BUS<b>:I2S:CLOCk:SOURce. 616

BUS<b>:I2S:CLOCk:THReshold 618

BUS<b>:I2S:DATA:POLarity. 618

BUS<b>:I2S:DATA:SOURce. 617

BUS<b>:I2S:DATA:THReshold. 618

BUS<b>:I2S:DISPlay. 625

BUS<b>:I2S:FCOunt?. 628

BUS<b>:I2S:FOFFset 620

BUS<b>:I2S:FRAMe<n>:LEFT:STATe?. 630

BUS<b>:I2S:FRAMe<n>:LEFT:VALue? 630

BUS<b>:I2S:FRAMe<n>:RIGHt:STATe?. 630

BUS<b>:I2S:FRAMe<n>:RIGHt:VALue? 630

BUS<b>:I2S:FRAMe<n>:STARt?. 629

BUS<b>:I2S:FRAMe<n>:STATe?. 628

BUS<b>:I2S:FRAMe<n>:STOP?. 629

BUS<b>:I2S:FRAMe<n>:TDM<o>:STATe?. 630

BUS<b>:I2S:FRAMe<n>:TDM<o>:VALue?. 631

BUS<b>:I2S:TRACk:LEFT:POSition 625

BUS<b>:I2S:TRACk:LEFT:SCALe 626

BUS<b>:I2S:TRACk:RIGHt:POSition 626

BUS<b>:I2S:TRACk:RIGHt:SCALe 626

BUS<b>:I2S:TRACk:SET:DEFault 628

BUS<b>:I2S:TRACk:SET:SCReen 628

BUS<b>:I2S:TRACk:TDM<o>:POSition. 627

BUS<b>:I2S:TRACk:TDM<o>:SCALe. 627

BUS<b>:I2S:TRACk:TDM<o>:STATe 627

BUS<b>:I2S:WLENgth. 619

BUS<b>:I2S:WSELect:POLarity 617

BUS<b>:I2S:WSELect:SOURce 617

BUS<b>:I2S:WSELect:THReshold 618

BUS<b>:LABel. 549

BUS<b>:LABel:STATe. 549

BUS<b>:LIN:BITRate. 603

BUS<b>:LIN:DATA:SOURce. 602

BUS<b>:LIN:FCOunt?. 607

BUS<b>:LIN:FRAMe<n>:BCOunt?. 611

BUS<b>:LIN:FRAMe<n>:BYTE<o>:STATe?. 611

BUS<b>:LIN:FRAMe<n>:BYTE<o>:VALue?. 612

BUS<b>:LIN:FRAMe<n>:CSSTate?. 608

BUS<b>:LIN:FRAMe<n>:CSValue? 609

BUS<b>:LIN:FRAMe<n>:DATA?. 607

BUS<b>:LIN:FRAMe<n>:IDPValue? 609

BUS<b>:LIN:FRAMe<n>:IDSTate?. 609

BUS<b>:LIN:FRAMe<n>:IDValue? 610

BUS<b>:LIN:FRAMe<n>:STARt?. 608

BUS<b>:LIN:FRAMe<n>:STATus?. 607

BUS<b>:LIN:FRAMe<n>:STOP?. 608

BUS<b>:LIN:FRAMe<n>:SYSTate?. 610

BUS<b>:LIN:FRAMe<n>:SYValue? 610

BUS<b>:LIN:FRAMe<n>:VERSion? 610

BUS<b>:LIN:POLarity. 602

BUS<b>:LIN:STANdard. 602

BUS<b>:LIST:SAVE 551

BUS<b>:LIST?. 550

BUS<b>:MILStd:POLarity. 631

BUS<b>:MILStd:RESPonsetime:MAXimum 632

BUS<b>:MILStd:SOURce. 632

BUS<b>:MILStd:THReshold:HIGH. 632

BUS<b>:MILStd:THReshold:LOW. 632

BUS<b>:MILStd:WCOunt?. 640

BUS<b>:MILStd:WORD<n>:COMMand:MCODe:CODE?. 641

BUS<b>:MILStd:WORD<n>:COMMand:MCODe:VALue? 641

BUS<b>:MILStd:WORD<n>:COMMand:RTADdress? 641

BUS<b>:MILStd:WORD<n>:COMMand:SADDress? 641

BUS<b>:MILStd:WORD<n>:COMMand:WCOunt?. 642

BUS<b>:MILStd:WORD<n>:DATA?. 642

BUS<b>:MILStd:WORD<n>:IMGTime?. 642

BUS<b>:MILStd:WORD<n>:PARity?. 642

BUS<b>:MILStd:WORD<n>:RTIMe?. 643

BUS<b>:MILStd:WORD<n>:STARt?. 643

BUS<b>:MILStd:WORD<n>:STATus:BCReceived? 643

BUS<b>:MILStd:WORD<n>:STATus:BUSY? 644

BUS<b>:MILStd:WORD<n>:STATus:DBCaccept? 644

BUS<b>:MILStd:WORD<n>:STATus:INSTrument? 644

BUS<b>:MILStd:WORD<n>:STATus:MERRor? 644

BUS<b>:MILStd:WORD<n>:STATus:RTADdress? 645

BUS<b>:MILStd:WORD<n>:STATus:SREQuest? 645

BUS<b>:MILStd:WORD<n>:STATus:SUBSystem? 645

BUS<b>:MILStd:WORD<n>:STATus:TERMinal? 645

BUS<b>:MILStd:WORD<n>:STATus?. 643

BUS<b>:MILStd:WORD<n>:STOP? 646

BUS<b>:MILStd:WORD<n>:TRMode?. 646

BUS<b>:MILStd:WORD<n>:TYPE?. 646

BUS<b>:PARallel:DATA<m>:SOURce 723

BUS<b>:PARallel:FCOunt?. 725

BUS<b>:PARallel:FRAMe<n>:DATA?. 726

BUS<b>:PARallel:FRAMe<n>:STARt?. 726

BUS<b>:PARallel:FRAMe<n>:STATe?. 726

BUS<b>:PARallel:FRAMe<n>:STOP?. 727

BUS<b>:PARallel:WIDTh 723

BUS<b>:POSition. 550

BUS<b>:RESult. 550

BUS<b>:SPI:BORDer. 554

BUS<b>:SPI:CLOCk:POLarity. 552

BUS<b>:SPI:CLOCk:SOURce. 552

BUS<b>:SPI:CS:POLarity. 552

BUS<b>:SPI:CS:SOURce. 551

BUS<b>:SPI:DATA:POLarity. 553

BUS<b>:SPI:DATA:SOURce 553

BUS<b>:SPI:FCOunt?. 557

BUS<b>:SPI:FRAME<n>:DATA:MISO?. 559

BUS<b>:SPI:FRAME<n>:DATA:MOSI?. 558

BUS<b>:SPI:FRAME<n>:STARt?. 558

BUS<b>:SPI:FRAME<n>:STATus?. 557

BUS<b>:SPI:FRAME<n>:STOP?. 558

BUS<b>:SPI:FRAME<n>:WCOunt? 559

BUS<b>:SPI:FRAME<n>:WORD<o>:MISO?. 561

BUS<b>:SPI:FRAME<n>:WORD<o>:MOSI?. 560

BUS<b>:SPI:FRAME<n>:WORD<o>:STARt?. 560

BUS<b>:SPI:FRAME<n>:WORD<o>:STOP?. 560

BUS<b>:SPI:MISO:POLarity. 554

BUS<b>:SPI:MISO:SOURce. 553

BUS<b>:SPI:MOSI:POLarity. 553

BUS<b>:SPI:MOSI:SOURce. 553

BUS<b>:SPI:SSIZe 554

BUS<b>:SSPI:BITime. 563

BUS<b>:SSPI:BORDer. 564

BUS<b>:SSPI:CLOCk:POLarity. 562

BUS<b>:SSPI:CLOCk:SOURce. 562

BUS<b>:SSPI:DATA:POLarity. 563

BUS<b>:SSPI:DATA:SOURce 562

BUS<b>:SSPI:MISO:POLarity. 563

BUS<b>:SSPI:MISO:SOURce. 562

BUS<b>:SSPI:MOSI:POLarity. 563

BUS<b>:SSPI:MOSI:SOURce. 562

BUS<b>:SSPI:SSIZe 564

BUS<b>:STATe. 548

BUS<b>:TYPE. 548

BUS<b>:UART:BAUDrate. 579

BUS<b>:UART:BITime. 579

BUS<b>:UART:DATA:POLarity. 577

BUS<b>:UART:DATA:SOURce. 576

BUS<b>:UART:PARity. 578

BUS<b>:UART:POLarity. 577

BUS<b>:UART:RX:FCOunt?. 582

BUS<b>:UART:RX:FRAMe<n>:WCOunt?. 582

BUS<b>:UART:RX:FRAMe<n>:WORD<o>:STARt?. 583

BUS<b>:UART:RX:FRAMe<n>:WORD<o>:STATe?. 583

BUS<b>:UART:RX:FRAMe<n>:WORD<o>:STOP?. 584

BUS<b>:UART:RX:FRAMe<n>:WORD<o>:VALue? 584

BUS<b>:UART:RX:SOURce. 576

BUS<b>:UART:SBIT. 578

BUS<b>:UART:SSIZe. 578

BUS<b>:UART:TX:FCOunt?. 582

BUS<b>:UART:TX:FRAMe<n>:WCOunt?. 582

BUS<b>:UART:TX:FRAMe<n>:WORD<o>:STARt?. 583

BUS<b>:UART:TX:FRAMe<n>:WORD<o>:STATe?. 583

BUS<b>:UART:TX:FRAMe<n>:WORD<o>:STOP? 584

BUS<b>:UART:TX:FRAMe<n>:WORD<o>:VALue?. 584

BUS<b>:UART:TX:SOURce. 577

CALCulate:MATH<m>:ARIThmetics. 501

CALCulate:MATH<m>:DATA:ENVelope:HEADer? 507

CALCulate:MATH<m>:DATA:ENVelope:HEADer? 738

CALCulate:MATH<m>:DATA:ENVelope:POINts?. 508

CALCulate:MATH<m>:DATA:ENVelope:POINts?. 738

CALCulate:MATH<m>:DATA:ENVelope:XINCrement? 742

CALCulate:MATH<m>:DATA:ENVelope:XORigin? 742

CALCulate:MATH<m>:DATA:ENVelope:YINCrement? 743

CALCulate:MATH<m>:DATA:ENVelope:YORigin? 743

CALCulate:MATH<m>:DATA:ENVelope:YRESolution? 743

CALCulate:MATH<m>:DATA:ENVelope? 507

CALCulate:MATH<m>:DATA:ENVelope? 737

CALCulate:MATH<m>:DATA:HEADer? 499

CALCulate:MATH<m>:DATA:HEADer? 506

CALCulate:MATH<m>:DATA:HEADer? 737

CALCulate:MATH<m>:DATA:POINts?. 500

CALCulate:MATH<m>:DATA:POINts?. 507

CALCulate:MATH<m>:DATA:POINts?. 737

CALCulate:MATH<m>:DATA:XINCrement? 742

CALCulate:MATH<m>:DATA:XORigin? 742

CALCulate:MATH<m>:DATA:YINCrement? 743

CALCulate:MATH<m>:DATA:YORigin? 743

CALCulate:MATH<m>:DATA:YRESolution? 743

CALCulate:MATH<m>:DATA?. 499

CALCulate:MATH<m>:DATA?. 506

CALCulate:MATH<m>:DATA?. 736

CALCulate:MATH<m>:FFT:AVERage:COMPlete? 502

CALCulate:MATH<m>:FFT:AVERage:COUNt. 502

CALCulate:MATH<m>:FFT:BANDwidth[:RESolution]:ADJusted?. 503

CALCulate:MATH<m>:FFT:BANDwidth[:RESolution]:AUTO. 503

CALCulate:MATH<m>:FFT:BANDwidth[:RESolution]:RATio. 503

CALCulate:MATH<m>:FFT:BANDwidth[:RESolution][:VALue]. 504

CALCulate:MATH<m>:FFT:CFRequency 504

CALCulate:MATH<m>:FFT:FULLspan. 504

CALCulate:MATH<m>:FFT:MAGNitude:SCALe. 503

CALCulate:MATH<m>:FFT:SPAN. 504

CALCulate:MATH<m>:FFT:SRATe?. 505

CALCulate:MATH<m>:FFT:STARt. 504

CALCulate:MATH<m>:FFT:STOP 505

CALCulate:MATH<m>:FFT:TIME:POSition. 505

CALCulate:MATH<m>:FFT:TIME:RANGe 505

CALCulate:MATH<m>:FFT:WINDow:TYPE. 501

CALCulate:MATH<m>:HISTory:CURRent 439

CALCulate:MATH<m>:HISTory:PALL. 439

CALCulate:MATH<m>:HISTory:PLAYer:SPEed 441

CALCulate:MATH<m>:HISTory:PLAYer:STATe. 442

CALCulate:MATH<m>:HISTory:REPLay 441

CALCulate:MATH<m>:HISTory:STARt. 440

CALCulate:MATH<m>:HISTory:STOP. 440

CALCulate:MATH<m>:HISTory:TSABsolute:ALL? 444

CALCulate:MATH<m>:HISTory:TSABsolute? 444

CALCulate:MATH<m>:HISTory:TSDate:ALL? 445

CALCulate:MATH<m>:HISTory:TSDate?. 444

CALCulate:MATH<m>:HISTory:TSRelative:ALL?. 443

CALCulate:MATH<m>:HISTory:TSRelative? 443

CALCulate:MATH<m>:POSition 498

CALCulate:MATH<m>:SCALe 497

CALCulate:MATH<m>:STATe. 497

CALCulate:MATH<m>[:EXPRession][:DEFine] 498

CALibration 755

CALibration:STATe?. 756

CHANnel<m>:AOFF 422

CHANnel<m>:AON. 422

CHANnel<m>:ARIThmetics. 419

CHANnel<m>:BANDwidth. 424

CHANnel<m>:COUPling. 422

CHANnel<m>:DATA:ENVelope:HEADer? 429

CHANnel<m>:DATA:ENVelope:HEADer? 736

CHANnel<m>:DATA:ENVelope:XINCrement? 742

CHANnel<m>:DATA:ENVelope:XORigin? 742

CHANnel<m>:DATA:ENVelope:YINCrement? 743

CHANnel<m>:DATA:ENVelope:YORigin? 743

CHANnel<m>:DATA:ENVelope:YRESolution? 743

CHANnel<m>:DATA:ENVelope? 429

CHANnel<m>:DATA:ENVelope? 735

CHANnel<m>:DATA:HEADer? 428

CHANnel<m>:DATA:HEADer? 734

CHANnel<m>:DATA:POINts. 430

CHANnel<m>:DATA:POINts. 734

CHANnel<m>:DATA:XINCrement? 742

CHANnel<m>:DATA:XORigin? 742

CHANnel<m>:DATA:YINCrement? 743

CHANnel<m>:DATA:YORigin? 743

CHANnel<m>:DATA:YRESolution? 743

CHANnel<m>:DATA?. 428

CHANnel<m>:DATA?. 733

CHANnel<m>:HISTory:CURRent 439

CHANnel<m>:HISTory:PALL 440

CHANnel<m>:HISTory:PLAYer:SPEed 441

CHANnel<m>:HISTory:PLAYer:STATe. 442

CHANnel<m>:HISTory:REPLay 441

CHANnel<m>:HISTory:STARt. 440

CHANnel<m>:HISTory:STOP. 440

CHANnel<m>:HISTory:TSABsolute:ALL? 444

CHANnel<m>:HISTory:TSABsolute? 444

CHANnel<m>:HISTory:TSDate:ALL? 445

CHANnel<m>:HISTory:TSDate? 445

CHANnel<m>:HISTory:TSRelative:ALL?. 443

CHANnel<m>:HISTory:TSRelative? 443

CHANnel<m>:LABel. 426

CHANnel<m>:LABel:STATe. 427

CHANnel<m>:OFFSet 424

CHANnel<m>:OVERload. 425

CHANnel<m>:POLarity. 425

CHANnel<m>:POSition. 424

CHANnel<m>:RANGe. 423

CHANnel<m>:SCALe. 423

CHANnel<m>:SKEW 426

CHANnel<m>:STATe 421

CHANnel<m>:THReshold. 426

CHANnel<m>:THReshold:FINDlevel 555

CHANnel<m>:THReshold:FINDlevel 564

CHANnel<m>:THReshold:FINDlevel 566

CHANnel<m>:THReshold:FINDlevel 579

CHANnel<m>:THReshold:FINDlevel 586

CHANnel<m>:THReshold:FINDlevel 603

CHANnel<m>:THReshold:FINDlevel 618

CHANnel<m>:THReshold:HYSTeresis 426

CHANnel<m>:TYPE 419

CHANnel<m>:ZOFFset[:VALue]. 427

CURSor<m>:AOFF. 476

CURSor<m>:FUNCtion 477

CURSor<m>:RESult? 481

CURSor<m>:SNPeak 480

CURSor<m>:SOURce 476

CURSor<m>:SPPeak 480

CURSor<m>:SSCReen 480

CURSor<m>:STATe. 476

CURSor<m>:SWAVe. 480

CURSor<m>:TRACking:SCALe[:STATe] 481

CURSor<m>:TRACking[:STATe] 479

CURSor<m>:X1Position 479

CURSor<m>:X2Position 479

CURSor<m>:X3Position 479

CURSor<m>:XCOupling 480

CURSor<m>:XDELta:INVerse? 481

CURSor<m>:XDELta[:VALue]? 481

CURsor<m>:XRATio:UNIT. 482

CURSor<m>:XRATio[:VALue]? 483

CURSor<m>:Y1Position 479

CURSor<m>:Y2Position 479

CURSor<m>:Y3Position 479

CURSor<m>:YCOupling 480

CURSor<m>:YDELta:SLOPe? 482

CURSor<m>:YDELta[:VALue]? 482

CURSor<m>:YRATio:UNIT. 483

CURSor<m>:YRATio[:VALue]? 483

DIGital<m>:CURRent:STATe:MAXimum?. 717

DIGital<m>:CURRent:STATe:MINimum? 717

DIGital<m>:DATA:HEADer?. 721

DIGital<m>:DATA:HEADer?. 739

DIGital<m>:DATA:POINts 722

DIGital<m>:DATA:POINts 739

DIGital<m>:DATA:XINCrement?. 742

DIGital<m>:DATA:XORigin?. 742

DIGital<m>:DATA:YINCrement?. 743

DIGital<m>:DATA:YORigin?. 743

DIGital<m>:DATA:YRESolution? 743

DIGital<m>:DATA?. 721

DIGital<m>:DATA?. 738

DIGital<m>:DESKew. 719

DIGital<m>:DISPlay. 718

DIGital<m>:HISTory:CURRent. 439

DIGital<m>:HISTory:PALL. 439

DIGital<m>:HISTory:PLAYer:SPEed. 441

DIGital<m>:HISTory:PLAYer:STATe 442

DIGital<m>:HISTory:REPLay. 441

DIGital<m>:HISTory:STARt 440

DIGital<m>:HISTory:STOP 440

DIGital<m>:HISTory:TSABsolute:ALL?. 444

DIGital<m>:HISTory:TSABsolute?. 444

DIGital<m>:HISTory:TSDate:ALL?. 445

DIGital<m>:HISTory:TSDate?. 444

DIGital<m>:HISTory:TSRelative:ALL?. 443

DIGital<m>:HISTory:TSRelative?. 443

DIGital<m>:Hysteresis. 719

DIGital<m>:LABel. 720

DIGital<m>:LABel:STATe. 720

DIGital<m>:POSition. 720

DIGital<m>:SIZE 719

DIGital<m>:TECHnology 718

DIGital<m>:THCoupling 719

DIGital<m>:THReshold 718

DISPlay:DIALog:CLOSe. 462

DISPlay:DIALog:MESSage 462

DISPlay:DIALog:TRANsparency 463

DISPlay:GRID:STYLe. 467

DISPlay:INTensity:BACKlight. 465

DISPlay:INTensity:GRID. 466

DISPlay:INTensity:WAVeform. 465

DISPlay:LANGuage 755

DISPlay:MODE. 462

DISPlay:PALette. 463

DISPlay:PERSistence:CLEar 467

DISPlay:PERSistence:INFinite 467

DISPlay:PERSistence:STATe. 466

DISPlay:PERSistence:TIME. 466

DISPlay:PERSistence:TIME:AUTO. 467

DISPlay:STYLe. 467

DISPlay:VSCReen:ENABle. 468

DISPlay:VSCReen:POSition. 468

DISPlay:XY:XSOurce. 463

DISPlay:XY:Y1Source. 464

DISPlay:XY:Y2Source. 464

DISPlay:XY:ZMODe. 464

DISPlay:XY:ZSOurce. 465

DISPlay:XY:ZTHReshold 465

DVM<m>:ENABle. 728

DVM<m>:POSition. 729

DVM<m>:RESult[:ACTual]:STATus?. 729

DVM<m>:RESult[:ACTual]?. 729

DVM<m>:SOURce. 728

DVM<m>:TYPE. 728

EXPort:ATABle:NAME. 445

EXPort:ATABle:SAVE. 446

EXPort:MEASurement<m>:STATistics:ALL:NAME. 494

EXPort:MEASurement<m>:STATistics:ALL:NAME. 669

EXPort:MEASurement<m>:STATistics:ALL:SAVE. 494

EXPort:MEASurement<m>:STATistics:ALL:SAVE. 669

EXPort:MEASurement<m>:STATistics:NAME 493

EXPort:MEASurement<m>:STATistics:NAME 669

EXPort:MEASurement<m>:STATistics:SAVE. 493

EXPort:MEASurement<m>:STATistics:SAVE. 669

EXPort:POWer:NAME. 682

EXPort:POWer:NAME. 692

EXPort:POWer:SAVE. 682

EXPort:POWer:SAVE. 692

EXPort:SEARch:NAME. 547

EXPort:SEARch:SAVE. 547

EXPort:WAVeform:NAME 744

EXPort:WAVeform:SAVE. 745

EXPort:WAVeform:SOURce 744

FORMat:BORDer 733

FORMat[:DATA]. 731

HCOPy:COLor:SCHeme 753

HCOPy:DATA?. 753

HCOPy:DESTination 752

HCOPy:LANGuage 753

HCOpy:MENU[:ENABle]. 753

HCOPy:PAGE:ORIentation 753

HCOPy:PAGE:SIZE. 753

HCOPy[:IMMediate]. 752

MASK:ACTion:PRINt:EVENt:COUNt. 528

MASK:ACTion:PRINt:EVENt:MODE. 527

MASK:ACTion:PULSe:EVENt:COUNt. 528

MASK:ACTion:PULSe:EVENt:MODE. 527

MASK:ACTion:PULSe:PLENgth 529

MASK:ACTion:PULSe:POLarity. 529

MASK:ACTion:SCRSave:DESTination 528

MASK:ACTion:SCRSave:EVENt:COUNt. 528

MASK:ACTion:SCRSave:EVENt:MODE. 527

MASK:ACTion:SOUNd:EVENt:COUNt. 528

MASK:ACTion:SOUNd:EVENt:MODE. 527

MASK:ACTion:STOP:EVENt:COUNt. 528

MASK:ACTion:STOP:EVENt:MODE. 527

MASK:ACTion:WFMSave:DESTination. 528

MASK:ACTion:WFMSave:EVENt:COUNt. 528

MASK:ACTion:WFMSave:EVENt:MODE. 527

MASK:CHCopy. 525

MASK:COUNt?. 526

MASK:DATA:HEADer? 530

MASK:DATA:HEADer? 740

MASK:DATA:XINCrement? 742

MASK:DATA:XORigin? 742

MASK:DATA:YINCrement? 743

MASK:DATA:YORigin? 743

MASK:DATA:YRESolution? 743

MASK:DATA?. 529

MASK:DATA?. 740

MASK:LOAD. 524

MASK:RESet:COUNter. 526

MASK:SAVE. 525

MASK:SAVE. 530

MASK:SOURce. 525

MASK:STATe 524

MASK:TEST 524

MASK:VCOunt?. 526

MASK:XWIDth 526

MASK:YPOSition. 525

MASK:YSCale. 525

MASK:YWIDth 526

MEASurement<m>:ALL[:STATe]. 484

MEASurement<m>:AOFF. 484

MEASurement<m>:AON. 484

MEASurement<m>:ARESult?. 484

MEASurement<m>:CATegory? 489

MEASurement<m>:DELay:SLOPe. 489

MEASurement<m>:MAIN. 485

MEASurement<m>:RESult:AVG?. 491

MEASurement<m>:RESult:NPEak? 492

MEASurement<m>:RESult:PPEak?. 492

MEASurement<m>:RESult:STDDev? 491

MEASurement<m>:RESult:WFMCount?. 492

MEASurement<m>:RESult[:ACTual]?. 489

MEASurement<m>:SOURce. 487

MEASurement<m>:STATistics:RESet. 491

MEASurement<m>:STATistics:VALue:ALL?. 492

MEASurement<m>:STATistics:VALue<n>?. 493

MEASurement<m>:STATistics:WEIGht 490

MEASurement<m>:STATistics[:ENABle]. 490

MEASurement<m>[:ENABle]. 485

MMEMory:CATalog:LENGth? 749

MMEMory:CATalog? 748

MMEMory:CDIRectory. 746

MMEMory:COPY. 749

MMEMory:DATA. 750

MMEMory:DCATalog:LENGth? 748

MMEMory:DCATalog? 747

MMEMory:DELete. 750

MMEMory:DRIVes?. 745

MMEMory:LOAD:STATe. 751

MMEMory:MDIRectory. 746

MMEMory:MOVE. 749

MMEMory:MSIS. 746

MMEMory:NAME. 752

MMEMory:RDIRectory. 747

MMEMory:STORe:STATe 751

POWer:ATYPe. 665

POWer:CONSumption:EXECute. 675

POWer:CONSumption:REPort:ADD. 676

POWer:CONSumption:RESTart. 676

POWer:CONSumption:RESult:DURation? 676

POWer:CONSumption:RESult:ENERgy? 676

POWer:CONSumption:RESult:REALpower? 676

POWer:DESKew[:EXECute]. 667

POWer:DONResistance:EXECute. 701

POWer:DONResistance:GATE<n>:START. 701

POWer:DONResistance:GATE<n>STOP. 701

POWer:DONResistance:REPort:ADD. 701

POWer:DONResistance:RESult:DONResistance? 701

POWer:EFFiciency:EXECute. 702

POWer:EFFiciency:REPort:ADD. 702

POWer:EFFiciency:RESult:EFFiciency:AVG?. 702

POWer:EFFiciency:RESult:EFFiciency:NPEak?. 702

POWer:EFFiciency:RESult:EFFiciency:PPEak?. 702

POWer:EFFiciency:RESult:EFFiciency:STDDev?. 702

POWer:EFFiciency:RESult:EFFiciency:WFMCount?. 702

POWer:EFFiciency:RESult:EFFiciency[:ACTual]?. 702

POWer:EFFiciency:RESult:INPut:REALpower:AVG?. 702

POWer:EFFiciency:RESult:INPut:REALpower:NPEak? 702

POWer:EFFiciency:RESult:INPut:REALpower:PPEak? 703

POWer:EFFiciency:RESult:INPut:REALpower:STDDev? 703

POWer:EFFiciency:RESult:INPut:REALpower:WFMCount? 703

POWer:EFFiciency:RESult:INPut:REALpower[:ACTual]? 702

POWer:EFFiciency:RESult:OUTPut:REALpower:AVG?. 703

POWer:EFFiciency:RESult:OUTPut:REALpower:NPEak? 703

POWer:EFFiciency:RESult:OUTPut:REALpower:PPEak?. 703

POWer:EFFiciency:RESult:OUTPut:REALpower:STDDev? 703

POWer:EFFiciency:RESult:OUTPut:REALpower:WFMCount?. 703

POWer:EFFiciency:RESult:OUTPut:REALpower[:ACTual]?. 703

POWer:ENABle 666

POWer:HARMonics:AVAilable? 678

POWer:HARMonics:DOFRequency 677

POWer:HARMonics:ENFRequency 677

POWer:HARMonics:EXECute. 677

POWer:HARMonics:MEASurement:DURation? 678

POWer:HARMonics:MEASurement:FREQuency:AVG?. 678

POWer:HARMonics:MEASurement:FREQuency:NPEak? 679

POWer:HARMonics:MEASurement:FREQuency:PPeak? 679

POWer:HARMonics:MEASurement:FREQuency:STDDev? 679

POWer:HARMonics:MEASurement:FREQuency[:ACTual]? 679

POWer:HARMonics:MEASurement:REALpower[:ACTual]?. 679

POWer:HARMonics:MEASurement:THDistortion:AVG?. 679

POWer:HARMonics:MEASurement:THDistortion:NPEak?. 680

POWer:HARMonics:MEASurement:THDistortion:PPeak?. 680

POWer:HARMonics:MEASurement:THDistortion:STDDev?. 680

POWer:HARMonics:MEASurement:THDistortion[:ACTual]?. 680

POWer:HARMonics:MIFRequency 677

POWer:HARMonics:REPort:ADD. 677

POWer:HARMonics:RESult<n>:FREQency? 680

POWer:HARMonics:RESult<n>:LEVel:LIMit?. 680

POWer:HARMonics:RESult<n>:LEVel[:VALue]? 681

POWer:HARMonics:RESult<n>:MAXimum? 681

POWer:HARMonics:RESult<n>:MEAN? 681

POWer:HARMonics:RESult<n>:MINimum? 681

POWer:HARMonics:RESult<n>:RESet. 677

POWer:HARMonics:RESult<n>:VALid? 682

POWer:HARMonics:RESult<n>:VCOunt? 682

POWer:HARMonics:RESult<n>:WFMCount? 682

POWer:HARMonics:STANdard 677

POWer:INRushcurrent:EXECute. 684

POWer:INRushcurrent:GATE<n>:STARt 684

POWer:INRushcurrent:GATE<n>:STOP 684

POWer:INRushcurrent:GCOunt. 684

POWer:INRushcurrent:REPort:ADD. 684

POWer:INRushcurrent:RESult<n>:AREA? 684

POWer:INRushcurrent:RESult<n>:MAXCurrent? 685

POWer:MODulation:EXECute. 698

POWer:MODulation:REPort:ADD. 698

POWer:MODulation:RESult:LPEak:AVG?. 698

POWer:MODulation:RESult:LPEak:NPEak? 698

POWer:MODulation:RESult:LPEak:PPEak? 698

POWer:MODulation:RESult:LPEak:STDDev? 698

POWer:MODulation:RESult:LPEak:WFMCount? 698

POWer:MODulation:RESult:LPEak[:ACTual]? 698

POWer:MODulation:RESult:MEAN:AVG?. 699

POWer:MODulation:RESult:MEAN:NPEak? 699

POWer:MODulation:RESult:MEAN:PPEak?. 699

POWer:MODulation:RESult:MEAN:STDDev? 699

POWer:MODulation:RESult:MEAN:WFMCount?. 699

POWer:MODulation:RESult:MEAN[:ACTual]?. 699

POWer:MODulation:RESult:RMS:AVG?. 699

POWer:MODulation:RESult:RMS:NPEak? 699

POWer:MODulation:RESult:RMS:PPEak?. 699

POWer:MODulation:RESult:RMS:STDDev? 699

POWer:MODulation:RESult:RMS:WFMCount?. 699

POWer:MODulation:RESult:RMS[:ACTual]?. 699

POWer:MODulation:RESult:STDDev:AVG?. 700

POWer:MODulation:RESult:STDDev:NPEak? 700

POWer:MODulation:RESult:STDDev:PPEak? 700

POWer:MODulation:RESult:STDDev:STDDev? 700

POWer:MODulation:RESult:STDDev:WFMCount? 700

POWer:MODulation:RESult:STDDev[:ACTual]? 700

POWer:MODulation:RESult:UPEak:AVG?. 700

POWer:MODulation:RESult:UPEak:NPEak? 700

POWer:MODulation:RESult:UPEak:PPEak? 700

POWer:MODulation:RESult:UPEak:STDDev? 700

POWer:MODulation:RESult:UPEak[:ACTual]? 700

POWer:MODulation:RESult:UPEakWFMCount? 700

POWer:MODulation:TYPE. 698

POWer:ONOFf:EXECute. 707

POWer:ONOFf:MEASurement. 707

POWer:ONOFf:REPort:ADD. 708

POWer:ONOFf:RESult<n>:TIME?. 708

POWer:QUALity:EXECute 672

POWer:QUALity:REPort:ADD 672

POWer:QUALity:RESult:CURRent:CREStfactor:AVG?. 672

POWer:QUALity:RESult:CURRent:CREStfactor:NPEak? 673

POWer:QUALity:RESult:CURRent:CREStfactor:PPEak?. 673

POWer:QUALity:RESult:CURRent:CREStfactor:STDDev? 673

POWer:QUALity:RESult:CURRent:CREStfactor:WFMCount?. 674

POWer:QUALity:RESult:CURRent:CREStfactor[:ACTual]?. 672

POWer:QUALity:RESult:CURRent:FREQuency:AVG?. 672

POWer:QUALity:RESult:CURRent:FREQuency:NPEak? 673

POWer:QUALity:RESult:CURRent:FREQuency:PPEak? 673

POWer:QUALity:RESult:CURRent:FREQuency:STDDev? 673

POWer:QUALity:RESult:CURRent:FREQuency:WFMCount? 674

POWer:QUALity:RESult:CURRent:FREQuency[:ACTual]? 672

POWer:QUALity:RESult:CURRent:RMS:AVG?. 672

POWer:QUALity:RESult:CURRent:RMS:NPEak? 673

POWer:QUALity:RESult:CURRent:RMS:PPEak?. 673

POWer:QUALity:RESult:CURRent:RMS:STDDev? 673

POWer:QUALity:RESult:CURRent:RMS:WFMCount? 673

POWer:QUALity:RESult:CURRent:RMS[:ACTual]?. 672

POWer:QUALity:RESult:POWer:APParent:AVG?. 674

POWer:QUALity:RESult:POWer:APParent:NPEak? 674

POWer:QUALity:RESult:POWer:APParent:PPEak? 674

POWer:QUALity:RESult:POWer:APParent:STDDev? 675

POWer:QUALity:RESult:POWer:APParent:WFMCount? 675

POWer:QUALity:RESult:POWer:APParent[:ACTual]? 674

POWer:QUALity:RESult:POWer:PFACtor:AVG?. 674

POWer:QUALity:RESult:POWer:PFACtor:NPEak? 674

POWer:QUALity:RESult:POWer:PFACtor:PPEak?. 675

POWer:QUALity:RESult:POWer:PFACtor:STDDev? 675

POWer:QUALity:RESult:POWer:PFACtor:WFMCount?. 675

POWer:QUALity:RESult:POWer:PFACtor[:ACTual]?. 674

POWer:QUALity:RESult:POWer:PHASe:AVG?. 674

POWer:QUALity:RESult:POWer:PHASe:NPEak? 674

POWer:QUALity:RESult:POWer:PHASe:PPEak? 675

POWer:QUALity:RESult:POWer:PHASe:STDDev? 675

POWer:QUALity:RESult:POWer:PHASe:WFMCount? 675

POWer:QUALity:RESult:POWer:PHASe[:ACTual]? 674

POWer:QUALity:RESult:POWer:REACtive:AVG?. 674

POWer:QUALity:RESult:POWer:REACtive:NPEak?. 674

POWer:QUALity:RESult:POWer:REACtive:PPEak?. 674

POWer:QUALity:RESult:POWer:REACtive:STDDev?. 675

POWer:QUALity:RESult:POWer:REACtive:WFMCount?. 675

POWer:QUALity:RESult:POWer:REACtive[:ACTual]? 674

POWer:QUALity:RESult:POWer:REALpower:AVG?. 674

POWer:QUALity:RESult:POWer:REALpower:NPEak?. 674

POWer:QUALity:RESult:POWer:REALpower:PPEak?. 674

POWer:QUALity:RESult:POWer:REALpower:STDDev?. 675

POWer:QUALity:RESult:POWer:REALpower:WFMCount?. 675

POWer:QUALity:RESult:POWer:REALpower[:ACTual]?. 674

POWer:QUALity:RESult:VOLTage:CREStfactor:AVG?. 672

POWer:QUALity:RESult:VOLTage:CREStfactor:NPEak?. 673

POWer:QUALity:RESult:VOLTage:CREStfactor:PPEak?. 673

POWer:QUALity:RESult:VOLTage:CREStfactor:STDDev?. 673

POWer:QUALity:RESult:VOLTage:CREStfactor:WFMCount?. 673

POWer:QUALity:RESult:VOLTage:CREStfactor[:ACTual]? 672

POWer:QUALity:RESult:VOLTage:FREQuency:AVG?. 672

POWer:QUALity:RESult:VOLTage:FREQuency:NPEak?. 673

POWer:QUALity:RESult:VOLTage:FREQuency:PPEak?. 673

POWer:QUALity:RESult:VOLTage:FREQuency:STDDev?. 673

POWer:QUALity:RESult:VOLTage:FREQuency:WFMCount?. 673

POWer:QUALity:RESult:VOLTage:FREQuency[:ACTual]?. 672

POWer:QUALity:RESult:VOLTage:RMS:AVG?. 672

POWer:QUALity:RESult:VOLTage:RMS:NPEak?. 673

POWer:QUALity:RESult:VOLTage:RMS:PPEak?. 673

POWer:QUALity:RESult:VOLTage:RMS:STDDev?. 673

POWer:QUALity:RESult:VOLTage:RMS:WFMCount?. 673

POWer:QUALity:RESult:VOLTage:RMS[:ACTual]? 672

POWer:REPort:ADD 667

POWer:REPort:DESCription 668

POWer:REPort:DUT 668

POWer:REPort:OUTPut. 668

POWer:REPort:SITE. 668

POWer:REPort:TEMPerature 668

POWer:REPort:USER 668

POWer:RESult:TABLe. 666

POWer:RIPPle:EXECute. 686

POWer:RIPPle:REPort:ADD. 686

POWer:RIPPle:RESult:FREQuency:AVG?. 686

POWer:RIPPle:RESult:FREQuency:NPEak?. 686

POWer:RIPPle:RESult:FREQuency:PPEak?. 686

POWer:RIPPle:RESult:FREQuency:STDDev?. 686

POWer:RIPPle:RESult:FREQuency:WFMCount?. 686

POWer:RIPPle:RESult:FREQuency[:ACTual]?. 686

POWer:RIPPle:RESult:LPEak:AVG?. 687

POWer:RIPPle:RESult:LPEak:NPEak?. 687

POWer:RIPPle:RESult:LPEak:PPEak?. 687

POWer:RIPPle:RESult:LPEak:STDDev?. 687

POWer:RIPPle:RESult:LPEak:WFMCount?. 687

POWer:RIPPle:RESult:LPEak[:ACTual]?. 687

POWer:RIPPle:RESult:MEAN:AVG?. 687

POWer:RIPPle:RESult:MEAN:NPEak?. 687

POWer:RIPPle:RESult:MEAN:PPEak?. 687

POWer:RIPPle:RESult:MEAN:STDDev?. 687

POWer:RIPPle:RESult:MEAN:WFMCount?. 687

POWer:RIPPle:RESult:MEAN[:ACTual]?. 687

POWer:RIPPle:RESult:NDCYcle:AVG?. 687

POWer:RIPPle:RESult:NDCYcle:NPEak? 688

POWer:RIPPle:RESult:NDCYcle:PPEak? 688

POWer:RIPPle:RESult:NDCYcle:STDDev? 688

POWer:RIPPle:RESult:NDCYcle:WFMCount? 688

POWer:RIPPle:RESult:NDCYcle[:ACTual]? 687

POWer:RIPPle:RESult:PDCYcle:AVG?. 688

POWer:RIPPle:RESult:PDCYcle:NPEak? 688

POWer:RIPPle:RESult:PDCYcle:PPEak?. 688

POWer:RIPPle:RESult:PDCYcle:STDDev? 688

POWer:RIPPle:RESult:PDCYcle:WFMCount?. 688

POWer:RIPPle:RESult:PDCYcle[:ACTual]?. 688

POWer:RIPPle:RESult:PEAK:AVG?. 688

POWer:RIPPle:RESult:PEAK:NPEak? 688

POWer:RIPPle:RESult:PEAK:PPEak? 688

POWer:RIPPle:RESult:PEAK:STDDev? 688

POWer:RIPPle:RESult:PEAK:WFMCount? 688

POWer:RIPPle:RESult:PEAK[:ACTual]? 688

POWer:RIPPle:RESult:PERiod:AVG?. 689

POWer:RIPPle:RESult:PERiod:NPEak? 689

POWer:RIPPle:RESult:PERiod:PPEak?. 689

POWer:RIPPle:RESult:PERiod:STDDev? 689

POWer:RIPPle:RESult:PERiod:WFMCount?. 689

POWer:RIPPle:RESult:PERiod[:ACTual]?. 689

POWer:RIPPle:RESult:STDDev:AVG?. 689

POWer:RIPPle:RESult:STDDev:NPEak?. 689

POWer:RIPPle:RESult:STDDev:PPEak?. 689

POWer:RIPPle:RESult:STDDev:STDDev?. 689

POWer:RIPPle:RESult:STDDev:WFMCount?. 689

POWer:RIPPle:RESult:STDDev[:ACTual]?. 689

POWer:RIPPle:RESult:UPEak:AVG?. 689

POWer:RIPPle:RESult:UPEak:NPEak?. 689

POWer:RIPPle:RESult:UPEak:PPEak?. 689

POWer:RIPPle:RESult:UPEak:STDDev?. 690

POWer:RIPPle:RESult:UPEak:WFMCount?. 690

POWer:RIPPle:RESult:UPEak[:ACTual]?. 689

POWer:SLEWrate:DSAMple 696

POWer:SLEWrate:DTIMe. 696

POWer:SLEWrate:EXECute 696

POWer:SLEWrate:REPort:ADD 696

POWer:SLEWrate:RESult:LPEak:AVG?. 696

POWer:SLEWrate:RESult:LPEak:NPEak?. 696

POWer:SLEWrate:RESult:LPEak:PPEak?. 696

POWer:SLEWrate:RESult:LPEak:STDDev?. 696

POWer:SLEWrate:RESult:LPEak:WFMCount?. 696

POWer:SLEWrate:RESult:LPEak[:ACTual]? 696

POWer:SLEWrate:RESult:UPEak:AVG?. 697

POWer:SLEWrate:RESult:UPEak:NPEak?. 697

POWer:SLEWrate:RESult:UPEak:PPEak?. 697

POWer:SLEWrate:RESult:UPEak:STDDev?. 697

POWer:SLEWrate:RESult:UPEak:WFMCount?. 697

POWer:SLEWrate:RESult:UPEak[:ACTual]? 697

POWer:SOA:EXECute. 708

POWer:SOA:LINear:ADD 709

POWer:SOA:LINear:COUNt? 712

POWer:SOA:LINear:INSert. 709

POWer:SOA:LINear:POINt<m>:CURRent 709

POWer:SOA:LINear:POINt<m>:CURRent:MAXimum 710

POWer:SOA:LINear:POINt<m>:CURRent:MINimum 710

POWer:SOA:LINear:POINt<m>:VOLTage. 710

POWer:SOA:LINear:REMove 710

POWer:SOA:LOGarithmic:ADD 709

POWer:SOA:LOGarithmic:COUNt? 712

POWer:SOA:LOGarithmic:INSert. 709

POWer:SOA:LOGarithmic:POINt<m>:CURRent. 709

POWer:SOA:LOGarithmic:POINt<m>:CURRent:MAXimum 710

POWer:SOA:LOGarithmic:POINt<m>:CURRent:MINimum 710

POWer:SOA:LOGarithmic:POINt<m>:VOLTage. 710

POWer:SOA:LOGarithmic:REMove 710

POWer:SOA:RESTart. 709

POWer:SOA:RESult:ACQuisition:FAILed?. 712

POWer:SOA:RESult:ACQuisition:FRATe?. 712

POWer:SOA:RESult:ACQuisition:PASSed?. 712

POWer:SOA:RESult:ACQuisition:POINts?. 712

POWer:SOA:RESult:ACQuisition:STATe?. 712

POWer:SOA:RESult:ACQuisition:TOLerance. 711

POWer:SOA:RESult:ACQuisition:VCOunt?. 713

POWer:SOA:RESult:ACQuisition:VIOLation<n>:CURRent? 713

POWer:SOA:RESult:ACQuisition:VIOLation<n>:VOLTage?. 713

POWer:SOA:RESult:ACQuisition:VIOLation<n>?. 713

POWer:SOA:RESult:TOTal:COUNt?. 714

POWer:SOA:RESult:TOTal:FAILed?. 714

POWer:SOA:RESult:TOTal:FRATe?. 714

POWer:SOA:RESult:TOTal:PASSed?. 714

POWer:SOA:RESult:TOTal:SAMPle:COUNt?. 713

POWer:SOA:RESult:TOTal:SAMPle:FAILed?. 714

POWer:SOA:RESult:TOTal:SAMPle:PASSed?. 714

POWer:SOA:RESult:TOTal:STATe?. 715

POWer:SOA:RESult:TOTal:TOLerance. 711

POWer:SOA:RESult:TOTal:VCOunt?. 715

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:HEADer?. 716

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:XINCrement?. 716

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:XORigin?. 716

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:YINCrement?. 716

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:YORigin?. 717

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA:YRESolution? 717

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent:DATA?. 716

POWer:SOA:RESult:TOTal:VIOLation<n>:CURRent? 715

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:HEADer? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:XINCrement? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:XORigin? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:YINCrement? 716

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:YORigin? 717

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA:YRESolution? 717

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage:DATA?. 716

POWer:SOA:RESult:TOTal:VIOLation<n>:VOLTage? 715

POWer:SOA:RESult:TOTal:VIOLation<n>?. 715

POWer:SOA:SCALe:DISPlay 709

POWer:SOA:SCALe:MASK. 709

POWer:SOURce:CURRent<n> 666

POWer:SOURce:VOLTage<n>. 666

POWer:SPECtrum:EXECute 690

POWer:SPECtrum:FREQuency 690

POWer:SPECtrum:REPort:ADD 690

POWer:SPECtrum:RESult<n>:FREQuency?. 691

POWer:SPECtrum:RESult<n>:LEVel[:VALue]?. 691

POWer:SPECtrum:RESult<n>:MAXimum?. 691

POWer:SPECtrum:RESult<n>:MEAN?. 691

POWer:SPECtrum:RESult<n>:MINimum?. 691

POWer:SPECtrum:RESult<n>:RESet. 692

POWer:SPECtrum:RESult<n>:WFMCount?. 692

POWer:STATistics:RESet. 667

POWer:STATistics:VISible 667

POWer:SWITching:EXECute 704

POWer:SWITching:GATE:CONDuction:STARt 704

POWer:SWITching:GATE:CONDuction:STOP 704

POWer:SWITching:GATE:NCONduction:STARt 704

POWer:SWITching:GATE:NCONduction:STOP 705

POWer:SWITching:GATE:SWAVe. 705

POWer:SWITching:GATE:TOFF:STARt. 705

POWer:SWITching:GATE:TOFF:STOP. 705

POWer:SWITching:GATE:TON:STARt 705

POWer:SWITching:GATE:TON:STOP 705

POWer:SWITching:REPort:ADD 705

POWer:SWITching:RESult:CONDuction:ENERgy? 706

POWer:SWITching:RESult:CONDuction:POWer?. 706

POWer:SWITching:RESult:NCONduction:ENERgy? 706

POWer:SWITching:RESult:NCONduction:POWer?. 706

POWer:SWITching:RESult:TOFF:ENERgy?. 706

POWer:SWITching:RESult:TOFF:POWer?. 706

POWer:SWITching:RESult:TON:ENERgy? 707

POWer:SWITching:RESult:TON:POWer?. 707

POWer:SWITching:RESult:TOTal:ENERgy? 707

POWer:SWITching:RESult:TOTal:POWer?. 707

POWer:SWITching:TYPE. 704

POWer:TRANsient:EXECute. 694

POWer:TRANsient:REPort:ADD. 694

POWer:TRANsient:RESult:DELay?. 694

POWer:TRANsient:RESult:OVERshoot?. 694

POWer:TRANsient:RESult:PEAK:TIME? 694

POWer:TRANsient:RESult:PEAK:VALue?. 694

POWer:TRANsient:RESult:RTIMe?. 695

POWer:TRANsient:RESult:SETTlingtime?. 695

POWer:TRANsient:SIGHigh. 695

POWer:TRANsient:SIGLow. 695

POWer:TRANsient:STARt. 695

POWer:TRANsient:STOP 695

POWer:ZOFFset[:EXECute] 667

PROBe<m>:ID:BUILd?. 436

PROBe<m>:ID:PARTnumber?. 436

PROBe<m>:ID:PRDate?. 436

PROBe<m>:ID:SRNumber?. 437

PROBe<m>:ID:SWVersion?. 437

PROBe<m>:SETup:ATTenuation:MANual 432

PROBe<m>:SETup:ATTenuation:UNIT. 432

PROBe<m>:SETup:ATTenuation[:AUTO]?. 432

PROBe<m>:SETup:BANDwidth? 433

PROBe<m>:SETup:CAPacitance? 433

PROBe<m>:SETup:CMOFfset 435

PROBe<m>:SETup:DCOFfset?. 433

PROBe<m>:SETup:IMPedance?. 433

PROBe<m>:SETup:MODE 434

PROBe<m>:SETup:NAME?. 434

PROBe<m>:SETup:OFFSwitch 434

PROBe<m>:SETup:TYPE?. 435

PROBe<m>:SETup:UOFFset 435

REFCurve<m>:DATA:HEADer? 474

REFCurve<m>:DATA:HEADer? 741

REFCurve<m>:DATA:POINts?. 475

REFCurve<m>:DATA:POINts?. 742

REFCurve<m>:DATA:XINCrement?. 742

REFCurve<m>:DATA:XORigin? 742

REFCurve<m>:DATA:YINCrement?. 743

REFCurve<m>:DATA:YORigin? 743

REFCurve<m>:DATA:YRESolution? 743

REFCurve<m>:DATA?. 474

REFCurve<m>:DATA?. 741

REFCurve<m>:HORizontal:POSition. 473

REFCurve<m>:HORizontal:SCALe. 473

REFCurve<m>:LOAD. 472

REFCurve<m>:LOAD:STATe. 473

REFCurve<m>:SAVE. 472

REFCurve<m>:SOURce. 471

REFCurve<m>:SOURce:CATalog? 472

REFCurve<m>:STATe. 471

REFCurve<m>:UPDate 472

REFCurve<m>:VERTical:POSition 474

REFCurve<m>:VERTical:SCALe 473

REFLevel:RELative:LOWer. 496

REFLevel:RELative:MIDDle. 496

REFLevel:RELative:MODE. 496

REFLevel:RELative:UPPer. 496

RUN. 413

RUNContinous 413

RUNSingle 414

SEARch:CONDition 531

SEARch:GATE:ABSolute:START 533

SEARch:GATE:ABSolute:STOP 534

SEARch:GATE:MODE. 533

SEARch:MEASure:LEVel:PEAK:MAGNitude 537

SEARch:MEASure:PEAK:POLarity. 536

SEARch:PROTocol:ARINc:CONDition 662

SEARch:PROTocol:ARINc:DATA:CONDition 662

SEARch:PROTocol:ARINc:DATA:MAXimum. 662

SEARch:PROTocol:ARINc:DATA:MINimum. 663

SEARch:PROTocol:ARINc:DATA:OFFSet 663

SEARch:PROTocol:ARINc:DATA:SIZE. 663

SEARch:PROTocol:ARINc:ERRor 663

SEARch:PROTocol:ARINc:FORMat. 663

SEARch:PROTocol:ARINc:LABel:CONDition 664

SEARch:PROTocol:ARINc:LABel:MAXimum 664

SEARch:PROTocol:ARINc:LABel:MINimum 664

SEARch:PROTocol:ARINc:SDI. 664

SEARch:PROTocol:ARINc:SSM. 664

SEARch:PROTocol:ARINc:WORD[:TYPE] 665

SEARch:PROTocol:CAN:ACKerror 599

SEARch:PROTocol:CAN:BITSterror. 599

SEARch:PROTocol:CAN:CONDition 598

SEARch:PROTocol:CAN:CRCerror 599

SEARch:PROTocol:CAN:DATA. 601

SEARch:PROTocol:CAN:DCONdition 601

SEARch:PROTocol:CAN:DLENgth 601

SEARch:PROTocol:CAN:FORMerror. 600

SEARch:PROTocol:CAN:FRAMe. 598

SEARch:PROTocol:CAN:FTYPe. 600

SEARch:PROTocol:CAN:ICONdition 600

SEARch:PROTocol:CAN:IDENtifier 600

SEARch:PROTocol:CAN:ITYPe. 600

SEARch:PROTocol:LIN:CHKSerror 614

SEARch:PROTocol:LIN:CONDition 612

SEARch:PROTocol:LIN:DATA. 615

SEARch:PROTocol:LIN:DCONdition 615

SEARch:PROTocol:LIN:DLENgth 614

SEARch:PROTocol:LIN:FRAMe. 613

SEARch:PROTocol:LIN:ICONdition 614

SEARch:PROTocol:LIN:IDENtifier. 614

SEARch:PROTocol:LIN:IPERror. 613

SEARch:PROTocol:LIN:SYERror. 614

SEARch:PROTocol:MILStd:CONDition 647

SEARch:PROTocol:MILStd:DATA:COMPare. 647

SEARch:PROTocol:MILStd:DATA:CONDition. 648

SEARch:PROTocol:MILStd:DATA:MAXimum. 648

SEARch:PROTocol:MILStd:DATA:MINimum. 648

SEARch:PROTocol:MILStd:DATA:OFFSet 648

SEARch:PROTocol:MILStd:DATA:WORDs. 648

SEARch:PROTocol:MILStd:ERRor. 648

SEARch:PROTocol:MILStd:MCODe. 648

SEARch:PROTocol:MILStd:RTADdress:COMPare. 649

SEARch:PROTocol:MILStd:RTADdress:CONDition 649

SEARch:PROTocol:MILStd:RTADdress:MAXimum. 649

SEARch:PROTocol:MILStd:RTADdress:MINimum. 649

SEARch:PROTocol:MILStd:SADDress:COMPare. 649

SEARch:PROTocol:MILStd:SADDress:CONDition 650

SEARch:PROTocol:MILStd:SADDress:MAXimum. 650

SEARch:PROTocol:MILStd:SADDress:MCADdress 650

SEARch:PROTocol:MILStd:SADDress:MINimum. 650

SEARch:PROTocol:MILStd:STATus:BCReceived 650

SEARch:PROTocol:MILStd:STATus:BUSY 650

SEARch:PROTocol:MILStd:STATus:DBCaccept 651

SEARch:PROTocol:MILStd:STATus:INSTrument 651

SEARch:PROTocol:MILStd:STATus:MERRor 651

SEARch:PROTocol:MILStd:STATus:SREQuest 651

SEARch:PROTocol:MILStd:STATus:SUBSystem 651

SEARch:PROTocol:MILStd:STATus:TERMinal 651

SEARch:PROTocol:MILStd:TRMode. 652

SEARch:PROTocol:MILStd:TTYPe. 652

SEARch:PROTocol:MILStd:WCOunt:COMPare. 652

SEARch:PROTocol:MILStd:WCOunt:CONDition. 652

SEARch:PROTocol:MILStd:WCOunt:MAXimum. 653

SEARch:PROTocol:MILStd:WCOunt:MINimum. 653

SEARch:PROTocol:MILStd:WSTart. 652

SEARch:RCOunt?. 546

SEARch:RESDiagram:SHOW. 545

SEARch:RESult:ALL?. 545

SEARch:RESult:BCOunt?. 545

SEARch:RESult<n>?. 546

SEARch:SOURce. 533

SEARch:STATe. 531

SEARch:TRIGger:DATatoclock:CEDGe. 542

SEARch:TRIGger:DATatoclock:CLEVel 541

SEARch:TRIGger:DATatoclock:CLEVel:DELTa 541

SEARch:TRIGger:DATatoclock:CSOurce. 541

SEARch:TRIGger:DATatoclock:DLEVel 541

SEARch:TRIGger:DATatoclock:DLEVel:DELTa 541

SEARch:TRIGger:DATatoclock:HTIMe. 542

SEARch:TRIGger:DATatoclock:STIMe. 542

SEARch:TRIGger:EDGE:LEVel. 534

SEARch:TRIGger:EDGE:LEVel:DELTa. 534

SEARch:TRIGger:EDGE:SLOPe. 534

SEARch:TRIGger:LEVel:RISetime:LOWer. 537

SEARch:TRIGger:LEVel:RISetime:UPPer. 538

SEARch:TRIGger:LEVel:RUNT:LOWer. 539

SEARch:TRIGger:LEVel:RUNT:UPPer. 539

SEARch:TRIGger:PATTern:FUNCtion. 543

SEARch:TRIGger:PATTern:LEVel<n>. 543

SEARch:TRIGger:PATTern:LEVel<n>:DELTa. 543

SEARch:TRIGger:PATTern:SOURce. 542

SEARch:TRIGger:PATTern:WIDTh:DELTa. 544

SEARch:TRIGger:PATTern:WIDTh:RANGe. 544

SEARch:TRIGger:PATTern:WIDTh[:WIDTh]. 544

SEARch:TRIGger:RISetime:DELTa. 538

SEARch:TRIGger:RISetime:RANGe. 538

SEARch:TRIGger:RISetime:SLOPe. 537

SEARch:TRIGger:RISetime:TIME. 538

SEARch:TRIGger:RUNT:DELTa. 540

SEARch:TRIGger:RUNT:POLarity. 539

SEARch:TRIGger:RUNT:RANGe. 540

SEARch:TRIGger:RUNT:WIDTh. 540

SEARch:TRIGger:WIDTh:DELTa 536

SEARch:TRIGger:WIDTh:LEVel 535

SEARch:TRIGger:WIDTh:LEVel:DELTa. 535

SEARch:TRIGger:WIDTh:POLarity 535

SEARch:TRIGger:WIDTh:RANGe 535

SEARch:TRIGger:WIDTh:WIDTh. 536

SINGle. 414

SPECtrum:DIAGram:COLor:MAGNitude:MODE. 522

SPECtrum:DIAGram:COLor:MAXimum[:LEVel]. 522

SPECtrum:DIAGram:COLor:MINimum[:LEVel]. 523

SPECtrum:DIAGram:COLor:SCHeme:FDOMain 523

SPECtrum:DIAGram:COLor:SCHeme:SPECtrogramm 523

SPECtrum:DIAGram:FDOMain[:ENABle]. 523

SPECtrum:DIAGram:SPECtrogram[:ENABle]. 523

SPECtrum:DIAGram:TDOMain[:ENABle]. 523

SPECtrum:FREQuency:AVERage:COMPlete? 509

SPECtrum:FREQuency:AVERage:COUNt. 509

SPECtrum:FREQuency:BANDwidth[:RESolution]:AUTO. 518

SPECtrum:FREQuency:BANDwidth[:RESolution]:RATio. 518

SPECtrum:FREQuency:BANDwidth[:RESolution][:VALue]. 519

SPECtrum:FREQuency:CENTer. 517

SPECtrum:FREQuency:FULLspan 517

SPECtrum:FREQuency:MAGNitude:SCALe 509

SPECtrum:FREQuency:POSition. 509

SPECtrum:FREQuency:RESet. 509

SPECtrum:FREQuency:SCALe. 510

SPECtrum:FREQuency:SPAN. 518

SPECtrum:FREQuency:STARt. 518

SPECtrum:FREQuency:STOP. 518

SPECtrum:FREQuency:WINDow:TYPE. 510

SPECtrum:HISTory:CURRent. 439

SPECtrum:HISTory:EXPort:NAME 446

SPECtrum:HISTory:EXPort:SAVE. 446

SPECtrum:HISTory:PALL. 440

SPECtrum:HISTory:PLAYer:SPEed. 441

SPECtrum:HISTory:PLAYer:STATe 442

SPECtrum:HISTory:REPLay. 441

SPECtrum:HISTory:STARt 440

SPECtrum:HISTory:STOP 440

SPECtrum:HISTory:TSABsolute:ALL?. 444

SPECtrum:HISTory:TSABsolute?. 444

SPECtrum:HISTory:TSDate:ALL?. 445

SPECtrum:HISTory:TSDate?. 445

SPECtrum:HISTory:TSRelative:ALL?. 443

SPECtrum:HISTory:TSRelative?. 443

SPECtrum:MARKer:DISPlay. 511

SPECtrum:MARKer:RCOunt?. 514

SPECtrum:MARKer:REFerence:SETup:FREQuency 513

SPECtrum:MARKer:REFerence:SETup:INDex 513

SPECtrum:MARKer:REFerence:SETup:MODE. 513

SPECtrum:MARKer:REFerence:SETup:SPAN. 513

SPECtrum:MARKer:RESult<n>:ALL:DELTa? 516

SPECtrum:MARKer:RESult<n>:ALL? 516

SPECtrum:MARKer:RESult<n>:DELTa? 516

SPECtrum:MARKer:RESult<n>:FREQuency:DELTa? 517

SPECtrum:MARKer:RESult<n>:FREQuency? 516

SPECtrum:MARKer:RESult<n>:LEVel:DELTa? 517

SPECtrum:MARKer:RESult<n>:LEVel? 517

SPECtrum:MARKer:RESult<n>?. 515

SPECtrum:MARKer:RMARker:FREQuency? 515

SPECtrum:MARKer:RMARker:LEVel? 515

SPECtrum:MARKer:RMARker? 515

SPECtrum:MARKer:RMODe. 514

SPECtrum:MARKer:RTABle:ENABle 514

SPECtrum:MARKer:RTABle:POSition. 515

SPECtrum:MARKer:SETup:DISTance. 512

SPECtrum:MARKer:SETup:EXCursion 512

SPECtrum:MARKer:SETup:MLEVel. 512

SPECtrum:MARKer:SETup:MMODe. 512

SPECtrum:MARKer:SETup:MWIDth. 513

SPECtrum:MARKer:SOURce. 511

SPECtrum:MARKer[:ENABle]. 512

SPECtrum:SOURce. 509

SPECtrum:SPECtrogram:RESet. 511

SPECtrum:SPECtrogram:SCALe. 511

SPECtrum:TIME:POSition 519

SPECtrum:TIME:RANGe 519

SPECtrum:WAVeform:AVERage:DATA:HEADer?. 520

SPECtrum:WAVeform:AVERage:DATA:POINts?. 521

SPECtrum:WAVeform:AVERage:DATA:XINCrement?. 521

SPECtrum:WAVeform:AVERage:DATA:XORigin? 521

SPECtrum:WAVeform:AVERage:DATA:YINCrement?. 521

SPECtrum:WAVeform:AVERage:DATA:YORigin? 521

SPECtrum:WAVeform:AVERage:DATA:YRESolution? 522

SPECtrum:WAVeform:AVERage:DATA?. 520

SPECtrum:WAVeform:AVERage[:ENABle]. 520

SPECtrum:WAVeform:MAXimum:DATA:HEADer?. 520

SPECtrum:WAVeform:MAXimum:DATA:POINts? 521

SPECtrum:WAVeform:MAXimum:DATA:XINCrement?. 521

SPECtrum:WAVeform:MAXimum:DATA:XORigin?. 521

SPECtrum:WAVeform:MAXimum:DATA:YINCrement?. 521

SPECtrum:WAVeform:MAXimum:DATA:YORigin?. 521

SPECtrum:WAVeform:MAXimum:DATA:YRESolution? 522

SPECtrum:WAVeform:MAXimum:DATA?. 520

SPECtrum:WAVeform:MAXimum[:ENABle]. 520

SPECtrum:WAVeform:MINimum:DATA:HEADer?. 520

SPECtrum:WAVeform:MINimum:DATA:POINts? 521

SPECtrum:WAVeform:MINimum:DATA:XINCrement?. 521

SPECtrum:WAVeform:MINimum:DATA:XORigin?. 521

SPECtrum:WAVeform:MINimum:DATA:YINCrement?. 521

SPECtrum:WAVeform:MINimum:DATA:YORigin?. 522

SPECtrum:WAVeform:MINimum:DATA:YRESolution? 522

SPECtrum:WAVeform:MINimum:DATA?. 520

SPECtrum:WAVeform:MINimum[:ENABle]. 520

SPECtrum:WAVeform:SPECtrum:DATA:HEADer? 520

SPECtrum:WAVeform:SPECtrum:DATA:POINts?. 521

SPECtrum:WAVeform:SPECtrum:DATA:XINCrement? 521

SPECtrum:WAVeform:SPECtrum:DATA:XORigin? 521

SPECtrum:WAVeform:SPECtrum:DATA:YINCrement? 521

SPECtrum:WAVeform:SPECtrum:DATA:YORigin? 522

SPECtrum:WAVeform:SPECtrum:DATA:YRESolution? 522

SPECtrum:WAVeform:SPECtrum:DATA?. 520

SPECtrum:WAVeform:SPECtrum[:ENABle] 520

SPECtrum[:STATe] 508

STATus:OPERation:CONDition? 759

STATus:OPERation:ENABle. 760

STATus:OPERation:NTRansition 760

STATus:OPERation:PTRansition. 760

STATus:OPERation[:EVENt]? 760

STATus:PRESet 762

STATus:QUEStionable:CONDition? 762

STATus:QUEStionable:COVerload:CONDition? 762

STATus:QUEStionable:COVerload:ENABle. 762

STATus:QUEStionable:COVerload:NTRansition 763

STATus:QUEStionable:COVerload:PTRansition 763

STATus:QUEStionable:COVerload[:EVENt]?. 763

STATus:QUEStionable:ENABle 762

STATus:QUEStionable:LIMit:CONDition? 762

STATus:QUEStionable:LIMit:ENABle. 762

STATus:QUEStionable:LIMit:NTRansition 763

STATus:QUEStionable:LIMit:PTRansition 763

STATus:QUEStionable:LIMit[:EVENt]?. 763

STATus:QUEStionable:MASK:CONDition? 762

STATus:QUEStionable:MASK:ENABle. 762

STATus:QUEStionable:MASK:NTRansition 763

STATus:QUEStionable:MASK:PTRansition 763

STATus:QUEStionable:MASK[:EVENt]?. 763

STATus:QUEStionable:NTRansition 763

STATus:QUEStionable:PTRansition 763

STATus:QUEStionable[:EVENt]?. 763

STOP 414

SYST:PRESet 759

SYSTem:BEEPer:CONTrol:STATe. 757

SYSTem:BEEPer:ERRor:STATe. 757

SYSTem:BEEPer:TRIG:STATe. 758

SYSTem:BEEPer[:IMMediate] 758

SYSTem:COMMunicate:PRINter:CSET. 754

SYSTem:COMMunicate:PRINter:ENUMerate:FIRSt?. 754

SYSTem:COMMunicate:PRINter:ENUMerate[:NEXT]?. 754

SYSTem:COMMunicate:PRINter:SELect. 754

SYSTem:DATE. 757

SYSTem:EDUCation:PRESet. 759

SYSTem:ERRor:[NEXT]?. 758

SYSTem:ERRor:ALL?. 758

SYSTem:NAME. 756

SYSTem:SET 758

SYSTem:TIME 757

TCOunter<t>:ENAB. 727

TCOunter<t>:RESult[:ACTual]:FREQuency?. 727

TCOunter<t>:RESult[:ACTual]:PERiod?. 728

TIMebase:ACQTime. 415

TIMebase:DIVisions? 415

TIMebase:POSition. 416

TIMebase:RANGe. 415

TIMebase:RATime?. 415

TIMebase:REFerence 416

TIMebase:ROLL:ENABle. 420

TIMebase:SCALe. 414

TIMebase:ZOOM:POSition 469

TIMebase:ZOOM:SCALe 469

TIMebase:ZOOM:STATe. 468

TIMebase:ZOOM:TIME. 469

TRIGger:A:ARINc:DATA:CONDition 655

TRIGger:A:ARINc:DATA:MAXimum 655

TRIGger:A:ARINc:DATA:MINimum 655

TRIGger:A:ARINc:DATA:OFFSet. 655

TRIGger:A:ARINc:DATA:SIZE. 656

TRIGger:A:ARINc:ERRor:CODing. 656

TRIGger:A:ARINc:ERRor:GAP. 656

TRIGger:A:ARINc:ERRor:PARity. 656

TRIGger:A:ARINc:FORMat. 656

TRIGger:A:ARINc:LABel:CONDition. 656

TRIGger:A:ARINc:LABel:MAXimum. 657

TRIGger:A:ARINc:LABel:MINimum. 657

TRIGger:A:ARINc:SDI. 657

TRIGger:A:ARINc:SSM. 657

TRIGger:A:ARINc:TTIMe:CONDition 658

TRIGger:A:ARINc:TTIMe:MAXimum. 658

TRIGger:A:ARINc:TTIMe:MINimum. 658

TRIGger:A:ARINc:TYPE. 658

TRIGger:A:ARINc:WORD:TYPE. 658

TRIGger:A:CAN:ACKerror. 590

TRIGger:A:CAN:BITSterror 590

TRIGger:A:CAN:CRCerror. 590

TRIGger:A:CAN:DATA. 590

TRIGger:A:CAN:DCONdition 589

TRIGger:A:CAN:DLC. 589

TRIGger:A:CAN:FORMerror. 590

TRIGger:A:CAN:FTYPe 588

TRIGger:A:CAN:ICONdition. 589

TRIGger:A:CAN:IDENtifier. 589

TRIGger:A:CAN:ITYPe 588

TRIGger:A:CAN:TYPE 587

TRIGger:A:EDGE:COUPling 450

TRIGger:A:EDGE:FILTer:LPASs. 450

TRIGger:A:EDGE:FILTer:NREJect. 451

TRIGger:A:EDGE:SLOPe. 450

TRIGger:A:FINDlevel 448

TRIGger:A:HOLDoff:MODE. 449

TRIGger:A:HOLDoff:TIME. 449

TRIGger:A:HYSTeresis 451

TRIGger:A:I2C:ACCess 567

TRIGger:A:I2C:ADDRess 568

TRIGger:A:I2C:AMODe 567

TRIGger:A:I2C:MODE. 567

TRIGger:A:I2C:PATTern. 568

TRIGger:A:I2C:PLENgth 568

TRIGger:A:I2C:POFFset. 569

TRIGger:A:I2S:CHANnel:LEFT:CONDition. 623

TRIGger:A:I2S:CHANnel:LEFT:DMAX. 623

TRIGger:A:I2S:CHANnel:LEFT:DMIN. 623

TRIGger:A:I2S:CHANnel:RIGHt:CONDition. 623

TRIGger:A:I2S:CHANnel:RIGHt:DMAX. 623

TRIGger:A:I2S:CHANnel:RIGHt:DMIN. 623

TRIGger:A:I2S:CHANnel:TDM<n>:CONDition 623

TRIGger:A:I2S:CHANnel:TDM<n>:DMAX. 623

TRIGger:A:I2S:CHANnel:TDM<n>:DMIN. 623

TRIGger:A:I2S:FUNCtion 624

TRIGger:A:I2S:SOWords. 624

TRIGger:A:I2S:TYPE. 622

TRIGger:A:I2S:WINDow:LENGth. 624

TRIGger:A:I2S:WSELect:SLOPe. 624

TRIGger:A:I2S:WSSLope 624

TRIGger:A:LEVel<n>:HYSTeresis. 451

TRIGger:A:LEVel<n>:RISetime:LOWer. 458

TRIGger:A:LEVel<n>:RISetime:UPPer. 458

TRIGger:A:LEVel<n>:RUNT:LOWer. 457

TRIGger:A:LEVel<n>:RUNT:UPPer. 457

TRIGger:A:LEVel<n>[:VALue]. 447

TRIGger:A:LIN:CHKSerror 605

TRIGger:A:LIN:DATA. 606

TRIGger:A:LIN:DCONdition 606

TRIGger:A:LIN:DLENgth 606

TRIGger:A:LIN:ICONdition 605

TRIGger:A:LIN:IDENtifier 605

TRIGger:A:LIN:IPERror 605

TRIGger:A:LIN:SYERror 605

TRIGger:A:LIN:TYPE. 604

TRIGger:A:MILStd:COMMand:TYPE 634

TRIGger:A:MILStd:DATA:CONDition 638

TRIGger:A:MILStd:DATA:MAXimum. 639

TRIGger:A:MILStd:DATA:MINimum. 639

TRIGger:A:MILStd:DATA:OFFSet. 639

TRIGger:A:MILStd:DATA:OFFSet:CONDition 639

TRIGger:A:MILStd:DATA:WORDs. 639

TRIGger:A:MILStd:ERRor:MANChester. 633

TRIGger:A:MILStd:ERRor:PARity. 633

TRIGger:A:MILStd:ERRor:SYNC. 634

TRIGger:A:MILStd:ERRor:TIMeout 634

TRIGger:A:MILStd:MCODe:CODE 634

TRIGger:A:MILStd:MCODe:VALue 635

TRIGger:A:MILStd:RTADdress:CONDition. 635

TRIGger:A:MILStd:RTADdress:MAXimum. 635

TRIGger:A:MILStd:RTADdress:MINimum. 635

TRIGger:A:MILStd:SADDress:CONDition. 636

TRIGger:A:MILStd:SADDress:MAXimum. 636

TRIGger:A:MILStd:SADDress:MCADdress. 636

TRIGger:A:MILStd:SADDress:MINimum. 636

TRIGger:A:MILStd:STATus:BCReceived 637

TRIGger:A:MILStd:STATus:BUSY. 637

TRIGger:A:MILStd:STATus:DBCaccept. 637

TRIGger:A:MILStd:STATus:INSTrument. 637

TRIGger:A:MILStd:STATus:MERRor. 638

TRIGger:A:MILStd:STATus:SREQuest. 638

TRIGger:A:MILStd:STATus:SUBSystem. 638

TRIGger:A:MILStd:STATus:TERMinal 638

TRIGger:A:MILStd:SYNC 633

TRIGger:A:MILStd:TRMode 636

TRIGger:A:MILStd:TTYPe. 639

TRIGger:A:MILStd:TYPE. 633

TRIGger:A:MILStd:WCOunt:CONDition 636

TRIGger:A:MILStd:WCOunt:MAXimum. 637

TRIGger:A:MILStd:WCOunt:MINimum. 637

TRIGger:A:MILStd:WORD. 633

TRIGger:A:MODE. 447

TRIGger:A:PATTern:CONDition 455

TRIGger:A:PATTern:FUNCtion 455

TRIGger:A:PATTern:MODE. 456

TRIGger:A:PATTern:SOURce 455

TRIGger:A:PATTern:WIDTh:DELTa. 457

TRIGger:A:PATTern:WIDTh:RANGe. 456

TRIGger:A:PATTern:WIDTh[:WIDTh] 456

TRIGger:A:RISetime:DELTa. 459

TRIGger:A:RISetime:RANGe. 458

TRIGger:A:RISetime:SLOPe. 458

TRIGger:A:RISetime:TIME 459

TRIGger:A:RUNT:POLarity. 457

TRIGger:A:SOURce 448

TRIGger:A:SOURce 555

TRIGger:A:SOURce 566

TRIGger:A:SOURce 580

TRIGger:A:SOURce 587

TRIGger:A:SOURce 603

TRIGger:A:SOURce 621

TRIGger:A:SPI:MODE. 555

TRIGger:A:SPI:PATTern. 556

TRIGger:A:SPI:PLENgth. 556

TRIGger:A:SPI:POFFset. 557

TRIGger:A:TV:FIELd. 453

TRIGger:A:TV:LINE. 454

TRIGger:A:TV:POLarity. 453

TRIGger:A:TV:STANdard 453

TRIGger:A:TYPE. 448

TRIGger:A:UART:MODE. 580

TRIGger:A:UART:PATTern. 581

TRIGger:A:UART:PLENgth 581

TRIGger:A:UART:POFFset. 582

TRIGger:A:WIDTh:DELTa. 452

TRIGger:A:WIDTh:POLarity. 451

TRIGger:A:WIDTh:RANGe. 452

TRIGger:A:WIDTh:WIDTh. 452

TRIGger:B:DELay 460

TRIGger:B:EDGE:SLOPe. 460

TRIGger:B:ENABle 459

TRIGger:B:EVENt:COUNt. 461

TRIGger:B:FINDlevel 460

TRIGger:B:HYSTeresis 461

TRIGger:B:LEVel 460

TRIGger:B:LEVel:HYSTeresis. 461

TRIGger:B:MODE. 460

TRIGger:B:SOURce 459

TRIGger:EXTern:COUPling. 449

TRIGger:EXTern:OVERload. 449

TRIGger:EXTern:TERMination. 449

TRIGger:OUT:MODE. 756

TRIGger:OUT:PLENgth 756

TRIGger:OUT:POLarity. 756

TSTamp:ACLear. 470

TSTamp:CLEar. 470

TSTamp:NEXT. 470

TSTamp:PREVious. 470

TSTamp:SET 470
