import '../assets/HotDealItem.css'
const HotDealItem = () => {
    return (
        <div className="HotDealItem">
            <div>쇼핑몰</div>
            <div className='title'>제목</div>
            <div className='price'>
                <div>가격</div>
                <div className='delivery'>배달비</div>
            </div>
        </div>
    )
}

export default HotDealItem;