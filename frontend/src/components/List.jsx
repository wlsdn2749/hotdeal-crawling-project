import React, { useEffect, useState } from 'react';
import Select from 'react-select';
import { fetchItemsByCategories, searchItems } from '../api/Api';
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

const itemsPerPageOptions = [
    { value: 10, label: '10개씩 보기' },
    { value: 20, label: '20개씩 보기' },
    { value: 30, label: '30개씩 보기' },
    { value: 40, label: '40개씩 보기' },
    { value: 50, label: '50개씩 보기' }
];

const List = () => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(() => {
        const params = new URLSearchParams(window.location.search);
        const pageParam = params.get('page');
        const currentPage = pageParam ? Number(pageParam) : 1;
        return currentPage;
    });
    const [pageCount, setPageCount] = useState(0);
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [selectedSites, setSelectedSites] = useState([]);
    const [order, setOrder] = useState(orderOptions[0]); // 기본 정렬을 최신순으로 설정
    const [searchQuery, setSearchQuery] = useState(''); // 검색어 상태 변수
    const [searchMode, setSearchMode] = useState(searchModeOptions[1]); // 검색 모드 상태 변수
    const [itemsPerPage, setItemsPerPage] = useState(() => {
        // localStorage에서 itemsPerPage 값을 불러오거나 기본값으로 10을 사용
        const saved = localStorage.getItem('itemsPerPage');
        return saved ? parseInt(saved, 10) : itemsPerPageOptions[0].value;
    });
    const navigate = useNavigate();
    const location = useLocation(); // 현재 URL의 쿼리 파라미터를 가져오기 위해 useLocation 사용

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const pageParam = params.get('page');
        const currentPage = pageParam ? Number(pageParam) : 1;
        if (page !== currentPage) {
            setPage(currentPage);
        }

    }, [location.search]);

    useEffect(() => {
        const getItems = async () => {
            setLoading(true);
            try {
                const result = await fetchItemsByCategories(
                    page,
                    itemsPerPage,
                    selectedCategories.map(c => c.value),
                    order.value,
                    selectedSites.map(s => s.value)
                );
                const { items, total } = result;
                console.log('서버에서 받아온 items', items);
                setItems(Array.isArray(items) ? items : []);
                setPageCount(Math.ceil(total / itemsPerPage));
                setError(null); // 에러 초기화
            } catch (error) {
                setError(error);
            } finally {
                setLoading(false);
            }
        };

        getItems();
        // 의존성 배열에 필요한 값들만 포함
    }, [page, itemsPerPage, selectedCategories, order, selectedSites]);

    useEffect(() => {
        // itemsPerPage 값이 변경될 때 localStorage에 저장
        localStorage.setItem('itemsPerPage', itemsPerPage);
    }, [itemsPerPage]);

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

    const handleItemsPerPageChange = (selected) => {
        setItemsPerPage(selected.value);
        setPage(1); // 페이지를 1로 초기화
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
            setError(null); // 에러 초기화
            setLoading(false);
        } catch (error) {
            if (error.response && error.response.status === 400) {
                setItems([]); // items를 빈 배열로 설정
                setPageCount(0); // 페이지 수를 0으로 설정
                setError({ message: '일치하는 항목이 없습니다.' });
            } else {
                setError(error);
            }
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
                    <div className="react-select-container">
                        <Select
                            options={itemsPerPageOptions}
                            value={itemsPerPageOptions.find(option => option.value === itemsPerPage)}
                            onChange={handleItemsPerPageChange}
                            placeholder="항목 개수 선택"
                            closeMenuOnSelect={true}
                            className="items-per-page-dropdown"
                        />
                    </div>
                </div>
            </div>

            {loading ? (
                <div>Loading...</div>
            ) : error && error.message === '일치하는 항목이 없습니다.' ? (
                <div className="no-matches">{error.message}</div>
            ) : error ? (
                <div>Error: {error.message}</div>


            ) : (
                <div className="wrapper">
                    {items.map((item, index) => (
                        <HotDealItem key={index} item={item} onClick={() => handleItemClick(item)} />
                    ))}
                </div>
            )}

            {pageCount > 0 && !error && ( // pageCount가 0보다 크고 에러가 없을 때만 ReactPaginate를 렌더링
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

            <div className='searchForm'>
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

        </div>
    );
};

export default List;
