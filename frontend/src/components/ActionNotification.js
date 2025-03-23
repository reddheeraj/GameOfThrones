import React, { useState, useEffect } from 'react';
import './ActionNotification.css';

function ActionNotification({ actionQueue, setActionQueue }) {
  const [currentAction, setCurrentAction] = useState(null);

  useEffect(() => {
    if (actionQueue.length > 0) {
      setCurrentAction(actionQueue[0]);
      const timeout = setTimeout(() => {
        setActionQueue((prevQueue) => prevQueue.slice(1));
      }, 3000); // Display for 3 seconds

      return () => clearTimeout(timeout);
    }
  }, [actionQueue, setActionQueue]);

  return (
    <div className="action-notification-container">
      {currentAction && (
        <div className="action-notification">
          {currentAction}
        </div>
      )}
    </div>
  );
}

export default ActionNotification;
