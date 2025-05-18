"use client";
import React from 'react';
import styled from 'styled-components';

const Steps = ({ stepNumber, title, description }) => {
  return (
    <StyledStep>
      <div className="step-circle">{stepNumber}</div>
      <div className="text">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </StyledStep>
  );
};

const StyledStep = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 260px;
  gap: 16px;

  .step-circle {
    width: 48px;
    height: 48px;
    background-color: #007bff;
    color: white;
    border-radius: 50%;
    font-size: 20px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .text {
    text-align: center;
  }

  .text h3 {
    font-size: 18px;
    margin-bottom: 8px;
  }

  .text p {
    font-size: 15px;
    color: #444;
    margin: 0;
  }
`;

export default Steps;
