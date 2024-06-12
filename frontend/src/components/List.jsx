import React, { useEffect, useState } from 'react';
import { fetchItems } from '../api/test';
import '../assets/List.css';
import HotDealItem from './HotDealItem';

const List = () => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getItems = async () => {
            try {
                const data = await fetchItems();
                console.log('가져온 data', data);
                setItems(data);
                setLoading(false);
            } catch (error) {
                setError(error);
                setLoading(false);
            }
        };

        getItems();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <div className="List">
            <div className="search-container">
                <div className="dropdown">
                    <button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                        카테고리
                    </button>
                    <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                        <li><a className="dropdown-item" href="#">Action</a></li>
                        <li><a className="dropdown-item" href="#">Another action</a></li>
                        <li><a className="dropdown-item" href="#">Something else here</a></li>
                    </ul>
                </div>

                <form className="d-flex">
                    <input className="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
                    <button className="btn btn-outline-success" type="submit">검색</button>
                </form>
            </div>

            <div className="wrapper">
                {items.map((item, index) => (
                    <HotDealItem key={index} item={item} />
                ))}
            </div>
        </div>
    );
};

export default List;
