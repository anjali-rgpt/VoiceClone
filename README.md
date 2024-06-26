# Experiments and Insights

The Misalignment Museum in San Francisco has an exhibit that consists of a clown doll speaking back to visitors in a clone of their voice, demonstrating the ease of voice cloning. This exhibit sometimes fails due to noisy background environments. Additionally, the exhibit relies on an external API, potentially storing recordings of children's voices externally. By experimenting with various methods for noise reduction, we propose a new pipeline that will do voice cloning locally on a Macbook with better performance in noisy environments and at lower cost to the museum. We accomplish this by processing the incoming sound files using DeepFilterNet, then converting a pre-trained model to sound like the target voice using OpenVoice.

We used the Microsoft Scalable Noisy Dataset to test our simulated noisy experiments. This dataset comes with code to combine the noiseless speech files with the noise files. Using this code, we generated 1 hour of speech for two different speakers. All audio results can be found on our Google Drive: [https://drive.google.com/drive/folders/1fDdinPMP_5aKNUxtee1GWOhwuK5hxCl6?usp=sharing](https://drive.google.com/drive/folders/1fDdinPMP_5aKNUxtee1GWOhwuK5hxCl6?usp=sharing).

We used each speaker to test our pipeline in a simulated environment. The [audio input](https://drive.google.com/file/d/17tHm1xgFtgyYCO3VnV9B3KLTxZ_H0pmO/view?usp=drive_link) we begin with consists of this speech overlayed with [airport announcements noise](https://drive.google.com/file/d/10WZMsEWiAtNh_856eS0Cxq77TZ3GFiaz/view?usp=drive_link). With this noisy input, we used OpenVoice to generate a [simple output, which sounded very staticky and unclear](https://drive.google.com/file/d/1U0JwHBYpHjEOC0w8nvbLuC-1mmN8p0yx/view?usp=drive_link). We also generated a [longer output, a sentence with a lot of emotion](https://drive.google.com/file/d/1xm6xIvttjhauytsulQr5ZwTgBomH-Fz7/view?usp=drive_link) so that we could test the emotion conveyed in the voice clone.

To improve on this baseline, we first began by using spectral gating to remove background noise from the sample. This resulted in a ["cleaned" input](https://drive.google.com/file/d/1RtT4AOyMT8-CWMblJzXYCC__0zn5fQYc/view?usp=drive_link) that sounded almost identical to the baseline. The [generated voice clone](https://drive.google.com/file/d/16cuSyey-8ZFAL9yiDOySS9WJ8RqTjcFm/view?usp=drive_link) also sounded almost identical to the baseline.

We then used DeepFilterNet to remove background noise. This resulted in an [input audio file that sounded like no noise had ever been added](https://drive.google.com/file/d/1cOsVKwSDjko4OWk5yqL8xg-kjQbZ0f6N/view?usp=drive_link). The [generated voice clone](https://drive.google.com/file/d/15sbAg5rqZ66Mkyg8rKtfRdGYHbR0q4FR/view?usp=drive_link) was a remarkable improvement over the baseline. 

We also completed this same process for a female speaker. The [original noisy file](https://drive.google.com/file/d/1-BfSwHDuA-SrYyuZDkR_kJN74bkmFOgE/view?usp=drive_link) used a [different background noise](https://drive.google.com/file/d/1r1iBpSyUVXWPXRZMmPou9hAMnQjTbhyF/view?usp=drive_link) that we thought obfuscated the speaker's voice the most. Again, the [baseline voice clone](https://drive.google.com/file/d/1HkRAQYGV2jO3ionSYZWdnJe0EOH1IvHx/view?usp=drive_link) was very staticky.

After applying spectral gating, the ["cleaned input"](https://drive.google.com/file/d/1iX2jnD6jYCqW-8fh9c04HBk8adoOkvy9/view?usp=drive_link) sounded much the same and produced a very similar sounding [clone](https://drive.google.com/file/d/1YnrRboCzpgZHeG_nlPZW3T-mFQ_08jYl/view?usp=drive_link).

Applying DeepFilterNet produced a [very clean input audio](https://drive.google.com/file/d/1b7toWtdP9nsZqvIdk2mX_ySE4H0ZW5Ov/view?usp=drive_link) with great results on the [voice clone](https://drive.google.com/file/d/1ZMHOXsJNHjYm0dpT-wtWby_x5Ddvw4VD/view?usp=drive_link).

Having completed our experiments to determine the appropriate interventions, we compiled these steps into a pipeline to be used in the exhibit, adapting the existing exhibit's pipeline.
We provide here an example of the pipeline as applied to the poem used in the exhibit (you can find the poem in the main.py file, at the beginning). If we imagine that the exhibit takes place in a noisy room with many conversations, [the poem will be read with lots of background noise](https://drive.google.com/file/d/1NB8Y6c91cwBB1bi-VVjmEuq1P_a0INdY/view?usp=drive_link). This recording starts slightly after the start of the poem because Google speech recognizer listened for the start of the poem to start recording. The recorded audio is then passed into DeepFilterNet, resulting in a [cleaned input](https://drive.google.com/file/d/13RHZSijp-Daj-MeeV3WxvIGC9jlPMjWk/view?usp=drive_link) for the voice clone. This then goes through OpenVoice to be transformed into a [voice clone reading out the script urging visitors to donate to the museum](https://drive.google.com/file/d/1uf3jQE9DK9_2Y3uGaAQmW40hmICg7gY5/view?usp=drive_link).

Here are two more examples of the voice clone being tested in a [quiet](https://drive.google.com/file/d/1jV75rPpf_mKAKToszsQ4Kvm5w5JcEzF6/view?usp=sharing) and a [synthetically noisy](https://drive.google.com/file/d/1WNBuxi0RkJ6UOEoiw6yWXK_sRuz8sEFg/view?usp=sharing) environment. 

# Where to find everything
The main code is run simply by the command python3 main.py
The [main.py](main.py) file contains the entire pipeline to run the code, from continuous input streaming to noise reduction, voice cloning, and playback. 
The [openvoicemain.py](openvoicemain.py) file contains the class to run the OpenVoice voice clone and associated functionality.
The [deepfilternet.py](deepfilternet.py) file contains the class to run the DeepFilterNet module.
The [audio_sample](audio_samples/) folder contains audio files for the simulated experiments, in this case, for the male speaker, including the original sample with noise, the baseline OpenVoice output, the outputs of spectral gating, DeepFilterNet, and the resulting voice clones.
The [MuseumBaselineCode](MuseumBaselineCode/) folder contains the original code we received from the museum to work with and test. 


Troubleshooting and setup can be found in [setup_info.md](setup_info.md)





