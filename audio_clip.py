import numpy as np
import librosa
from math import ceil
from tinytag import TinyTag



class AudioClip:
    def __init__(self, fp, frame_len=1024):
        self.fp = fp
        self.metadata = self.parse_comment(fp)
        self.clip, self.sr = librosa.load(fp, sr=None)

        # creates spectrogram
        stft_clip = librosa.stft(self.clip, n_fft=frame_len, hop_length=frame_len//2+1)
        stft_mag, stft_ph = librosa.magphase(stft_clip)
        self.spec = librosa.amplitude_to_db(stft_mag)
        self.spec = self.norm(self.spec)  # norm between 0 and 1
        self.spec = self.spec[np.where(np.sum(self.spec, axis=1) > 1)]
        self.spec = np.flipud(self.spec)  # flip so low sounds are on bottom

    @staticmethod
    def norm(spec):
        """
        spec - 2d numpy array - representation of clip in frequency domain
        return - 2d numpy array - same shape, normalized between 0 and 1
        """
        min_num = np.amin(spec)
        max_num = np.amax(spec)
        return np.divide(np.add(spec, -min_num), max_num-min_num)

    @staticmethod
    def parse_comment(fp):
        """
        Parses the comment provided in recordings by audio moth.
        fp - str - full file path
        returns - a dictionary of the provided information
        """
        comment = TinyTag.get(fp).comment
        split_up = comment.split(' ')
        time = split_up[2]
        date = split_up[3]
        timezone = split_up[4]
        am_id = split_up[7]
        gain_setting = split_up[11]
        battery_level = split_up[16]

        return {
            'time': time,
            'date': date,
            'timezone': timezone,
            'id': am_id,
            'gain': gain_setting,
            'battery': battery_level
        }

    def write_mini_clip(self, fp, start_spec, end_spec):
        """
        fp - string - the full filepath to save the clip
        start_ind - int - the desired starting place in spec
        end_ind - int - the desired stopping place in spec
        return - None
        """
        _, spec_w = self.spec.shape
        start = int(start_spec * len(self.clip) / spec_w)
        end   = int(end_spec   * len(self.clip) / spec_w)

        librosa.output.write_wav(fp, self.clip[start:end], self.sr)
