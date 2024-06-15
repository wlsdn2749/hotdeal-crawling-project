// src/components/HotDealItem.jsx
import React from 'react';
import '../assets/HotDealItem.css';

const HotDealItem = ({ item, onClick }) => {
    return (
        <div className="HotDealItem" onClick={onClick}>
            <div className="info">
                <div className="shoppingmall">[{item.shoppingmall}]</div>
                <div className='title'>{item.title}</div>
                <div className='details'>
                    <div>작성자: {item.author}</div>
                    <div>카테고리: {item.category}</div>
                    <div>추천수: {item.recommend}</div>
                    <div>댓글수: {item.comment}</div>
                    <div>사이트: {item.site}</div>
                    <div>등록일: {new Date(item.time).toLocaleDateString()}</div>
                </div>
            </div>
            <div className='price'>
                <div>{item.price}</div>
                <div className='delivery'>배달비 : {item.deliveryfee}</div>
            </div>
        </div>
    );
};

export default HotDealItem;
