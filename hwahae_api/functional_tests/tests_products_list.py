"""
# 피부 타입마다 성분 기반으로 화장품을 추천해주는 서비스
# RESTful API 기능 테스트

# 상품 목록 조회하기
피부 타입 별로 상품 목록을 필터링해 조회하는 기능

"""

# 주어진 피부 타입에 따라 성분 점수를 계산해서 높은 상품 순으로 조회
# /products?skin_type=oily
# /products?skin_type=dry
# /products?skin_type=sensitive

# 점수가 동일하면 낮은 가격의 상품 표시

# 50개 단위로 페이징
# /products?skin_type=oily&page=3

# 상품 카테고리 선택
# /products?skin_type=oily&page=1&category=skincare
# /products?skin_type=oily&page=1&category=maskpack
# skincare maskpack suncare basemakeup

# 제외 성분 선택
# exclude_ingredient

# 포함 성분 선택
# include_ingredient

# 제외 성분 > 포함 성분 : 둘다 쿼리에 포함되었을 때 제외 성분을 우선으로 출력
