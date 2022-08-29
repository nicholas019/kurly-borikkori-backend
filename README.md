# 컬리 제 1회 입사 연계 특전 온라인 해커톤 (KURLY HACK FESTA 2022) : 본선 프로젝트(팀명 : borikkori)
![borikkori](https://user-images.githubusercontent.com/103249222/187138416-14cab604-36d8-4c06-825a-e206af811eb1.png)


## 🌼 프로젝트 소개 🌼
* 프로젝트명 : Kurmmunity
* 컬리 핵 페스타 2022 본선진출.
* Kurmmunity는 마켓컬리 회원들이 각자의 레시피와 생활 팁 등을 공유할 수 있는 커뮤니티 사이트를 개발하고자 했다. 하지만 개발 기간이 짧아 레시피만을 위한 커뮤니티 사이트를 필수 구현으로 진행했다.
* Kurmmunity는 마켓 컬리에서 판매하는 원재료나 제품들을 통해,고객들이 직접 요리를 제작하고 본인들의 레시피를 공유 하면서 고객들끼리 본인들이 원하는 정보와 제품을 추천할 수 있다는 순기능이 있다. 또한, 베스트 게시글이나 레벨제 와 같이 지속적인 커뮤니티 활동을 하는 사용자의 경우에는 적립금, 경품과 같은 혜택들을 부여하여 고객 유치의 지속성 역시 기대해볼 수 있다.

[🍽️시연영상 보러가기](https://www.youtube.com/watch?v=Bk5nmkSkW0U&t=2)
<br/>
[:heart:프론트엔드 github](https://github.com/jinhengxi/Borikkori)


<br/>

## 🌼 개발 인원 및 기간 🌼
**개발기간** : 
1. 예선 계획서 제출 기간 : 2022/07/25/ ~ 2022/08/15/
2. 본선 결과발표 : 2022/08/17/
3. 본선 개발 기간 : 2022/08/19/ ~ 2022/08/24

<br/>

**개발인원 및 파트** : 
#### Frontend (3명)
- 손가영 🐷 : 팀장
- 김형겸 🍋 
- 김형석 🌟 


#### Backend (1명)
- 임한구 🎅🏻

<br/>

## 🌼 기술 🌼
**Front-End** : JavaScript, React.js, Next.js, Styled-compontents, axios
<br/>
**Back-End** : Python, Django web framework, MySQL, AWS S3/RDS, Knolpy
<br/>
**Common** : Git-Hub, slack, trello

<br/>
## 🌼 ERD 🌼
<img width="1237" alt="스크린샷 2022-08-29 오후 4 09 38" src="https://user-images.githubusercontent.com/103249222/187143802-d53364b2-5cd4-4af3-9235-842490184bac.png">



## 🌼 핵심 기능 설명 🌼

### Ricipe APP
#### 1. RecipeList API
 - EndPoint 01 :  GET method /recipe/<int:menu_id>/list
   - 레시피관련 리스트 조회기능
   - menu_id를 통해 마켓컬리 레시피인지, 회원레시피인지 구별하여 반환
   - 사용페이지 : 레시피 리스트 게시판(기본값 최신순)
 - EndPoint 02 :  GET method /recipe/<int:menu_id>/list?sort=<int>
   - 레시피관련 리스트 정렬기능
   - 딕셔너리 언페킹을 이용한 정렬기능 구현
   - 4가지 기능별 정렬 기능(작성순, 조회수순, 좋아요순, 조회수기준에서 좋아요 많은 순)
   - 사용페이지 : 베스트게시판, 메인 게시판(상단, 중단)
 - EndPoint 03 :  GET method /recipe/<int:menu_id>/list?main=<int>&sub=<int>
   - 레시피관련 리스트 필터기능
   - 메인 필터와 서브필터로 나눠 Q객체를 활용하여 필터기능 구현
   - 사용 페이지 : 레시피 리스트게시판 필터기능
 - EndPoint 04 :  GET method /recipe/<int:menu_id>/list?search=<string>
   - 레시피관련 리스트 검색기능
   - Q객체와 icontains를 활용하여 검색기능 구현
   - 사용 페이지 : 레시피 리스트게시판 


![형석 main re](https://user-images.githubusercontent.com/103249222/187154917-94fb8640-60f1-4401-abb7-14fd90d4cc0e.gif)
<br/>
![형겸 BEST,리스트 re (1)](https://user-images.githubusercontent.com/103249222/187154736-ca9b1099-7a8d-4b4a-b164-c1d03e7e9375.gif)
 
  
#### 2. RicipeWrite API
 - EndPoint 01 :  POST method /recipe/<int:menu_id>/write
   - 레시피 등록 기능
   - menu_id를 통해 마켓컬리 레시피인지, 회원레시피인지 구별하여 반환
   - 레시피 등록 게시판에서 form-date형식으로 데이터를 받아 처리
   - 파일의 경우, thumbnail, content_image이 있으며, 확장자 검사를 하여 사진 파일임을 확인하면, file_handler를 거쳐, file_upload에 있는 boto3 라이브러리를 통해 S3에 저장하고 S3의 URL을 반환하여 DB에 저장
   - 이외의 비파일자료는 여개가 함께 전송되어오는 ingredient, product, content는 json형식에서 딕셔너리형태로 바꿔 처리.
   - DB저장은 Recipe모델을 중심으로 참조되어있는 모델(Ingredient, RecipeProduct, Hash)들을 트랜젝션을 활용하여 동시 저장하도록 구현,
   - 리스트형태의 데이터들은 저장시에 쿼리를 줄이기위해 bulk_create를 활용하여 한번에 저장하도록 기능구현
   - content와 content_image의 경우 하나의 레시피에 여러개의 본문이 저장되어야함으로 반복문을 통해 순차적으로 저장하도록 구현하였으며, content와 content_image는 한쌍으로 등록이 되어야 함으로 트랜젝션을 이용하여 저장 기능 구현
   - 사용 페이지 : 레시피 작성 게시판(마켓컬리/회원)
  
![형석 레시피작성 1 re](https://user-images.githubusercontent.com/103249222/187155270-0aff71c3-e910-448d-80c4-0b769ab208d5.gif)
<br/>
![형석 레시피작성 2 re](https://user-images.githubusercontent.com/103249222/187155379-0ee820d2-c914-42e6-84d2-0bba3f19f2c6.gif)
<br/>
![형석 레시피작성 3 re](https://user-images.githubusercontent.com/103249222/187155390-508676ae-91d9-40a2-bb1e-2b313349465f.gif)
<br/>
![형석 레시피작성 4 re](https://user-images.githubusercontent.com/103249222/187155398-0f3c8d2e-db46-4071-ac69-47f24978e6cd.gif)
<br/>
![형석 레시피작성 5 re](https://user-images.githubusercontent.com/103249222/187155413-abf3741c-b1ab-4203-923f-1be37a5aa3ad.gif)

  
#### 3. RecipeDetailView API
 - EndPoint 01 :  GET method /recipe/detail/<int:recipe_id>
   - 레시피 상세보기 기능
   - recipe_id를 통해 해당 아이디의 상세페이지 반환 기능
   - EndPoint호출시 hit갯수를 하나씩 증가하여 조회수 기능 구현
   - 사용 페이지 : 레시피 상세 페이지
  
#### 4. RecipeCommentView API
 - EndPoint 01 :  GET method /recipe/detail/<int:recipe_id>/comment
   - 레시피 댓글 조회 기능
   - recipe_id로 DB필터하여 댓글리스트 반환
   - 그냥 댓글일경우 parent_comment_id에 None값을 넣고 저장.
   - tag의 경우 질문과 일반 밖에 없어 boolen field로 처리
   - 사용 페이지 : 레시피 상세 페이지
 - EndPoint 02 :  POST method /recipe/detail/<int:recipe_id>/comment
   - 레시피 댓글 등록 기능
   - 저장되는 데이터는 text 데이터 뿐이여서 request.body를 통해 데이터 전달.
   - 이 엔드포인트로 들어온 댓글은 대댓글이 아니므로 DB에 저장할때 parent_comment_id는 None값으로 저장
   - 사용 페이지 : 레시피 상세 페이지
 - EndPoint 03 :  DELETE method /recipe/detail/<int:recipe_id>/comment/<int:comment_id>
   - 레시피 댓글 삭제 기능
   - 패스파라메터로 들어온 id값으로 데이터 조회 후 삭제 기능
   - 사용 페이지 : 레시피 상세페이지
 
#### 5. ReCommentView API
 - EndPoint 01 :  GET method /recipe/detail/<int:recipe_id>/recomment/<int:comment_id>
   - 레시피 대댓글 조회기능
   - 각 레시피 댓글의 귀속되어있는 대댓글을 조회하는 기능.
   - 패스파라메터에서 정보를 얻어 DB조회하여 결과값 반환.
   - 사용 페이지 : 레시피 상세페이지
 
 - EndPoint 02 :  POST method /recipe/detail/<int:recipe_id>/recomment/<int:commnet_id>
   - 레시피 대댓글 등록 기능
   - 레시피 댓글 등록 기능과 동일하지만 다른것은 tag값이 없는것과, parent_comment_id값이 패스파라메터에서 받는 comment_id값을 저장하여 어떤 댓글의 대댓글인지 확인
   - 사용 페이지 : 레시피 상세페이지
 
#### 6. RecipeSimiltude API
 - EndPoint 01 :  GET method /recipe/detail/<int:recipe_id>/similtude
  - 관련 레시피 추천 기능
  - 현재 보고있는 레시피의 본문에 있는 텍스트들중 명사들을 추출하여 빈도순으로 정렬하여 많이나온 순서대로 전체 레시피에서 검색하여 관련도순으로 정렬하여 반환.
  - 문자 추출기능은 Knolpy라이브러리 사용하였으며 명사를 추출하는 기능은 Knolpy라이브러리의 Twitter클래스를 활용
  - 사용 페이지 : 레시피 상세페이지
 
#### 7. RecipeLikevie API/ RecipeCommentLike API
 - 레시피 좋아요 기능/ 레시피 댓글 좋아요 기능
 - 각 엔드포인트의 패스파라미터와 로그인데코레이터의 유저아이디로 각 대상과 like의 중간테이블을 만들어 기록, 저장할때 like의 값에 user_id가 1개씩만 가능하도록 구현
 - 좋아요 취소기능은 삭제기능을 통해 구현
 - 사용페이지 : 레시피 상세페이지
 
 
#### 8. 이외의 기능
  - UserBestList : 레시피 업로드 상위 유저 리스트 API
  - UserInfo : 유저 상세 정보 API
  - UserRecipeWrite : 유저가 작성한 레시피 리스트 API
  - UserRe퍋ㅈWrite : 유저가 작성한 후기 리스트 API
  - ProductList : 레시피등록시 레시피에 사용한 마켓컬리 제품 목록 검색을 위한 상품리스트 API  




