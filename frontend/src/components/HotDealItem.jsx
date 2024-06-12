// src/HotDealItem.jsx
import React from 'react';
import '../assets/HotDealItem.css';

const HotDealItem = ({ item }) => {
    return (
        <div className="HotDealItem">
            <div>{item.shoppingmall}</div>
            <div className='title'>{item.title}</div>
            <div className='price'>
                <div>{item.price}</div>
                <div className='delivery'>{item.deliveryfee}</div>
            </div>
        </div>
    );
};

export default HotDealItem;
