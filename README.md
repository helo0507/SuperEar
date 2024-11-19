# SuperEar  
<--- **SuperEar** is a research project aimed at utilizing acoustic metamaterials to achieve eavesdropping and tracking of phone calls in outdoor environments.  

The project integrates gain balancing and noise suppression algorithms to optimize the raw audio captured by acoustic metamaterials, effectively addressing issues like uneven gain and noise interference.  

- **Distortion Suppression Algorithm**: Designed to reduce distortion in the original gain curve obtained by acoustic metamaterials. You can directly use the gain curve file provided in the project to implement this algorithm. The result will be a set of gain difference values across different frequencies, which can be multiplied by the spectrum of the original audio obtained using the equipment described in the paper.  
- **Noise Suppression Algorithm**: Aimed at minimizing the impact of environmental noise on audio reconstruction. You can use the sample audio files provided in the project or replace them with your own files to implement this algorithm.

For a detailed explanation of the algorithm, please refer to the paper: *"Stealthy Voice Eavesdropping with Acoustic Metamaterials: Unraveling a New Privacy Threat."*
 --->
