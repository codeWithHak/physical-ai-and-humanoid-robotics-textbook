import React, { useState } from 'react';
import styles from './styles.module.css';
import gpuData from './data.json';

export default function HardwareCheck() {
  const [selectedGpuName, setSelectedGpuName] = useState(gpuData[0].name);
  const [ram, setRam] = useState(32);

  const selectedGpu = gpuData.find(g => g.name === selectedGpuName) || gpuData[0];

  const getResult = () => {
    if (!selectedGpu.cuda) {
      return {
        status: 'red',
        message: "❌ Incompatible: NVIDIA RTX GPU with CUDA support is required for Isaac Sim."
      };
    }
    
    if (selectedGpu.vram < 12) {
      return {
        status: 'yellow',
        message: `⚠️ Caution: ${selectedGpu.vram}GB VRAM is borderline. You may experience crashes in complex simulations.`
      };
    }

    if (ram < 32) {
      return {
        status: 'yellow',
        message: "⚠️ Caution: 32GB System RAM is recommended for smooth operation."
      };
    }

    return {
      status: 'green',
      message: "✅ Ready for Isaac Sim: Your hardware meets the recommended specs."
    };
  };

  const result = getResult();

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Interactive Hardware Validator</h3>
      
      <div className={styles.formGroup}>
        <label className={styles.label}>Select your GPU:</label>
        <select 
          className={styles.select}
          value={selectedGpuName}
          onChange={(e) => setSelectedGpuName(e.target.value)}
        >
          {gpuData.map(g => (
            <option key={g.name} value={g.name}>{g.name} ({g.vram}GB VRAM)</option>
          ))}
        </select>
      </div>

      <div className={styles.formGroup}>
        <label className={styles.label}>System RAM (GB):</label>
        <input 
          type="number" 
          className={styles.input}
          value={ram}
          onChange={(e) => setRam(parseInt(e.target.value) || 0)}
        />
      </div>

      <div className={`${styles.result} ${styles[`result${result.status.charAt(0).toUpperCase() + result.status.slice(1)}`]}`}>
        {result.message}
      </div>
    </div>
  );
}
