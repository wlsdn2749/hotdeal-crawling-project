// src/components/HotDealItem.jsx
import React from 'react';
import '../assets/HotDealItem.css';

const HotDealItem = ({ item, onClick }) => {
    return (
        <div className="HotDealItem" onClick={onClick}>
            <div>[{item.shoppingmall}]</div>
            <div className='title'>{item.title}</div>
            <div className='price'>
                <div>{item.price}</div>
                <div className='delivery'>배달비 : {item.deliveryfee}</div>
            </div>
        </div>
    );
};

export default HotDealItem;
