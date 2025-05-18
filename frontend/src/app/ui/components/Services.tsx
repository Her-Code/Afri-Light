"use client";
import React from 'react';
import Card from '@/app/ui/card/ServiceCard'; 
import styled from 'styled-components';
import { CircleDollarSign, Zap,Smartphone } from 'lucide-react';

const Services = () => {
  return (
    <ServicesWrapper>
      <Card
        icon={
          <IconBox style={{ backgroundColor: '#e0f0ff' }}>
            <Zap color="#007bff" size={32} />
          </IconBox>
        }
        title="Instant Transfers"
        description="Send money that arrives in seconds, not days. Lightning-fast transactions, 24/7."
      />
      <Card
        icon={
          <IconBox style={{ backgroundColor: '#e6ffea' }}>
            <CircleDollarSign color="#28a745" size={32} />
          </IconBox>
        }
        title="Low Fees"
        description="Save up to 80% on remittance fees compared to traditional services."
      />
      <Card
        icon={
          <IconBox style={{ backgroundColor: '#ffe9d6' }}>
            <Smartphone color="#cc7722" size={32} />
          </IconBox>
        }

        title="Mobile Money Integration"
        description="Recipients can cash out directly to popular mobile money services across Africa."
      />
    </ServicesWrapper>
  );
};

const ServicesWrapper = styled.div`
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
`;
const IconBox = styled.div`
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
`;


export default Services;
