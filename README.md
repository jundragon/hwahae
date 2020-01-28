# programmers 과제

```
피부 타입마다 성분 기반으로 화장품을 추천해 주는 서비스의 API 구현
```

## Swagger

```
swagger/
docs/
```

## Response Status Code

| Status Code               | Description                            |
| ------------------------- | -------------------------------------- |
| 200 OK                    | 성공                                   |
| 400 Bad Request           | 클라이언트 요청 오류, 형식이 맞지 않음 |
| 404 NotFound              | 페이지를 찾을 수 없음                  |
| 500 Internal Server Error | 서버에 문제가 있음                     |

## Reference

### 1. BASE URL

https://young-scrubland-14937.herokuapp.com/

> 엔드포인트에 Query Parameter

### 2. 상품 목록 조회 하기

#### 기능 상세

- 주어진 피부 타입에 대한 성분 점수를 계산해서 높은 상품 순으로 보여집니다. 점수가 같다면 낮은 가격의 상품을 먼저 표시합니다.
- 상품 목록을 50개 단위로 페이징 합니다. 인자로 페이지 번호가 주어지면, 해당되는 상품 목록이 보여집니다.
- 상품 카테고리를 선택할 수 있습니다.
- 제외해야 하는 성분들을 지정할 수 있습니다.
  - exclude_ingredient 인자로 전달한 성분들을 모두 가지지 않는 상품들만 목록에 포함합니다.
- 포함해야 하는 성분들을 지정할 수 있습니다.
  - include_ingredient 인자로 전달한 성분들을 모두 가지고 있는 상품들만 목록에 포함합니다.

#### URL

`/products`

#### Method

`GET`

#### Request Header 구조 예시

```
GET /products?skin_type=dry
Content-Type: application/json
```

#### Query Parameter

| Parameter          | Type                        | Description                                           |
| ------------------ | --------------------------- | ----------------------------------------------------- |
| skin_type          | String                      | (필수) 지성(oily)/건성(dry)/민감성(sensitive) 중 택 1 |
| category           | String (선택) 상품 카테고리 |
| page               | Integer                     | (선택) 페이지 번호                                    |
| exclude_ingredient | String                      | (선택) 제외해야 하는 성분 목록(콤마로 구분)           |
| include_ingredient | String                      | (선택) 포함해야 하는 성분 목록(콤마로 구분)           |

#### Sample Call

```
/products?skin_type=oily&category=skincare&page=3&include_ingredient=Glycerin
```

#### Success Response

```
[
  {
    "id": 17,
    "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
    "name": "화해 에센스 토너",
    "price": 23000,
    "ingredients": "Glycerin,Methyl Gluceth-20,Pulsatilla Koreana Extract,Purified Water",
    "monthlySales": 1682
  },
  {
    "id": 23,
    "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
    "name": "화해 엔젤 토너",
    "price": 4800,
    "ingredients": "Glycerin,Sodium Hyaluronate,Xanthan Gum,Niacinamide,Orchid Extract",
    "monthlySales": 463
  },

  ...


  {
    "id": 88,
    "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
    "name": "화해 화이트 브라이트닝 소프너 인리치드",
    "price": 24000,
    "ingredients": "Glycerin,Alcohol,Purified Water,Vinyl Dimethicone,PEG-10 Dimethicone",
    "monthlySales": 4437
  }

]
```

#### Response Body 구성

| Column       | Type    | Description          |
| ------------ | ------- | -------------------- |
| id           | Integer | 상품 아이디          |
| imgUrl       | String  | 제품의 이미지 URL    |
| name         | String  | 상품명               |
| price        | Integer | 가격                 |
| ingredients  | String  | 성분 명(콤마로 구분) |
| monthlySales | Integer | 이번 달 판매 수량    |

### 2. 상품 상세 정보 조회하기

상품 상세 정보를 조회할 수 있습니다. 동일한 카테고리의 상위 3개 추천 상품들도 함께 조회할 수 있습니다.

#### 기능 상세

- 상품 id로 특정 상품의 상세 정보를 조회할 수 있습니다.
- 이미지 id를 base URL과 조합해 상품 이미지를 불러올 수 있는 URL을 보여줍니다.
- 동일한 카테고리의 상품 중 상위 3개의 추천 상품 정보를 조회할 수 있습니다.
  - 인자로 받은 피부 타입에 대한 성분 점수가 높은 순서로 추천합니다. 점수가 같다면, 가격이 낮은 상품을 먼저 추천합니다.
  - 추천 상품 정보는 상품 아이디, 상품 썸네일 이미지 URL, 상품명, 가격 을 포함합니다.

#### URL

`/product/:id`

#### Method

`GET`

#### Request Header 구조 예시

```
GET /product/17?skin_type=oily
Content-Type: application/json
```

#### Query Parameter

| Parameter | Type   | Description                        |
| --------- | ------ | ---------------------------------- |
| skin_type | String | (필수) 지성(oily)/건성(dry)/민감성 | (sensitive) 중 택 1 |

#### Sample Call

```
/product/17?skin_type=oily
```

#### Success Response

```
[
  {
    "id": 17,
    "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/image/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
    "name": "화해 에센스 토너",
    "price": 23000,
    "gender": "all",
    "category": "skincare",
    "ingredients": "Glycerin,Methyl Gluceth-20,Pulsatilla Koreana Extract,Purified Water",
    "monthlySales": 1682
  },
  {
    "id": 23,
    "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
    "name": "화해 엔젤 토너",
    "price": 33000
  },
  {
    "id": 37,
    "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
    "name": "화해 화이트 브라이트닝 소프너 인리치드",
    "price": 24800
  },
  {
    "id": 141,
    "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
    "name": "화해 퍼펙트 스킨케어",
    "price": 14800
  }
]
```

#### Response Body 구성

상품 상세 정보 response body는 해당 id 상품 정보와 3개의 추천 상품 정보를 배열로 구성합니다.

#### 상품 정보

| Column       | Type    | Description              |
| ------------ | ------- | ------------------------ |
| id           | Integer | 상품 아이디              |
| imgUrl       | String  | 상품 fullsize 이미지 URL |
| name         | String  | 상품명                   |
| price        | Integer | 가격                     |
| gender       | String  | 성별(남/여/구분 없음)    |
| category     | String  | 카테고리                 |
| ingredients  | String  | 성분 명(콤마로 구분      | ) |
| monthlySales | Integer | 이번 달 판매 수량        |

#### 추천 상품 정보

| Column | Type    | Description               |
| ------ | ------- | ------------------------- |
| id     | Integer | 상품 아이디               |
| imgUrl | String  | 상품 thumbnail 이미지 URL |
| name   | String  | 상품명                    |
| price  | Integer | 가격                      |

#### 전반적인 구현과 관련한 요청 사항

- 테스트 코드를 작성하는 경우 가산점이 있습니다.
- 프로젝트 구조 및 성능: 사용하는 프레임워크의 Best practice를 활용해서 프로젝트를 구성해 주세요.
- 기능성: 버그 없이 기능이 정상적으로 동작해야 합니다.
- 코딩 스타일: 다른 사람이 읽기 쉽고, 디버그하기 쉽도록 Clean한 코딩 스타일을 유지해 주세요.
