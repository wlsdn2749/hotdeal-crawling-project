import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { detailItem } from '../api/Api';
import '../assets/Detail.css';

const Detail = () => {
    const location = useLocation();
    const { site, url } = location.state;
    const [item, setItem] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getItem = async () => {
            setLoading(true);
            try {
                const data = await detailItem(site, url);
                console.log('detail에서 가져온 item', data);
                setItem(data.item);
                setLoading(false);
            } catch (error) {
                setError(error);
                setLoading(false);
            }
        };

        getItem();
    }, [site, url]);

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    if (error) {
        return <div className="error">Error: {error.message}</div>;
    }

    return (
        <div className="detail-container">
            <div className="detail-header">
                <h1 className="detail-title">{item.title}</h1>
                <div className="detail-meta">
                    <span className="author">작성자: {item.author}</span>
                    <span className="date">
                        {item.date ? new Date(item.date).toLocaleDateString() : '날짜 없음'}
                    </span>
                </div>
            </div>
            <div className="detail-body">
                <div className="detail-info">
                    <span>조회수: {item.views}</span>
                    <span>좋아요: {item.likes}</span>
                    <span>댓글수: {item.comment_count}</span>
                </div>
                <table className="detail-table">
                    <tbody>
                        <tr>
                            <td>관련 URL</td>
                            <td><a href={item.related_url} target="_blank" rel="noopener noreferrer">{item.related_url}</a></td>
                        </tr>
                        <tr>
                            <td>쇼핑몰</td>
                            <td>{item.shoppingmall}</td>
                        </tr>
                        <tr>
                            <td>상품명</td>
                            <td>{item.product_name}</td>
                        </tr>
                        <tr>
                            <td>가격</td>
                            <td>{item.price}</td>
                        </tr>
                        <tr>
                            <td>배송</td>
                            <td>{item.deliveryfee}</td>
                        </tr>
                    </tbody>
                </table>
                <div className="detail-article">
                    {(item.article ?? '').split(',').map((paragraph, index) => (
                        <p key={index}>{paragraph}</p>
                    ))}
                </div>

                <div className="detail-comments">
                    <h2>댓글</h2>
                    {Array.isArray(item.comments) && item.comments.length > 0 ? (
                        item.comments.map((comment, index) => (
                            <div key={index} className="comment">
                                <div className="comment-meta">
                                    <span className="comment-author">{comment.author}</span>
                                    <span className="comment-date">{new Date(comment.date).toLocaleString()}</span>
                                </div>
                                <p className="comment-content">{comment.content}</p>
                            </div>
                        ))
                    ) : (
                        <p>댓글이 없습니다.</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Detail;
