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

                // const { item } = await detailItem(site, url);
                // console.log('detail에서 가져온 item', item);
                const item = {
                    "title": "[G마켓] 2개XCGN 실리마린 컴플렉스 1년분 300mg 360베지캡슐(삼카) (49,060원) (무료)",
                    "date": "2024.06.11 13:11",
                    "author": "코코쟈니",
                    "views": "9102",
                    "likes": "14",
                    "comment_count": "21",
                    "related_url": "https://item.gmarket.co.kr/Item?goodscode=2904552108",
                    "shoppingmall": "G마켓",
                    "product_name": "2개XCGN 실리마린 컴플렉스 1년분 300mg 360베지캡슐(삼카)",
                    "price": "49,060원",
                    "deliveryfee": "무료",
                    "article": [
                        "유클쿠폰+20%쿠폰+삼카할인까지하면 49,060원으로 1통당 24,530원 (삼카없을경우는 25,030원)",
                        "저번에 올라온거보다 싸길래 올림",
                        "요즘은 종비+오메가에 거의 필수적으로 같이 먹는 영양제중에 하나인듯",
                        "이거는 간세포 보호하고 재생하는데에 도움주기때문에 자기전에 복용하는게 좋다고 본거같네"
                    ],
                    "comments": "코멘트"
                }

                setItem(item);
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
                    <span className="date">{item.date}</span>
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
                    {item.article.map((paragraph, index) => (
                        <p key={index}>{paragraph}</p>
                    ))}
                </div>
                <div className="detail-comments">
                    <h2>댓글</h2>
                    <p>{item.comments}</p>
                </div>
            </div>
        </div>
    );
};

export default Detail;
