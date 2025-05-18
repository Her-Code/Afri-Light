"use client";
import React from 'react';
import styled from 'styled-components';

const Card = ({ title, description, icon }) => {
  return (
    <StyledWrapper>
      <div className="card">
        <div className="icon-wrapper">
          {icon}
        </div>
        <div className="content">
          <h3>{title}</h3>
          <p>{description}</p>
        </div>
      </div>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  .card {
    width: 400px;
    height: 200px;
    background: rgba(217, 217, 217, 0.58);
    border: 1px solid white;
    box-shadow: 12px 17px 51px rgba(0, 0, 0, 0.22);
    backdrop-filter: blur(6px);
    border-radius: 17px;
    text-align: center;
    cursor: pointer;
    transition: all 0.5s;
    display: flex;
    align-items: center;
    justify-content: center;
    user-select: none;
    color: black;
    padding: 20px;
  }

  .icon-wrapper {
    width: 64px;
    height: 64px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .content {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .card h3 {
    font-size: 20px;
    font-weight: bold;
    margin: 0;
  }

  .card p {
    font-size: 16px;
    line-height: 1.4;
  }

  .card:hover {
    border: 1px solid black;
    transform: scale(1.05);
  }

  .card:active {
    transform: scale(0.95) rotateZ(1.7deg);
  }
`;

export default Card;
