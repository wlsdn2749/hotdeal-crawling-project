// src/components/ItemDetail.jsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchItemById } from '../api/test';
import '../assets/ItemDetail.css';

const ItemDetail = () => {
    const { id } = useParams();
    const [item, setItem] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getItem = async () => {
            try {
                const data = await fetchItemById(id);
                setItem(data);
                setLoading(false);
            } catch (error) {
                setError(error);
                setLoading(false);
            }
        };

        getItem();
    }, [id]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <div className="ItemDetail">
            {item && (
                <div>
                    <h1>{item.title}</h1>
                    <p>쇼핑몰: {item.shoppingmall}</p>
                    <p>가격: {item.price}</p>
                    <p>배달비: {item.deliveryfee}</p>
                    <p>작성자: {item.author}</p>
                    <p>조회수: {item.views}</p>
                    <p>좋아요: {item.likes}</p>
                    <p>댓글수: {item.comment_count}</p>
                    <p>상품명: {item.product_name}</p>
                    <a href={item.related_url} target="_blank" rel="noopener noreferrer">관련 링크</a>
                    <div>
                        {item.article.map((paragraph, index) => (
                            <p key={index}>{paragraph}</p>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ItemDetail;
