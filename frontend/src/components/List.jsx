import React, { useEffect, useState } from 'react';
import Select from 'react-select';
import { fetchItems, fetchItemsByCategories, searchItems } from '../api/Api';
import '../assets/List.css';
import HotDealItem from './HotDealItem';
import ReactPaginate from 'react-paginate';
import { useNavigate, useLocation } from 'react-router-dom';

const categoryOptions = [
    { value: '먹거리', label: '먹거리' },
    { value: 'SW/게임', label: 'SW/게임' },
    { value: 'PC제품', label: 'PC제품' },
    { value: '가전제품', label: '가전제품' },
    { value: '생활용품', label: '생활용품' },
    { value: '의류', label: '의류' },
    { value: '세일정보', label: '세일정보' },
    { value: '화장품', label: '화장품' },
    { value: '모바일/상품권', label: '모바일/상품권' },
    { value: '패키지/이용권', label: '패키지/이용권' },
    { value: '기타', label: '기타' },
    { value: '해외핫딜', label: '해외핫딜' }
];

const orderOptions = [
    { value: 'desc', label: '최신순' },
    { value: 'asc', label: '오래된 순' }
];

const searchModeOptions = [
    { value: 'title', label: '제목' },
    { value: 'title_content', label: '제목+내용' }
];

const siteOptions = [
    { value: 'fm', label: '에펨코리아' },
    { value: 'qz', label: '퀘이사존' },
    { value: 'ruli', label: '루리웹' },
    { value: 'arca', label: '아카라이브' }
];

const List = () => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [pageCount, setPageCount] = useState(0);
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [selectedSites, setSelectedSites] = useState([]);
    const [order, setOrder] = useState(orderOptions[0]); // 기본 정렬을 최신순으로 설정
    const [searchQuery, setSearchQuery] = useState(''); // 검색어 상태 변수
    const [searchMode, setSearchMode] = useState(searchModeOptions[0]); // 검색 모드 상태 변수
    const itemsPerPage = 10;
    const navigate = useNavigate();
    const location = useLocation(); // 현재 URL의 쿼리 파라미터를 가져오기 위해 useLocation 사용

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const pageParam = params.get('page');
        const currentPage = pageParam ? Number(pageParam) : 1;
        setPage(currentPage);
    }, [location.search]);

    useEffect(() => {
        const getItems = async () => {
            setLoading(true);
            try {
                const result = await fetchItemsByCategories(page, itemsPerPage, selectedCategories.map(c => c.value), order.value, selectedSites.map(s => s.value));
                const { items, total } = result;
                console.log('서버에서 받아온 items', items);
                setItems(Array.isArray(items) ? items : []);
                setPageCount(Math.ceil(total / itemsPerPage));
                setLoading(false);
            } catch (error) {
                setError(error);
                setLoading(false);
            }
        };

        getItems();
    }, [page, itemsPerPage, selectedCategories, selectedSites, order]);

    const handlePageClick = (event) => {
        const selectedPage = event.selected + 1;
        navigate(`?page=${selectedPage}`);
    };

    const handleItemClick = (item) => {
        navigate(`/detail`, { state: { site: item.site, url: item.url } });
    };

    const handleCategoryChange = (selected) => {
        setSelectedCategories(selected);
        setPage(1); // 카테고리가 변경될 때 페이지를 1로 초기화
    };

    const handleSiteChange = (selected) => {
        setSelectedSites(selected);
        setPage(1); // 사이트가 변경될 때 페이지를 1로 초기화
    };

    const handleOrderChange = (selected) => {
        setOrder(selected);
        setPage(1); // 정렬 방식이 변경될 때 페이지를 1로 초기화
    };

    const handleSearchModeChange = (selected) => {
        setSearchMode(selected); // 검색 모드 변경 시 상태 업데이트
    };

    const handleSearchChange = (event) => {
        setSearchQuery(event.target.value); // 검색어 입력 시 상태 업데이트
    };

    const handleSearchSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            const result = await searchItems(1, itemsPerPage, searchQuery, searchMode.value, order.value);
            const { items, total } = result;
            console.log('서버에서 받아온 items', items);
            setItems(Array.isArray(items) ? items : []);
            setPageCount(Math.ceil(total / itemsPerPage));
            setPage(1); // 검색할 때 페이지를 1로 초기화
            setLoading(false);
        } catch (error) {
            setError(error);
            setLoading(false);
        }
    };

    return (
        <div className="List">
            <div className="search-container">
                <div className="dropdown-container">
                    <div className="react-select-container">
                        <Select
                            isMulti
                            options={categoryOptions}
                            value={selectedCategories}
                            onChange={handleCategoryChange}
                            placeholder="카테고리 분류"
                            closeMenuOnSelect={false}
                        />
                    </div>
                    <div className="react-select-container">
                        <Select
                            isMulti
                            options={siteOptions}
                            value={selectedSites}
                            onChange={handleSiteChange}
                            placeholder="사이트 분류"
                            closeMenuOnSelect={false}
                            className="site-dropdown"
                        />
                    </div>
                    <div className="react-select-container">
                        <Select
                            options={orderOptions}
                            value={order}
                            onChange={handleOrderChange}
                            placeholder="정렬 방식 선택"
                            closeMenuOnSelect={true}
                            className="order-dropdown"
                        />
                    </div>
                </div>

                <form className="d-flex" onSubmit={handleSearchSubmit}>
                    <div className="react-select-container search-mode-dropdown">
                        <Select
                            options={searchModeOptions}
                            value={searchMode}
                            onChange={handleSearchModeChange}
                            placeholder="검색 모드 선택"
                            closeMenuOnSelect={true}
                        />
                    </div>
                    <input className="form-control me-2" type="search" placeholder="Search" aria-label="Search" value={searchQuery} onChange={handleSearchChange} /> {/* 검색어 입력 */}
                    <button className="btn btn-outline-success" type="submit">검색</button> {/* 검색 버튼 */}
                </form>
            </div>

            {loading ? (
                <div>Loading...</div>
            ) : error ? (
                <div>Error: {error.message}</div>
            ) : (
                <div className="wrapper">
                    {items.map((item, index) => (
                        <HotDealItem key={index} item={item} onClick={() => handleItemClick(item)} />
                    ))}
                </div>
            )}

            {pageCount > 0 && ( // pageCount가 0보다 클 때만 ReactPaginate를 렌더링
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
                    forcePage={page - 1} // 현재 페이지를 반영하기 위해 forcePage 사용
                />
            )}
        </div>
    );
};

export default List;
