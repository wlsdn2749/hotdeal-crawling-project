import '../assets/List.css'
import Item from './HotDealItem'

const List = () => {

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
                <Item />
                <Item />
                <Item />
                <Item />
            </div>
        </div>
    )
}

export default List;
