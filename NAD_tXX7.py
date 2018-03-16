
import sys
import time
import serial
from collections import namedtuple


if sys.version_info.major < 3:
    raise RuntimeError("Python 3 only")


# Named variable with a default value for operators
Variable = namedtuple('variable', ['description', 'possible_values', 'operators'])
Variable.__new__.__defaults__ = ('=+-?',)


class TBase:
    """Serial driver for the NAD T777 Sorround Receiver"""

    specification = {
        'DSP.Version': Variable(
            'Query DSP Version',
            None,
            {'?'},
        ),
        'Ipod.Album': Variable(
            'Get the current playing album name',
            None,
            {'?'},
        ),
        'Ipod.Artist': Variable(
            'Get the current playing track artist',
            None,
            {'?'},
        ),
        'Ipod.AudiobookSpeed': Variable(
            'iPod Audiobook Speed',
            {'Normal', 'Slow', 'Fast'},
        ),
        'Ipod.AutoConnect': Variable(
            'AutoConnect to iPod when iPod source is selected',
            {'No', 'Yes'},
        ),
        'Ipod.Enabled': Variable(
            'Enable/Disable the iPod interface',
            {'No', 'Yes'},
        ),
        'Ipod.MenuTimeout': Variable(
            'Timeout before returning to iPod "Now Playing" screen',
            range(0, 61, 5),
        ),
        'Ipod.PlayMode': Variable(
            'Set the iPod to Rewind',
            {'Pause', 'Rewind', 'FastForward', 'Play'},
        ),
        'Ipod.Repeat': Variable(
            'Set the iPod to Repeat Off, One, or All',
            {'Off', 'All', 'One'},
        ),
        'Ipod.Shuffle': Variable(
            'Set the iPod to Shuffle Off, Songs, or Albums. Note: must be set before selecting music.',
            {'Off', 'Albums', 'Songs'},
        ),
        'Ipod.Title': Variable(
            'Get the current playing track title',
            None,
            {'?'},
        ),
        'Ipod.Track': Variable(
            'Track Next/Previous',
            None,
            {'+', '-'},
        ),
        'Main.Amp.Back': Variable(
            'Set the back Amplifier output to Zone3',
            {'Front', 'Back', 'Zone3', 'Zone4', 'Zone2'},
        ),
        'Main.Audyssey': Variable(
            'Set the Audyssey Curve',
            {'Audyssey', 'Off', 'Flat', 'NAD'},
        ),
        'Main.Audyssey.ADV': Variable(
            'Audyssey Volume (Command Valid with AM200 Only)',
            {'Off', 'Heavy', 'Light', 'Medium'},
        ),
        'Main.Audyssey.DEQ': Variable(
            'Audyssey Dynamic EQ (Command Valid with AM200 Only)',
            {'Off', 'On'},
        ),
        'Main.Audyssey.Offset': Variable(
            'Audyssey Dynamic EQ Offset (Command Valid with AM200 Only)',
            range(0, 16),
        ),
        'Main.AutoTrigger': Variable(
            'Set Trigger Input',
            {'Zone3', 'All', 'Main', 'Zone4', 'Zone2'},
        ),
        'Main.Bass': Variable(
            'Set the Bass Tone Control',
            range(-10, 11, 2),
        ),
        'Main.CEC.Arc': Variable(
            'Enables selection of ARC in Source Setup OSD Menu',
            {'SourceSetup', 'Off', 'Auto'},
        ),
        'Main.CEC.Audio': Variable(
            'Feature Disabled',
            {'Off', 'On'},
        ),
        'Main.CEC.Power': Variable(
            'Allows receiver to be turned on and off via CEC (TXX5 series only turns off)',
            {'Off', 'On'},
        ),
        'Main.CEC.Switch': Variable(
            'Allows CEC to change receiver\'s source',
            {'Off', 'On'},
        ),
        'Main.CenterDialog': Variable(
            'Set the CenterDialog Tone Control',
            range(-6, 7, 2),
        ),
        'Main.ControlStandby': Variable(
            'Allow Ethernet control when in standby',
            {'Off', 'On'},
        ),
        'Main.DTS.CenterGain': Variable(
            'Set DTS Center Gain',
            {'0.5', '0.2', '0.3', '0.1', '0', '0.4'},
        ),
        'Main.DTS.DRC': Variable(
            'Set DTS Dynamic Range Control',
            range(25, 101, 25),
        ),
        'Main.Dimmer': Variable(
            'Front VFD Dimmer',
            {'Off', 'On'},
        ),
        'Main.Distance.BackLeft': Variable(
            'Set the speaker distance in Feet',
            range(0, 31),
        ),
        'Main.Distance.BackRight': Variable(
            'Set the speaker distance in Feet',
            range(0, 31),
        ),
        'Main.Distance.Center': Variable(
            'Set the speaker distance in Feet',
            range(0, 31),
        ),
        'Main.Distance.Left': Variable(
            'Set the speaker distance in Feet',
            range(0, 31),
        ),
        'Main.Distance.Right': Variable(
            'Set the speaker distance in Feet',
            range(0, 31),
        ),
        'Main.Distance.Sub': Variable(
            'Set the speaker distance in Feet',
            range(0, 31),
        ),
        'Main.Distance.SurroundLeft': Variable(
            'Set the speaker distance in Feet',
            range(0, 31),
        ),
        'Main.Distance.SurroundRight': Variable(
            'Set the speaker distance in Feet',
            range(0, 31),
        ),
        'Main.Distance.UOM': Variable(
            'Set the Unit of Measurement',
            {'Feet', 'Meters'},
        ),
        'Main.Dolby.CenterWidth': Variable(
            'Dolby Center Width',
            range(0, 8),
        ),
        'Main.Dolby.DRC': Variable(
            'Dolby Dynamic Range Control (100% is maximum dynamic range)',
            range(25, 101, 25),
        ),
        'Main.Dolby.Dimension': Variable(
            'Dolby Dimension',
            range(-7, 8),
        ),
        'Main.Dolby.Panorama': Variable(
            'Set Dolby Panorama',
            {'Off', 'On'},
        ),
        'Main.EnhancedBass': Variable(
            'Set Enhanced Bass On/Off',
            {'Off', 'On'},
        ),
        'Main.EnhancedStereo.Back': Variable(
            'Set Enhanced Stereo Speakers',
            {'Off', 'On'},
        ),
        'Main.EnhancedStereo.Center': Variable(
            'Set Enhanced Stereo Speakers',
            {'Off', 'On'},
        ),
        'Main.EnhancedStereo.Front': Variable(
            'Set Enhanced Stereo Speakers',
            {'Off', 'On'},
        ),
        'Main.EnhancedStereo.Surround': Variable(
            'Set Enhanced Stereo Speakers',
            {'Off', 'On'},
        ),
        'Main.IR': Variable(
            'Send IR Commands via RS232 where <VALUE> is decimal IR code',
            {'<VALUE>'},
            {'='},
        ),
        'Main.IR.Channel': Variable(
            'Set the Main IR Channel (allows for two NAD\'s to be controlled seperately)',
            range(0, 2),
        ),
        'Main.IR1': Variable(
            'String showing the HEX value of a supported IR command (0x877C customer code)',
            {'<VALUE>'},
            {'='},
        ),
        'Main.IR2': Variable(
            'String showing the HEX value of a supported IR command (0x860F customer code)',
            {'<VALUE>'},
            {'='},
        ),
        'Main.Level.BackLeft': Variable(
            'Set Speaker Level',
            range(-12, 13),
        ),
        'Main.Level.BackRight': Variable(
            'Set Speaker Level',
            range(-12, 13),
        ),
        'Main.Level.Center': Variable(
            'Set Speaker Level',
            range(-12, 13),
        ),
        'Main.Level.Left': Variable(
            'Set Speaker Level',
            range(-12, 13),
        ),
        'Main.Level.Right': Variable(
            'Set Speaker Level',
            range(-12, 13),
        ),
        'Main.Level.Sub': Variable(
            'Set Speaker Level',
            range(-12, 13),
        ),
        'Main.Level.SurroundLeft': Variable(
            'Set Speaker Level',
            range(-12, 13),
        ),
        'Main.Level.SurroundRight': Variable(
            'Set Speaker Level',
            range(-12, 13),
        ),
        'Main.LipSyncDelay': Variable(
            'Set Lip Sync Delay',
            range(0, 121),
        ),
        'Main.ListeningMode': Variable(
            'Set Active Listening Mode',
            {'EARS', 'PLIIMusic', 'NEO6Music', 'PLIIMovie', 'NEO6Cinema', 'EnhancedStereo', 'SurroundEX', 'AnalogBypass', 'None', 'ProLogic', 'StereoDownmix'},
        ),
        'Main.ListeningMode.Analog': Variable(
            'Set default Analog Signal Listening Mode',
            {'EARS', 'PLIIMusic', 'NEO6Music', 'PLIIMovie', 'NEO6Cinema', 'EnhancedStereo', 'AnalogBypass', 'None', 'ProLogic'},
        ),
        'Main.ListeningMode.DTS': Variable(
            'Set default DTS Listening Mode',
            {'NEO6Music', 'None', 'StereoDownmix'},
        ),
        'Main.ListeningMode.Digital': Variable(
            'Set default Digital Signal Listening Mode',
            {'EARS', 'NEO6Music', 'PLIIMusic', 'PLIIMovie', 'NEO6Cinema', 'EnhancedStereo', 'None', 'ProLogic', 'StereoDownmix'},
        ),
        'Main.ListeningMode.DolbyDigital': Variable(
            'Set default Dolby Digital Listening Mode',
            {'PLIIMusic', 'PLIIMovie', 'SurroundEX', 'None', 'StereoDownmix'},
        ),
        'Main.ListeningMode.DolbyDigital2ch': Variable(
            'Set default Dolby Digital 2 channel Listening Mode',
            {'PLIIMusic', 'ProLogic', 'PLIIMovie', 'None'},
        ),
        'Main.Model': Variable(
            'Query AVR Model',
            None,
            {'?'},
        ),
        'Main.Mute': Variable(
            'Set Mute',
            {'Off', 'On'},
        ),
        'Main.OSD.TempDisplay': Variable(
            'Set OSD Temp Display On/Off',
            {'Off', 'On'},
        ),
        'Main.Power': Variable(
            'Turn the Main Power On/Off',
            {'Off', 'On'},
        ),
        'Main.Sleep': Variable(
            'Set Time before Sleep',
            range(0, 91),
        ),
        'Main.Source': Variable(
            'Set Main Source',
            range(1, 11),
        ),
        'Main.Speaker.Back.Config1': Variable(
            'Set Back Speakers to Off, One, or Two speakers',
            range(0, 3),
        ),
        'Main.Speaker.Back.Config2': Variable(
            'Set Speaker Size',
            {'Small', 'Large'},
        ),
        'Main.Speaker.Back.Frequency': Variable(
            'Set Speaker Crossover',
            range(40, 201, 10),
        ),
        'Main.Speaker.Center.Config': Variable(
            'Set Speaker Size or Turn Speaker Off',
            {'Off', 'Small', 'Large'},
        ),
        'Main.Speaker.Center.Frequency': Variable(
            'Set Speaker Crossover',
            range(40, 201, 10),
        ),
        'Main.Speaker.Front.Config': Variable(
            'Set Speaker Size',
            {'Small', 'Large'},
        ),
        'Main.Speaker.Front.Frequency': Variable(
            'Set Speaker Crossover',
            range(40, 201, 10),
        ),
        'Main.Speaker.Sub': Variable(
            'Set Subwoofer On/Off',
            {'Off', 'On'},
        ),
        'Main.Speaker.Surround.Config': Variable(
            'Set Speaker Size or Turn Speaker Off',
            {'Off', 'Small', 'Large'},
        ),
        'Main.Speaker.Surround.Frequency': Variable(
            'Set Speaker Crossover',
            range(40, 201, 10),
        ),
        'Main.ToneDefeat': Variable(
            'Set Tone Defeat On/Off',
            {'Off', 'On'},
        ),
        'Main.Treble': Variable(
            'Set Treble Tone Control',
            range(-10, 11, 2),
        ),
        'Main.Trigger1.Delay': Variable(
            'Set Trigger 1 Delay',
            range(0, 16),
        ),
        'Main.Trigger1.Out': Variable(
            'Set Trigger 1',
            {'Zone234', 'Zone3', 'Main', 'Zone4', 'Source', 'Zone2'},
        ),
        'Main.Trigger2.Delay': Variable(
            'Set Trigger 2 Delay',
            range(0, 16),
        ),
        'Main.Trigger2.Out': Variable(
            'Set Trigger 2',
            {'Zone234', 'Zone3', 'Main', 'Zone4', 'Source', 'Zone2'},
        ),
        'Main.Trigger3.Delay': Variable(
            'Set Trigger 3 Delay',
            range(0, 16),
        ),
        'Main.Trigger3.Out': Variable(
            'Set Trigger 3',
            {'Zone234', 'Zone3', 'Main', 'Zone4', 'Source', 'Zone2'},
        ),
        'Main.Trim.Center': Variable(
            'Set Trim Level (Not saved when receiver power is cycled)',
            range(-6, 7),
        ),
        'Main.Trim.Sub': Variable(
            'Set Trim Level (Not saved when receiver power is cycled)',
            range(-6, 7),
        ),
        'Main.Trim.Surround': Variable(
            'Set Trim Level (Not saved when receiver power is cycled)',
            range(-6, 7),
        ),
        'Main.VFD.Display': Variable(
            'Set VFD Display Temp/On',
            {'On', 'Temp'},
        ),
        'Main.VFD.Line1': Variable(
            'Set VFD Line 1 Item',
            {'Volume', 'Off', 'AudioSourceFormat', 'Zone2Source', 'Zone4Source', 'ListeningMode', 'MainSource', 'Zone3Source'},
        ),
        'Main.VFD.Line2': Variable(
            'Set VFD Line 2 Item',
            {'Volume', 'Off', 'AudioSourceFormat', 'Zone2Source', 'MainSource', 'ListeningMode', 'Zone4Source', 'Zone3Source'},
        ),
        'Main.VFD.TempLine': Variable(
            'Set VFD Time Line to 1 or 2',
            range(1, 3),
        ),
        'Main.Version': Variable(
            'Query Main MCU Version',
            None,
            {'?'},
        ),
        'Main.Video.Aspect.Mode': Variable(
            'Zome the video output (Command Valid with VM200 Only)',
            {'Stretch', 'LetterBox', 'Zoom'},
        ),
        'Main.Video.Aspect.Ratio': Variable(
            '(Command Valid with VM200 Only)',
            {'4:3', '16:9'},
        ),
        'Main.Video.Brightness': Variable(
            'Brightness (Command Valid with VM200 Only)',
            range(0, 101),
        ),
        'Main.Video.Contrast': Variable(
            'Contrast (Command Valid with VM200 Only)',
            range(0, 101),
        ),
        'Main.Video.EdgeEnhancement.Level': Variable(
            'Edge Enhacement (Command Valid with VM200 Only)',
            range(0, 101),
        ),
        'Main.Video.EdgeEnhancement.Treshold': Variable(
            'Edge Enhacement (Command Valid with VM200 Only)',
            range(0, 101),
        ),
        'Main.Video.NoiseReduction': Variable(
            'Noise Reduction (Command Valid with VM200 Only)',
            range(0, 51),
        ),
        'Main.Video.Rate': Variable(
            '(Command Valid with VM200 Only)',
            {'60', '50'},
        ),
        'Main.Video.Resolution': Variable(
            'Video Resolution (Command Valid with VM200 Only)',
            {'480i', '576i', '576p', '480p', '720p', '1080p', '1080i'},
        ),
        'Main.VideoMode': Variable(
            'Set Main Video Mode',
            {'NTSC', 'PAL'},
        ),
        'Main.Volume': Variable(
            'Set Main Volume (range depends on levels, trims, etc)',
            range(-99, 20),
        ),
        'Preset1.Setup.DSPOptions': Variable(
            'Set Preset to include DSP Options',
            {'No', 'Yes'},
        ),
        'Preset1.Setup.ListeningMode': Variable(
            'Set Preset to include Listening Mode Options',
            {'No', 'Yes'},
        ),
        'Preset1.Setup.PictureControls': Variable(
            '(Command Valid with VM200 Only)',
            {'No', 'Yes'},
        ),
        'Preset1.Setup.Speaker': Variable(
            'Set Preset to not include Speaker Settings',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.Display': Variable(
            'Set Preset to not include Display settings',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.PictureControls': Variable(
            '(Command Valid with VM200 Only)',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.Display': Variable(
            'Set Preset to not include Display settings',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.PictureControls': Variable(
            '(Command Valid with VM200 Only)',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.Speaker': Variable(
            'Set Preset to not include Speaker Settings',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.DSPOptions': Variable(
            'Set Preset to not include DSP Options',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.ListeningMode': Variable(
            'Set Preset to not include Listening Mode Options',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.PictureControls': Variable(
            '(Command Valid with VM200 Only)',
            {'No', 'Yes'},
        ),
        'Preset5.Setup.DSPOptions': Variable(
            'Set Preset to not include DSP Options',
            {'No', 'Yes'},
        ),
        'Preset5.Setup.Display': Variable(
            'Set Preset to not include Display settings',
            {'No', 'Yes'},
        ),
        'Preset5.Setup.ListeningMode': Variable(
            'Set Preset to not include Listening Mode Options',
            {'No', 'Yes'},
        ),
        'Preset5.Setup.PictureControls': Variable(
            '(Command Valid with VM200 Only)',
            {'No', 'Yes'},
        ),
        'Preset5.Setup.Speaker': Variable(
            'Set Preset to not include Speaker Settings',
            {'No', 'Yes'},
        ),
        'Preset5.Setup.ToneControls': Variable(
            'Set Preset to not include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Source1.AnalogAudioFormat': Variable(
            'Set Analog Audio Format',
            {'Off', '7.1', 'Stereo'},
        ),
        'Source1.AnalogAudioInput': Variable(
            'Set Analog Audio Input',
            range(1, 9),
        ),
        'Source1.AnalogGain': Variable(
            'Set Analog Audio Gain',
            range(-12, 13, 3),
        ),
        'Source1.DigitalAudioFormat': Variable(
            'Set source\'s digital audio to HDMI\'s audio return channel (ARC)',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source1.DigitalAudioInput': Variable(
            'Set Digital Audio Input',
            range(1, 9),
        ),
        'Source1.Enabled': Variable(
            'Set Source Enabled No/Yes',
            {'No', 'Yes'},
        ),
        'Source1.Preset': Variable(
            'Set Source Preset',
            range(0, 6),
        ),
        'Source1.TriggerOut': Variable(
            'Set Source Trigger Out',
            range(0, 8),
        ),
        'Source1.VideoFormat': Variable(
            'Set Source Video Format',
            {'Component', 'Off', 'Video', 'HDMI', 'SVideo'},
        ),
        'Source1.VideoInput': Variable(
            'Set Source Video Input',
            range(1, 9),
        ),
        'Source10.AnalogAudioFormat': Variable(
            'Set Analog Audio Format',
            {'Stereo'},
        ),
        'Source10.AnalogAudioInput': Variable(
            'Set Analog Audio Format',
            range(9, 10),
        ),
        'Source10.AnalogGain': Variable(
            'Set Analog Audio Format',
            range(-12, 13, 3),
        ),
        'Source10.DigitalAudioInput': Variable(
            'Set Digital Audio Input',
            range(1, 9),
        ),
        'Source10.Enabled': Variable(
            'Set Enabled Yes',
            {'Yes'},
        ),
        'Source10.Preset': Variable(
            'Set Source Preset',
            range(0, 6),
        ),
        'Source10.TriggerOut': Variable(
            'Set Source Trigger Out',
            range(0, 8),
        ),
        'Source10.VideoFormat': Variable(
            'Set Video Format',
            {'Component', 'Off', 'Video', 'HDMI', 'SVideo'},
        ),
        'Source10.VideoInput': Variable(
            'Set Video Input',
            range(1, 9),
        ),
        'Source2.AnalogAudioFormat': Variable(
            'Set Analog Audio Format',
            {'7.1', 'Off', 'Stereo'},
        ),
        'Source2.AnalogAudioInput': Variable(
            'Set Analog Audio Input',
            range(1, 9),
        ),
        'Source2.AnalogGain': Variable(
            'Set Analog Audio Gain',
            range(-12, 13, 3),
        ),
        'Source2.DigitalAudioInput': Variable(
            'Set Digital Audio Input',
            range(1, 9),
        ),
        'Source2.Enabled': Variable(
            'Set Source Enabled No/Yes',
            {'No', 'Yes'},
        ),
        'Source2.Preset': Variable(
            'Set Source Preset',
            range(0, 6),
        ),
        'Source2.TriggerOut': Variable(
            'Set Source Trigger Out',
            range(0, 8),
        ),
        'Source2.VideoFormat': Variable(
            'Set Source Video Format',
            {'Component', 'Off', 'Video', 'HDMI', 'SVideo'},
        ),
        'Source2.VideoInput': Variable(
            'Set Source Video Input',
            range(1, 9),
        ),
        'Source3.AnalogAudioFormat': Variable(
            'Set Analog Audio Format',
            {'Off', '7.1', 'Stereo'},
        ),
        'Source3.AnalogAudioInput': Variable(
            'Set Analog Audio Input',
            range(1, 9),
        ),
        'Source3.AnalogGain': Variable(
            'Set Analog Audio Gain',
            range(-12, 13, 3),
        ),
        'Source3.DigitalAudioInput': Variable(
            'Set Digital Audio Input',
            range(1, 9),
        ),
        'Source3.Enabled': Variable(
            'Set Source Enabled No/Yes',
            {'No', 'Yes'},
        ),
        'Source3.Preset': Variable(
            'Set Source Preset',
            range(0, 6),
        ),
        'Source3.TriggerOut': Variable(
            'Set Source Trigger Out',
            range(0, 8),
        ),
        'Source3.VideoFormat': Variable(
            'Set Source Video Format',
            {'Component', 'Off', 'Video', 'HDMI', 'SVideo'},
        ),
        'Source3.VideoInput': Variable(
            'Set Source Video Input',
            range(1, 9),
        ),
        'Source4.AnalogAudioFormat': Variable(
            'Set Analog Audio Format',
            {'7.1', 'Off', 'Stereo'},
        ),
        'Source4.AnalogAudioInput': Variable(
            'Set Analog Audio Input',
            range(1, 9),
        ),
        'Source4.AnalogGain': Variable(
            'Set Analog Audio Gain',
            range(-12, 13, 3),
        ),
        'Source4.DigitalAudioInput': Variable(
            'Set Digital Audio Input',
            range(1, 9),
        ),
        'Source4.Enabled': Variable(
            'Set Source Enabled No/Yes',
            {'No', 'Yes'},
        ),
        'Source4.Preset': Variable(
            'Set Source Preset',
            range(0, 6),
        ),
        'Source4.TriggerOut': Variable(
            'Set Source Trigger Out',
            range(0, 8),
        ),
        'Source4.VideoFormat': Variable(
            'Set Source Video Format',
            {'Component', 'Off', 'Video', 'HDMI', 'SVideo'},
        ),
        'Source4.VideoInput': Variable(
            'Set Source Video Input',
            range(1, 9),
        ),
        'Source5.AnalogAudioFormat': Variable(
            'Set Analog Audio Format',
            {'Off', '7.1', 'Stereo'},
        ),
        'Source5.AnalogAudioInput': Variable(
            'Set Analog Audio Input',
            range(1, 9),
        ),
        'Source5.AnalogGain': Variable(
            'Set Analog Audio Gain',
            range(-12, 13, 3),
        ),
        'Source5.DigitalAudioFormat': Variable(
            'Set Digital Audio Format',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source5.DigitalAudioInput': Variable(
            'Set Digital Audio Input',
            range(1, 9),
        ),
        'Source5.Enabled': Variable(
            'Set Source Enabled No/Yes',
            {'No', 'Yes'},
        ),
        'Source5.Preset': Variable(
            'Set Source Preset',
            range(0, 6),
        ),
        'Source5.TriggerOut': Variable(
            'Set Source Trigger Out',
            range(0, 8),
        ),
        'Source5.VideoFormat': Variable(
            'Set Source Video Format',
            {'Component', 'Off', 'Video', 'HDMI', 'SVideo'},
        ),
        'Source5.VideoInput': Variable(
            'Set Source Video Input',
            range(1, 9),
        ),
        'Source6.AnalogAudioFormat': Variable(
            'Set Analog Audio Format',
            {'Off', '7.1', 'Stereo'},
        ),
        'Source6.AnalogAudioInput': Variable(
            'Set Analog Audio Input',
            range(1, 9),
        ),
        'Source6.AnalogGain': Variable(
            'Set Analog Audio Gain',
            range(-12, 13, 3),
        ),
        'Source6.DigitalAudioInput': Variable(
            'Set Digital Audio Input',
            range(1, 9),
        ),
        'Source6.Enabled': Variable(
            'Set Source Enabled No/Yes',
            {'No', 'Yes'},
        ),
        'Source6.Preset': Variable(
            'Set Source Preset',
            range(0, 6),
        ),
        'Source6.TriggerOut': Variable(
            'Set Source Trigger Out',
            range(0, 8),
        ),
        'Source6.VideoFormat': Variable(
            'Set Source Video Format',
            {'Component', 'Off', 'Video', 'HDMI', 'SVideo'},
        ),
        'Source6.VideoInput': Variable(
            'Set Source Video Input',
            range(1, 9),
        ),
        'Source7.AnalogAudioFormat': Variable(
            'Set Analog Audio Format',
            {'Off', '7.1', 'Stereo'},
        ),
        'Source7.AnalogAudioInput': Variable(
            'Set Analog Audio Input',
            range(1, 9),
        ),
        'Source7.AnalogGain': Variable(
            'Set Analog Audio Gain',
            range(-12, 13, 3),
        ),
        'Source7.DigitalAudioFormat': Variable(
            'Set source\'s digital audio to HDMI\'s audio return channel (ARC)',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source7.DigitalAudioInput': Variable(
            'Set Digital Audio Input',
            range(1, 9),
        ),
        'Source7.Enabled': Variable(
            'Set Source Enabled No/Yes',
            {'No', 'Yes'},
        ),
        'Source7.Preset': Variable(
            'Set Source Preset',
            range(0, 6),
        ),
        'Source7.TriggerOut': Variable(
            'Set Source Trigger Out',
            range(0, 8),
        ),
        'Source7.VideoFormat': Variable(
            'Set Source Video Format',
            {'Component', 'Off', 'Video', 'HDMI', 'SVideo'},
        ),
        'Source7.VideoInput': Variable(
            'Set Source Video Input',
            range(1, 9),
        ),
        'Source8.AnalogAudioFormat': Variable(
            'Set Analog Audio Format',
            {'Off', '7.1', 'Stereo'},
        ),
        'Source8.AnalogAudioInput': Variable(
            'Set Analog Audio Input',
            range(1, 9),
        ),
        'Source8.AnalogGain': Variable(
            'Set Analog Audio Gain',
            range(-12, 13, 3),
        ),
        'Source8.DigitalAudioFormat': Variable(
            'Set Digital Audio Format',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source8.DigitalAudioInput': Variable(
            'Set Digital Audio Input',
            range(1, 9),
        ),
        'Source8.Enabled': Variable(
            'Set Source Enabled No/Yes',
            {'No', 'Yes'},
        ),
        'Source8.Preset': Variable(
            'Set Source Preset',
            range(0, 6),
        ),
        'Source8.TriggerOut': Variable(
            'Set Source Trigger Out',
            range(0, 8),
        ),
        'Source8.VideoFormat': Variable(
            'Set Source Video Format',
            {'Component', 'Off', 'Video', 'HDMI', 'SVideo'},
        ),
        'Source8.VideoInput': Variable(
            'Set Source Video Input',
            range(1, 9),
        ),
        'Source9.AnalogAudioFormat': Variable(
            'Set Analog Audio Format',
            {'7.1', 'Off', 'Stereo'},
        ),
        'Source9.AnalogAudioInput': Variable(
            'Set Analog Audio Input',
            range(1, 9),
        ),
        'Source9.AnalogGain': Variable(
            'Set Analog Audio Gain',
            range(-12, 13, 3),
        ),
        'Source9.DigitalAudioFormat': Variable(
            'Set Digital Audio Format',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source9.DigitalAudioInput': Variable(
            'Set Digital Audio Input',
            range(1, 9),
        ),
        'Source9.Enabled': Variable(
            'Set Source Enabled No/Yes',
            {'No', 'Yes'},
        ),
        'Source9.Preset': Variable(
            'Set Source Preset',
            range(0, 6),
        ),
        'Source9.TriggerOut': Variable(
            'Set Source Trigger Out',
            range(0, 8),
        ),
        'Source9.VideoFormat': Variable(
            'Set Source Video Format',
            {'Component', 'Off', 'Video', 'HDMI', 'SVideo'},
        ),
        'Source9.VideoInput': Variable(
            'Set Source Video Input',
            range(1, 9),
        ),
        'Tuner.AM.Frequency': Variable(
            'AM Frequency String (ie. "680")',
            {'String'},
        ),
        'Tuner.AMStep': Variable(
            'Set Tuner AM Step Value',
            range(9, 11),
        ),
        'Tuner.Band': Variable(
            'Set Tuner Band',
            {'FM', 'DAB', 'AM', 'XM'},
        ),
        'Tuner.DAB.DLS': Variable(
            'DAB DLS Text',
            None,
            {'?'},
        ),
        'Tuner.DAB.Service': Variable(
            'DAB Service Name',
            None,
            {'?'},
        ),
        'Tuner.DigitalMode': Variable(
            'Set Digital Mode (C Version)',
            {'DAB', 'XM'},
        ),
        'Tuner.FM.Frequency': Variable(
            'FM Frequency String (ie. "102.1")',
            {'String'},
        ),
        'Tuner.FM.Mute': Variable(
            'Set Tuner FM Mute On/Off',
            {'Off', 'On'},
        ),
        'Tuner.FM.RDSName': Variable(
            'FM RDS Name',
            None,
            {'?'},
        ),
        'Tuner.FM.RDSText': Variable(
            'FM RDS Text',
            None,
            {'?'},
        ),
        'Tuner.Preset': Variable(
            'Set Tuner Preset',
            range(1, 41),
        ),
        'Tuner.XM.Channel': Variable(
            'XM Channel Number',
            range(0, 256),
        ),
        'Tuner.XM.ChannelName': Variable(
            'XM Channel Name',
            None,
            {'?'},
        ),
        'Tuner.XM.Name': Variable(
            'XM Song name',
            None,
            {'?'},
        ),
        'Tuner.XM.Title': Variable(
            'XM Song Title',
            None,
            {'?'},
        ),
        'UART.Version': Variable(
            'Query UART Version',
            None,
            {'?'},
        ),
        'Zone2.Mute': Variable(
            'Set Zone Mute',
            {'Off', 'On'},
        ),
        'Zone2.Power': Variable(
            'Set Zone Power',
            {'Off', 'On'},
        ),
        'Zone2.Source': Variable(
            'Set Zone Source',
            range(1, 12),
        ),
        'Zone2.Volume': Variable(
            'Set Zone Volume',
            range(-99, 20),
        ),
        'Zone2.VolumeControl': Variable(
            'Set Zone Volume Control Variable/Fixed',
            {'Fixed', 'Variable'},
        ),
        'Zone2.VolumeFixed': Variable(
            'Set Zone Fixed Volume Value',
            range(-95, 17),
        ),
        'Zone3.Mode': Variable(
            'Set Zone Mode Zone/Record',
            {'Record', 'Zone'},
        ),
        'Zone3.Mute': Variable(
            'Set Zone Mute',
            {'Off', 'On'},
        ),
        'Zone3.Power': Variable(
            'Set Zone Power',
            {'Off', 'On'},
        ),
        'Zone3.Source': Variable(
            'Set Zone Source',
            range(1, 12),
        ),
        'Zone3.Volume': Variable(
            'Set Zone Volume',
            range(-99, 20),
        ),
        'Zone3.VolumeControl': Variable(
            'Set Zone Volume Control Variable/Fixed',
            {'Fixed', 'Variable'},
        ),
        'Zone3.VolumeFixed': Variable(
            'Set Zone Fixed Volume',
            range(-95, 17),
        ),
        'Zone4.Mode': Variable(
            'Set Zone Mode Zone/Record',
            {'Record', 'Zone'},
        ),
        'Zone4.Mute': Variable(
            'Set Zone Mute',
            {'Off', 'On'},
        ),
        'Zone4.Power': Variable(
            'Set Zone Power',
            {'Off', 'On'},
        ),
        'Zone4.Source': Variable(
            'Set Zone Source',
            range(1, 12),
        ),
        'Zone4.Volume': Variable(
            'Set Zone Volume',
            range(-99, 20),
        ),
        'Zone4.VolumeControl': Variable(
            'Set Zone Volume Control Variable/Fixed',
            {'Fixed', 'Variable'},
        ),
        'Zone4.VolumeFixed': Variable(
            'Set Zone Fixed Volume',
            range(-95, 17),
        ),
    }

    _invalid_operator_base_error = (
        "The variable '{{0}}' cannot be {0}. To check if a variable can be {0}, check "
        "whether the '{1}' operator is present in .specification[{{0}}].operators. For "
        "this variable, valid operators are: {{1}}"
    )
    invalid_query_error = _invalid_operator_base.format('queried', '?')
    invalid_set_error = _invalid_operator_base.format('queried', '=')
    invalid_increment_error = _invalid_operator_base.format('queried', '+')
    invalid_decrement_error = _invalid_operator_base.format('queried', '-')


    def __init__(self, serial_device):
        self.serial = serial.Serial(
            serial_device,
            115200,
        )

    def com(self, command, expect_reply=True):
        self.serial.write('\x0d{}\x0d'.format(command).encode('ascii'))
        if not expect_reply:
            return

        reply = b''
        while len(reply) == 0 or reply[-1] != 0x0d:  # \n
            reply += self.serial.read(self.serial.inWaiting())
            time.sleep(0.01)

        return reply.decode('ascii').replace(command, '').strip()

    def get(self, name):
        if name not in self.specification:
            message = (
                "'{}' is not a valid prefix.variable name. Valid prefix.variable names "
                "are keys the dict stored in the 'specification' property"
            )
            raise ValueError(message.format(name))
        variable = self.specification[name]
        if '?' not in variable.operators:
            message = (
            )
            raise ValueError(message.format(name, variable.operators))

    def set(self, name value):
        pass

    def increment(self, name):
        pass

    def decrement(self, name):
        pass

    def __getattr__(self, name):
        print("__getattr__", name)

    def __setattr__(self, name, value):
        print("__getattr__", name)

    #@property
    #def power(self):
    #    return self.com("Main.Power?")

    #@power.setter
    #def power(self, value):
    #    self.com("Main.Power=" + value)

    #@property
    #def volume(self):
    #    return self.com("Main.Volume?")

    #@volume.setter
    #def volume(self, value):
    #    self.com("Main.Volume={}".format(value), False)

class T777(TBase):
    specification = TBase.secification.copy()
    specification.update({
        'Main.SpeakerA': Variable(
            'Set Speaker A On/Off',
            {'Off', 'On'},
        ),
        'Main.SpeakerB': Variable(
            'Set Speaker B On/Off',
            {'Off', 'On'},
        ),
        'Preset1.Setup.Display': Variable(
            'Set Preset to include Display settings',
            {'No', 'Yes'},
        ),
        'Preset1.Setup.ToneControls': Variable(
            'Set Preset to not include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.DSPOptions': Variable(
            'Set Preset to include DSP Options',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.ListeningMode': Variable(
            'Set Preset to not include Listening Mode Options',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.Speaker': Variable(
            'Set Preset to include Speaker Settings',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.ToneControls': Variable(
            'Set Preset to not include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.DSPOptions': Variable(
            'Set Preset to include DSP Options',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.ListeningMode': Variable(
            'Set Preset to not include Listening Mode Options',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.ToneControls': Variable(
            'Set Preset to not include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.Display': Variable(
            'Set Preset to include Display settings',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.Speaker': Variable(
            'Set Preset to include Speaker Settings',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.ToneControls': Variable(
            'Set Preset to not include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Source10.DigitalAudioFormat': Variable(
            'Set source\'s digital audio to HDMI\'s audio return channel (ARC)',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source2.DigitalAudioFormat': Variable(
            'Set source\'s digital audio to HDMI\'s audio return channel (ARC)',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source3.DigitalAudioFormat': Variable(
            'Set Digital Audio Format',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source4.DigitalAudioFormat': Variable(
            'Set Digital Audio Format',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source6.DigitalAudioFormat': Variable(
            'Set source\'s digital audio to HDMI\'s audio return channel (ARC)',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
    })


class T787(TBase):
    specification = TBase.secification.copy()
    specification.update({
        'Main.SpeakerA': Variable(
            'Set Speaker A On/Off',
            {'Off', 'On'},
        ),
        'Main.SpeakerB': Variable(
            'Set Speaker B On/Off',
            {'Off', 'On'},
        ),
        'Preset1.Setup.Display': Variable(
            'Set Preset to include Display settings',
            {'No', 'Yes'},
        ),
        'Preset1.Setup.ToneControls': Variable(
            'Set Preset to not include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.DSPOptions': Variable(
            'Set Preset to include DSP Options',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.ListeningMode': Variable(
            'Set Preset to not include Listening Mode Options',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.Speaker': Variable(
            'Set Preset to include Speaker Settings',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.ToneControls': Variable(
            'Set Preset to not include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.DSPOptions': Variable(
            'Set Preset to include DSP Options',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.ListeningMode': Variable(
            'Set Preset to not include Listening Mode Options',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.ToneControls': Variable(
            'Set Preset to not include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.Display': Variable(
            'Set Preset to include Display settings',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.Speaker': Variable(
            'Set Preset to include Speaker Settings',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.ToneControls': Variable(
            'Set Preset to not include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Source10.DigitalAudioFormat': Variable(
            'Set source\'s digital audio to HDMI\'s audio return channel (ARC)',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source2.DigitalAudioFormat': Variable(
            'Set source\'s digital audio to HDMI\'s audio return channel (ARC)',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source3.DigitalAudioFormat': Variable(
            'Set Digital Audio Format',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source4.DigitalAudioFormat': Variable(
            'Set Digital Audio Format',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source6.DigitalAudioFormat': Variable(
            'Set source\'s digital audio to HDMI\'s audio return channel (ARC)',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
    })


class T187(TBase):
    specification = TBase.secification.copy()
    specification.update({
        'Preset1.Setup.Display': Variable(
            'Set Preset to not include Display settings',
            {'No', 'Yes'},
        ),
        'Preset1.Setup.ToneControls': Variable(
            'Set Preset to include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.DSPOptions': Variable(
            'Set Preset to not include DSP Options',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.ListeningMode': Variable(
            'Set Preset to include Listening Mode Options',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.Speaker': Variable(
            'Set Preset to not include Speaker Settings',
            {'No', 'Yes'},
        ),
        'Preset2.Setup.ToneControls': Variable(
            'Set Preset to include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.DSPOptions': Variable(
            'Set Preset to not include DSP Options',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.ListeningMode': Variable(
            'Set Preset to include Listening Mode Options',
            {'No', 'Yes'},
        ),
        'Preset3.Setup.ToneControls': Variable(
            'Set Preset to include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.Display': Variable(
            'Set Preset to not include Display settings',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.Speaker': Variable(
            'Set Preset to not include Speaker Settings',
            {'No', 'Yes'},
        ),
        'Preset4.Setup.ToneControls': Variable(
            'Set Preset to include Tone Control Settings',
            {'No', 'Yes'},
        ),
        'Source10.DigitalAudioFormat': Variable(
            'Set Digital Audio Format',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source2.DigitalAudioFormat': Variable(
            'Set Digital Audio Format',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source3.DigitalAudioFormat': Variable(
            'Set source\'s digital audio to HDMI\'s audio return channel (ARC)',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source4.DigitalAudioFormat': Variable(
            'Set source\'s digital audio to HDMI\'s audio return channel (ARC)',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
        'Source6.DigitalAudioFormat': Variable(
            'Set Digital Audio Format',
            {'Coaxial', 'Off', 'HDMI', 'Optical', 'ARC'},
        ),
    })


t747 = TBase('/dev/ttyUSB0')
t747.volume
#t747.volume=-11
#print(t747.volume)


