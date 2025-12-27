import React from 'react';
import ChatWidget from '../ChatWidget/ChatWidget';

const LayoutWrapper = ({ children }) => {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
};

export default LayoutWrapper;