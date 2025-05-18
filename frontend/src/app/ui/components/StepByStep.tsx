"use client";
import React from 'react';
import StepBlock from '@/app/ui/card/StepsCard'; 
import styled from 'styled-components';

const StepByStep = () => {
  return (
    <StepsContainer>
      <StepBlock
        stepNumber="1"
        title="Create an Account"
        description="Sign up and complete our simple verification process to get started."
      />
      <StepBlock
        stepNumber="2"
        title="Enter Amount & Recipient"
        description="Choose how much to send and enter your recipient's mobile money details."
      />
      <StepBlock
        stepNumber="3"
        title="Instant Delivery"
        description="Money is delivered to your recipient's mobile money account within seconds."
      />
    </StepsContainer>
  );
};

const StepsContainer = styled.div`
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 40px;
  padding: 40px 20px;
`;

export default StepByStep;
