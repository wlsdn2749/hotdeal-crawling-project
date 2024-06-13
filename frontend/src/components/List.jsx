import React, { useEffect, useState } from 'react';
import { fetchItems } from '../api/Api';
import '../assets/List.css';
import HotDealItem from './HotDealItem';
import ReactPaginate from 'react-paginate';
import { useNavigate } from 'react-router-dom';

const List = () => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [pageCount, setPageCount] = useState(0);
    const itemsPerPage = 10;
    const navigate = useNavigate();

    useEffect(() => {
        const getItems = async () => {
            setLoading(true);
            try {
                console.log('서버로 보내는 page 번호', page);
                const { items, total } = await fetchItems(page, itemsPerPage);
                console.log('가져온 data', items);
                setItems(Array.isArray(items) ? items : []);
                setPageCount(Math.ceil(total / itemsPerPage));
                setLoading(false);
            } catch (error) {
                setError(error);
                setLoading(false);
            }
        };

        getItems();
    }, [page, itemsPerPage]);

    const handlePageClick = (event) => {
        const selectedPage = event.selected + 1;
        setPage(selectedPage);
        console.log('버튼을 눌렀을 때 event', selectedPage);
    };

    const handleItemClick = (item) => {
        navigate(`/detail`, { state: { site: item.site, url: item.url } });
    };

    if (loading) {
        return (
            <div>
                Loading...
                <ReactPaginate
                    previousLabel={'«'}
                    nextLabel={'»'}
                    breakLabel={'...'}
                    breakClassName={'break-me'}
                    pageCount={pageCount}
                    marginPagesDisplayed={2}
                    pageRangeDisplayed={5}
                    onPageChange={handlePageClick}
                    containerClassName={'pagination'}
                    subContainerClassName={'pages pagination'}
                    activeClassName={'active'}
                    previousClassName={'page-item'}
                    nextClassName={'page-item'}
                    pageClassName={'page-item'}
                    previousLinkClassName={'page-link'}
                    nextLinkClassName={'page-link'}
                    pageLinkClassName={'page-link'}
                    breakLinkClassName={'page-link'}
                    activeLinkClassName={'active'}
                    disabledClassName={'disabled'}
                />
            </div>
        );
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
                    <HotDealItem key={index} item={item} onClick={() => handleItemClick(item)} />
                ))}
            </div>

            <ReactPaginate
                previousLabel={'«'}
                nextLabel={'»'}
                breakLabel={'...'}
                breakClassName={'break-me'}
                pageCount={pageCount}
                marginPagesDisplayed={2}
                pageRangeDisplayed={5}
                onPageChange={handlePageClick}
                containerClassName={'pagination'}
                subContainerClassName={'pages pagination'}
                activeClassName={'active'}
                previousClassName={'page-item'}
                nextClassName={'page-item'}
                pageClassName={'page-item'}
                previousLinkClassName={'page-link'}
                nextLinkClassName={'page-link'}
                pageLinkClassName={'page-link'}
                breakLinkClassName={'page-link'}
                activeLinkClassName={'active'}
                disabledClassName={'disabled'}
            />
        </div>
    );
};

export default List;