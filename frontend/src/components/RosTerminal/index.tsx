import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

const SUPPORTED_COMMANDS = {
  'ros2 node list': {
    output: '/camera\n/perception\n/planner\n/controller',
  },
  'ros2 topic list': {
    output: '/camera/image_raw\n/odometry\n/cmd_vel\n/scan',
  },
  'ros2 node info /planner': {
    output: 'Node: /planner\nSubscribers:\n  /scan: sensor_msgs/msg/LaserScan\n  /odometry: nav_msgs/msg/Odometry\nPublishers:\n  /cmd_vel: geometry_msgs/msg/Twist',
  },
  'help': {
    output: 'Supported commands: ros2 node list, ros2 topic list, ros2 node info /planner',
  }
};

export default function RosTerminal() {
  const [history, setHistory] = useState([]);
  const [input, setInput] = useState('');
  const inputRef = useRef(null);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') {
      const command = input.trim();
      const newHistory = [...history, { type: 'input', content: command }];
      
      if (SUPPORTED_COMMANDS[command]) {
        newHistory.push({ type: 'output', content: SUPPORTED_COMMANDS[command].output });
      } else {
        newHistory.push({ type: 'output', content: `Command not found: ${command}. Type 'help' for a list of supported commands.` });
      }
      
      setHistory(newHistory);
      setInput('');
    }
  };

  const handleAutoType = (command) => {
    setInput(command);
    inputRef.current.focus();
  };
  
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  return (
    <div className={styles.rosTerminal}>
      <div className={styles.history}>
        {history.map((item, index) => (
          <div key={index} className={styles[item.type]}>
            {item.type === 'input' && <span className={styles.prompt}>$</span>}
            <pre>{item.content}</pre>
          </div>
        ))}
      </div>
      <div className={styles.inputContainer}>
        <span className={styles.prompt}>$</span>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleInputKeyDown}
          className={styles.input}
          placeholder="Type a command and press Enter"
        />
      </div>
      <div className={styles.autoTypeContainer}>
        {Object.keys(SUPPORTED_COMMANDS).map((command) => (
          <button
            key={command}
            className={styles.autoTypeButton}
            onClick={() => handleAutoType(command)}
          >
            {command}
          </button>
        ))}
      </div>
    </div>
  );
}
