# 피규어 종류 확인 문서

값을 기입하고 해당 그룹의 모든 상품에 맞는지 확인한 뒤 `approved`를 `true`로 바꿉니다.
확정할 수 없으면 null/false를 유지합니다. 해당 없음이 확실하면 value=null, not_applicable=true로 적습니다.
캐릭터 value는 `["이름1", "이름2"]`, 작품명은 문자열, 종류는 아래 코드 문자열입니다.
인터넷에 정보가 없다는 판정이 아니라 현재까지 확정하지 못한 항목입니다.

사용 가능한 코드:

- `noodle_stopper`: 누들 스토퍼
- `scale_figure`: 스케일 피규어
- `action_figure`: 액션 피규어
- `chibi_figure`: 데포르메 피규어
- `nendoroid`: 넨도로이드
- `soft_vinyl`: 소프비
- `plush`: 봉제인형
- `acrylic_stand`: 아크릴 스탠드
- `mini_figure`: 미니 피규어
- `prize_figure`: 프라이즈 피규어
- `static_figure`: 고정형 피규어
- `model_kit`: 프라모델·조립 모형
- `figure_parts`: 피규어 부품·소품
- `rubber_mascot`: 러버 마스코트
- `keychain`: 키링·스트랩
- `lottery_goods`: 캐릭터 복권 상품
- `non_scale_figure`: 논스케일 피규어
- `completed_figure`: 완성품 피규어

## R0001 — FURYU Prize (439개)

상품 ID: 5002, 5003, 5142, 5151, 5154, 5155, 5156, 5175, 5176, 5177, 5196, 5197, 5219, 5220, 5221, 5222, 5223, 5224, 5225, 5226, 5227, 5228, 5229, 5230, 5231, 5232, 5233, 5234, 5235, 5236, 5237, 5238, 5239, 5240, 5241, 5242, 5243, 5244, 5246, 5247, 5248, 5249, 5250, 5251, 5252, 5253, 5254, 5255, 5256, 5257, 5258, 5259, 5260, 5261, 5262, 5263, 5264, 5265, 5266, 5267, 5268, 5269, 5270, 5271, 5272, 5273, 5284, 5285, 5286, 5287, 5288, 5289, 5290, 5291, 5292, 5293, 5294, 5295, 5296, 5297, 5298, 5299, 5300, 5301, 5302, 5303, 5304, 5305, 5306, 5307, 5308, 5309, 5310, 5311, 5312, 5313, 5314, 5315, 5316, 5317, 5318, 5319, 5320, 5321, 5322, 5323, 5324, 5325, 5327, 5328, 5329, 5330, 5331, 5333, 5334, 5335, 5336, 5338, 5339, 5340, 5342, 5343, 5344, 5345, 5346, 5348, 5349, 5351, 5352, 5353, 5354, 5355, 5356, 5357, 5358, 5360, 5361, 5362, 5363, 5364, 5365, 5367, 5368, 5369, 5370, 5371, 5373, 5374, 5375, 5377, 5378, 5379, 5381, 5382, 5383, 5384, 5385, 5386, 5387, 5388, 5389, 5391, 5392, 5394, 5395, 5396, 5397, 5399, 5400, 5401, 5402, 5405, 5406, 5409, 5410, 5411, 5413, 5414, 5415, 5416, 5417, 5418, 5419, 5420, 5421, 5422, 5423, 5424, 5425, 5426, 5427, 5428, 5430, 5431, 5432, 5433, 5434, 5435, 5436, 5437, 5438, 5439, 5440, 5441, 5444, 5445, 5446, 5450, 5451, 5452, 5453, 5454, 5455, 5456, 5457, 5458, 5459, 5460, 5461, 5471, 5472, 5473, 5474, 5475, 5476, 5477, 5478, 5487, 5488, 5491, 5493, 5494, 5501, 5503, 5509, 5510, 5511, 5527, 5528, 5531, 5551, 5552, 5553, 5554, 5555, 5556, 5557, 5558, 5559, 5560, 5561, 5562, 5563, 5564, 5565, 5566, 5567, 5568, 5569, 5570, 5571, 5572, 5573, 5574, 5575, 5576, 5577, 5578, 5579, 5580, 5581, 5582, 5583, 5584, 5585, 5586, 5587, 5588, 5589, 5590, 5591, 5592, 5593, 5594, 5595, 5596, 5597, 5598, 5599, 5600, 5601, 5602, 5603, 5604, 5605, 5606, 5607, 5608, 5609, 5610, 5611, 5612, 5613, 5614, 5615, 5616, 5617, 5618, 5619, 5620, 5621, 5622, 5623, 5624, 5625, 5626, 5627, 5628, 5629, 5630, 5631, 5632, 5633, 5634, 5635, 5636, 5637, 5638, 5639, 5640, 5641, 5642, 5643, 5644, 5645, 5646, 5647, 5648, 5649, 5650, 5651, 5652, 5653, 5654, 5655, 5656, 5657, 5658, 5659, 5660, 5661, 5662, 5663, 5664, 5665, 5666, 5667, 5668, 5669, 5670, 5671, 5672, 5673, 5674, 5675, 5676, 5677, 5678, 5679, 5680, 5681, 5682, 5683, 5684, 5685, 5686, 5687, 5688, 5689, 5690, 5691, 5692, 5693, 5694, 5695, 5696, 5697, 5698, 5699, 5700, 5701, 5702, 5703, 5704, 5705, 5706, 5707, 5708, 5709, 5710, 5711, 5712, 5713, 5714, 5715, 5716, 5717, 5718, 5719, 5720, 5721, 5722, 5723, 5724, 5725, 5726, 5727, 5728, 5729, 5730, 5732, 5733, 5734, 5735, 5736, 5737, 5738, 5739, 5740, 5741, 5744, 5745, 5746, 5748, 5749, 5750, 5779, 5780, 5792

- [Trickstar フィギュア(赤)](https://prtimes.jp/main/html/rd/p/000000634.000005167.html#item-d97d5a29c0d820e439fa)
- [Trickstar フィギュア(青)](https://prtimes.jp/main/html/rd/p/000000634.000005167.html#item-ce67d7d4d68251741993)
- [Re:ゼロから始める異世界生活 王選候補者と騎士フィギュアーエミリア陣営ー](https://furyuprize.com/item/22097)

```json
{
  "review_id": "R0001",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0002 — TENITOL (92개)

상품 ID: 51, 52, 54, 55, 56, 57, 58, 59, 90, 91, 93, 5508, 5512, 5513, 5514, 5515, 5524, 5525, 5532, 5536, 5775, 5776, 5793, 5794, 5797, 5798, 5799, 5800, 5802, 5803, 5804, 5805, 5806, 5807, 5808, 5810, 5813, 5814, 5820, 5821, 5822, 5823, 5824, 5825, 5826, 5827, 5828, 5829, 5831, 5833, 5843, 5844, 5849, 5851, 5852, 5853, 5855, 5856, 5857, 5866, 5867, 5870, 5871, 5873, 5875, 5877, 5878, 5885, 5886, 5887, 5888, 5890, 5892, 5893, 5901, 5902, 5904, 5905, 5906, 5909, 5910, 5915, 5916, 5918, 5919, 5922, 5923, 5924, 5927, 5935, 5944, 5945

- [TENITOL TALL フリーレン クラシカルワンピースver.](https://furyu-hm.com/products/tnl-zua4ajhp)
- [TENITOL TALL フェルン クラシカルワンピースver.](https://furyu-hm.com/products/tnl-b4hj45rl)
- [TENITOL TALL 鹿目まどか&暁美ほむら スペシャルセット](https://furyu-hm.com/products/tnl-7dckkixl)

```json
{
  "review_id": "R0002",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0003 — Figuarts ZERO (45개)

상품 ID: 1657, 1729, 1731, 1738, 1743, 1769, 1771, 1774, 1797, 1820, 1839, 1851, 1870, 1884, 1889, 1897, 1911, 1929, 1942, 1961, 1970, 2013, 2014, 2050, 2066, 2079, 2089, 2111, 2112, 2117, 2119, 2134, 2135, 2136, 2137, 2143, 2144, 2149, 2150, 2151, 2152, 2160, 2164, 2168, 3501

- [피규아트 제로 우즈마키 나루토 -NARUTO 72 series- 29](https://www.bnkrmall.co.kr/goods/detail.do?gno=93561748)
- [피규아트 제로 도우마](https://www.bnkrmall.co.kr/goods/detail.do?gno=98828130)
- [피규아트 제로 (STARTune) 손오공 -결전장 도착-](https://www.bnkrmall.co.kr/goods/detail.do?gno=23407647)

```json
{
  "review_id": "R0003",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0004 — S-FIRE (33개)

상품 ID: 4712, 4713, 4715, 4716, 4718, 4720, 4721, 4722, 4723, 4724, 4725, 4729, 4730, 4731, 4732, 4733, 4742, 4743, 4744, 4745, 4746, 4747, 4754, 4761, 4762, 4764, 4765, 4766, 4774, 4776, 4779, 4785, 4792

- [僕のヒーローアカデミア　フィギュア　緑谷出久](https://s-fire.net/products/4570001951558)
- [僕のヒーローアカデミア　フィギュア　爆豪勝己](https://s-fire.net/products/4570001951565)
- [僕のヒーローアカデミア　フィギュア　轟焦凍](https://s-fire.net/products/4570001959820)

```json
{
  "review_id": "R0004",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0005 — Trio-Try-iT Figure (30개)

상품 ID: 5119, 5143, 5144, 5145, 5161, 5165, 5166, 5167, 5169, 5170, 5171, 5187, 5188, 5192, 5194, 5195, 5202, 5216, 5217, 5218, 5526, 5530, 5533, 5545, 5546, 5547, 5769, 5772, 5773, 5774

- [Trio-Try-iT Figureー初音ミク×チロルチョコ ミルクver.ー](https://prtimes.jp/main/html/rd/p/000002189.000005167.html)
- [TVアニメ「ローゼンメイデン」 Trio-Try-iT Figureー翠星石ー](https://furyuprize.com/item/21760)
- [TVアニメ『千歳くんはラムネ瓶のなか』 Trio-Try-iT Figureー七瀬 悠月ー](https://furyuprize.com/item/21103)

```json
{
  "review_id": "R0005",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0006 — GUNDAM UNIVERSE (24개)

상품 ID: 1597, 1678, 1721, 1722, 1777, 1779, 1781, 1856, 1900, 1914, 1915, 1916, 1983, 1984, 2057, 2058, 2069, 2091, 2092, 2120, 2121, 2157, 2159, 6145

- [건담 유니버스 RX-0 유니콘 건담 리뉴얼](https://www.bnkrmall.co.kr/goods/detail.do?gno=49797780)
- [건담 유니버스 ZGMF-X20A 스트라이크 프리덤 건담 리뉴얼](https://www.bnkrmall.co.kr/goods/detail.do?gno=78326139)
- [건담 유니버스 ZGMF/A-262PD-P 마이티 스트라이크 프리덤 건담](https://www.bnkrmall.co.kr/goods/detail.do?gno=53106536)

```json
{
  "review_id": "R0006",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0007 — 초합금혼 (20개)

상품 ID: 1594, 1611, 1618, 1658, 1665, 1679, 1713, 1714, 1759, 1811, 1818, 1866, 1913, 1943, 1981, 2003, 2008, 2124, 2154, 2169

- [초합금혼 GX-88 기갑함대 다이라가XV](https://www.bnkrmall.co.kr/goods/detail.do?gno=86197535)
- [초합금혼 GX-04S UFO로보 그렌다이저 우주의 왕자 세트](https://www.bnkrmall.co.kr/goods/detail.do?gno=97813258)
- [초합금혼 GX-43 투장 다이모스](https://www.bnkrmall.co.kr/goods/detail.do?gno=42442325)

```json
{
  "review_id": "R0007",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0008 — 초합금 (18개)

상품 ID: 1598, 1667, 1669, 1717, 1733, 1746, 1791, 1798, 1803, 1819, 1841, 1857, 1908, 1931, 1960, 2045, 2063, 2158

- [DX 초합금 VF-25 MESSIAH VALKYRIE Top Gun: Maverick Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=418341)
- [초합금 볼트론](https://www.bnkrmall.co.kr/goods/detail.do?gno=47658534)
- [초합금 비밀전대 고레인저](https://www.bnkrmall.co.kr/goods/detail.do?gno=53645518)

```json
{
  "review_id": "R0008",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0010 — DRESSTA (16개)

상품 ID: 4804, 4805, 4814, 4815, 4816, 4824, 4828, 4843, 4844, 4845, 4846, 4847, 4855, 4856, 4884, 4885

- [ワンパンマン　DRESSTA　戦慄のタツマキ](https://taito-goods.jp/shop/g/g80101150/)
- [ワンパンマン　DRESSTA　地獄のフブキ](https://taito-goods.jp/shop/g/g80101160/)
- [幽☆遊☆白書　DRESSTA　浦飯幽助](https://taito-goods.jp/shop/g/g80101120/)

```json
{
  "review_id": "R0010",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0011 — ムチュートフィギュア (12개)

상품 ID: 5150, 5152, 5153, 5158, 5172, 5173, 5184, 5199, 5210, 5211, 5212, 5214

- [ばっどがーる ムチュートフィギュア―涼風 涼―](https://furyuprize.com/item/21763)
- [オーバーロード ムチュートフィギュアーアルベド・aqua ver.ー](https://furyuprize.com/item/21779)
- [クラスで2番目に可愛い女の子と友だちになった ムチュートフィギュアー朝凪海ー](https://furyuprize.com/item/21782)

```json
{
  "review_id": "R0011",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0012 — S.H.MonsterArts (11개)

상품 ID: 1647, 1648, 1712, 1732, 1742, 1812, 1850, 1879, 1941, 1972, 1973

- [S.H.몬스터아츠 고질라 (2014) 『GODZILLA 고질라』 -Movie Graphic Plus-](https://www.bnkrmall.co.kr/goods/detail.do?gno=60411621)
- [S.H.몬스터아츠 고질라 (1975)](https://www.bnkrmall.co.kr/goods/detail.do?gno=25721326)
- [S.H.몬스터아츠 고질라 (고질라 더 라이드: 그레이트 크래시)](https://www.bnkrmall.co.kr/goods/detail.do?gno=73632501)

```json
{
  "review_id": "R0012",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0013 — METAL BUILD (9개)

상품 ID: 1718, 1792, 1837, 1888, 1901, 2039, 2055, 2126, 6147

- [메탈빌드 스트라이크 프리덤 건담](https://www.bnkrmall.co.kr/goods/detail.do?gno=22916830)
- [메탈빌드 가면라이더 제로원](https://www.bnkrmall.co.kr/goods/detail.do?gno=53319574)
- [메탈빌드 하츠네 미쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=39360491)

```json
{
  "review_id": "R0013",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0014 — 성투사성의신화 (9개)

상품 ID: 1660, 1670, 1741, 1745, 1757, 1892, 2027, 2052, 2163

- [세인트세이야 EX 드래곤 시류 (신성의)](https://www.bnkrmall.co.kr/goods/detail.do?gno=78733419)
- [세인트세이야 천마 자리의 성의 페가수스 크로스 (초회 한정 성의 박스 포함판)](https://www.bnkrmall.co.kr/goods/detail.do?gno=45575136)
- [세인트세이야 페가수스 세이야 초기 청동 성의 (리바이벌판)](https://www.bnkrmall.co.kr/goods/detail.do?gno=70366102)

```json
{
  "review_id": "R0014",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0017 — EXQ (6개)

상품 ID: 3106, 3138, 3139, 3163, 3217, 3223

- [Re:제로부터 시작하는 이세계 생활 반프레스토 클로니클 EXQ 피규어 렘 Vol.4 (메이드 아머 Ver.)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59285)
- [RE:제로부터 시작하는 이세계 생활 반프레스토 클로니클 EXQ 피규어 렘](https://www.bnkrmall.co.kr/goods/detail.do?gno=58282)
- [RE:제로부터 시작하는 이세계 생활 반프레스토 클로니클 EXQ 피규어 람](https://www.bnkrmall.co.kr/goods/detail.do?gno=58281)

```json
{
  "review_id": "R0017",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0018 — F:NEX (6개)

상품 ID: 62, 1531, 5046, 5495, 5496, 5948

- [フリーレン フォトフレームフィギュア](https://furyu-hm.com/products/fnx-cyv366r3)
- [コミッサ太郎&コミッサ花子 スケールフィギュア](https://furyu-hm.com/products/fnx-std7srm8)
- [エヴァンゲリオン初号機 ヒューマンスケールフィギュア](https://www.furyu.jp/news/2021/03/fnex_evangelion)

```json
{
  "review_id": "R0018",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0019 — NXEDGE STYLE (6개)

상품 ID: 2029, 2090, 2093, 2108, 2132, 2161

- [NXEDGE 페넬로페](https://www.bnkrmall.co.kr/goods/detail.do?gno=58638301)
- [NXEDGE 신성 쟈코마루](https://www.bnkrmall.co.kr/goods/detail.do?gno=57915)
- [NXEDGE 류코마루](https://www.bnkrmall.co.kr/goods/detail.do?gno=57895)

```json
{
  "review_id": "R0019",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0020 — PROPLICA (6개)

상품 ID: 1954, 1977, 2068, 2110, 2125, 2129

- [PROPLICA 일륜도 (토미오카 기유)](https://www.bnkrmall.co.kr/goods/detail.do?gno=72904495)
- [PROPLICA 일륜도 (카마도 탄지로) 렌고쿠 쿄쥬로의 코등이 Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=88064956)
- [PROPLICA 붉은 책](https://www.bnkrmall.co.kr/goods/detail.do?gno=58843)

```json
{
  "review_id": "R0020",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0022 — BiCute (5개)

상품 ID: 5168, 5183, 5189, 5203, 5208

- [To LOVEる-とらぶる-ダークネス BiCute Ribbons Figure―モモ・ベリア・デビルーク―](https://furyuprize.com/item/21911)
- [貞子 BiCute Bunnies Figureー貞子ー](https://furyuprize.com/item/21899)
- [けいおん! BiCute Dark Figureー平沢唯ー](https://furyuprize.com/item/22557)

```json
{
  "review_id": "R0022",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0023 — G.E.M. (5개)

상품 ID: 43, 44, 45, 46, 47

- [NARUTO-ナルト- 疾風伝 てのひらミナト](https://megahobby.jp/products/item/6044/)
- [鬼滅の刃 てのひらしのぶさん【再販】](https://megahobby.jp/products/item/5941/)
- [文豪ストレイドッグス てのひら太宰さん](https://megahobby.jp/products/item/6045/)

```json
{
  "review_id": "R0023",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0056 — Coreful (3개)

상품 ID: 109, 110, 111

- [葬送のフリーレン Coreful フィギュア フェルン(タイクレ限定)](https://www.taito.co.jp/taito-prize/0451852500)
- [葬送のフリーレン Coreful フィギュア フリーレン~ドレスver.~](https://www.taito.co.jp/taito-prize/0451950600)
- [葬送のフリーレン Coreful フィギュア フリーレン](https://www.taito.co.jp/en/taito-prize/0451972800)

```json
{
  "review_id": "R0056",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0057 — Luminasta (3개)

상품 ID: 106, 107, 108

- [葬送のフリーレン Luminasta “フリーレン” ～葬送のフリーレン～](https://segaplaza.jp/prize/D121425/)
- [葬送のフリーレン Luminasta “フリーレン” ～インミミック～](https://segaplaza.jp/prize/D122835/)
- [葬送のフリーレン Luminasta “フリーレン” ～SUMMER DRESS～](https://segaplaza.jp/prize/D123005/)

```json
{
  "review_id": "R0057",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0058 — ONE PIECE トニートニー・チョッパー (3개)

상품 ID: 142, 489, 522

- [ONE PIECE トニートニー・チョッパー](https://megahobby.jp/products/item/3628/)
- [ONE PIECE トニートニー・チョッパー【再販】](https://megahobby.jp/products/item/4422/)
- [ONE PIECE  トニートニー・チョッパー【再販】](https://megahobby.jp/products/item/4500/)

```json
{
  "review_id": "R0058",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0059 — SPY×FAMILY アーニャ・フォージャー (3개)

상품 ID: 169, 439, 1198

- [SPY×FAMILY アーニャ・フォージャー](https://megahobby.jp/products/item/3695/)
- [SPY×FAMILY アーニャ・フォージャー【再販】](https://megahobby.jp/products/item/4322/)
- [SPY×FAMILY アーニャ・フォージャー【再販】](https://megahobby.jp/products/item/5829/)

```json
{
  "review_id": "R0059",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0060 — ひっかけフィギュア (3개)

상품 ID: 5157, 5178, 5209

- [ホロライブプロダクション ひっかけフィギュアVol.7](https://furyuprize.com/item/22846)
- [ホロライブプロダクション ひっかけフィギュアVol.10](https://furyuprize.com/item/22845)
- [ホロライブプロダクション ひっかけフィギュアVol.5](https://furyuprize.com/item/22857)

```json
{
  "review_id": "R0060",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0061 — 呪術廻戦 宿儺 (3개)

상품 ID: 663, 1195, 1371

- [呪術廻戦 宿儺【再販】](https://megahobby.jp/products/item/4785/)
- [呪術廻戦 宿儺【再販】](https://megahobby.jp/products/item/5826/)
- [呪術廻戦　宿儺](https://www.megahobby.jp/products/item/3721/)

```json
{
  "review_id": "R0061",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0062 — 機動戦士ガンダム 機動戦士ニャンダム ジオン公国軍ニャ！ (3개)

상품 ID: 230, 487, 1202

- [機動戦士ガンダム 機動戦士ニャンダム　ジオン公国軍ニャ！](https://megahobby.jp/products/item/3862/)
- [機動戦士ガンダム 機動戦士ニャンダム　ジオン公国軍ニャ！【再販】](https://megahobby.jp/products/item/4420/)
- [機動戦士ガンダム 機動戦士ニャンダム　ジオン公国軍ニャ！【再販】](https://megahobby.jp/products/item/5833/)

```json
{
  "review_id": "R0062",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0063 — 機動戦士ガンダム 機動戦士ニャンダム 地球連邦軍だニャー！ (3개)

상품 ID: 213, 488, 1201

- [機動戦士ガンダム 機動戦士ニャンダム 地球連邦軍だニャー！](https://megahobby.jp/products/item/3831/)
- [機動戦士ガンダム 機動戦士ニャンダム　地球連邦軍だニャー！【再販】](https://megahobby.jp/products/item/4421/)
- [機動戦士ガンダム 機動戦士ニャンダム　地球連邦軍だニャー！【再販】](https://megahobby.jp/products/item/5832/)

```json
{
  "review_id": "R0063",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0169 — BLEACH 千年血戦篇 BLEACHニャン！ (2개)

상품 ID: 281, 1102

- [BLEACH　千年血戦篇 BLEACHニャン！](https://megahobby.jp/products/item/3994/)
- [BLEACH 千年血戦篇 BLEACHニャン！【再販】](https://megahobby.jp/products/item/5685/)

```json
{
  "review_id": "R0169",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0170 — COLLECTION 09 機動戦士ガンダム 地球連邦軍 アムロ・レイ ノーマルスーツVer. (2개)

상품 ID: 116, 893

- [COLLECTION 09 機動戦士ガンダム 地球連邦軍 アムロ・レイ ノーマルスーツVer.【再販】](https://megahobby.jp/products/item/6103/)
- [COLLECTION 09 機動戦士ガンダム 地球連邦軍 アムロ・レイ ノーマルスーツVer.](https://megahobby.jp/products/item/5309/)

```json
{
  "review_id": "R0170",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0171 — Exc∞d Creative Figure (2개)

상품 ID: 5282, 5529

- [Exc∞d Creative Figureーしろたん×初音ミクー](https://furyuprize.com/item/21932)
- [SPY×FAMILY Exc∞d Creative Figure-アーニャ・フォージャー3-](https://store.shopping.yahoo.co.jp/media-world/61733755001.html)

```json
{
  "review_id": "R0171",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0172 — Heritage Edition- 新世紀GPXサイバーフォーミュラ11 エクスペリオンZ/A-8 ナイト・シューマッハ機 (2개)

상품 ID: 786, 1074

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ11 エクスペリオンZ/A-8 ナイト・シューマッハ機](https://megahobby.jp/products/item/5010/)
- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ11 エクスペリオンZ/A-8 ナイト・シューマッハ機【再販】](https://megahobby.jp/products/item/5615/)

```json
{
  "review_id": "R0172",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0173 — Heritage Edition- 新世紀GPXサイバーフォーミュラ11 スーパーアスラーダAKF-11 (2개)

상품 ID: 787, 1076

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ11 スーパーアスラーダAKF-11](https://megahobby.jp/products/item/5011/)
- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ11 スーパーアスラーダAKF-11【再販】](https://megahobby.jp/products/item/5617/)

```json
{
  "review_id": "R0173",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0174 — Heritage Edition- 新世紀GPXサイバーフォーミュラ イシュザーク (2개)

상품 ID: 594, 854

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ イシュザーク](https://megahobby.jp/products/item/4626/)
- [-Heritage Edition-  新世紀GPXサイバーフォーミュラ イシュザーク【再販】](https://megahobby.jp/products/item/5224/)

```json
{
  "review_id": "R0174",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0175 — Heritage Edition- 新世紀GPXサイバーフォーミュラ ファイアースペリオンG.T.R (2개)

상품 ID: 595, 855

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ ファイアースペリオンG.T.R](https://megahobby.jp/products/item/4627/)
- [-Heritage Edition-  新世紀GPXサイバーフォーミュラ ファイアースペリオンG.T.R【再販】](https://megahobby.jp/products/item/5225/)

```json
{
  "review_id": "R0175",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0176 — MEGA CAT PROJECT NARUTO -ナルト- ニャルト!お名前缶バッジコレクション (2개)

상품 ID: 1383, 1387

- [MEGA CAT PROJECT NARUTO -ナルト-  ニャルト!お名前缶バッジコレクション](https://megahobby.jp/products/item/5572/)
- [MEGA CAT PROJECT NARUTO -ナルト-  ニャルト!お名前缶バッジコレクション【再販】](https://megahobby.jp/products/item/5999/)

```json
{
  "review_id": "R0176",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0177 — MEGA CAT PROJECT ワンピース ニャンピースニャーン!お名前缶バッジコレクション (2개)

상품 ID: 1384, 1386

- [MEGA CAT PROJECT ワンピース ニャンピースニャーン!お名前缶バッジコレクション](https://megahobby.jp/products/item/5573/)
- [MEGA CAT PROJECT ワンピース ニャンピースニャーン!お名前缶バッジコレクション【再販】](https://megahobby.jp/products/item/5998/)

```json
{
  "review_id": "R0177",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0178 — MeloDoll Figure (2개)

상품 ID: 5281, 5283

- [MeloDoll Figureーラム・ブライズメイドー](https://furyuprize.com/item/21919)
- [MeloDoll Figureーレム・ブライズメイドー](https://furyuprize.com/item/21765)

```json
{
  "review_id": "R0178",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0179 — NARUTO-ナルト- 疾風伝 うちはイタチ暗部ver. (2개)

상품 ID: 504, 1104

- [NARUTO-ナルト- 疾風伝 うちはイタチ暗部ver.](https://megahobby.jp/products/item/4468/)
- [NARUTO-ナルト- 疾風伝 うちはイタチ暗部ver.【再販】](https://megahobby.jp/products/item/5687/)

```json
{
  "review_id": "R0179",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0180 — NARUTO-ナルト- 疾風伝 てのひらカカシ先生 (2개)

상품 ID: 652, 1148

- [NARUTO-ナルト- 疾風伝 てのひらカカシ先生](https://megahobby.jp/products/item/4743/)
- [NARUTO-ナルト- 疾風伝 てのひらカカシ先生【再販】](https://megahobby.jp/products/item/5752/)

```json
{
  "review_id": "R0180",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0181 — NARUTO-ナルト- 疾風伝 はたけカカシ暗部ver. (2개)

상품 ID: 503, 1103

- [NARUTO-ナルト- 疾風伝 はたけカカシ暗部ver.](https://megahobby.jp/products/item/4467/)
- [NARUTO-ナルト- 疾風伝 はたけカカシ暗部ver.【再販】](https://megahobby.jp/products/item/5686/)

```json
{
  "review_id": "R0181",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0182 — NARUTO-ナルト- 疾風伝 サソリ (2개)

상품 ID: 419, 6141

- [ NARUTO-ナルト- 疾風伝 サソリ](https://megahobby.jp/products/item/4274/)
- [NARUTO-ナルト- 疾風伝 サソリ【再販】](https://megahobby.jp/products/item/6167/)

```json
{
  "review_id": "R0182",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0183 — NARUTO-ナルト- 疾風伝 デイダラ (2개)

상품 ID: 420, 766

- [NARUTO-ナルト- 疾風伝 デイダラ](https://megahobby.jp/products/item/4275/)
- [NARUTO-ナルト- 疾風伝 デイダラ【再販】](https://megahobby.jp/products/item/4990/)

```json
{
  "review_id": "R0183",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0184 — NARUTO-ナルト- 疾風伝 ニャルト！LAST BATTLE編 (2개)

상품 ID: 263, 678

- [NARUTO-ナルト- 疾風伝 ニャルト！LAST　BATTLE編](https://megahobby.jp/products/item/3950/)
- [ NARUTO-ナルト- 疾風伝 ニャルト！LAST　BATTLE編【再販】](https://megahobby.jp/products/item/4820/)

```json
{
  "review_id": "R0184",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0185 — NARUTO -ナルト- 疾風伝 ニャルト！少しむかしむかしの 木ノ葉隠れの里だってばよ！ (2개)

상품 ID: 141, 1207

- [NARUTO　-ナルト-　疾風伝  ニャルト！少しむかしむかしの 木ノ葉隠れの里だってばよ！](https://megahobby.jp/products/item/3627/)
- [NARUTO　-ナルト-　疾風伝 ニャルト！少しむかしむかしの 木ノ葉隠れの里だってばよ！【再販】](https://megahobby.jp/products/item/5841/)

```json
{
  "review_id": "R0185",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0186 — NARUTO-ナルト- 疾風伝 ニャルト！ 師弟・絆編 (2개)

상품 ID: 476, 1292

- [NARUTO-ナルト- 疾風伝 ニャルト！ 師弟・絆編](https://megahobby.jp/products/item/4398/)
- [NARUTO-ナルト- 疾風伝 ニャルト！ 師弟・絆編【再販】](https://megahobby.jp/products/item/6012/)

```json
{
  "review_id": "R0186",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0187 — NARUTO-ナルト- 疾風伝 ニャルト！ 開戦！第四次忍界大戦編 (2개)

상품 ID: 192, 573

- [NARUTO-ナルト- 疾風伝  ニャルト！　開戦！第四次忍界大戦編](https://megahobby.jp/products/item/3751/)
- [NARUTO-ナルト- 疾風伝 ニャルト！　開戦！第四次忍界大戦編【再販】](https://megahobby.jp/products/item/4605/)

```json
{
  "review_id": "R0187",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0188 — NARUTO-ナルト- 疾風伝 我愛羅 (2개)

상품 ID: 244, 571

- [NARUTO-ナルト- 疾風伝 我愛羅](https://megahobby.jp/products/item/3904/)
- [NARUTO-ナルト- 疾風伝 我愛羅【再販】](https://megahobby.jp/products/item/4603/)

```json
{
  "review_id": "R0188",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0189 — NARUTO-ナルト- 疾風伝 波風ミナト (2개)

상품 ID: 703, 1137

- [NARUTO-ナルト- 疾風伝 波風ミナト](https://megahobby.jp/products/item/4862/)
- [NARUTO-ナルト- 疾風伝 波風ミナト【再販】](https://megahobby.jp/products/item/5741/)

```json
{
  "review_id": "R0189",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0190 — ONE PIECE サボ (2개)

상품 ID: 310, 660

- [ONE PIECE サボ](https://megahobby.jp/products/item/4064/)
- [ONE PIECE サボ【再販】](https://megahobby.jp/products/item/4782/)

```json
{
  "review_id": "R0190",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0191 — ONE PIECE サンジ (2개)

상품 ID: 184, 496

- [ONE PIECE サンジ【再販】](https://megahobby.jp/products/item/3732/)
- [ONE PIECE サンジ](https://megahobby.jp/products/item/4429/)

```json
{
  "review_id": "R0191",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0192 — ONE PIECE ジュラキュール・ミホーク (2개)

상품 ID: 305, 631

- [ONE PIECE ジュラキュール・ミホーク【再販】](https://megahobby.jp/products/item/4059/)
- [ONE PIECE ジュラキュール・ミホーク](https://megahobby.jp/products/item/4689/)

```json
{
  "review_id": "R0192",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0193 — ONE PIECE トラファルガー・ロー (2개)

상품 ID: 143, 490

- [ONE PIECE トラファルガー・ロー](https://megahobby.jp/products/item/3629/)
- [ONE PIECE トラファルガー・ロー【再販】](https://megahobby.jp/products/item/4423/)

```json
{
  "review_id": "R0193",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0194 — ONE PIECE ナミ (2개)

상품 ID: 495, 521

- [ONE PIECE ナミ](https://megahobby.jp/products/item/4428/)
- [ONE PIECE ナミ【再販】](https://megahobby.jp/products/item/4499/)

```json
{
  "review_id": "R0194",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0195 — ONE PIECE ニコ・ロビン (2개)

상품 ID: 815, 1120

- [ONE PIECE ニコ・ロビン【再販】](https://megahobby.jp/products/item/5150/)
- [ONE PIECE ニコ・ロビン](https://megahobby.jp/products/item/5704/)

```json
{
  "review_id": "R0195",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0196 — ONE PIECE モンキー・D・ルフィ ギア5 (2개)

상품 ID: 401, 661

- [ONE PIECE モンキー・D・ルフィ ギア5](https://megahobby.jp/products/item/4235/)
- [ONE PIECE モンキー・D・ルフィ ギア5【再販】](https://megahobby.jp/products/item/4783/)

```json
{
  "review_id": "R0196",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0197 — ONE PIECE モンキー・D・ルフィ 未来島Ver. (2개)

상품 ID: 617, 791

- [ONE PIECE モンキー・D・ルフィ 未来島Ver.](https://megahobby.jp/products/item/4674/)
- [ONE PIECE モンキー・D・ルフィ 未来島Ver.【再販】](https://megahobby.jp/products/item/5040/)

```json
{
  "review_id": "R0197",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0198 — ONE PIECE ロロノア・ゾロ (2개)

상품 ID: 201, 292

- [ONE PIECE ロロノア・ゾロ【再販】](https://megahobby.jp/products/item/3789/)
- [ONE PIECE ロロノア・ゾロ【再販】](https://megahobby.jp/products/item/4019/)

```json
{
  "review_id": "R0198",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0199 — Re:ゼロから始める異世界生活 てのひら レム (2개)

상품 ID: 500, 1108

- [　Re:ゼロから始める異世界生活 てのひら レム](https://megahobby.jp/products/item/4437/)
- [Re:ゼロから始める異世界生活 てのひらレム 【再販】](https://megahobby.jp/products/item/5691/)

```json
{
  "review_id": "R0199",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0200 — WIND BREAKER 桜遥 (2개)

상품 ID: 560, 790

- [WIND BREAKER 桜遥](https://megahobby.jp/products/item/4559/)
- [WIND BREAKER 桜遥【再販】](https://megahobby.jp/products/item/5039/)

```json
{
  "review_id": "R0200",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0201 — 『ディズニー ツイステッドワンダーランド』 アズール・アーシェングロット (2개)

상품 ID: 136, 1128

- [『ディズニー ツイステッドワンダーランド』 アズール・アーシェングロット](https://megahobby.jp/products/item/3555/)
- [『ディズニー ツイステッドワンダーランド』 アズール・アーシェングロット【再販】](https://megahobby.jp/products/item/5715/)

```json
{
  "review_id": "R0201",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0202 — 『ディズニー ツイステッドワンダーランド』 イデア・シュラウド (2개)

상품 ID: 208, 1138

- [『ディズニー ツイステッドワンダーランド』 イデア・シュラウド](https://megahobby.jp/products/item/3811/)
- [『ディズニー ツイステッドワンダーランド』 イデア・シュラウド【再販】](https://megahobby.jp/products/item/5742/)

```json
{
  "review_id": "R0202",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0203 — 『ディズニー ツイステッドワンダーランド』 マレウス・ドラコニア (2개)

상품 ID: 207, 1139

- [『ディズニー ツイステッドワンダーランド』 マレウス・ドラコニア](https://megahobby.jp/products/item/3810/)
- [『ディズニー ツイステッドワンダーランド』 マレウス・ドラコニア【再販】](https://megahobby.jp/products/item/5743/)

```json
{
  "review_id": "R0203",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0204 — 『ディズニー ツイステッドワンダーランド』 ヴィル・シェーンハイト (2개)

상품 ID: 209, 1140

- [『ディズニー ツイステッドワンダーランド』 ヴィル・シェーンハイト](https://megahobby.jp/products/item/3812/)
- [『ディズニー ツイステッドワンダーランド』 ヴィル・シェーンハイト【再販】](https://megahobby.jp/products/item/5744/)

```json
{
  "review_id": "R0204",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0205 — お兄ちゃんはおしまい！ てのひら まひろちゃん (2개)

상품 ID: 359, 695

- [ お兄ちゃんはおしまい！ てのひら　まひろちゃん](https://megahobby.jp/products/item/4138/)
- [ お兄ちゃんはおしまい！ てのひら　まひろちゃん【再販】](https://megahobby.jp/products/item/4854/)

```json
{
  "review_id": "R0205",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0206 — とびマス ONE PIECE (2개)

상품 ID: 931, 1253

- [とびマス ONE PIECE](https://megahobby.jp/products/item/5379/)
- [とびマス ONE PIECE【再販】](https://megahobby.jp/products/item/5936/)

```json
{
  "review_id": "R0206",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0207 — とびマス ドラゴンボール (2개)

상품 ID: 750, 1043

- [とびマス  ドラゴンボール](https://megahobby.jp/products/item/4968/)
- [とびマス  ドラゴンボール【再販】](https://megahobby.jp/products/item/5558/)

```json
{
  "review_id": "R0207",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0208 — ぴたきゅーと サンリオキャラクターズ (2개)

상품 ID: 945, 1293

- [ぴたきゅーと サンリオキャラクターズ](https://megahobby.jp/products/item/5393/)
- [ぴたきゅーと サンリオキャラクターズ【再販】](https://megahobby.jp/products/item/6013/)

```json
{
  "review_id": "R0208",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0209 — ぼっち・ざ・ろっく！ 後藤ひとり (2개)

상품 ID: 438, 680

- [ぼっち・ざ・ろっく！ 後藤ひとり](https://megahobby.jp/products/item/4313/)
- [ぼっち・ざ・ろっく！ 後藤ひとり【再販】](https://megahobby.jp/products/item/4822/)

```json
{
  "review_id": "R0209",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0210 — ジョジョの奇妙な冒険 スターダストクルセイダース DIO (2개)

상품 ID: 737, 1145

- [ジョジョの奇妙な冒険 スターダストクルセイダース DIO](https://megahobby.jp/products/item/4942/)
- [ジョジョの奇妙な冒険 スターダストクルセイダース DIO【再販】](https://megahobby.jp/products/item/5749/)

```json
{
  "review_id": "R0210",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0211 — ジョジョの奇妙な冒険 スターダストクルセイダース 空条承太郎 (2개)

상품 ID: 738, 1146

- [ジョジョの奇妙な冒険 スターダストクルセイダース 空条承太郎](https://megahobby.jp/products/item/4943/)
- [ジョジョの奇妙な冒険 スターダストクルセイダース 空条承太郎【再販】](https://megahobby.jp/products/item/5750/)

```json
{
  "review_id": "R0211",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0212 — チェンソーマン パワー (2개)

상품 ID: 220, 768

- [チェンソーマン パワー](https://megahobby.jp/products/item/3847/)
- [チェンソーマン パワー【再販】](https://megahobby.jp/products/item/4992/)

```json
{
  "review_id": "R0212",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0213 — チェンソーマン マキマ (2개)

상품 ID: 225, 767

- [チェンソーマン マキマ](https://megahobby.jp/products/item/3857/)
- [チェンソーマン マキマ【再販】](https://megahobby.jp/products/item/4991/)

```json
{
  "review_id": "R0213",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0214 — デジモンアドベンチャー ガブモン (2개)

상품 ID: 251, 464

- [デジモンアドベンチャー ガブモン](https://megahobby.jp/products/item/3920/)
- [デジモンアドベンチャー ガブモン【再販】](https://megahobby.jp/products/item/4371/)

```json
{
  "review_id": "R0214",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0215 — デジモンアドベンチャー ゴマモン (2개)

상품 ID: 586, 6154

- [デジモンアドベンチャー ゴマモン](https://megahobby.jp/products/item/4618/)
- [デジモンアドベンチャー ゴマモン【再販】](https://megahobby.jp/products/item/6165/)

```json
{
  "review_id": "R0215",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0216 — デジモンアドベンチャー パタモン (2개)

상품 ID: 250, 463

- [デジモンアドベンチャー パタモン](https://megahobby.jp/products/item/3919/)
- [デジモンアドベンチャー パタモン【再販】](https://megahobby.jp/products/item/4370/)

```json
{
  "review_id": "R0216",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0217 — デジモンアドベンチャー ピヨモン (2개)

상품 ID: 585, 6153

- [デジモンアドベンチャー ピヨモン](https://megahobby.jp/products/item/4617/)
- [デジモンアドベンチャー ピヨモン【再販】](https://megahobby.jp/products/item/6166/)

```json
{
  "review_id": "R0217",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0218 — ハイキュ―!! てのひら影山飛雄 (2개)

상품 ID: 350, 601

- [ハイキュ―!! てのひら影山飛雄](https://megahobby.jp/products/item/4129/)
- [ハイキュ―!! てのひら影山飛雄【再販】](https://megahobby.jp/products/item/4657/)

```json
{
  "review_id": "R0218",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0219 — ハイキュ―!! 孤爪研磨 (2개)

상품 ID: 421, 923

- [ ハイキュ―!! 孤爪研磨](https://megahobby.jp/products/item/4289/)
- [ハイキュ―!! 孤爪研磨【再販】](https://megahobby.jp/products/item/5339/)

```json
{
  "review_id": "R0219",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0220 — ハイキュ―!! 影山飛雄 (2개)

상품 ID: 190, 762

- [ハイキュ―!! 影山飛雄](https://megahobby.jp/products/item/3748/)
- [ハイキュ―!! 影山飛雄【再販】](https://megahobby.jp/products/item/4985/)

```json
{
  "review_id": "R0220",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0221 — ハイキュ―!! 影山飛雄 ユニフォームVer. (2개)

상품 ID: 507, 1039

- [ハイキュ―!! 影山飛雄 ユニフォームVer.](https://megahobby.jp/products/item/4471/)
- [ハイキュ―!! 影山飛雄 ユニフォームVer.【再販】](https://megahobby.jp/products/item/5540/)

```json
{
  "review_id": "R0221",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0222 — ハイキュ―!! 日向翔陽 ユニフォームVer. (2개)

상품 ID: 508, 1038

- [ハイキュ―!! 日向翔陽 ユニフォームVer.](https://megahobby.jp/products/item/4472/)
- [ハイキュ―!! 日向翔陽 ユニフォームVer.【再販】](https://megahobby.jp/products/item/5539/)

```json
{
  "review_id": "R0222",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0223 — ハイキュ―!! 木兎光太郎 (2개)

상품 ID: 481, 1047

- [ハイキュ―!! 木兎光太郎](https://megahobby.jp/products/item/4403/)
- [ハイキュ―!! 木兎光太郎【再販】](https://megahobby.jp/products/item/5562/)

```json
{
  "review_id": "R0223",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0224 — ハイキュ―!! 赤葦京治 (2개)

상품 ID: 480, 1046

- [ハイキュ―!! 赤葦京治](https://megahobby.jp/products/item/4402/)
- [ハイキュ―!! 赤葦京治【再販】](https://megahobby.jp/products/item/5561/)

```json
{
  "review_id": "R0224",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0225 — ハイキュ―!! 黒尾鉄朗 (2개)

상품 ID: 422, 924

- [ハイキュ―!! 黒尾鉄朗](https://megahobby.jp/products/item/4290/)
- [ハイキュ―!! 黒尾鉄朗【再販】](https://megahobby.jp/products/item/5340/)

```json
{
  "review_id": "R0225",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0226 — ハイキュー!! (2개)

상품 ID: 609, 990

- [  ハイキュー!!](https://megahobby.jp/products/item/4665/)
- [ハイキュー‼](https://megahobby.jp/products/item/5442/)

```json
{
  "review_id": "R0226",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0227 — ハイキュー!! 及川徹 (2개)

상품 ID: 253, 994

- [ハイキュー!! 及川徹](https://megahobby.jp/products/item/3922/)
- [ハイキュー!! 及川 徹【再販】](https://megahobby.jp/products/item/5451/)

```json
{
  "review_id": "R0227",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0228 — ハイキュー!! 岩泉一 (2개)

상품 ID: 252, 995

- [ハイキュー!! 岩泉一](https://megahobby.jp/products/item/3921/)
- [ハイキュー!! 岩泉 一【再販】](https://megahobby.jp/products/item/5452/)

```json
{
  "review_id": "R0228",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0229 — ブルーロック 凪 誠士郎 (2개)

상품 ID: 238, 392

- [ブルーロック 凪 誠士郎](https://megahobby.jp/products/item/3888/)
- [ブルーロック 凪 誠士郎【再販】](https://megahobby.jp/products/item/4226/)

```json
{
  "review_id": "R0229",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0230 — ブルーロック 千切豹馬 (2개)

상품 ID: 239, 410

- [ブルーロック 千切豹馬](https://megahobby.jp/products/item/3889/)
- [ブルーロック 千切豹馬【再販】](https://megahobby.jp/products/item/4265/)

```json
{
  "review_id": "R0230",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0231 — ブルーロック 潔 世一 (2개)

상품 ID: 228, 393

- [ブルーロック 潔 世一](https://megahobby.jp/products/item/3860/)
- [ブルーロック 潔 世一【再販】](https://megahobby.jp/products/item/4227/)

```json
{
  "review_id": "R0231",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0232 — ブルーロック 糸師 冴 (2개)

상품 ID: 527, 992

- [ブルーロック 糸師 冴](https://megahobby.jp/products/item/4505/)
- [ブルーロック 糸師 冴【再販】](https://megahobby.jp/products/item/5449/)

```json
{
  "review_id": "R0232",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0233 — ブルーロック 蜂楽 廻 (2개)

상품 ID: 227, 408

- [ブルーロック 蜂楽 廻](https://megahobby.jp/products/item/3859/)
- [ブルーロック 蜂楽 廻【再販】](https://megahobby.jp/products/item/4263/)

```json
{
  "review_id": "R0233",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0234 — ポンチョ ハイキュー!! カゲガラス (2개)

상품 ID: 764, 1254

- [ポンチョ  ハイキュー!!  カゲガラス](https://megahobby.jp/products/item/4987/)
- [ポンチョ ハイキュー!! カゲガラス【再販】](https://megahobby.jp/products/item/5937/)

```json
{
  "review_id": "R0234",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0235 — ポンチョ ハイキュー!! クロオネコ (2개)

상품 ID: 913, 1211

- [ポンチョ  ハイキュー!!  クロオネコ](https://megahobby.jp/products/item/5329/)
- [ポンチョ  ハイキュー!!  クロオネコ【再販】](https://megahobby.jp/products/item/5845/)

```json
{
  "review_id": "R0235",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0236 — ポンチョ ハイキュー!! ケンマネコ (2개)

상품 ID: 912, 1210

- [ポンチョ ハイキュー!! ケンマネコ](https://megahobby.jp/products/item/5328/)
- [ポンチョ  ハイキュー!!  ケンマネコ【再販】](https://megahobby.jp/products/item/5844/)

```json
{
  "review_id": "R0236",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0237 — ポンチョ ハイキュー!! ヒナガラス (2개)

상품 ID: 765, 1255

- [ポンチョ  ハイキュー!!  ヒナガラス](https://megahobby.jp/products/item/4988/)
- [ポンチョ ハイキュー!! ヒナガラス【再販】](https://megahobby.jp/products/item/5938/)

```json
{
  "review_id": "R0237",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0238 — マシンビルドシリーズ マシンロボ クロノスの大逆襲 バイクロボ (2개)

상품 ID: 224, 425

- [マシンビルドシリーズ　 マシンロボ　クロノスの大逆襲　 バイクロボ](https://megahobby.jp/products/item/3856/)
- [マシンビルドシリーズ マシンロボ　クロノスの大逆襲 バイクロボ【再販】](https://megahobby.jp/products/item/4300/)

```json
{
  "review_id": "R0238",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0239 — マシンビルドシリーズ 機動戦士ガンダム バストライナー (2개)

상품 ID: 328, 658

- [マシンビルドシリーズ 機動戦士ガンダム バストライナー](https://megahobby.jp/products/item/4082/)
- [マシンビルドシリーズ 機動戦士ガンダム バストライナー【再販】](https://megahobby.jp/products/item/4780/)

```json
{
  "review_id": "R0239",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0240 — マスコット ハイキュー!! Vol.1 (2개)

상품 ID: 179, 462

- [マスコット ハイキュー!!　Vol.1](https://megahobby.jp/products/item/3723/)
- [マスコット ハイキュー!! vol.1【再販】](https://megahobby.jp/products/item/4369/)

```json
{
  "review_id": "R0240",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0241 — マスコット ハイキュー!! Vol.2 (2개)

상품 ID: 218, 477

- [マスコット ハイキュー!! Vol.2](https://megahobby.jp/products/item/3836/)
- [マスコット ハイキュー!! vol.2【再販】](https://megahobby.jp/products/item/4399/)

```json
{
  "review_id": "R0241",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0242 — ミニチュアコレクション 呪術廻戦 (2개)

상품 ID: 911, 1206

- [ミニチュアコレクション 呪術廻戦](https://megahobby.jp/products/item/5327/)
- [ミニチュアコレクション  呪術廻戦【再販】](https://megahobby.jp/products/item/5840/)

```json
{
  "review_id": "R0242",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0243 — メイドインアビス 烈日の黄金郷 ナナチ (2개)

상품 ID: 368, 1142

- [メイドインアビス 烈日の黄金郷 ナナチ](https://megahobby.jp/products/item/4171/)
- [メイドインアビス 烈日の黄金郷 ナナチ【再販】](https://megahobby.jp/products/item/5746/)

```json
{
  "review_id": "R0243",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0244 — モブサイコ100 Ⅲ 影山茂夫 (2개)

상품 ID: 402, 996

- [モブサイコ100 Ⅲ 影山茂夫](https://megahobby.jp/products/item/4236/)
- [モブサイコ100 Ⅲ 影山茂夫【再販】](https://megahobby.jp/products/item/5453/)

```json
{
  "review_id": "R0244",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0245 — モブサイコ100 Ⅲ 霊幻新隆 (2개)

상품 ID: 397, 997

- [モブサイコ100 Ⅲ 霊幻新隆](https://megahobby.jp/products/item/4231/)
- [モブサイコ100 Ⅲ 霊幻新隆【再販】](https://megahobby.jp/products/item/5454/)

```json
{
  "review_id": "R0245",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0246 — ワンピース おやすみニャンピースニャーン！編 (2개)

상품 ID: 704, 998

- [ワンピース おやすみニャンピースニャーン！編](https://megahobby.jp/products/item/4863/)
- [ワンピース おやすみニャンピースニャーン！編【再販】](https://megahobby.jp/products/item/5455/)

```json
{
  "review_id": "R0246",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0247 — ワンピース グランドラインコレクション (2개)

상품 ID: 707, 999

- [ワンピース グランドラインコレクション](https://megahobby.jp/products/item/4866/)
- [ワンピース グランドラインコレクション【再販】](https://megahobby.jp/products/item/5456/)

```json
{
  "review_id": "R0247",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0248 — ワンピース ニャンピースニャーン！ ルフィとワノ国編でござる (2개)

상품 ID: 248, 542

- [ワンピース ニャンピースニャーン！　ルフィとワノ国編でござる](https://megahobby.jp/products/item/3916/)
- [ワンピース ニャンピースニャーン！　ルフィとワノ国編でござる【再販】](https://megahobby.jp/products/item/4541/)

```json
{
  "review_id": "R0248",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0249 — ワンピース ニャンピースニャーン！ ルフィと好敵手編 (2개)

상품 ID: 183, 456

- [ワンピース ニャンピースニャーン！　ルフィと好敵手編](https://megahobby.jp/products/item/3731/)
- [ワンピース ニャンピースニャーン！　ルフィと好敵手編【再販】](https://megahobby.jp/products/item/4344/)

```json
{
  "review_id": "R0249",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0250 — ワンピース ニャンピースニャーン！ ルフィと王下七武海 (2개)

상품 ID: 407, 1208

- [ワンピース ニャンピースニャーン！　ルフィと王下七武海](https://megahobby.jp/products/item/4262/)
- [ワンピース ニャンピースニャーン！　ルフィと王下七武海【再販】](https://megahobby.jp/products/item/5842/)

```json
{
  "review_id": "R0250",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0251 — ヱヴァンゲリヲン新劇場版 式波・アスカ・ラングレー (2개)

상품 ID: 445, 681

- [ヱヴァンゲリヲン新劇場版 式波・アスカ・ラングレー](https://megahobby.jp/products/item/4333/)
- [ヱヴァンゲリヲン新劇場版 式波・アスカ・ラングレー【再販】](https://megahobby.jp/products/item/4823/)

```json
{
  "review_id": "R0251",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0252 — ヱヴァンゲリヲン新劇場版 渚カヲル (2개)

상품 ID: 174, 1143

- [ヱヴァンゲリヲン新劇場版 渚カヲル](https://megahobby.jp/products/item/3700/)
- [ヱヴァンゲリヲン新劇場版 渚カヲル【再販】](https://megahobby.jp/products/item/5747/)

```json
{
  "review_id": "R0252",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0253 — ヱヴァンゲリヲン新劇場版 碇シンジ (2개)

상품 ID: 173, 1144

- [ヱヴァンゲリヲン新劇場版 碇シンジ](https://megahobby.jp/products/item/3699/)
- [ヱヴァンゲリヲン新劇場版 碇シンジ【再販】](https://megahobby.jp/products/item/5748/)

```json
{
  "review_id": "R0253",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0254 — ヱヴァンゲリヲン新劇場版 綾波レイ (2개)

상품 ID: 446, 682

- [ヱヴァンゲリヲン新劇場版 綾波レイ](https://megahobby.jp/products/item/4334/)
- [ヱヴァンゲリヲン新劇場版 綾波レイ【再販】](https://megahobby.jp/products/item/4824/)

```json
{
  "review_id": "R0254",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0255 — 僕のヒーローアカデミア トガヒミコ (2개)

상품 ID: 687, 1214

- [僕のヒーローアカデミア トガヒミコ](https://megahobby.jp/products/item/4829/)
- [僕のヒーローアカデミア トガヒミコ【再販】](https://megahobby.jp/products/item/5848/)

```json
{
  "review_id": "R0255",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0256 — 僕のヒーローアカデミア ヒロアカニャンコNO.01 (2개)

상품 ID: 806, 1136

- [僕のヒーローアカデミア ヒロアカニャンコNO.01](https://megahobby.jp/products/item/5055/)
- [僕のヒーローアカデミア ヒロアカニャンコNO.01【再販】](https://megahobby.jp/products/item/5740/)

```json
{
  "review_id": "R0256",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0257 — 僕のヒーローアカデミア 爆豪勝己 (2개)

상품 ID: 414, 639

- [ 僕のヒーローアカデミア 爆豪勝己](https://megahobby.jp/products/item/4269/)
- [僕のヒーローアカデミア 爆豪勝己【再販】](https://megahobby.jp/products/item/4697/)

```json
{
  "review_id": "R0257",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0258 — 僕のヒーローアカデミア 緑谷出久 (2개)

상품 ID: 416, 638

- [ 僕のヒーローアカデミア 緑谷出久](https://megahobby.jp/products/item/4271/)
- [僕のヒーローアカデミア 緑谷出久【再販】](https://megahobby.jp/products/item/4696/)

```json
{
  "review_id": "R0258",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0259 — 僕のヒーローアカデミア 轟焦凍 (2개)

상품 ID: 468, 659

- [僕のヒーローアカデミア 轟焦凍](https://megahobby.jp/products/item/4375/)
- [僕のヒーローアカデミア 轟焦凍【再販】](https://megahobby.jp/products/item/4781/)

```json
{
  "review_id": "R0259",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0260 — 初音ミク (2개)

상품 ID: 903, 1283

- [初音ミク](https://megahobby.jp/products/item/5319/)
- [初音ミク【再販】](https://megahobby.jp/products/item/6000/)

```json
{
  "review_id": "R0260",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0261 — 劇場版『チェンソーマン レゼ篇』 レゼ (2개)

상품 ID: 840, 1287

- [劇場版『チェンソーマン レゼ篇』 レゼ](https://megahobby.jp/products/item/5182/)
- [劇場版『チェンソーマン レゼ篇』 レゼ【再販】](https://megahobby.jp/products/item/6004/)

```json
{
  "review_id": "R0261",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0262 — 呪術廻戦 (2개)

상품 ID: 610, 640

- [  呪術廻戦](https://megahobby.jp/products/item/4666/)
- [呪術廻戦【再販】](https://megahobby.jp/products/item/4698/)

```json
{
  "review_id": "R0262",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0263 — 呪術廻戦 七海建人 (2개)

상품 ID: 492, 1370

- [呪術廻戦 七海建人【再販】](https://megahobby.jp/products/item/4425/)
- [呪術廻戦　七海建人](https://www.megahobby.jp/products/item/3720/)

```json
{
  "review_id": "R0263",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0264 — 呪術廻戦 五条悟 高専ver. (2개)

상품 ID: 342, 524

- [呪術廻戦 五条悟 高専ver.](https://megahobby.jp/products/item/4121/)
- [呪術廻戦 五条悟 高専ver.【再販】](https://megahobby.jp/products/item/4502/)

```json
{
  "review_id": "R0264",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0265 — 呪術廻戦 伏黒甚爾 (2개)

상품 ID: 365, 662

- [呪術廻戦　伏黒甚爾](https://megahobby.jp/products/item/4168/)
- [呪術廻戦 伏黒甚爾【再販】](https://megahobby.jp/products/item/4784/)

```json
{
  "review_id": "R0265",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0266 — 呪術廻戦 呪術ニャンコ 懐玉・玉折 (2개)

상품 ID: 621, 1209

- [呪術廻戦 呪術ニャンコ　懐玉・玉折](https://megahobby.jp/products/item/4678/)
- [呪術廻戦 呪術ニャンコ　懐玉・玉折　【再販】](https://megahobby.jp/products/item/5843/)

```json
{
  "review_id": "R0266",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0267 — 呪術廻戦 呪術ニャンコ 渋谷事変 (2개)

상품 ID: 718, 1200

- [呪術廻戦 呪術ニャンコ　渋谷事変](https://megahobby.jp/products/item/4898/)
- [呪術廻戦 呪術ニャンコ 渋谷事変【再販】](https://megahobby.jp/products/item/5831/)

```json
{
  "review_id": "R0267",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0268 — 呪術廻戦 夏油傑 高専ver. (2개)

상품 ID: 341, 523

- [呪術廻戦 夏油傑 高専ver.](https://megahobby.jp/products/item/4120/)
- [呪術廻戦 夏油傑 高専ver.【再販】](https://megahobby.jp/products/item/4501/)

```json
{
  "review_id": "R0268",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0269 — 呪術廻戦 脹相 (2개)

상품 ID: 710, 1107

- [呪術廻戦 脹相](https://megahobby.jp/products/item/4870/)
- [呪術廻戦 脹相【再販】](https://megahobby.jp/products/item/5690/)

```json
{
  "review_id": "R0269",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0270 — 怪獣８号 保科宗四郎 (2개)

상품 ID: 530, 846

- [怪獣８号 保科宗四郎](https://megahobby.jp/products/item/4508/)
- [怪獣8号 保科宗四郎【再販】](https://megahobby.jp/products/item/5214/)

```json
{
  "review_id": "R0270",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0271 — 怪獣８号 古橋伊春 (2개)

상품 ID: 555, 921

- [怪獣８号 古橋伊春](https://megahobby.jp/products/item/4554/)
- [怪獣8号 古橋伊春【再販】](https://megahobby.jp/products/item/5337/)

```json
{
  "review_id": "R0271",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0272 — 怪獣８号 市川レノ (2개)

상품 ID: 556, 922

- [怪獣８号 市川レノ](https://megahobby.jp/products/item/4555/)
- [怪獣8号 市川レノ【再販】](https://megahobby.jp/products/item/5338/)

```json
{
  "review_id": "R0272",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0273 — 怪獣８号 日比野カフカ (2개)

상품 ID: 531, 847

- [怪獣８号 日比野カフカ](https://megahobby.jp/products/item/4509/)
- [怪獣8号 日比野カフカ【再販】](https://megahobby.jp/products/item/5215/)

```json
{
  "review_id": "R0273",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0274 — 映画「鬼太郎誕生 ゲゲゲの謎」 水木 (2개)

상품 ID: 618, 929

- [映画「鬼太郎誕生 ゲゲゲの謎」 水木](https://megahobby.jp/products/item/4675/)
- [映画「鬼太郎誕生 ゲゲゲの謎」 水木【再販】](https://megahobby.jp/products/item/5377/)

```json
{
  "review_id": "R0274",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0275 — 映画「鬼太郎誕生 ゲゲゲの謎」 鬼太郎の父 (2개)

상품 ID: 619, 930

- [映画「鬼太郎誕生 ゲゲゲの謎」 鬼太郎の父](https://megahobby.jp/products/item/4676/)
- [映画「鬼太郎誕生 ゲゲゲの謎」 鬼太郎の父【再販】](https://megahobby.jp/products/item/5378/)

```json
{
  "review_id": "R0275",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0276 — 機動戦士ガンダムSEED FREEDOM アスラン・ザラ (2개)

상품 ID: 635, 848

- [機動戦士ガンダムSEED FREEDOM  アスラン・ザラ](https://megahobby.jp/products/item/4693/)
- [機動戦士ガンダムSEED FREEDOM アスラン・ザラ【再販】](https://megahobby.jp/products/item/5216/)

```json
{
  "review_id": "R0276",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0277 — 機動戦士ガンダムSEED FREEDOM キラ・ヤマト (2개)

상품 ID: 636, 849

- [機動戦士ガンダムSEED FREEDOM  キラ・ヤマト](https://megahobby.jp/products/item/4694/)
- [機動戦士ガンダムSEED FREEDOM キラ・ヤマト【再販】](https://megahobby.jp/products/item/5217/)

```json
{
  "review_id": "R0277",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0278 — 機動戦士ガンダムUC ネェル・アーガマRe. (2개)

상품 ID: 386, 1289

- [機動戦士ガンダムUC ネェル・アーガマRe.](https://megahobby.jp/products/item/4220/)
- [機動戦士ガンダムUC ネェル・アーガマRe.【再販】](https://megahobby.jp/products/item/6006/)

```json
{
  "review_id": "R0278",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0279 — 機動戦士ガンダム セイラ・マス ～休息～ (2개)

상품 ID: 352, 1217

- [機動戦士ガンダム セイラ・マス ～休息～](https://megahobby.jp/products/item/4131/)
- [機動戦士ガンダム セイラ・マス～休息～【再販】](https://megahobby.jp/products/item/5851/)

```json
{
  "review_id": "R0279",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0280 — 無職転生 ～異世界行ったら本気だす～ てのひら ロキシー (2개)

상품 ID: 403, 792

- [　無職転生 ～異世界行ったら本気だす～ てのひら ロキシー](https://megahobby.jp/products/item/4258/)
- [無職転生 ～異世界行ったら本気だす～ てのひら ロキシー 【再販】](https://megahobby.jp/products/item/5041/)

```json
{
  "review_id": "R0280",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0281 — 犬夜叉 殺生丸 (2개)

상품 ID: 965, 6143

- [犬夜叉 殺生丸](https://megahobby.jp/products/item/5413/)
- [犬夜叉 殺生丸【再販】](https://megahobby.jp/products/item/6163/)

```json
{
  "review_id": "R0281",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0282 — 犬夜叉 犬夜叉 (2개)

상품 ID: 966, 6142

- [犬夜叉 犬夜叉](https://megahobby.jp/products/item/5414/)
- [犬夜叉 犬夜叉【再販】](https://megahobby.jp/products/item/6164/)

```json
{
  "review_id": "R0282",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0283 — 葬送のフリーレン フリーレン (2개)

상품 ID: 472, 1286

- [葬送のフリーレン フリーレン](https://megahobby.jp/products/item/4379/)
- [葬送のフリーレン フリーレン【再販】](https://megahobby.jp/products/item/6003/)

```json
{
  "review_id": "R0283",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0284 — 薬屋のひとりごと 宮中CATS 薬屋のひとりごニャ！ (2개)

상품 ID: 781, 1134

- [薬屋のひとりごと 宮中CATS　薬屋のひとりごニャ！](https://megahobby.jp/products/item/5005/)
- [薬屋のひとりごと 宮中CATS　薬屋のひとりごニャ！【再販】](https://megahobby.jp/products/item/5738/)

```json
{
  "review_id": "R0284",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0285 — 進撃の巨人 進撃のニャンコ 調査兵団集合だニャン！ (2개)

상품 ID: 191, 461

- [進撃の巨人 進撃のニャンコ　調査兵団集合だニャン！](https://megahobby.jp/products/item/3750/)
- [進撃の巨人 進撃のニャンコ　調査兵団集合だニャン！【再販】](https://megahobby.jp/products/item/4368/)

```json
{
  "review_id": "R0285",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0286 — 銀魂 (2개)

상품 ID: 667, 941

- [  銀魂](https://megahobby.jp/products/item/4789/)
- [銀魂](https://megahobby.jp/products/item/5389/)

```json
{
  "review_id": "R0286",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0287 — 銀魂 にゃん魂 ニャンニャンいっちゃうぜコノヤロー編 (2개)

상품 ID: 949, 1282

- [銀魂 にゃん魂 ニャンニャンいっちゃうぜコノヤロー編](https://megahobby.jp/products/item/5397/)
- [銀魂 にゃん魂 ニャンニャンいっちゃうぜコノヤロー編【再販】](https://megahobby.jp/products/item/5997/)

```json
{
  "review_id": "R0287",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0288 — 銀魂 土方十四郎 (2개)

상품 ID: 511, 746

- [銀魂 土方十四郎](https://megahobby.jp/products/item/4475/)
- [銀魂 土方十四郎【再販】](https://megahobby.jp/products/item/4964/)

```json
{
  "review_id": "R0288",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0289 — 銀魂 坂田銀時 (2개)

상품 ID: 512, 747

- [銀魂 坂田銀時](https://megahobby.jp/products/item/4476/)
- [銀魂 坂田銀時【再販】](https://megahobby.jp/products/item/4965/)

```json
{
  "review_id": "R0289",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0290 — 銀魂 沖田総悟 (2개)

상품 ID: 713, 1284

- [銀魂 沖田総悟](https://megahobby.jp/products/item/4873/)
- [銀魂 沖田総悟【再販】](https://megahobby.jp/products/item/6001/)

```json
{
  "review_id": "R0290",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0291 — 銀魂 神楽 (2개)

상품 ID: 714, 1285

- [銀魂 神楽](https://megahobby.jp/products/item/4874/)
- [銀魂 神楽【再販】](https://megahobby.jp/products/item/6002/)

```json
{
  "review_id": "R0291",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0292 — 鬼滅の刃 てのひら不死川さん (2개)

상품 ID: 211, 1034

- [鬼滅の刃 てのひら不死川さん](https://megahobby.jp/products/item/3814/)
- [鬼滅の刃 てのひら不死川さん【再販】](https://megahobby.jp/products/item/5535/)

```json
{
  "review_id": "R0292",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0293 — 鬼滅の刃 てのひら伊黒さん (2개)

상품 ID: 206, 1051

- [鬼滅の刃 てのひら伊黒さん](https://megahobby.jp/products/item/3794/)
- [鬼滅の刃 てのひら伊黒さん【再販】](https://megahobby.jp/products/item/5566/)

```json
{
  "review_id": "R0293",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0294 — 鬼滅の刃 てのひら時透さん (2개)

상품 ID: 170, 1005

- [鬼滅の刃 てのひら時透さん](https://megahobby.jp/products/item/3696/)
- [鬼滅の刃 てのひら時透さん【再販】](https://megahobby.jp/products/item/5484/)

```json
{
  "review_id": "R0294",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0295 — 鬼滅の刃 てのひら甘露寺さん (2개)

상품 ID: 217, 329

- [鬼滅の刃 てのひら甘露寺さん](https://megahobby.jp/products/item/3835/)
- [鬼滅の刃 てのひら甘露寺さん【再販】](https://megahobby.jp/products/item/4098/)

```json
{
  "review_id": "R0295",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0296 — 鬼滅の刃 冨岡義勇 きょとんver. (2개)

상품 ID: 552, 1048

- [鬼滅の刃 冨岡義勇 きょとんver.](https://megahobby.jp/products/item/4551/)
- [鬼滅の刃 冨岡義勇 きょとんver.【再販】](https://megahobby.jp/products/item/5563/)

```json
{
  "review_id": "R0296",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0297 — 鬼滅の刃 嘴平伊之助 むん！ver. (2개)

상품 ID: 525, 1105

- [鬼滅の刃 嘴平伊之助 むん！ver.](https://megahobby.jp/products/item/4503/)
- [鬼滅の刃 嘴平伊之助　むん！ver.【再販】](https://megahobby.jp/products/item/5688/)

```json
{
  "review_id": "R0297",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0298 — 鬼滅の刃 悲鳴嶼行冥 (2개)

상품 ID: 144, 850

- [鬼滅の刃 悲鳴嶼行冥](https://megahobby.jp/products/item/3630/)
- [鬼滅の刃 悲鳴嶼行冥【再販】](https://megahobby.jp/products/item/5218/)

```json
{
  "review_id": "R0298",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0299 — 鬼滅の刃 我妻善逸 にこっとver. (2개)

상품 ID: 526, 1000

- [鬼滅の刃 我妻善逸 にこっとver.](https://megahobby.jp/products/item/4504/)
- [鬼滅の刃 我妻善逸 にこっとver.【再販】](https://megahobby.jp/products/item/5479/)

```json
{
  "review_id": "R0299",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0300 — 鬼滅の刃 時透無一郎 ほほえみver. (2개)

상품 ID: 551, 1049

- [鬼滅の刃 時透無一郎 ほほえみver.](https://megahobby.jp/products/item/4550/)
- [鬼滅の刃 時透無一郎　ほほえみver.【再販】](https://megahobby.jp/products/item/5564/)

```json
{
  "review_id": "R0300",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0301 — 鬼滅の刃 煉獄杏寿郎 にっこりver. (2개)

상품 ID: 582, 1050

- [鬼滅の刃 煉獄杏寿郎　にっこりver.](https://megahobby.jp/products/item/4614/)
- [鬼滅の刃 煉獄杏寿郎 にっこりver.【再販】](https://megahobby.jp/products/item/5565/)

```json
{
  "review_id": "R0301",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0302 — 鬼滅の刃 真菰 (2개)

상품 ID: 153, 1037

- [鬼滅の刃 真菰](https://megahobby.jp/products/item/3659/)
- [鬼滅の刃 真菰【再販】](https://megahobby.jp/products/item/5538/)

```json
{
  "review_id": "R0302",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0303 — 鬼滅の刃 童磨 (2개)

상품 ID: 958, 1216

- [鬼滅の刃 童磨](https://megahobby.jp/products/item/5406/)
- [鬼滅の刃 童磨【再販】](https://megahobby.jp/products/item/5850/)

```json
{
  "review_id": "R0303",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0304 — 鬼滅の刃 錆兎 (2개)

상품 ID: 154, 1036

- [鬼滅の刃 錆兎](https://megahobby.jp/products/item/3660/)
- [鬼滅の刃 錆兎【再販】](https://megahobby.jp/products/item/5537/)

```json
{
  "review_id": "R0304",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0305 — 맨후드 스페셜VER. (A:골 D 로저) (2개)

상품 ID: 3997, 4442

- [원피스 맨후드 스페셜VER. (A:골 D 로저)](https://www.bnkrmall.co.kr/goods/detail.do?gno=77844194)
- [원피스 맨후드 스페셜VER. (A:골 D 로저)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59222)

```json
{
  "review_id": "R0305",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0306 — 맨후드 스페셜VER. (B:에드워드 뉴게이트) (2개)

상품 ID: 3996, 4441

- [원피스 맨후드 스페셜VER. (B:에드워드 뉴게이트)](https://www.bnkrmall.co.kr/goods/detail.do?gno=70359348)
- [원피스 맨후드 스페셜VER. (B:에드워드 뉴게이트)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59223)

```json
{
  "review_id": "R0306",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0307 — 브레이크 타임 콜렉션 VOL.2 (2개)

상품 ID: 3282, 4467

- [약사의 혼잣말 브레이크 타임 콜렉션 VOL.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=63118445)
- [나의 히어로 아카데미아 브레이크 타임 콜렉션 VOL.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=58824)

```json
{
  "review_id": "R0307",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0308 — 브레이크 타임 콜렉션 VOL.3 (2개)

상품 ID: 4084, 4440

- [체인소 맨 브레이크 타임 콜렉션 VOL.3](https://www.bnkrmall.co.kr/goods/detail.do?gno=70527249)
- [나의 히어로 아카데미아 브레이크 타임 콜렉션 VOL.3](https://www.bnkrmall.co.kr/goods/detail.do?gno=59224)

```json
{
  "review_id": "R0308",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0309 — 전광절경 몽키 D 루피 (2개)

상품 ID: 3423, 4241

- [원피스 전광절경 몽키 D 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=53346767)
- [원피스 전광절경 몽키 D 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=83453771)

```json
{
  "review_id": "R0309",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0310 — 초사이어인4 손오공 (2개)

상품 ID: 3909, 4689

- [드래곤볼 DAIMA 초사이어인4 손오공 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=98220994)
- [드래곤볼 GT 초사이어인4 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=15605)

```json
{
  "review_id": "R0310",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0311 — 콤비네이션 배틀2 우치하 사스케 (2개)

상품 ID: 3644, 3841

- [나루토 질풍전 콤비네이션 배틀2 우치하 사스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=15757706)
- [나루토 콤비네이션 배틀2 우치하 사스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=7214787)

```json
{
  "review_id": "R0311",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0312 — 콤비네이션 배틀 우치하 사스케 (2개)

상품 ID: 3724, 4085

- [나루토 질풍전 콤비네이션 배틀 우치하 사스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=77267464)
- [나루토 콤비네이션 배틀 우치하 사스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=35373403)

```json
{
  "review_id": "R0312",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R0313 — 히스토리 박스 손오공 (2개)

상품 ID: 3535, 3947

- [드래곤볼 히스토리 박스 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=559760)
- [드래곤볼 Z 히스토리 박스 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=9685259)

```json
{
  "review_id": "R0313",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2801 — #1 사이타마 (1개)

상품 ID: 4328

- [원펀맨 피규어#1 사이타마](https://www.bnkrmall.co.kr/goods/detail.do?gno=77486817)

```json
{
  "review_id": "R2801",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2802 — #5 전율의 타츠마키 (1개)

상품 ID: 4169

- [원펀맨 피규어#5 전율의 타츠마키](https://www.bnkrmall.co.kr/goods/detail.do?gno=89591873)

```json
{
  "review_id": "R2802",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2803 — #6 전율의 지옥의 후부키 (1개)

상품 ID: 4168

- [원펀맨 피규어#6 전율의 지옥의 후부키](https://www.bnkrmall.co.kr/goods/detail.do?gno=76150811)

```json
{
  "review_id": "R2803",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2804 — ＇녀석들아 잔치다!＇나미 (1개)

상품 ID: 4262

- [원피스 ＇녀석들아 잔치다!＇나미](https://www.bnkrmall.co.kr/goods/detail.do?gno=18127927)

```json
{
  "review_id": "R2804",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2805 — (ガンダムミリタリージェネレーション） 機動戦士ガンダム ジオン公国軍V-01 ジオン兵専用バイク (1개)

상품 ID: 137

- [(ガンダムミリタリージェネレーション） 機動戦士ガンダム ジオン公国軍V-01 ジオン兵専用バイク](https://megahobby.jp/products/item/3602/)

```json
{
  "review_id": "R2805",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2806 — (ガンダムミリタリージェネレーション） 機動戦士ガンダム 地球連邦軍 V-01 地球連邦軍専用バギー (1개)

상품 ID: 216

- [(ガンダムミリタリージェネレーション） 機動戦士ガンダム 地球連邦軍 V-01　地球連邦軍専用バギー](https://megahobby.jp/products/item/3834/)

```json
{
  "review_id": "R2806",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2807 — (ガンダムミリタリージェネレーション） 機動戦士ガンダム 第08MS小隊 地球連邦軍V-02 連邦兵専用バイク (1개)

상품 ID: 266

- [(ガンダムミリタリージェネレーション） 機動戦士ガンダム 第08MS小隊 地球連邦軍V-02 連邦兵専用バイク](https://megahobby.jp/products/item/3953/)

```json
{
  "review_id": "R2807",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2808 — (ガンダムミリタリージェネレーション） 機動戦士ガンダム 第08MS小隊 地球連邦軍V-SP09 一般兵士＆連邦兵専用バイク (1개)

상품 ID: 267

- [(ガンダムミリタリージェネレーション） 機動戦士ガンダム 第08MS小隊 地球連邦軍V-SP09 一般兵士＆連邦兵専用バイク](https://megahobby.jp/products/item/3954/)

```json
{
  "review_id": "R2808",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2809 — 02 SOFVIMATES 브이몬 (1개)

상품 ID: 3387

- [디지몬 어드벤처 02 SOFVIMATES 브이몬](https://www.bnkrmall.co.kr/goods/detail.do?gno=46131839)

```json
{
  "review_id": "R2809",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2810 — 2ndLAP 新世紀GPXサイバーフォーミュラ11 スーパーアスラーダSA-01/C (1개)

상품 ID: 1352

- [2ndLAP 新世紀GPXサイバーフォーミュラ11  スーパーアスラーダSA-01/C](https://megahobby.jp/products/item/6080/)

```json
{
  "review_id": "R2810",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2811 — 2ndLAP 新世紀GPXサイバーフォーミュラ スーパーアスラーダ01 Ver.2 (1개)

상품 ID: 349

- [2ndLAP 新世紀GPXサイバーフォーミュラ スーパーアスラーダ01 Ver.2](https://megahobby.jp/products/item/4128/)

```json
{
  "review_id": "R2811",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2812 — 3年Z組銀八先生 土方十四郎 (1개)

상품 ID: 906

- [3年Z組銀八先生 土方十四郎](https://megahobby.jp/products/item/5322/)

```json
{
  "review_id": "R2812",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2813 — 3年Z組銀八先生 坂田銀八 (1개)

상품 ID: 905

- [3年Z組銀八先生 坂田銀八](https://megahobby.jp/products/item/5321/)

```json
{
  "review_id": "R2813",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2814 — 3年Z組銀八先生 沖田総悟 (1개)

상품 ID: 978

- [3年Z組銀八先生 沖田総悟](https://megahobby.jp/products/item/5430/)

```json
{
  "review_id": "R2814",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2815 — 3年Z組銀八先生 神威 (1개)

상품 ID: 1028

- [3年Z組銀八先生 神威](https://megahobby.jp/products/item/5529/)

```json
{
  "review_id": "R2815",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2816 — 3年Z組銀八先生 神楽 (1개)

상품 ID: 979

- [3年Z組銀八先生 神楽](https://megahobby.jp/products/item/5431/)

```json
{
  "review_id": "R2816",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2817 — 3年Z組銀八先生 高杉晋助 (1개)

상품 ID: 1027

- [3年Z組銀八先生 高杉晋助](https://megahobby.jp/products/item/5528/)

```json
{
  "review_id": "R2817",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2818 — 3학년 Z반 긴파치 선생 데스크 오키타 소고 (1개)

상품 ID: 1896

- [은혼 3학년 Z반 긴파치 선생 데스크 피규어 오키타 소고](https://www.bnkrmall.co.kr/goods/detail.do?gno=79464829)

```json
{
  "review_id": "R2818",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2819 — 72 series- 03 우즈마키 나루토&하타케 카카시 (A:우즈마키 나루토) (1개)

상품 ID: 3529

- [-나루토 72 series- 03 우즈마키 나루토&하타케 카카시 (A:우즈마키 나루토)](https://www.bnkrmall.co.kr/goods/detail.do?gno=24265658)

```json
{
  "review_id": "R2819",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2820 — 72 series- 03 우즈마키 나루토&하타케 카카시 (B:하타케 카카시) (1개)

상품 ID: 3528

- [-나루토 72 series- 03 우즈마키 나루토&하타케 카카시 (B:하타케 카카시)](https://www.bnkrmall.co.kr/goods/detail.do?gno=28403628)

```json
{
  "review_id": "R2820",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2821 — 72 series- 16 우즈마키 나루토&우미노 이루카 (A:우즈마키 나루토) (1개)

상품 ID: 3629

- [-나루토 72 series- 16 우즈마키 나루토&우미노 이루카 (A:우즈마키 나루토)](https://www.bnkrmall.co.kr/goods/detail.do?gno=89672717)

```json
{
  "review_id": "R2821",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2822 — 72 series- 16 우즈마키 나루토&우미노 이루카 (B:우미노 이루카) (1개)

상품 ID: 3628

- [-나루토 72 series- 16 우즈마키 나루토&우미노 이루카 (B:우미노 이루카)](https://www.bnkrmall.co.kr/goods/detail.do?gno=66839271)

```json
{
  "review_id": "R2822",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2823 — 72 series- 19 인계조형열전 우즈마키 나루토 (1개)

상품 ID: 3509

- [-나루토 72 series- 19 인계조형열전 우즈마키 나루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=89100675)

```json
{
  "review_id": "R2823",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2824 — 72 series- 53 (1개)

상품 ID: 3463

- [-나루토 72 series- 53 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=62356322)

```json
{
  "review_id": "R2824",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2825 — 72 series- 72 우즈마키 나루토 (1개)

상품 ID: 3462

- [-나루토 72 series- 72 우즈마키 나루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=28300357)

```json
{
  "review_id": "R2825",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2826 — 7기 미도리아 이즈쿠 (1개)

상품 ID: 4215

- [나의 히어로 아카데미아 7기 피규어 미도리아 이즈쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=2149457)

```json
{
  "review_id": "R2826",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2827 — [THE METALLIC] (1개)

상품 ID: 4108

- [괴수 8호 (THE METALLIC)](https://www.bnkrmall.co.kr/goods/detail.do?gno=78446685)

```json
{
  "review_id": "R2827",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2828 — ABSOLUTE ACT 스트라이크 프리덤 건담 (1개)

상품 ID: 1668

- [ABSOLUTE ACT 스트라이크 프리덤 건담](https://www.bnkrmall.co.kr/goods/detail.do?gno=51738854)

```json
{
  "review_id": "R2828",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2829 — Adokenette 루비 (1개)

상품 ID: 2004

- [Adokenette 루비](https://www.bnkrmall.co.kr/goods/detail.do?gno=68739272)

```json
{
  "review_id": "R2829",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2830 — Adokenette 미도리야 이즈쿠 (1개)

상품 ID: 1764

- [Adokenette 미도리야 이즈쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=71156908)

```json
{
  "review_id": "R2830",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2831 — Adokenette 바쿠고 카츠키 (1개)

상품 ID: 1765

- [Adokenette 바쿠고 카츠키](https://www.bnkrmall.co.kr/goods/detail.do?gno=12202172)

```json
{
  "review_id": "R2831",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2832 — Adokenette 아리마 카나 (1개)

상품 ID: 2002

- [Adokenette 아리마 카나](https://www.bnkrmall.co.kr/goods/detail.do?gno=6754806)

```json
{
  "review_id": "R2832",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2833 — Adokenette 아쿠아 (1개)

상품 ID: 2005

- [Adokenette 아쿠아](https://www.bnkrmall.co.kr/goods/detail.do?gno=94152527)

```json
{
  "review_id": "R2833",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2834 — Adokenette 오키타 소고 (1개)

상품 ID: 1882

- [Adokenette 오키타 소고](https://www.bnkrmall.co.kr/goods/detail.do?gno=75229179)

```json
{
  "review_id": "R2834",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2835 — Adokenette 우메미야 하지메 (1개)

상품 ID: 1987

- [Adokenette 우메미야 하지메](https://www.bnkrmall.co.kr/goods/detail.do?gno=2105647)

```json
{
  "review_id": "R2835",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2836 — Adokenette 토도로키 쇼토 (1개)

상품 ID: 1763

- [Adokenette 토도로키 쇼토](https://www.bnkrmall.co.kr/goods/detail.do?gno=84548412)

```json
{
  "review_id": "R2836",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2837 — Adokenette 히지카타 토시로 (1개)

상품 ID: 1883

- [Adokenette 히지카타 토시로](https://www.bnkrmall.co.kr/goods/detail.do?gno=13056405)

```json
{
  "review_id": "R2837",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2838 — ALIEN STAGE イヴァン (1개)

상품 ID: 1156

- [ALIEN STAGE イヴァン](https://megahobby.jp/products/item/5761/)

```json
{
  "review_id": "R2838",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2839 — ALIEN STAGE スア (1개)

상품 ID: 1130

- [ALIEN STAGE スア](https://megahobby.jp/products/item/5717/)

```json
{
  "review_id": "R2839",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2840 — ALIEN STAGE ティル (1개)

상품 ID: 1157

- [ALIEN STAGE ティル](https://megahobby.jp/products/item/5762/)

```json
{
  "review_id": "R2840",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2841 — ALIEN STAGE ヒョナ (1개)

상품 ID: 1167

- [ALIEN STAGE ヒョナ](https://megahobby.jp/products/item/5776/)

```json
{
  "review_id": "R2841",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2842 — ALIEN STAGE ミジ (1개)

상품 ID: 1131

- [ALIEN STAGE ミジ](https://megahobby.jp/products/item/5718/)

```json
{
  "review_id": "R2842",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2843 — ALIEN STAGE ルカ (1개)

상품 ID: 1168

- [ALIEN STAGE ルカ](https://megahobby.jp/products/item/5777/)

```json
{
  "review_id": "R2843",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2844 — Atelier Yumia: The Alchemist of Memories & the Envisioned Land (1개)

상품 ID: 3

- [Yumia Liessfeldt Sun Shower Ver.](https://www.kotobukiya.co.jp/en/product/detail/p4934054070602/)

```json
{
  "review_id": "R2844",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2845 — B-121s シルフィーⅡ Mode-B コンポジットウェポンセット (1개)

상품 ID: 182

- [B-121s シルフィーⅡ Mode-B コンポジットウェポンセット](https://megahobby.jp/products/item/3730/)

```json
{
  "review_id": "R2845",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2846 — B-121s シルフィーⅡ コンポジットウェポンセット (1개)

상품 ID: 181

- [B-121s シルフィーⅡ コンポジットウェポンセット](https://megahobby.jp/products/item/3729/)

```json
{
  "review_id": "R2846",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2847 — BANPRESTO EVOLVE C.C. (1개)

상품 ID: 2274

- [코드 기어스 반역의 를르슈 BANPRESTO EVOLVE C.C. 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=36525298)

```json
{
  "review_id": "R2847",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2848 — BANPRESTO EVOLVE CLASSICAL TUNING 백조의 호수 (1개)

상품 ID: 2667

- [하츠네 미쿠 BANPRESTO EVOLVE CLASSICAL TUNING 백조의 호수 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=11787458)

```json
{
  "review_id": "R2848",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2849 — BANPRESTO EVOLVE Classical tuning 백조의 호수 흑조 ver. (1개)

상품 ID: 2181

- [하츠네 미쿠 BANPRESTO EVOLVE Classical tuning 백조의 호수 피규어 흑조 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=42588533)

```json
{
  "review_id": "R2849",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2850 — BANPRESTO EVOLVE 라크스 클라인 여명의 수레바퀴 엔딩 ver. (1개)

상품 ID: 2261

- [기동전사 건담 SEED BANPRESTO EVOLVE 라크스 클라인 피규어 여명의 수레바퀴 엔딩 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=31991018)

```json
{
  "review_id": "R2850",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2851 — BANPRESTO EVOLVE 에메랄드젬 (1개)

상품 ID: 2564

- [하츠네 미쿠 BANPRESTO EVOLVE 에메랄드젬 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=50488191)

```json
{
  "review_id": "R2851",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2852 — BANPRESTO EVOLVE 클래시컬 터닝 호두까기 인형 (1개)

상품 ID: 2204

- [하츠네 미쿠 BANPRESTO EVOLVE 클래시컬 터닝 호두까기 인형 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=12581823)

```json
{
  "review_id": "R2852",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2853 — BANPRESTO EVOLVE 클리오네 (1개)

상품 ID: 2576

- [하츠네 미쿠 BANPRESTO EVOLVE 클리오네 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=1378316)

```json
{
  "review_id": "R2853",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2854 — BANPRESTO EVOLVE 클리오네 젤리피쉬 (1개)

상품 ID: 2205

- [하츠네 미쿠 BANPRESTO EVOLVE 클리오네 젤리피쉬 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=10880914)

```json
{
  "review_id": "R2854",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2855 — BEASTARS ルイ (1개)

상품 ID: 398

- [BEASTARS ルイ](https://megahobby.jp/products/item/4232/)

```json
{
  "review_id": "R2855",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2856 — BEASTARS レゴシ (1개)

상품 ID: 399

- [BEASTARS レゴシ](https://megahobby.jp/products/item/4233/)

```json
{
  "review_id": "R2856",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2857 — BIG SOFVIMATES 드릴머리가 되어버렸어 (1개)

상품 ID: 3543

- [장송의 프리렌 BIG SOFVIMATES 드릴머리가 되어버렸어](https://www.bnkrmall.co.kr/goods/detail.do?gno=89922429)

```json
{
  "review_id": "R2857",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2858 — BIG SOFVIMATES 따끈따끈 (1개)

상품 ID: 3484

- [장송의 프리렌 BIG SOFVIMATES 따끈따끈](https://www.bnkrmall.co.kr/goods/detail.do?gno=34247372)

```json
{
  "review_id": "R2858",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2859 — BIG SOFVIMATES 라분 (1개)

상품 ID: 3788

- [원피스 BIG SOFVIMATES 라분](https://www.bnkrmall.co.kr/goods/detail.do?gno=90651589)

```json
{
  "review_id": "R2859",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2860 — BIG SOFVIMATES 마스터 시바 (1개)

상품 ID: 3886

- [블루 아카이브 BIG SOFVIMATES 마스터 시바](https://www.bnkrmall.co.kr/goods/detail.do?gno=20462031)

```json
{
  "review_id": "R2860",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2861 — BIG SOFVIMATES 마오마오 Ⅱ (1개)

상품 ID: 3578

- [약사의 혼잣말 BIG SOFVIMATES 마오마오 Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=24921770)

```json
{
  "review_id": "R2861",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2862 — BIG SOFVIMATES 몽키 D 루피 (1개)

상품 ID: 3478

- [원피스 BIG SOFVIMATES 몽키 D 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=96277667)

```json
{
  "review_id": "R2862",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2863 — BIG SOFVIMATES 세르포 성인 (1개)

상품 ID: 3271

- [단다단 BIG SOFVIMATES 세르포 성인](https://www.bnkrmall.co.kr/goods/detail.do?gno=24496308)

```json
{
  "review_id": "R2863",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2864 — BIG SOFVIMATES 쵸파 드럼 왕국ver. (1개)

상품 ID: 3547

- [원피스 BIG SOFVIMATES 쵸파 드럼 왕국ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=30469793)

```json
{
  "review_id": "R2864",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2865 — BIG SOFVIMATES 포치타 (1개)

상품 ID: 4031

- [체인소 맨 BIG SOFVIMATES 포치타](https://www.bnkrmall.co.kr/goods/detail.do?gno=89204266)

```json
{
  "review_id": "R2865",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2866 — BIG SOFVIMATE 마오마오 (1개)

상품 ID: 3650

- [약사의 혼잣말 BIG SOFVIMATE 마오마오](https://www.bnkrmall.co.kr/goods/detail.do?gno=77465501)

```json
{
  "review_id": "R2866",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2867 — BLEACH 千年血戦篇 てのひら ルキア (1개)

상품 ID: 692

- [ BLEACH 千年血戦篇  てのひら ルキア](https://megahobby.jp/products/item/4834/)

```json
{
  "review_id": "R2867",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2868 — BLEACH 千年血戦篇 朽木白哉 (1개)

상품 ID: 367

- [BLEACH　千年血戦篇 朽木白哉](https://megahobby.jp/products/item/4170/)

```json
{
  "review_id": "R2868",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2869 — BLEACH 千年血戦篇 黒崎一護 (1개)

상품 ID: 366

- [BLEACH　千年血戦篇 黒崎一護](https://megahobby.jp/products/item/4169/)

```json
{
  "review_id": "R2869",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2870 — BLOOD OF SAIYANS 손오반 비스트 (1개)

상품 ID: 3317

- [드래곤볼 슈퍼 BLOOD OF SAIYANS 손오반 비스트](https://www.bnkrmall.co.kr/goods/detail.do?gno=13207894)

```json
{
  "review_id": "R2870",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2871 — BLOOD OF SAIYANS 초사이어인 버독 (1개)

상품 ID: 3246

- [드래곤볼 Z BLOOD OF SAIYANS 초사이어인 버독](https://www.bnkrmall.co.kr/goods/detail.do?gno=90952988)

```json
{
  "review_id": "R2871",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2872 — BLOOD OF SAIYANS 초사이어인 베지터 (1개)

상품 ID: 3534

- [드래곤볼 Z BLOOD OF SAIYANS 초사이어인 베지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=65349902)

```json
{
  "review_id": "R2872",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2873 — BLOOD OF SAIYANS 초사이어인 손오공 Ⅱ (1개)

상품 ID: 3262

- [드래곤볼 Z BLOOD OF SAIYANS 초사이어인 손오공 Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=97816151)

```json
{
  "review_id": "R2873",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2874 — BLOOD OF SAIYANS 초사이어인 손오공 iii (1개)

상품 ID: 3444

- [드래곤볼 Z BLOOD OF SAIYANS 초사이어인 손오공 iii](https://www.bnkrmall.co.kr/goods/detail.do?gno=36475336)

```json
{
  "review_id": "R2874",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2875 — BLOOD OF SAIYANS 초사이어인 손오반 Ⅱ (1개)

상품 ID: 3331

- [드래곤볼 Z BLOOD OF SAIYANS 초사이어인 손오반 Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=21968625)

```json
{
  "review_id": "R2875",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2876 — BLOOD OF SAIYANS 초사이어인 트랭크스 Ⅱ (1개)

상품 ID: 3559

- [드래곤볼 Z BLOOD OF SAIYANS 초사이어인 트랭크스 Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=99074696)

```json
{
  "review_id": "R2876",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2877 — BWFC 조형 아카데미 SMSP 올마이트 [THE ANIME] (1개)

상품 ID: 4555

- [나의 히어로 아카데미아 BWFC 조형 아카데미 SMSP 올마이트 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56678)

```json
{
  "review_id": "R2877",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2878 — BWFC 조형 아카데미 SMSP 토도로키 쇼토 THE ANIME (1개)

상품 ID: 4590

- [나의 히어로 아카데미아 BWFC 조형 아카데미 SMSP 토도로키 쇼토 THE ANIME](https://www.bnkrmall.co.kr/goods/detail.do?gno=56294)

```json
{
  "review_id": "R2878",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2879 — BWFC 조형 아카데미 SMSP 토도로키 쇼토 THE BRUSH (1개)

상품 ID: 4591

- [나의 히어로 아카데미아 BWFC 조형 아카데미 SMSP 토도로키 쇼토 THE BRUSH](https://www.bnkrmall.co.kr/goods/detail.do?gno=56293)

```json
{
  "review_id": "R2879",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2880 — BWFC 조형왕 정상결전2 VOL.2 스페셜 Ver. (1개)

상품 ID: 4338

- [원피스 BWFC 조형왕 정상결전2 VOL.2 스페셜 Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=20823623)

```json
{
  "review_id": "R2880",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2881 — BWFC 조형왕 정상결전3 슈퍼 마스터 스타 피스 롤로노아 조로 THE ORIGINAL (1개)

상품 ID: 4506

- [원피스 BWFC 조형왕 정상결전3 슈퍼 마스터 스타 피스 롤로노아 조로 THE ORIGINAL](https://www.bnkrmall.co.kr/goods/detail.do?gno=57279)

```json
{
  "review_id": "R2881",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2882 — BWFC 조형왕 정상결전3 슈퍼 마스터 스타 피스 롤로노아 조로 THE TONES (1개)

상품 ID: 4505

- [원피스 BWFC 조형왕 정상결전3 슈퍼 마스터 스타 피스 롤로노아 조로 THE TONES](https://www.bnkrmall.co.kr/goods/detail.do?gno=57280)

```json
{
  "review_id": "R2882",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2883 — BWFC 조형천하제일무술대회3 VOL.4 VER.A (1개)

상품 ID: 4614

- [드래곤볼 Z BWFC 조형천하제일무술대회3 VOL.4 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=55754)

```json
{
  "review_id": "R2883",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2884 — BWFC 조형천하제일무술대회3 슈퍼마스터 스타피스 버독 THE BRUSH (1개)

상품 ID: 4579

- [드래곤볼 슈퍼 BWFC 조형천하제일무술대회3 슈퍼마스터 스타피스 버독 THE BRUSH](https://www.bnkrmall.co.kr/goods/detail.do?gno=56484)

```json
{
  "review_id": "R2884",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2885 — BWFC 조형천하제일무술대회3 슈퍼마스터 스타피스 버독 THE ORIGINAL (1개)

상품 ID: 4653

- [드래곤볼 슈퍼 BWFC 조형천하제일무술대회3 슈퍼마스터 스타피스 버독 THE ORIGINAL](https://www.bnkrmall.co.kr/goods/detail.do?gno=54963)

```json
{
  "review_id": "R2885",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2886 — BWFC 조형천하제일무술대회3 슈퍼마스터 스타피스 버독 THE TONES (1개)

상품 ID: 4654

- [드래곤볼 슈퍼 BWFC 조형천하제일무술대회3 슈퍼마스터 스타피스 버독 THE TONES](https://www.bnkrmall.co.kr/goods/detail.do?gno=54962)

```json
{
  "review_id": "R2886",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2887 — CELESTIAL VIVI 이누이 사쥬나 (1개)

상품 ID: 4150

- [그 비스크 돌은 사랑을 한다 CELESTIAL VIVI 이누이 사쥬나](https://www.bnkrmall.co.kr/goods/detail.do?gno=41011533)

```json
{
  "review_id": "R2887",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2888 — CELESTIAL VIVI 전율의 타츠마키 (1개)

상품 ID: 4445

- [원펀맨 CELESTIAL VIVI 전율의 타츠마키](https://www.bnkrmall.co.kr/goods/detail.do?gno=59219)

```json
{
  "review_id": "R2888",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2889 — CELESTIAL VIVI 지옥의 후부키 (1개)

상품 ID: 4369

- [원펀맨 CELESTIAL VIVI 지옥의 후부키](https://www.bnkrmall.co.kr/goods/detail.do?gno=59826)

```json
{
  "review_id": "R2889",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2890 — CELESTIAL VIVI 키타가와 마린 (1개)

상품 ID: 4040

- [그 비스크 돌은 사랑을 한다 CELESTIAL VIVI 키타가와 마린](https://www.bnkrmall.co.kr/goods/detail.do?gno=87155144)

```json
{
  "review_id": "R2890",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2891 — CHAIN SPIRITS VOL.1 (1개)

상품 ID: 4317

- [체인소 맨 CHAIN SPIRITS VOL.1](https://www.bnkrmall.co.kr/goods/detail.do?gno=95840870)

```json
{
  "review_id": "R2891",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2892 — CHAIN SPIRITS VOL.4 (1개)

상품 ID: 4305

- [체인소 맨 CHAIN SPIRITS VOL.4](https://www.bnkrmall.co.kr/goods/detail.do?gno=73759986)

```json
{
  "review_id": "R2892",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2893 — CHAIN SPIRITS VOL.5 (1개)

상품 ID: 4228

- [체인소 맨 CHAIN SPIRITS VOL.5](https://www.bnkrmall.co.kr/goods/detail.do?gno=54223052)

```json
{
  "review_id": "R2893",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2894 — CHANGEARTS 호이포이 캡슐 No.1 캡슐 하우스 (1개)

상품 ID: 1749

- [CHANGEARTS 호이포이 캡슐 No.1 캡슐 하우스](https://www.bnkrmall.co.kr/goods/detail.do?gno=95330160)

```json
{
  "review_id": "R2894",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2895 — CHANGEARTS 호이포이 캡슐 No.433 트랭크스의 타임머신 (1개)

상품 ID: 1737

- [CHANGEARTS 호이포이 캡슐 No.433 트랭크스의 타임머신](https://www.bnkrmall.co.kr/goods/detail.do?gno=86728041)

```json
{
  "review_id": "R2895",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2896 — CHANGEARTS 호이포이 캡슐 No.576 부르마의 비행기 (1개)

상품 ID: 1736

- [CHANGEARTS 호이포이 캡슐 No.576 부르마의 비행기](https://www.bnkrmall.co.kr/goods/detail.do?gno=56968757)

```json
{
  "review_id": "R2896",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2897 — CHANGEARTS 호이포이 캡슐 No.9 부르마의 바이크 (1개)

상품 ID: 1750

- [CHANGEARTS 호이포이 캡슐 No.9 부르마의 바이크](https://www.bnkrmall.co.kr/goods/detail.do?gno=30683723)

```json
{
  "review_id": "R2897",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2898 — Cheer Pico 미도리야 이즈쿠 (1개)

상품 ID: 3811

- [나의 히어로 아카데미아 Cheer Pico 미도리야 이즈쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=28596628)

```json
{
  "review_id": "R2898",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2899 — Cheer Pico 바쿠고 카츠키 (1개)

상품 ID: 3456

- [나의 히어로 아카데미아 Cheer Pico 바쿠고 카츠키](https://www.bnkrmall.co.kr/goods/detail.do?gno=73167193)

```json
{
  "review_id": "R2899",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2900 — Cheer Pico 토도로키 쇼토 (1개)

상품 ID: 3797

- [나의 히어로 아카데미아 Cheer Pico 토도로키 쇼토](https://www.bnkrmall.co.kr/goods/detail.do?gno=31943357)

```json
{
  "review_id": "R2900",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2901 — Classical tuning 잠자는 숲속의 미녀 모음곡 (1개)

상품 ID: 3393

- [하츠네 미쿠 Classical tuning 잠자는 숲속의 미녀 모음곡](https://www.bnkrmall.co.kr/goods/detail.do?gno=83564268)

```json
{
  "review_id": "R2901",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2902 — CLEARISE 마인 베지터 (1개)

상품 ID: 4304

- [드래곤볼 Z CLEARISE 마인 베지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=50008668)

```json
{
  "review_id": "R2902",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2903 — CLEARISE 손오공&베지터 (A:손오공) (1개)

상품 ID: 3694

- [드래곤볼 슈퍼 CLEARISE 손오공&베지터 (A:손오공)](https://www.bnkrmall.co.kr/goods/detail.do?gno=95971260)

```json
{
  "review_id": "R2903",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2904 — CLEARISE 손오공&베지터 (B:베지터) (1개)

상품 ID: 3693

- [드래곤볼 슈퍼 CLEARISE 손오공&베지터 (B:베지터)](https://www.bnkrmall.co.kr/goods/detail.do?gno=199414)

```json
{
  "review_id": "R2904",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2905 — CLEARISE 오공 블랙 & 초사이어인 로제 오공 블랙 (A:오공 블랙) (1개)

상품 ID: 4110

- [드래곤볼 슈퍼 CLEARISE 오공 블랙 & 초사이어인 로제 오공 블랙 (A:오공 블랙)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57463761)

```json
{
  "review_id": "R2905",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2906 — CLEARISE 오공 블랙 & 초사이어인 로제 오공 블랙 (B:초사이어인 로제 오공 블랙) (1개)

상품 ID: 4109

- [드래곤볼 슈퍼 CLEARISE 오공 블랙 & 초사이어인 로제 오공 블랙 (B:초사이어인 로제 오공 블랙)](https://www.bnkrmall.co.kr/goods/detail.do?gno=62377016)

```json
{
  "review_id": "R2906",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2907 — CLEARISE 오지터 & 베지트 (A:오지터) (1개)

상품 ID: 3616

- [드래곤볼 슈퍼 CLEARISE 오지터 & 베지트 (A:오지터)](https://www.bnkrmall.co.kr/goods/detail.do?gno=71520945)

```json
{
  "review_id": "R2907",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2908 — CLEARISE 오지터 & 베지트 (B:베지트) (1개)

상품 ID: 3615

- [드래곤볼 슈퍼 CLEARISE 오지터 & 베지트 (B:베지트)](https://www.bnkrmall.co.kr/goods/detail.do?gno=48784386)

```json
{
  "review_id": "R2908",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2909 — CLEARISE 초사이어인2 손오반 (1개)

상품 ID: 4463

- [드래곤볼 Z CLEARISE 초사이어인2 손오반](https://www.bnkrmall.co.kr/goods/detail.do?gno=58829)

```json
{
  "review_id": "R2909",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2910 — CLEARISE 초사이어인 갓 초사이어인 베지터 (1개)

상품 ID: 4600

- [드래곤볼 슈퍼 CLEARISE 초사이어인 갓 초사이어인 베지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=56093)

```json
{
  "review_id": "R2910",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2911 — CLEARISE 초사이어인 갓 초사이어인 베지트 (1개)

상품 ID: 4583

- [드래곤볼 슈퍼 CLEARISE 초사이어인 갓 초사이어인 베지트](https://www.bnkrmall.co.kr/goods/detail.do?gno=56315)

```json
{
  "review_id": "R2911",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2912 — CLEARISE 초사이어인 갓 초사이어인 손오공 (1개)

상품 ID: 4551

- [드래곤볼 슈퍼 CLEARISE 초사이어인 갓 초사이어인 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=56761)

```json
{
  "review_id": "R2912",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2913 — CLEARISE 초사이어인 갓 초사이어인 오지터 (1개)

상품 ID: 4491

- [드래곤볼 슈퍼 CLEARISE 초사이어인 갓 초사이어인 오지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=57423)

```json
{
  "review_id": "R2913",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2914 — CLEARISE 초사이어인 베지터 (1개)

상품 ID: 4465

- [드래곤볼 Z CLEARISE 초사이어인 베지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=58827)

```json
{
  "review_id": "R2914",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2915 — CLEARISE 초사이어인 브로리 (1개)

상품 ID: 4127

- [드래곤볼 Z CLEARISE 초사이어인 브로리](https://www.bnkrmall.co.kr/goods/detail.do?gno=84582552)

```json
{
  "review_id": "R2915",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2916 — CLEARISE 초사이어인 손오반(그레이트 사이어맨 VER) (1개)

상품 ID: 4409

- [드래곤볼 슈퍼 CLEARISE 초사이어인 손오반(그레이트 사이어맨 VER)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59524)

```json
{
  "review_id": "R2916",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2917 — CLEARISE 초사이어인 손오반(그레이트 사이어맨 VER)Ⅱ (VER.A) (1개)

상품 ID: 4000

- [드래곤볼 Z CLEARISE 초사이어인 손오반(그레이트 사이어맨 VER)Ⅱ (VER.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=94350017)

```json
{
  "review_id": "R2917",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2918 — CLEARISE 초사이어인 손오반(그레이트 사이어맨 VER)Ⅱ (VER.B) (1개)

상품 ID: 3999

- [드래곤볼 Z CLEARISE 초사이어인 손오반(그레이트 사이어맨 VER)Ⅱ (VER.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=47109294)

```json
{
  "review_id": "R2918",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2919 — COLLECTION 07 機動戦士ガンダム 地球連邦軍 カイ・シデン ノーマルスーツVer. (1개)

상품 ID: 866

- [COLLECTION 07 機動戦士ガンダム 地球連邦軍 カイ・シデン ノーマルスーツVer.](https://megahobby.jp/products/item/5237/)

```json
{
  "review_id": "R2919",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2920 — COLLECTION 08 機動戦士ガンダム ジオン公国軍 ランバ・ラル ノーマルスーツVer. (1개)

상품 ID: 865

- [COLLECTION 08 機動戦士ガンダム ジオン公国軍 ランバ・ラル ノーマルスーツVer.](https://megahobby.jp/products/item/5236/)

```json
{
  "review_id": "R2920",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2921 — COLLECTION 10 機動戦士ガンダム ジオン公国軍 シャア・アズナブル ノーマルスーツVer. (1개)

상품 ID: 894

- [COLLECTION 10 機動戦士ガンダム ジオン公国軍 シャア・アズナブル ノーマルスーツVer.](https://megahobby.jp/products/item/5310/)

```json
{
  "review_id": "R2921",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2922 — COLLECTION 12 機動戦士ガンダム 地球連邦軍 ミライ・ヤシマ (1개)

상품 ID: 968

- [COLLECTION 12 機動戦士ガンダム 地球連邦軍 ミライ・ヤシマ](https://megahobby.jp/products/item/5416/)

```json
{
  "review_id": "R2922",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2923 — COLLECTION 13 機動戦士ガンダム ジオン公国軍 黒い三連星 ガイア ノーマルスーツVer. (1개)

상품 ID: 1068

- [COLLECTION 13 機動戦士ガンダム ジオン公国軍 黒い三連星 ガイア ノーマルスーツVer.](https://megahobby.jp/products/item/5586/)

```json
{
  "review_id": "R2923",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2924 — COLLECTION 14 機動戦士ガンダム ジオン公国軍 黒い三連星 オルテガ ノーマルスーツVer. (1개)

상품 ID: 1067

- [COLLECTION 14 機動戦士ガンダム ジオン公国軍 黒い三連星 オルテガ ノーマルスーツVer.](https://megahobby.jp/products/item/5585/)

```json
{
  "review_id": "R2924",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2925 — COLLECTION 15 機動戦士ガンダム ジオン公国軍 黒い三連星 マッシュ ノーマルスーツVer. (1개)

상품 ID: 1066

- [COLLECTION 15 機動戦士ガンダム ジオン公国軍 黒い三連星 マッシュ ノーマルスーツVer.](https://megahobby.jp/products/item/5584/)

```json
{
  "review_id": "R2925",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2926 — COLLECTION 16 機動戦士ガンダム 地球連邦軍 アムロ・レイ制服Ver. (1개)

상품 ID: 1274

- [COLLECTION 16 機動戦士ガンダム 地球連邦軍 アムロ・レイ制服Ver.](https://megahobby.jp/products/item/5960/)

```json
{
  "review_id": "R2926",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2927 — COLLECTION 17 機動戦士ガンダム 地球連邦軍 セイラ・マス制服Ver. (1개)

상품 ID: 1273

- [COLLECTION 17 機動戦士ガンダム 地球連邦軍 セイラ・マス制服Ver.](https://megahobby.jp/products/item/5959/)

```json
{
  "review_id": "R2927",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2928 — COM 피규레이션 오지터 Vol.1 (1개)

상품 ID: 4674

- [드래곤볼 Z COM 피규레이션 오지터 Vol.1](https://www.bnkrmall.co.kr/goods/detail.do?gno=15789)

```json
{
  "review_id": "R2928",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2929 — COM 피규레이션 오지터 Vol.2 (1개)

상품 ID: 4672

- [드래곤볼 Z COM 피규레이션 오지터 Vol.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=15788)

```json
{
  "review_id": "R2929",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2930 — CRANE POP (A:프리렌) (1개)

상품 ID: 3269

- [장송의 프리렌 CRANE POP 피규어 (A:프리렌)](https://www.bnkrmall.co.kr/goods/detail.do?gno=16159960)

```json
{
  "review_id": "R2930",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2931 — CRANE POP (B:페른) (1개)

상품 ID: 3268

- [장송의 프리렌 CRANE POP 피규어 (B:페른)](https://www.bnkrmall.co.kr/goods/detail.do?gno=82280386)

```json
{
  "review_id": "R2931",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2932 — CREATOR X CREATOR 거대 원숭이 베지터 (1개)

상품 ID: 4668

- [드래곤볼 Z CREATOR X CREATOR 거대 원숭이 베지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=15824)

```json
{
  "review_id": "R2932",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2933 — CREATOR X CREATOR 롤로노아 조로 Ver.A (1개)

상품 ID: 4666

- [원피스 CREATOR X CREATOR 롤로노아 조로 Ver.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=15835)

```json
{
  "review_id": "R2933",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2934 — CREATOR X CREATOR 몽키 D 루피 Ver.A (1개)

상품 ID: 4671

- [원피스 CREATOR X CREATOR 몽키 D 루피 Ver.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=15791)

```json
{
  "review_id": "R2934",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2935 — CREATOR X CREATOR 버독 (1개)

상품 ID: 4701

- [드래곤볼 Z CREATOR X CREATOR 버독](https://www.bnkrmall.co.kr/goods/detail.do?gno=15393)

```json
{
  "review_id": "R2935",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2936 — CREATOR X CREATOR 보아 핸콕 II Ver.A (1개)

상품 ID: 4673

- [원피스 CREATOR X CREATOR 보아 핸콕 II Ver.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=15792)

```json
{
  "review_id": "R2936",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2937 — CREATOR X CREATOR 손오공 (Ultra Instinct) (1개)

상품 ID: 4708

- [드래곤볼 슈퍼 CREATOR X CREATOR 손오공 (Ultra Instinct)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15309)

```json
{
  "review_id": "R2937",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2938 — CREATOR X CREATOR 손오공 (Ultra Instinct -Sign-) (1개)

상품 ID: 4705

- [드래곤볼 슈퍼 CREATOR X CREATOR 손오공 (Ultra Instinct -Sign-)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15308)

```json
{
  "review_id": "R2938",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2939 — CROSS POSING 롤로노아 조로 (1개)

상품 ID: 3442

- [원피스 CROSS POSING 롤로노아 조로](https://www.bnkrmall.co.kr/goods/detail.do?gno=15145836)

```json
{
  "review_id": "R2939",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2940 — CROSS POSING 몽키 D 루피 (1개)

상품 ID: 3261

- [원피스 CROSS POSING 몽키 D 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=68033675)

```json
{
  "review_id": "R2940",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2941 — CROSS POSING 몽키 D 루피 ii (1개)

상품 ID: 3443

- [원피스 CROSS POSING 몽키 D 루피 ii](https://www.bnkrmall.co.kr/goods/detail.do?gno=14743793)

```json
{
  "review_id": "R2941",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2942 — CROSS POSING 스코퍼 가반 (1개)

상품 ID: 3386

- [원피스 CROSS POSING 스코퍼 가반](https://www.bnkrmall.co.kr/goods/detail.do?gno=30487891)

```json
{
  "review_id": "R2942",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2943 — CROSS POSING 에넬 (1개)

상품 ID: 3682

- [원피스 CROSS POSING 에넬](https://www.bnkrmall.co.kr/goods/detail.do?gno=55155899)

```json
{
  "review_id": "R2943",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2944 — DEMON SERIES VOL.10 (A:규타로) (1개)

상품 ID: 4293

- [귀멸의 칼날 피규어 DEMON SERIES VOL.10 (A:규타로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=79089709)

```json
{
  "review_id": "R2944",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2945 — DEMON SERIES VOL.10 (B:굣코) (1개)

상품 ID: 4292

- [귀멸의 칼날 피규어 DEMON SERIES VOL.10 (B:굣코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=61954394)

```json
{
  "review_id": "R2945",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2946 — DEMON SERIES VOL.11 (A:키부츠지 무잔) (1개)

상품 ID: 4287

- [귀멸의 칼날 피규어 DEMON SERIES VOL.11 (A:키부츠지 무잔)](https://www.bnkrmall.co.kr/goods/detail.do?gno=65455482)

```json
{
  "review_id": "R2946",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2947 — DEMON SERIES VOL.11 (B:한텐구) (1개)

상품 ID: 4286

- [귀멸의 칼날 피규어 DEMON SERIES VOL.11 (B:한텐구)](https://www.bnkrmall.co.kr/goods/detail.do?gno=87314393)

```json
{
  "review_id": "R2947",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2948 — DEMON SERIES VOL.12 (B:조하쿠텐) (1개)

상품 ID: 4235

- [귀멸의 칼날 피규어 DEMON SERIES VOL.12 (B:조하쿠텐)](https://www.bnkrmall.co.kr/goods/detail.do?gno=42964787)

```json
{
  "review_id": "R2948",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2949 — DEMON SERIES VOL.13 (키부츠지 무잔) (1개)

상품 ID: 3913

- [귀멸의 칼날 피규어 DEMON SERIES VOL.13 (키부츠지 무잔)](https://www.bnkrmall.co.kr/goods/detail.do?gno=62954937)

```json
{
  "review_id": "R2949",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2950 — DEMON SERIES VOL.14 (도우마) (1개)

상품 ID: 3895

- [귀멸의 칼날 피규어 DEMON SERIES VOL.14 (도우마)](https://www.bnkrmall.co.kr/goods/detail.do?gno=37699947)

```json
{
  "review_id": "R2950",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2951 — DEMON SERIES VOL.15 (1개)

상품 ID: 3756

- [귀멸의 칼날 피규어 DEMON SERIES VOL.15](https://www.bnkrmall.co.kr/goods/detail.do?gno=59970857)

```json
{
  "review_id": "R2951",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2952 — DEMON SERIES VOL.3 (A:루이) (1개)

상품 ID: 4634

- [귀멸의 칼날 피규어 DEMON SERIES VOL.3 (A:루이)](https://www.bnkrmall.co.kr/goods/detail.do?gno=55272)

```json
{
  "review_id": "R2952",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2953 — DEMON SERIES VOL.3 (B:엔무) (1개)

상품 ID: 4633

- [귀멸의 칼날 피규어 DEMON SERIES VOL.3 (B:엔무)](https://www.bnkrmall.co.kr/goods/detail.do?gno=55273)

```json
{
  "review_id": "R2953",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2954 — DEMON SERIES VOL.4 (B:아카자) (1개)

상품 ID: 4627

- [귀멸의 칼날 피규어 DEMON SERIES VOL.4 (B:아카자)](https://www.bnkrmall.co.kr/goods/detail.do?gno=55482)

```json
{
  "review_id": "R2954",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2955 — DEMON SERIES VOL.5 (A:아카자) (1개)

상품 ID: 4587

- [귀멸의 칼날 피규어 DEMON SERIES VOL.5 (A:아카자)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56305)

```json
{
  "review_id": "R2955",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2956 — DEMON SERIES VOL.5 (B:키부츠지 무잔) (1개)

상품 ID: 4586

- [귀멸의 칼날 피규어 DEMON SERIES VOL.5 (B:키부츠지 무잔)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56306)

```json
{
  "review_id": "R2956",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2957 — DEMON SERIES VOL.6 (VER.B) (1개)

상품 ID: 4484

- [귀멸의 칼날 피규어 DEMON SERIES VOL.6 (VER.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58263)

```json
{
  "review_id": "R2957",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2958 — DEMON SERIES VOL.7 (A:키부츠지 무잔) (1개)

상품 ID: 4479

- [귀멸의 칼날 피규어 DEMON SERIES VOL.7 (A:키부츠지 무잔)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58555)

```json
{
  "review_id": "R2958",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2959 — DEMON SERIES VOL.7 (B:다키) (1개)

상품 ID: 4478

- [귀멸의 칼날 피규어 DEMON SERIES VOL.7 (B:다키)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58557)

```json
{
  "review_id": "R2959",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2960 — DEMON SERIES VOL.8 (A:다키) (1개)

상품 ID: 4456

- [귀멸의 칼날 피규어 DEMON SERIES VOL.8 (A:다키)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59160)

```json
{
  "review_id": "R2960",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2961 — DEMON SERIES VOL.8 (B:규타로) (1개)

상품 ID: 4455

- [귀멸의 칼날 피규어 DEMON SERIES VOL.8 (B:규타로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59161)

```json
{
  "review_id": "R2961",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2962 — DEMON SERIES VOL.9 (1개)

상품 ID: 4368

- [귀멸의 칼날 피규어 DEMON SERIES VOL.9](https://www.bnkrmall.co.kr/goods/detail.do?gno=59828)

```json
{
  "review_id": "R2962",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2963 — DIORAMATIC 롤로노아 조로 [THE ANIME] (1개)

상품 ID: 4360

- [원피스 DIORAMATIC 롤로노아 조로 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59953)

```json
{
  "review_id": "R2963",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2964 — DIORAMATIC 롤로노아 조로 [THE BRUSH] (1개)

상품 ID: 4361

- [원피스 DIORAMATIC 롤로노아 조로 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59952)

```json
{
  "review_id": "R2964",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2965 — DIORAMATIC 몽키 D 루피 [THE ANIME] (1개)

상품 ID: 4311

- [원피스 DIORAMATIC 몽키 D 루피 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=65375426)

```json
{
  "review_id": "R2965",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2966 — DIORAMATIC 몽키 D 루피 [THE BRUSH] (1개)

상품 ID: 4313

- [원피스 DIORAMATIC 몽키 D 루피 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=84870863)

```json
{
  "review_id": "R2966",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2967 — DIORAMATIC 미도리야 이즈쿠 [THE ANIME] (1개)

상품 ID: 4459

- [나의 히어로 아카데미아 DIORAMATIC 미도리야 이즈쿠 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58835)

```json
{
  "review_id": "R2967",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2968 — DIORAMATIC 미도리야 이즈쿠 [THE BRUSH] (1개)

상품 ID: 4460

- [나의 히어로 아카데미아 DIORAMATIC 미도리야 이즈쿠 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58834)

```json
{
  "review_id": "R2968",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2969 — DIORAMATIC 바쿠고 카츠키 [THE ANIME] (1개)

상품 ID: 4448

- [나의 히어로 아카데미아 DIORAMATIC 바쿠고 카츠키 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59177)

```json
{
  "review_id": "R2969",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2970 — DIORAMATIC 바쿠고 카츠키 [THE BRUSH] (1개)

상품 ID: 4449

- [나의 히어로 아카데미아 DIORAMATIC 바쿠고 카츠키 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59176)

```json
{
  "review_id": "R2970",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2971 — DIORAMATIC 야마토 [THE ANIME] (1개)

상품 ID: 4339

- [원피스 DIORAMATIC 야마토 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=28155506)

```json
{
  "review_id": "R2971",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2972 — DIORAMATIC 야마토 [THE BRUSH] (1개)

상품 ID: 4340

- [원피스 DIORAMATIC 야마토 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=77466682)

```json
{
  "review_id": "R2972",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2973 — DIORAMATIC 우치하 이타치 [THE ANIME] (1개)

상품 ID: 4403

- [나루토 질풍전 DIORAMATIC 우치하 이타치 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59537)

```json
{
  "review_id": "R2973",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2974 — DIORAMATIC 우치하 이타치 [THE BRUSH] (1개)

상품 ID: 4404

- [나루토 질풍전 DIORAMATIC 우치하 이타치 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59536)

```json
{
  "review_id": "R2974",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2975 — DIORAMATIC 토도로키 쇼토 [THE ANIME] (1개)

상품 ID: 4401

- [나의 히어로 아카데미아 DIORAMATIC 토도로키 쇼토 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59541)

```json
{
  "review_id": "R2975",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2976 — DIORAMATIC 토도로키 쇼토 [THE BRUSH] (1개)

상품 ID: 4402

- [나의 히어로 아카데미아 DIORAMATIC 토도로키 쇼토 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59540)

```json
{
  "review_id": "R2976",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2977 — DX 新世紀GPXサイバーフォーミュラ スゴウレガード10V5000 -Livery Edition (1개)

상품 ID: 388

- [DX 新世紀GPXサイバーフォーミュラ スゴウレガード10V5000 -Livery Edition-](https://megahobby.jp/products/item/4222/)

```json
{
  "review_id": "R2977",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2978 — EMOTIONAL LENS 사이죠 쥬리 (1개)

상품 ID: 4273

- [아이돌마스터 샤이니 컬러즈 EMOTIONAL LENS 사이죠 쥬리](https://www.bnkrmall.co.kr/goods/detail.do?gno=58291965)

```json
{
  "review_id": "R2978",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2979 — EMOTIONAL LENS 아사쿠라 토오루 (1개)

상품 ID: 4069

- [아이돌마스터 샤이니 컬러즈 EMOTIONAL LENS 아사쿠라 토오루](https://www.bnkrmall.co.kr/goods/detail.do?gno=73401966)

```json
{
  "review_id": "R2979",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2980 — EMOTIONAL LENS 유코쿠 키리코 (1개)

상품 ID: 4187

- [아이돌마스터 샤이니 컬러즈 EMOTIONAL LENS 유코쿠 키리코](https://www.bnkrmall.co.kr/goods/detail.do?gno=60533423)

```json
{
  "review_id": "R2980",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2981 — EX [다키・규타로] (A:다키) (1개)

상품 ID: 4063

- [귀멸의 칼날 피규어 EX (다키・규타로) (A:다키)](https://www.bnkrmall.co.kr/goods/detail.do?gno=28908789)

```json
{
  "review_id": "R2981",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2982 — EX [다키・규타로] (B:규타로) (1개)

상품 ID: 4062

- [귀멸의 칼날 피규어 EX (다키・규타로) (B:규타로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=41217321)

```json
{
  "review_id": "R2982",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2983 — EX [렌고쿠 쿄쥬로・카마도 탄지로] (A:렌고쿠 쿄쥬로) (1개)

상품 ID: 3953

- [귀멸의 칼날 피규어 EX (렌고쿠 쿄쥬로・카마도 탄지로) (A:렌고쿠 쿄쥬로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=80116559)

```json
{
  "review_id": "R2983",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2984 — EX [렌고쿠 쿄쥬로・카마도 탄지로] (B:카마도 탄지로) (1개)

상품 ID: 3952

- [귀멸의 칼날 피규어 EX (렌고쿠 쿄쥬로・카마도 탄지로) (B:카마도 탄지로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=44453371)

```json
{
  "review_id": "R2984",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2985 — EX [엔무・아카자] (A:엔무) (1개)

상품 ID: 3971

- [귀멸의 칼날 피규어 EX (엔무・아카자) (A:엔무)](https://www.bnkrmall.co.kr/goods/detail.do?gno=36443720)

```json
{
  "review_id": "R2985",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2986 — EX [엔무・아카자] (B:아카자) (1개)

상품 ID: 3970

- [귀멸의 칼날 피규어 EX (엔무・아카자) (B:아카자)](https://www.bnkrmall.co.kr/goods/detail.do?gno=55449670)

```json
{
  "review_id": "R2986",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2987 — EX [이구로 오바나이・칸로지 미츠리] (A:이구로 오바나이) (1개)

상품 ID: 4135

- [귀멸의 칼날 피규어 EX (이구로 오바나이・칸로지 미츠리) (A:이구로 오바나이)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58328694)

```json
{
  "review_id": "R2987",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2988 — EX [이구로 오바나이・칸로지 미츠리] (B:칸로지 미츠리) (1개)

상품 ID: 4134

- [귀멸의 칼날 피규어 EX (이구로 오바나이・칸로지 미츠리) (B:칸로지 미츠리)](https://www.bnkrmall.co.kr/goods/detail.do?gno=86215711)

```json
{
  "review_id": "R2988",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2989 — EX [코쵸우 시노부・우즈이 텐겐] (A:코쵸우 시노부) (1개)

상품 ID: 4115

- [귀멸의 칼날 피규어 EX (코쵸우 시노부・우즈이 텐겐) (A:코쵸우 시노부)](https://www.bnkrmall.co.kr/goods/detail.do?gno=98116858)

```json
{
  "review_id": "R2989",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2990 — EX [코쵸우 시노부・우즈이 텐겐] (B:우즈이 텐겐) (1개)

상품 ID: 4114

- [귀멸의 칼날 피규어 EX (코쵸우 시노부・우즈이 텐겐) (B:우즈이 텐겐)](https://www.bnkrmall.co.kr/goods/detail.do?gno=49942007)

```json
{
  "review_id": "R2990",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2991 — EX [토미오카 기유・시나즈가와 사네미] (A:토미오카 기유) (1개)

상품 ID: 4137

- [귀멸의 칼날 피규어 EX (토미오카 기유・시나즈가와 사네미) (A:토미오카 기유)](https://www.bnkrmall.co.kr/goods/detail.do?gno=33074761)

```json
{
  "review_id": "R2991",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2992 — EX [토미오카 기유・시나즈가와 사네미] (B:시나즈가와 사네미) (1개)

상품 ID: 4136

- [귀멸의 칼날 피규어 EX (토미오카 기유・시나즈가와 사네미) (B:시나즈가와 사네미)](https://www.bnkrmall.co.kr/goods/detail.do?gno=3408207)

```json
{
  "review_id": "R2992",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2993 — EX [한텐구・조하쿠텐・굣코] (A:한텐구) (1개)

상품 ID: 4030

- [귀멸의 칼날 피규어 EX (한텐구・조하쿠텐・굣코) (A:한텐구)](https://www.bnkrmall.co.kr/goods/detail.do?gno=28009035)

```json
{
  "review_id": "R2993",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2994 — EX [한텐구・조하쿠텐・굣코] (B:조하쿠텐) (1개)

상품 ID: 4029

- [귀멸의 칼날 피규어 EX (한텐구・조하쿠텐・굣코) (B:조하쿠텐)](https://www.bnkrmall.co.kr/goods/detail.do?gno=10365228)

```json
{
  "review_id": "R2994",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2995 — EX [한텐구・조하쿠텐・굣코] (C:굣코) (1개)

상품 ID: 4028

- [귀멸의 칼날 피규어 EX (한텐구・조하쿠텐・굣코) (C:굣코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=35032608)

```json
{
  "review_id": "R2995",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2996 — EX [히메지마 교메이・토키토 무이치로] (A:히메지마 교메이) (1개)

상품 ID: 4133

- [귀멸의 칼날 피규어 EX (히메지마 교메이・토키토 무이치로) (A:히메지마 교메이)](https://www.bnkrmall.co.kr/goods/detail.do?gno=68950908)

```json
{
  "review_id": "R2996",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2997 — EX [히메지마 교메이・토키토 무이치로] (B:토키토 무이치로) (1개)

상품 ID: 4141

- [귀멸의 칼날 피규어 EX (히메지마 교메이・토키토 무이치로) (B:토키토 무이치로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=89336019)

```json
{
  "review_id": "R2997",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2998 — F-616[AR]s フェリルナビット ロッサ＆マシンフェンリル エアロ (1개)

상품 ID: 205

- [F-616(AR)s フェリルナビット ロッサ＆マシンフェンリル エアロ](https://megahobby.jp/products/item/3793/)

```json
{
  "review_id": "R2998",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R2999 — F-616[DR]s レインナビット＆マシンリュカオン (1개)

상품 ID: 306

- [F-616(DR)s レインナビット＆マシンリュカオン](https://megahobby.jp/products/item/4060/)

```json
{
  "review_id": "R2999",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3000 — FINAL SEASON 미도리야 이즈쿠 (1개)

상품 ID: 3751

- [나의 히어로 아카데미아 FINAL SEASON 미도리야 이즈쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=25715727)

```json
{
  "review_id": "R3000",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3001 — FINAL SEASON 미도리야 이즈쿠&시가라키 토무라 (B.시가라키 토무라) (1개)

상품 ID: 3445

- [나의 히어로 아카데미아 FINAL SEASON 피규어 미도리야 이즈쿠&시가라키 토무라 (B.시가라키 토무라)](https://www.bnkrmall.co.kr/goods/detail.do?gno=93379534)

```json
{
  "review_id": "R3001",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3002 — FIX 메탈 콤포지트 윙 건담 스노우 화이트 프렐류드 (1개)

상품 ID: 2009

- [FIX 메탈 콤포지트 윙 건담 스노우 화이트 프렐류드](https://www.bnkrmall.co.kr/goods/detail.do?gno=58221449)

```json
{
  "review_id": "R3002",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3003 — Fluffy Puffy～카라스노 고등학교·네코마 고등학교～(A：히나가라스) (1개)

상품 ID: 3641

- [하이큐!! Fluffy Puffy～카라스노 고등학교·네코마 고등학교～(A：히나가라스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=42989102)

```json
{
  "review_id": "R3003",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3004 — Fluffy Puffy～카라스노 고등학교·네코마 고등학교～(B：카게가라스) (1개)

상품 ID: 3640

- [하이큐!! Fluffy Puffy～카라스노 고등학교·네코마 고등학교～(B：카게가라스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=12409346)

```json
{
  "review_id": "R3004",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3005 — Fluffy Puffy～카라스노 고등학교·네코마 고등학교～(C：켄마네코) (1개)

상품 ID: 3639

- [하이큐!! Fluffy Puffy～카라스노 고등학교·네코마 고등학교～(C：켄마네코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=36952772)

```json
{
  "review_id": "R3005",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3006 — Fluffy Puffy～카라스노 고등학교·네코마 고등학교～(D：쿠로오네코) (1개)

상품 ID: 3638

- [하이큐!! Fluffy Puffy～카라스노 고등학교·네코마 고등학교～(D：쿠로오네코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=31234894)

```json
{
  "review_id": "R3006",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3007 — Fluffy Puffy 데쿠쉽&바쿠독&올마이고트 (A:데쿠쉽) (1개)

상품 ID: 3266

- [나의 히어로 아카데미아 Fluffy Puffy 데쿠쉽&바쿠독&올마이고트 (A:데쿠쉽)](https://www.bnkrmall.co.kr/goods/detail.do?gno=39203359)

```json
{
  "review_id": "R3007",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3008 — Fluffy Puffy 데쿠쉽&바쿠독&올마이고트 (B:바쿠독) (1개)

상품 ID: 3265

- [나의 히어로 아카데미아 Fluffy Puffy 데쿠쉽&바쿠독&올마이고트 (B:바쿠독)](https://www.bnkrmall.co.kr/goods/detail.do?gno=26017713)

```json
{
  "review_id": "R3008",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3009 — Fluffy Puffy 데쿠쉽&바쿠독&올마이고트 (C:올마이고트) (1개)

상품 ID: 3684

- [나의 히어로 아카데미아 Fluffy Puffy 데쿠쉽&바쿠독&올마이고트 (C:올마이고트)](https://www.bnkrmall.co.kr/goods/detail.do?gno=9084512)

```json
{
  "review_id": "R3009",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3010 — FLUFFY PUFFY 데쿠쉽 & 바쿠독 (A:데쿠쉽) (1개)

상품 ID: 3859

- [나의 히어로 아카데미아 FLUFFY PUFFY 데쿠쉽 & 바쿠독 (A:데쿠쉽)](https://www.bnkrmall.co.kr/goods/detail.do?gno=33795863)

```json
{
  "review_id": "R3010",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3011 — FLUFFY PUFFY 데쿠쉽 & 바쿠독 (B:바쿠독) (1개)

상품 ID: 3857

- [나의 히어로 아카데미아 FLUFFY PUFFY 데쿠쉽 & 바쿠독 (B:바쿠독)](https://www.bnkrmall.co.kr/goods/detail.do?gno=41426676)

```json
{
  "review_id": "R3011",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3012 — FLUFFY PUFFY 데쿠쉽 & 바쿠독Ⅱ (A:데쿠쉽) (1개)

상품 ID: 3551

- [나의 히어로 아카데미아 FLUFFY PUFFY 데쿠쉽 & 바쿠독Ⅱ (A:데쿠쉽)](https://www.bnkrmall.co.kr/goods/detail.do?gno=19789011)

```json
{
  "review_id": "R3012",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3013 — FLUFFY PUFFY 데쿠쉽 & 바쿠독Ⅱ (B:바쿠독) (1개)

상품 ID: 3550

- [나의 히어로 아카데미아 FLUFFY PUFFY 데쿠쉽 & 바쿠독Ⅱ (B:바쿠독)](https://www.bnkrmall.co.kr/goods/detail.do?gno=11635463)

```json
{
  "review_id": "R3013",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3014 — Fluffy Puffy 무키무키 네즈미 (ver.A) (1개)

상품 ID: 3358

- [귀멸의 칼날 Fluffy Puffy 무키무키 네즈미 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58126143)

```json
{
  "review_id": "R3014",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3015 — Fluffy Puffy 무키무키 네즈미 (ver.B) (1개)

상품 ID: 3357

- [귀멸의 칼날 Fluffy Puffy 무키무키 네즈미 (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=94661949)

```json
{
  "review_id": "R3015",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3016 — Fluffy Puffy 쇼토캣&고릴라고릴라고릴라&다비헤비 (A:쇼토캣) (1개)

상품 ID: 3566

- [나의 히어로 아카데미아 Fluffy Puffy 쇼토캣&고릴라고릴라고릴라&다비헤비 (A:쇼토캣)](https://www.bnkrmall.co.kr/goods/detail.do?gno=36306907)

```json
{
  "review_id": "R3016",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3017 — Fluffy Puffy 쇼토캣&고릴라고릴라고릴라&다비헤비 (B:고릴라고릴라고릴라) (1개)

상품 ID: 3565

- [나의 히어로 아카데미아 Fluffy Puffy 쇼토캣&고릴라고릴라고릴라&다비헤비 (B:고릴라고릴라고릴라)](https://www.bnkrmall.co.kr/goods/detail.do?gno=44364607)

```json
{
  "review_id": "R3017",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3018 — Fluffy Puffy 쇼토캣&고릴라고릴라고릴라&다비헤비 (C:다비헤비) (1개)

상품 ID: 3564

- [나의 히어로 아카데미아 Fluffy Puffy 쇼토캣&고릴라고릴라고릴라&다비헤비 (C:다비헤비)](https://www.bnkrmall.co.kr/goods/detail.do?gno=16222296)

```json
{
  "review_id": "R3018",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3019 — FLUFFY PUFFY 쇼토캣 & 오챠네코 (A:쇼토캣) (1개)

상품 ID: 3959

- [나의 히어로 아카데미아 FLUFFY PUFFY 쇼토캣 & 오챠네코 (A:쇼토캣)](https://www.bnkrmall.co.kr/goods/detail.do?gno=10338558)

```json
{
  "review_id": "R3019",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3020 — FLUFFY PUFFY 쇼토캣 & 오챠네코 (B:오챠네코) (1개)

상품 ID: 3958

- [나의 히어로 아카데미아 FLUFFY PUFFY 쇼토캣 & 오챠네코 (B:오챠네코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=88000685)

```json
{
  "review_id": "R3020",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3021 — FLUFFY PUFFY 쇼토캣 & 오챠네코Ⅱ (A:쇼토캣) (1개)

상품 ID: 3549

- [나의 히어로 아카데미아 FLUFFY PUFFY 쇼토캣 & 오챠네코Ⅱ (A:쇼토캣)](https://www.bnkrmall.co.kr/goods/detail.do?gno=34112773)

```json
{
  "review_id": "R3021",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3022 — FLUFFY PUFFY 쇼토캣 & 오챠네코Ⅱ (B:오챠네코) (1개)

상품 ID: 3548

- [나의 히어로 아카데미아 FLUFFY PUFFY 쇼토캣 & 오챠네코Ⅱ (B:오챠네코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=74278895)

```json
{
  "review_id": "R3022",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3023 — Fluffy Puffy 오챠네코&라키라키&토가케 (A:오챠네코) (1개)

상품 ID: 3539

- [나의 히어로 아카데미아 Fluffy Puffy 오챠네코&라키라키&토가케 (A:오챠네코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=20163570)

```json
{
  "review_id": "R3023",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3024 — Fluffy Puffy 오챠네코&라키라키&토가케 (B:라키라키) (1개)

상품 ID: 3537

- [나의 히어로 아카데미아 Fluffy Puffy 오챠네코&라키라키&토가케 (B:라키라키)](https://www.bnkrmall.co.kr/goods/detail.do?gno=68474646)

```json
{
  "review_id": "R3024",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3025 — Fluffy Puffy 오챠네코&라키라키&토가케 (C:토가케) (1개)

상품 ID: 3538

- [나의 히어로 아카데미아 Fluffy Puffy 오챠네코&라키라키&토가케 (C:토가케)](https://www.bnkrmall.co.kr/goods/detail.do?gno=61322274)

```json
{
  "review_id": "R3025",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3026 — Fluffy Puffy 짹타로&차차마루 (A:짹타로) (1개)

상품 ID: 3460

- [귀멸의 칼날 Fluffy Puffy 짹타로&차차마루 (A:짹타로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=93506927)

```json
{
  "review_id": "R3026",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3027 — Fluffy Puffy 짹타로&차차마루 (B:차차마루) (1개)

상품 ID: 3459

- [귀멸의 칼날 Fluffy Puffy 짹타로&차차마루 (B:차차마루)](https://www.bnkrmall.co.kr/goods/detail.do?gno=54411565)

```json
{
  "review_id": "R3027",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3028 — Fluffy Puffy 쵸파 & 카루 (B:카루) (1개)

상품 ID: 3768

- [원피스 Fluffy Puffy 쵸파 & 카루 (B:카루)](https://www.bnkrmall.co.kr/goods/detail.do?gno=25900552)

```json
{
  "review_id": "R3028",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3029 — Fluffy Puffy 쵸파 vol.1 (ver.A) (1개)

상품 ID: 3614

- [원피스 Fluffy Puffy 쵸파 vol.1 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=27551624)

```json
{
  "review_id": "R3029",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3030 — Fluffy Puffy 쵸파 vol.1 (ver.B) (1개)

상품 ID: 3613

- [원피스 Fluffy Puffy 쵸파 vol.1 (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=77908801)

```json
{
  "review_id": "R3030",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3031 — Fluffy Puffy 츠무키츠네&사무키츠네 (A.츠무키츠네) (1개)

상품 ID: 3235

- [하이큐!! Fluffy Puffy 츠무키츠네&사무키츠네 (A.츠무키츠네)](https://www.bnkrmall.co.kr/goods/detail.do?gno=34250106)

```json
{
  "review_id": "R3031",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3032 — Fluffy Puffy 츠무키츠네&사무키츠네 (B.사무키츠네) (1개)

상품 ID: 3234

- [하이큐!! Fluffy Puffy 츠무키츠네&사무키츠네 (B.사무키츠네)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58794264)

```json
{
  "review_id": "R3032",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3033 — Fluffy Puffy 카게가라스&쿠로오네코 (A:카게가라스) (1개)

상품 ID: 4183

- [하이큐!! Fluffy Puffy 카게가라스&쿠로오네코 (A:카게가라스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=85619516)

```json
{
  "review_id": "R3033",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3034 — Fluffy Puffy 카게가라스&쿠로오네코 (B:쿠로오네코) (1개)

상품 ID: 4182

- [하이큐!! Fluffy Puffy 카게가라스&쿠로오네코 (B:쿠로오네코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=84834247)

```json
{
  "review_id": "R3034",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3035 — Fluffy Puffy 터보 할멈 (마네키네코) (ver.A) (1개)

상품 ID: 3253

- [단다단 Fluffy Puffy 터보 할멈 (마네키네코) (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=21074526)

```json
{
  "review_id": "R3035",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3036 — Fluffy Puffy 터보 할멈 (마네키네코) (ver.B) (1개)

상품 ID: 3252

- [단다단 Fluffy Puffy 터보 할멈 (마네키네코) (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=79137117)

```json
{
  "review_id": "R3036",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3037 — Fluffy Puffy 포치타 VER.A (1개)

상품 ID: 3948

- [체인소 맨 Fluffy Puffy 포치타 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=27865376)

```json
{
  "review_id": "R3037",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3038 — Fluffy Puffy 히나가라스&켄마네코 (A:히나가라스) (1개)

상품 ID: 4191

- [하이큐!! Fluffy Puffy 히나가라스&켄마네코 (A:히나가라스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=61042893)

```json
{
  "review_id": "R3038",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3039 — Fluffy Puffy 히나가라스&켄마네코 (B:켄마네코) (1개)

상품 ID: 4190

- [하이큐!! Fluffy Puffy 히나가라스&켄마네코 (B:켄마네코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=14877161)

```json
{
  "review_id": "R3039",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3040 — FRAME ARMS GIRL (1개)

상품 ID: 13

- [DURGA I DARKNESS QUEEN Ver.](https://www.kotobukiya.co.jp/en/product/detail/p4934054082131/)

```json
{
  "review_id": "R3040",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3041 — Full Scale Works 機動戦士ガンダム シャア・アズナブル シュタールヘルム (1개)

상품 ID: 1320

- [Full Scale Works 機動戦士ガンダム シャア・アズナブル シュタールヘルム 【再販】](https://megahobby.jp/products/item/6040/)

```json
{
  "review_id": "R3041",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3042 — G-CERAMICAL 라이징 프리덤 건담 (1개)

상품 ID: 3884

- [기동전사 건담 SEED FREEDOM G-CERAMICAL 라이징 프리덤 건담](https://www.bnkrmall.co.kr/goods/detail.do?gno=37013860)

```json
{
  "review_id": "R3042",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3043 — G.E.M.Caratシリーズ 銀魂 坂田銀時Ver.攘夷志士 (1개)

상품 ID: 1324

- [G.E.M.Caratシリーズ 銀魂 坂田銀時Ver.攘夷志士](https://megahobby.jp/products/item/6046/)

```json
{
  "review_id": "R3043",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3044 — G.E.M.シリーズ TVアニメ「桃源暗鬼」 てのひら四季 (1개)

상품 ID: 1379

- [G.E.M.シリーズ TVアニメ「桃源暗鬼」 てのひら四季](https://megahobby.jp/products/item/5252/)

```json
{
  "review_id": "R3044",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3045 — G.M.G. COLLECTION 11 機動戦士ガンダム 地球連邦軍 スレッガー・ロウ ノーマルスーツVer. (1개)

상품 ID: 1381

- [G.M.G. COLLECTION 11 機動戦士ガンダム 地球連邦軍 スレッガー・ロウ ノーマルスーツVer.](https://megahobby.jp/products/item/5417/)

```json
{
  "review_id": "R3045",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3046 — GLASSCAPE 마오마오 (1개)

상품 ID: 3432

- [약사의 혼잣말 GLASSCAPE 마오마오](https://www.bnkrmall.co.kr/goods/detail.do?gno=24354719)

```json
{
  "review_id": "R3046",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3047 — GLASSCAPE 페른 (1개)

상품 ID: 3845

- [장송의 프리렌 GLASSCAPE 페른](https://www.bnkrmall.co.kr/goods/detail.do?gno=83065932)

```json
{
  "review_id": "R3047",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3048 — GLASSCAPE 프리렌 (1개)

상품 ID: 3846

- [장송의 프리렌 GLASSCAPE 프리렌](https://www.bnkrmall.co.kr/goods/detail.do?gno=1181279)

```json
{
  "review_id": "R3048",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3049 — GLASSCAPE 프리렌Ⅱ (1개)

상품 ID: 3334

- [장송의 프리렌 GLASSCAPE 프리렌Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=49277310)

```json
{
  "review_id": "R3049",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3050 — GLASSCAPE 힘멜 (1개)

상품 ID: 3339

- [장송의 프리렌 GLASSCAPE 힘멜](https://www.bnkrmall.co.kr/goods/detail.do?gno=35665439)

```json
{
  "review_id": "R3050",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3051 — G × 소재 (베지트･마인 부우) (A:베지트) (1개)

상품 ID: 4145

- [드래곤볼 Z G × 소재 (베지트･마인 부우) (A:베지트)](https://www.bnkrmall.co.kr/goods/detail.do?gno=54367497)

```json
{
  "review_id": "R3051",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3052 — G × 소재 (베지트･마인 부우) (B:마인 부우 (순수)) (1개)

상품 ID: 4144

- [드래곤볼 Z G × 소재 (베지트･마인 부우) (B:마인 부우 (순수))](https://www.bnkrmall.co.kr/goods/detail.do?gno=42999261)

```json
{
  "review_id": "R3052",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3053 — G × 소재 내퍼 (1개)

상품 ID: 4243

- [드래곤볼 Z G × 소재 내퍼](https://www.bnkrmall.co.kr/goods/detail.do?gno=30716834)

```json
{
  "review_id": "R3053",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3054 — G × 소재 리쿰 (1개)

상품 ID: 4197

- [드래곤볼 Z G × 소재 리쿰](https://www.bnkrmall.co.kr/goods/detail.do?gno=98302366)

```json
{
  "review_id": "R3054",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3055 — G × 소재 마인 부우 (1개)

상품 ID: 4355

- [드래곤볼 Z G × 소재 마인 부우](https://www.bnkrmall.co.kr/goods/detail.do?gno=59965)

```json
{
  "review_id": "R3055",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3056 — G × 소재 무천도사 (1개)

상품 ID: 4256

- [드래곤볼 Z G × 소재 무천도사](https://www.bnkrmall.co.kr/goods/detail.do?gno=68722182)

```json
{
  "review_id": "R3056",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3057 — G × 소재 버독 (1개)

상품 ID: 3969

- [드래곤볼 Z G × 소재 버독](https://www.bnkrmall.co.kr/goods/detail.do?gno=20153169)

```json
{
  "review_id": "R3057",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3058 — G × 소재 베지터Ⅱ (1개)

상품 ID: 3617

- [드래곤볼 Z G × 소재 베지터Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=64623908)

```json
{
  "review_id": "R3058",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3059 — G × 소재 베지트 (1개)

상품 ID: 4383

- [드래곤볼 Z G × 소재 베지트](https://www.bnkrmall.co.kr/goods/detail.do?gno=59789)

```json
{
  "review_id": "R3059",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3060 — G × 소재 손오공 2 (1개)

상품 ID: 4617

- [드래곤볼 G × 소재 손오공 2](https://www.bnkrmall.co.kr/goods/detail.do?gno=55745)

```json
{
  "review_id": "R3060",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3061 — G × 소재 손오공 3 (1개)

상품 ID: 4291

- [드래곤볼 G × 소재 손오공 3](https://www.bnkrmall.co.kr/goods/detail.do?gno=34378560)

```json
{
  "review_id": "R3061",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3062 — G × 소재 손오공Ⅳ (1개)

상품 ID: 3856

- [드래곤볼 Z G × 소재 손오공Ⅳ](https://www.bnkrmall.co.kr/goods/detail.do?gno=11954065)

```json
{
  "review_id": "R3062",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3063 — G × 소재 손오반 II (1개)

상품 ID: 4451

- [드래곤볼 Z G × 소재 손오반 II](https://www.bnkrmall.co.kr/goods/detail.do?gno=59167)

```json
{
  "review_id": "R3063",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3064 — G × 소재 손오반 Ⅲ (1개)

상품 ID: 3794

- [드래곤볼 Z G × 소재 손오반 Ⅲ](https://www.bnkrmall.co.kr/goods/detail.do?gno=5146314)

```json
{
  "review_id": "R3064",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3065 — G × 소재 오천크스 (1개)

상품 ID: 4669

- [드래곤볼 Z G × 소재 오천크스](https://www.bnkrmall.co.kr/goods/detail.do?gno=15827)

```json
{
  "review_id": "R3065",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3066 — G × 소재 인조인간 16호 (1개)

상품 ID: 4325

- [드래곤볼 Z G × 소재 인조인간 16호](https://www.bnkrmall.co.kr/goods/detail.do?gno=52426716)

```json
{
  "review_id": "R3066",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3067 — G × 소재 인조인간 18호 (1개)

상품 ID: 4113

- [드래곤볼 Z G × 소재 인조인간 18호](https://www.bnkrmall.co.kr/goods/detail.do?gno=50007983)

```json
{
  "review_id": "R3067",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3068 — G × 소재 천진반 (1개)

상품 ID: 4064

- [드래곤볼 Z G × 소재 천진반](https://www.bnkrmall.co.kr/goods/detail.do?gno=67998953)

```json
{
  "review_id": "R3068",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3069 — G × 소재 타레스 (1개)

상품 ID: 4079

- [드래곤볼 Z G × 소재 타레스](https://www.bnkrmall.co.kr/goods/detail.do?gno=70586409)

```json
{
  "review_id": "R3069",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3070 — G × 소재 트랭크스 (1개)

상품 ID: 3739

- [드래곤볼 Z G × 소재 트랭크스](https://www.bnkrmall.co.kr/goods/detail.do?gno=95779202)

```json
{
  "review_id": "R3070",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3071 — G × 소재 피콜로 (1개)

상품 ID: 4341

- [드래곤볼 Z G × 소재 피콜로](https://www.bnkrmall.co.kr/goods/detail.do?gno=63743834)

```json
{
  "review_id": "R3071",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3072 — Gのレコンギスタ メガファウナRe. (1개)

상품 ID: 620

- [Gのレコンギスタ メガファウナRe.](https://megahobby.jp/products/item/4677/)

```json
{
  "review_id": "R3072",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3073 — Heritage Edition- DX 新世紀GPXサイバーフォーミュラ スゴウレガード10V5000＆スーパーアスラーダ01 サーキットモード (1개)

상품 ID: 1165

- [-Heritage Edition- DX 新世紀GPXサイバーフォーミュラ スゴウレガード10V5000＆スーパーアスラーダ01 サーキットモード](https://megahobby.jp/products/item/5770/)

```json
{
  "review_id": "R3073",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3074 — Heritage Edition- 新世紀GPXサイバーフォーミュラSIN νアスラーダAKF-0/G スパイラルブーストモード (1개)

상품 ID: 1072

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラSIN νアスラーダAKF-0/G スパイラルブーストモード](https://megahobby.jp/products/item/5590/)

```json
{
  "review_id": "R3074",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3075 — Heritage Edition- 新世紀GPXサイバーフォーミュラSIN 凰呀AN-21 スーパー・エアロ・ブーストモード (1개)

상품 ID: 1071

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラSIN 凰呀AN-21 スーパー・エアロ・ブーストモード](https://megahobby.jp/products/item/5589/)

```json
{
  "review_id": "R3075",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3076 — Heritage Edition- 新世紀GPXサイバーフォーミュラ アオイステルスジャガーZ-7 (1개)

상품 ID: 1326

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ アオイステルスジャガーZ-7](https://megahobby.jp/products/item/6048/)

```json
{
  "review_id": "R3076",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3077 — Heritage Edition- 新世紀GPXサイバーフォーミュラ アオイスペリオンGT (1개)

상품 ID: 888

- [ -Heritage Edition- 新世紀GPXサイバーフォーミュラ アオイスペリオンGT](https://megahobby.jp/products/item/5304/)

```json
{
  "review_id": "R3077",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3078 — Heritage Edition- 新世紀GPXサイバーフォーミュラ アスラーダG.S.X (1개)

상품 ID: 886

- [ -Heritage Edition- 新世紀GPXサイバーフォーミュラ アスラーダG.S.X](https://megahobby.jp/products/item/5302/)

```json
{
  "review_id": "R3078",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3079 — Heritage Edition- 新世紀GPXサイバーフォーミュラ アスラーダG.S.X エアロモード (1개)

상품 ID: 1172

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ アスラーダG.S.X エアロモード](https://megahobby.jp/products/item/5803/)

```json
{
  "review_id": "R3079",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3080 — Heritage Edition- 新世紀GPXサイバーフォーミュラ アルバトランダー602 (1개)

상품 ID: 887

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ アルバトランダー602](https://megahobby.jp/products/item/5303/)

```json
{
  "review_id": "R3080",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3081 — Heritage Edition- 新世紀GPXサイバーフォーミュラ スーパーアスラーダ01 (1개)

상품 ID: 596

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ スーパーアスラーダ01](https://megahobby.jp/products/item/4628/)

```json
{
  "review_id": "R3081",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3082 — Heritage Edition- 新世紀GPXサイバーフォーミュラ スーパーアスラーダ01 サーキットモード (1개)

상품 ID: 856

- [-Heritage Edition-  新世紀GPXサイバーフォーミュラ スーパーアスラーダ01 サーキットモード【再販】](https://megahobby.jp/products/item/5226/)

```json
{
  "review_id": "R3082",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3083 — Heritage Edition- 新世紀GPXサイバーフォーミュラ ナイトセイバー005 (1개)

상품 ID: 1173

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ ナイトセイバー005](https://megahobby.jp/products/item/5804/)

```json
{
  "review_id": "R3083",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3084 — Heritage Edition- 新世紀GPXサイバーフォーミュラ プロトジャガーZ-6 (1개)

상품 ID: 1327

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ プロトジャガーZ-6](https://megahobby.jp/products/item/6049/)

```json
{
  "review_id": "R3084",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3085 — Heritage Edition- 新世紀GPXサイバーフォーミュラ ミッショネルVR-4 (1개)

상품 ID: 1174

- [-Heritage Edition- 新世紀GPXサイバーフォーミュラ ミッショネルVR-4](https://megahobby.jp/products/item/5805/)

```json
{
  "review_id": "R3085",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3086 — HEXA GEAR (1개)

상품 ID: 25

- [V-THOR Assault Type "Ji rei" (Swift Thunder)](https://www.kotobukiya.co.jp/en/product/detail/p4934054087594/)

```json
{
  "review_id": "R3086",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3087 — HI-METAL R VF-0S PHOENIX（ROY FOCKER USE） ＋ QF-2200D-B GHOST (1개)

상품 ID: 1871

- [HI-METAL R VF-0S PHOENIX（ROY FOCKER USE） ＋ QF-2200D-B GHOST](https://www.bnkrmall.co.kr/goods/detail.do?gno=22971933)

```json
{
  "review_id": "R3087",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3088 — HI-METAL R VF-2SS VALKYRIE II + SAP (Silvie Gena use) -Lovers Again (1개)

상품 ID: 1985

- [HI-METAL R VF-2SS VALKYRIE II + SAP (Silvie Gena use) -Lovers Again-](https://www.bnkrmall.co.kr/goods/detail.do?gno=45123267)

```json
{
  "review_id": "R3088",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3089 — HI-METAL R 드라고나-1 ＆ 캐벌리어 0 (1개)

상품 ID: 1659

- [HI-METAL R 드라고나-1 ＆ 캐벌리어 0](https://www.bnkrmall.co.kr/goods/detail.do?gno=77949491)

```json
{
  "review_id": "R3089",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3090 — HI-METAL R 드라고나-1 커스텀 (1개)

상품 ID: 2097

- [HI-METAL R 드라고나-1 커스텀](https://www.bnkrmall.co.kr/goods/detail.do?gno=57236)

```json
{
  "review_id": "R3090",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3091 — HI-METAL R 레이즈너 (1개)

상품 ID: 1827

- [HI-METAL R 레이즈너](https://www.bnkrmall.co.kr/goods/detail.do?gno=15319568)

```json
{
  "review_id": "R3091",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3092 — HI-METAL R 스코프 독 (1개)

상품 ID: 1858

- [HI-METAL R 스코프 독](https://www.bnkrmall.co.kr/goods/detail.do?gno=93124031)

```json
{
  "review_id": "R3092",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3093 — Holiday Memories 게임 (1개)

상품 ID: 3347

- [하츠네 미쿠 Holiday Memories 게임](https://www.bnkrmall.co.kr/goods/detail.do?gno=85494265)

```json
{
  "review_id": "R3093",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3094 — HOLIDAY MEMORIES 골프 (1개)

상품 ID: 4163

- [하츠네 미쿠 HOLIDAY MEMORIES 골프](https://www.bnkrmall.co.kr/goods/detail.do?gno=22098872)

```json
{
  "review_id": "R3094",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3095 — HOLIDAY MEMORIES 등산 (1개)

상품 ID: 4149

- [하츠네 미쿠 HOLIDAY MEMORIES 등산](https://www.bnkrmall.co.kr/goods/detail.do?gno=12175694)

```json
{
  "review_id": "R3095",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3096 — HOLIDAY MEMORIES 카메라 (1개)

상품 ID: 4014

- [하츠네 미쿠 HOLIDAY MEMORIES 카메라](https://www.bnkrmall.co.kr/goods/detail.do?gno=83147789)

```json
{
  "review_id": "R3096",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3097 — HUNTER×HUNTER MEMORABLE SAGA 스페셜 곤 (1개)

상품 ID: 1999

- [HUNTER×HUNTER MEMORABLE SAGA 스페셜 곤](https://www.bnkrmall.co.kr/goods/detail.do?gno=74674168)

```json
{
  "review_id": "R3097",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3098 — HUNTER×HUNTER MEMORABLE SAGA 스페셜 히소카 (1개)

상품 ID: 3875

- [HUNTER×HUNTER MEMORABLE SAGA 스페셜 히소카](https://www.bnkrmall.co.kr/goods/detail.do?gno=91293836)

```json
{
  "review_id": "R3098",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3099 — HUNTER×HUNTER MEMORABLE SAGA 키르아 (1개)

상품 ID: 3949

- [HUNTER×HUNTER MEMORABLE SAGA 키르아](https://www.bnkrmall.co.kr/goods/detail.do?gno=59246661)

```json
{
  "review_id": "R3099",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3100 — HUNTER×HUNTER NYANTER×NYANTER HUNTER×CAT (1개)

상품 ID: 1227

- [HUNTER×HUNTER NYANTER×NYANTER　HUNTER×CAT](https://megahobby.jp/products/item/5862/)

```json
{
  "review_id": "R3100",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3101 — HUNTER×HUNTER NYANTER×NYANTER 幻影旅団×CAT (1개)

상품 ID: 1264

- [HUNTER×HUNTER NYANTER×NYANTER　幻影旅団×CAT　 ](https://megahobby.jp/products/item/5948/)

```json
{
  "review_id": "R3101",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3102 — HUNTER×HUNTER キルア＝ゾルディック (1개)

상품 ID: 1277

- [HUNTER×HUNTER キルア＝ゾルディック](https://megahobby.jp/products/item/5964/)

```json
{
  "review_id": "R3102",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3103 — HUNTER×HUNTER クラピカ (1개)

상품 ID: 1344

- [HUNTER×HUNTER クラピカ](https://megahobby.jp/products/item/6072/)

```json
{
  "review_id": "R3103",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3104 — HUNTER×HUNTER クロロ (1개)

상품 ID: 6161

- [HUNTER×HUNTER クロロ](https://megahobby.jp/products/item/6185/)

```json
{
  "review_id": "R3104",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3105 — HUNTER×HUNTER ゴン＝フリークス (1개)

상품 ID: 1278

- [HUNTER×HUNTER ゴン＝フリークス](https://megahobby.jp/products/item/5965/)

```json
{
  "review_id": "R3105",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3106 — HUNTER×HUNTER ヒソカ (1개)

상품 ID: 6160

- [HUNTER×HUNTER ヒソカ](https://megahobby.jp/products/item/6186/)

```json
{
  "review_id": "R3106",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3107 — HUNTER×HUNTER レオリオ (1개)

상품 ID: 1345

- [HUNTER×HUNTER レオリオ](https://megahobby.jp/products/item/6073/)

```json
{
  "review_id": "R3107",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3108 — HUNTER×HUNTER 곤 G.I.편 (1개)

상품 ID: 3632

- [HUNTER×HUNTER 피규어 곤 G.I.편](https://www.bnkrmall.co.kr/goods/detail.do?gno=25834502)

```json
{
  "review_id": "R3108",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3109 — HUNTER×HUNTER 키르아 G.I.편 (1개)

상품 ID: 3631

- [HUNTER×HUNTER 피규어 키르아 G.I.편](https://www.bnkrmall.co.kr/goods/detail.do?gno=66264181)

```json
{
  "review_id": "R3109",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3110 — HUNTER×HUNTER 피그라이프 곤 (1개)

상품 ID: 3806

- [HUNTER×HUNTER 피그라이프 곤 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=90433474)

```json
{
  "review_id": "R3110",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3111 — HUNTER×HUNTER 피그라이프 포트크린 (1개)

상품 ID: 3278

- [HUNTER×HUNTER 피그라이프 포트크린](https://www.bnkrmall.co.kr/goods/detail.do?gno=31301583)

```json
{
  "review_id": "R3111",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3112 — HUNTER×HUNTER 헌팅 아카이브 네테로 (1개)

상품 ID: 3800

- [HUNTER×HUNTER 헌팅 아카이브 네테로](https://www.bnkrmall.co.kr/goods/detail.do?gno=62775294)

```json
{
  "review_id": "R3112",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3113 — HUNTER×HUNTER 헌팅 아카이브 크라피카 -EMPEROR TIME (1개)

상품 ID: 3465

- [HUNTER×HUNTER 헌팅 아카이브 크라피카 -EMPEROR TIME-](https://www.bnkrmall.co.kr/goods/detail.do?gno=96014117)

```json
{
  "review_id": "R3113",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3114 — HUNTER×HUNTER 헌팅 아카이브 클로로 (1개)

상품 ID: 3789

- [HUNTER×HUNTER 헌팅 아카이브 클로로](https://www.bnkrmall.co.kr/goods/detail.do?gno=98297170)

```json
{
  "review_id": "R3114",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3115 — HUNTER×HUNTER 헌팅 아카이브 키르아 (1개)

상품 ID: 3277

- [HUNTER×HUNTER 헌팅 아카이브 키르아](https://www.bnkrmall.co.kr/goods/detail.do?gno=53203462)

```json
{
  "review_id": "R3115",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3116 — HUNTER×HUNTER 히소카 G.I.편 (1개)

상품 ID: 3630

- [HUNTER×HUNTER 피규어 히소카 G.I.편](https://www.bnkrmall.co.kr/goods/detail.do?gno=88761000)

```json
{
  "review_id": "R3116",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3117 — HYOKOFIG 도우마 (1개)

상품 ID: 3743

- [귀멸의 칼날 HYOKOFIG 도우마](https://www.bnkrmall.co.kr/goods/detail.do?gno=64723045)

```json
{
  "review_id": "R3117",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3118 — HYOKOFIG 아카자 (1개)

상품 ID: 3368

- [귀멸의 칼날 HYOKOFIG 아카자](https://www.bnkrmall.co.kr/goods/detail.do?gno=53562853)

```json
{
  "review_id": "R3118",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3119 — HYOKOFIG 엠포리오 이반코프 (1개)

상품 ID: 3244

- [원피스 HYOKOFIG 엠포리오 이반코프](https://www.bnkrmall.co.kr/goods/detail.do?gno=47531607)

```json
{
  "review_id": "R3119",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3120 — HYOKOFIG 카마도 네즈코 (1개)

상품 ID: 3757

- [귀멸의 칼날 HYOKOFIG 카마도 네즈코](https://www.bnkrmall.co.kr/goods/detail.do?gno=43056812)

```json
{
  "review_id": "R3120",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3121 — INTERNAL STRUCTURE GAT-X105 스트라이크 건담 WEAPON ver.(ver.A) (1개)

상품 ID: 4486

- [기동전사 건담 SEED INTERNAL STRUCTURE GAT-X105 스트라이크 건담 WEAPON ver.(ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57995)

```json
{
  "review_id": "R3121",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3122 — INTERNAL STRUCTURE GAT-X105 스트라이크 건담 WEAPON ver.(verB) (1개)

상품 ID: 4485

- [기동전사 건담 SEED INTERNAL STRUCTURE GAT-X105 스트라이크 건담 WEAPON ver.(verB)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57996)

```json
{
  "review_id": "R3122",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3123 — INTERNAL STRUCTURE MS-06F 자쿠 II Ver.A (1개)

상품 ID: 4679

- [기동전사 건담 INTERNAL STRUCTURE MS-06F 자쿠 II Ver.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=15778)

```json
{
  "review_id": "R3123",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3124 — INTERNAL STRUCTURE RX-78-2 건담 블랙 클리어Ver. (1개)

상품 ID: 4421

- [기동전사 건담 INTERNAL STRUCTURE RX-78-2 건담 블랙 클리어Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=59288)

```json
{
  "review_id": "R3124",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3125 — INTERNAL STRUCTURE 스트라이크 건담 Ver.A (1개)

상품 ID: 4584

- [기동전사 건담 SEED INTERNAL STRUCTURE 스트라이크 건담 Ver.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=56313)

```json
{
  "review_id": "R3125",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3126 — K-303d メリッサ クィーン(メディック) (1개)

상품 ID: 683

- [K-303d メリッサ クィーン(メディック)](https://megahobby.jp/products/item/4825/)

```json
{
  "review_id": "R3126",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3127 — K-303s アリッサ デュオ(メディック) (1개)

상품 ID: 684

- [K-303s アリッサ デュオ(メディック)](https://megahobby.jp/products/item/4826/)

```json
{
  "review_id": "R3127",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3128 — KAITANICS Honda スーパーカブ110 ①グリントウェーブブルーメタリック ②バージンベージュ ③クラシカルホワイト ④タスマニアグリーンメタリック (1개)

상품 ID: 1323

- [KAITANICS Honda スーパーカブ110 ①グリントウェーブブルーメタリック ②バージンベージュ ③クラシカルホワイト ④タスマニアグリーンメタリック](https://megahobby.jp/products/item/6043/)

```json
{
  "review_id": "R3128",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3129 — KAITO (1개)

상품 ID: 1024

- [KAITO](https://megahobby.jp/products/item/5525/)

```json
{
  "review_id": "R3129",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3130 — LOGBOX RE BIRTH エッグヘッド編 02 (1개)

상품 ID: 1218

- [LOGBOX RE BIRTH エッグヘッド編 02](https://megahobby.jp/products/item/5853/)

```json
{
  "review_id": "R3130",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3131 — LUFFY's 모험의 기억 [Vol.1] 1BOX (1개)

상품 ID: 1948

- [LUFFY's 모험의 기억 (Vol.1) 1BOX](https://www.bnkrmall.co.kr/goods/detail.do?gno=62472418)

```json
{
  "review_id": "R3131",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3132 — LUFFY's 모험의 기억 [Vol.3] 1BOX (1개)

상품 ID: 1645

- [LUFFY's 모험의 기억 (Vol.3) 1BOX](https://www.bnkrmall.co.kr/goods/detail.do?gno=36541826)

```json
{
  "review_id": "R3132",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3133 — LUFFYs 모험의 기억 [Vol.2] (1개)

상품 ID: 1853

- [LUFFYs 모험의 기억 (Vol.2)](https://www.bnkrmall.co.kr/goods/detail.do?gno=95988505)

```json
{
  "review_id": "R3133",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3134 — LUFFYs 모험의 기억 [Vol.2] 1BOX (1개)

상품 ID: 1852

- [LUFFYs 모험의 기억 (Vol.2) 1BOX](https://www.bnkrmall.co.kr/goods/detail.do?gno=82718681)

```json
{
  "review_id": "R3134",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3135 — LUFFY’s 모험의 기억 [Vol.1] (1개)

상품 ID: 1949

- [LUFFY’s 모험의 기억 (Vol.1)](https://www.bnkrmall.co.kr/goods/detail.do?gno=29122192)

```json
{
  "review_id": "R3135",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3136 — LUFFY’s 모험의 기억 [Vol.4] (1개)

상품 ID: 1673

- [LUFFY’s 모험의 기억 (Vol.4)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15311346)

```json
{
  "review_id": "R3136",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3137 — LUFFY’s 모험의 기억 [Vol.4] 1BOX (1개)

상품 ID: 1672

- [LUFFY’s 모험의 기억 (Vol.4) 1BOX](https://www.bnkrmall.co.kr/goods/detail.do?gno=411733)

```json
{
  "review_id": "R3137",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3138 — LUPIN THE GALLERY 55th Limited Model (1개)

상품 ID: 1346

- [LUPIN THE GALLERY 55th Limited Model](https://megahobby.jp/products/item/6074/)

```json
{
  "review_id": "R3138",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3139 — LUPIN THE ⅢRD 루팡 3세 (1개)

상품 ID: 3464

- [LUPIN THE ⅢRD 루팡 3세 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=445900)

```json
{
  "review_id": "R3139",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3140 — LUPIN THE ⅢRD 미네 후지코 (1개)

상품 ID: 3346

- [LUPIN THE ⅢRD 미네 후지코 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=88552195)

```json
{
  "review_id": "R3140",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3141 — LUPIN THE ⅢRD 이시카와 고에몽 (1개)

상품 ID: 3274

- [LUPIN THE ⅢRD 이시카와 고에몽 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=35096191)

```json
{
  "review_id": "R3141",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3142 — LUPIN THE ⅢRD 제니가타 경부 (1개)

상품 ID: 3340

- [LUPIN THE ⅢRD 제니가타 경부 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=58230584)

```json
{
  "review_id": "R3142",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3143 — LUPIN THE ⅢRD 지겐 다이스케 (1개)

상품 ID: 3404

- [LUPIN THE ⅢRD 지겐 다이스케 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=96381116)

```json
{
  "review_id": "R3143",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3144 — Magic Knight Rayearth (1개)

상품 ID: 19

- [Hikaru Shidou](https://www.kotobukiya.co.jp/en/product/detail/p4934054076413/)

```json
{
  "review_id": "R3144",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3145 — Magic Repo Man : Dumped by My Party, I’ll Cash In With a Cute Support Fairy to Become the Strongest! (1개)

상품 ID: 11

- [Empee](https://www.kotobukiya.co.jp/en/product/detail/p4934054084869/)

```json
{
  "review_id": "R3145",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3146 — MAXIMATIC BLOOD CHAINS 이치고 (1개)

상품 ID: 3302

- [블리치 MAXIMATIC BLOOD CHAINS 이치고](https://www.bnkrmall.co.kr/goods/detail.do?gno=92110285)

```json
{
  "review_id": "R3146",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3147 — MAXIMATIC PLUS 롤로노아 조로 (1개)

상품 ID: 3251

- [원피스 MAXIMATIC PLUS 롤로노아 조로](https://www.bnkrmall.co.kr/goods/detail.do?gno=65982618)

```json
{
  "review_id": "R3147",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3148 — MAXIMATIC PLUS 몽키 D 루피Ⅰ (1개)

상품 ID: 3661

- [원피스 MAXIMATIC PLUS 몽키 D 루피Ⅰ](https://www.bnkrmall.co.kr/goods/detail.do?gno=88877473)

```json
{
  "review_id": "R3148",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3149 — MAXIMATIC PLUS 몽키 D 루피 Ⅱ (1개)

상품 ID: 3417

- [원피스 MAXIMATIC PLUS 몽키 D 루피 Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=26176671)

```json
{
  "review_id": "R3149",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3150 — MAXIMATICPLUS 몽키 D 루피 마린포드 (1개)

상품 ID: 3380

- [원피스 MAXIMATICPLUS 몽키 D 루피 마린포드](https://www.bnkrmall.co.kr/goods/detail.do?gno=56710199)

```json
{
  "review_id": "R3150",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3151 — MAXIMATIC PLUS 상디 (1개)

상품 ID: 3250

- [원피스 MAXIMATIC PLUS 상디](https://www.bnkrmall.co.kr/goods/detail.do?gno=82329891)

```json
{
  "review_id": "R3151",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3152 — MAXIMATIC PLUS 스쿠나 (1개)

상품 ID: 3742

- [주술회전 MAXIMATIC PLUS 스쿠나](https://www.bnkrmall.co.kr/goods/detail.do?gno=54362285)

```json
{
  "review_id": "R3152",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3153 — MAXIMATICPLUS 쿠라마 (1개)

상품 ID: 3561

- [유유백서 MAXIMATICPLUS 쿠라마](https://www.bnkrmall.co.kr/goods/detail.do?gno=21574089)

```json
{
  "review_id": "R3153",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3154 — MAXIMATICPLUS 포트거스 D. 에이스 마린포드 (1개)

상품 ID: 3315

- [원피스 MAXIMATICPLUS 포트거스 D. 에이스 마린포드](https://www.bnkrmall.co.kr/goods/detail.do?gno=26655981)

```json
{
  "review_id": "R3154",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3155 — MAXIMATIC 고죠 사토루 (1개)

상품 ID: 4082

- [주술회전 MAXIMATIC 고죠 사토루](https://www.bnkrmall.co.kr/goods/detail.do?gno=32489869)

```json
{
  "review_id": "R3155",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3156 — MAXIMATIC 고죠 사토루Ⅱ (1개)

상품 ID: 3894

- [주술회전 MAXIMATIC 고죠 사토루Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=4484020)

```json
{
  "review_id": "R3156",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3157 — MAXIMATIC 군코 궁 (1개)

상품 ID: 3245

- [원피스 MAXIMATIC 군코 궁](https://www.bnkrmall.co.kr/goods/detail.do?gno=28121068)

```json
{
  "review_id": "R3157",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3158 — MAXIMATIC 그림죠 재거잭 (1개)

상품 ID: 3801

- [블리치 MAXIMATIC 그림죠 재거잭](https://www.bnkrmall.co.kr/goods/detail.do?gno=26329982)

```json
{
  "review_id": "R3158",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3159 — MAXIMATIC 나오야 젠인 (1개)

상품 ID: 3697

- [주술회전 MAXIMATIC 나오야 젠인](https://www.bnkrmall.co.kr/goods/detail.do?gno=3841753)

```json
{
  "review_id": "R3159",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3160 — MAXIMATIC 도우마 (1개)

상품 ID: 3458

- [귀멸의 칼날 MAXIMATIC 도우마](https://www.bnkrmall.co.kr/goods/detail.do?gno=10041073)

```json
{
  "review_id": "R3160",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3161 — MAXIMATIC 렌고쿠 쿄쥬로 (1개)

상품 ID: 3937

- [귀멸의 칼날 MAXIMATIC 렌고쿠 쿄쥬로](https://www.bnkrmall.co.kr/goods/detail.do?gno=18117655)

```json
{
  "review_id": "R3161",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3162 — MAXIMATIC 몽키 D. 루피 I (1개)

상품 ID: 4680

- [원피스 MAXIMATIC 몽키 D. 루피 I](https://www.bnkrmall.co.kr/goods/detail.do?gno=15686)

```json
{
  "review_id": "R3162",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3163 — MAXIMATIC 몽키 D. 루피 II (1개)

상품 ID: 4684

- [원피스 MAXIMATIC 몽키 D. 루피 II](https://www.bnkrmall.co.kr/goods/detail.do?gno=15678)

```json
{
  "review_id": "R3163",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3164 — MAXIMATIC 몽키 D 루피 Ⅰ・Ⅱ 스페셜 (VER.A) (1개)

상품 ID: 3928

- [원피스 MAXIMATIC 몽키 D 루피 Ⅰ・Ⅱ 스페셜 (VER.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=22339184)

```json
{
  "review_id": "R3164",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3165 — MAXIMATIC 몽키 D 루피 Ⅰ・Ⅱ 스페셜 (VER.B) (1개)

상품 ID: 3927

- [원피스 MAXIMATIC 몽키 D 루피 Ⅰ・Ⅱ 스페셜 (VER.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=51602900)

```json
{
  "review_id": "R3165",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3166 — MAXIMATIC 미도리야 이즈쿠 (1개)

상품 ID: 3486

- [나의 히어로 아카데미아 MAXIMATIC 미도리야 이즈쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=16303238)

```json
{
  "review_id": "R3166",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3167 — MAXIMATIC 미도리야 이즈쿠 Ⅱ (1개)

상품 ID: 3455

- [나의 히어로 아카데미아 MAXIMATIC 미도리야 이즈쿠 Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=37680999)

```json
{
  "review_id": "R3167",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3168 — MAXIMATIC 미도리야 이즈쿠Ⅲ (1개)

상품 ID: 3620

- [나의 히어로 아카데미아 MAXIMATIC 미도리야 이즈쿠Ⅲ](https://www.bnkrmall.co.kr/goods/detail.do?gno=43488379)

```json
{
  "review_id": "R3168",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3169 — MAXIMATIC 미도리야 이즈쿠 THE BEGINNING (1개)

상품 ID: 3563

- [나의 히어로 아카데미아 MAXIMATIC 미도리야 이즈쿠 THE BEGINNING](https://www.bnkrmall.co.kr/goods/detail.do?gno=60878067)

```json
{
  "review_id": "R3169",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3170 — MAXIMATIC 미르코 (1개)

상품 ID: 3338

- [나의 히어로 아카데미아 MAXIMATIC 미르코](https://www.bnkrmall.co.kr/goods/detail.do?gno=97839002)

```json
{
  "review_id": "R3170",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3171 — MAXIMATIC 바쿠고 카츠키 (1개)

상품 ID: 3912

- [나의 히어로 아카데미아 MAXIMATIC 바쿠고 카츠키](https://www.bnkrmall.co.kr/goods/detail.do?gno=88972282)

```json
{
  "review_id": "R3171",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3172 — MAXIMATIC 바쿠고 카츠키&키리시마 에이지로 (B.키리시마 에이지로) (1개)

상품 ID: 3446

- [나의 히어로 아카데미아 MAXIMATIC 바쿠고 카츠키&키리시마 에이지로 (B.키리시마 에이지로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=62430330)

```json
{
  "review_id": "R3172",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3173 — MAXIMATIC 바쿠고 카츠키Ⅱ (1개)

상품 ID: 3666

- [나의 히어로 아카데미아 MAXIMATIC 바쿠고 카츠키Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=59348897)

```json
{
  "review_id": "R3173",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3174 — MAXIMATIC 바쿠고 카츠키 Ⅲ (1개)

상품 ID: 3337

- [나의 히어로 아카데미아 MAXIMATIC 바쿠고 카츠키 Ⅲ](https://www.bnkrmall.co.kr/goods/detail.do?gno=17895116)

```json
{
  "review_id": "R3174",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3175 — MAXIMATIC 바쿠고 카츠키 THE BEGINNING (1개)

상품 ID: 3562

- [나의 히어로 아카데미아 MAXIMATIC 바쿠고 카츠키 THE BEGINNING](https://www.bnkrmall.co.kr/goods/detail.do?gno=38579147)

```json
{
  "review_id": "R3175",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3176 — MAXIMATIC 베지터 II (1개)

상품 ID: 4603

- [드래곤볼 Z MAXIMATIC 베지터 II](https://www.bnkrmall.co.kr/goods/detail.do?gno=56070)

```json
{
  "review_id": "R3176",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3177 — MAXIMATIC 사이타마 (1개)

상품 ID: 3536

- [원펀맨 MAXIMATIC 사이타마](https://www.bnkrmall.co.kr/goods/detail.do?gno=30719171)

```json
{
  "review_id": "R3177",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3178 — MAXIMATIC 샹크스 (1개)

상품 ID: 3316

- [원피스 MAXIMATIC 샹크스](https://www.bnkrmall.co.kr/goods/detail.do?gno=22904790)

```json
{
  "review_id": "R3178",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3179 — MAXIMATIC 손오공 III (1개)

상품 ID: 4706

- [드래곤볼 Z MAXIMATIC 손오공 III](https://www.bnkrmall.co.kr/goods/detail.do?gno=15302)

```json
{
  "review_id": "R3179",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3180 — MAXIMATIC 손오공 IV (1개)

상품 ID: 4693

- [드래곤볼 Z MAXIMATIC 손오공 IV](https://www.bnkrmall.co.kr/goods/detail.do?gno=15497)

```json
{
  "review_id": "R3180",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3181 — MAXIMATIC 손오공 V (1개)

상품 ID: 4662

- [드래곤볼 슈퍼 MAXIMATIC 손오공 V](https://www.bnkrmall.co.kr/goods/detail.do?gno=15868)

```json
{
  "review_id": "R3181",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3182 — MAXIMATIC 슈타르크 (1개)

상품 ID: 3695

- [장송의 프리렌 MAXIMATIC 슈타르크](https://www.bnkrmall.co.kr/goods/detail.do?gno=15755692)

```json
{
  "review_id": "R3182",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3183 — MAXIMATIC 스쿠나 SPECIAL VER. (1개)

상품 ID: 3984

- [주술회전 MAXIMATIC 스쿠나 SPECIAL VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=70603889)

```json
{
  "review_id": "R3183",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3184 — MAXIMATIC 아가츠마 젠이츠 (1개)

상품 ID: 3254

- [귀멸의 칼날 MAXIMATIC 아가츠마 젠이츠](https://www.bnkrmall.co.kr/goods/detail.do?gno=54787134)

```json
{
  "review_id": "R3184",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3185 — MAXIMATIC 아카자 (1개)

상품 ID: 3503

- [귀멸의 칼날 MAXIMATIC 아카자](https://www.bnkrmall.co.kr/goods/detail.do?gno=44524280)

```json
{
  "review_id": "R3185",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3186 — MAXIMATIC 여성형 거인 (1개)

상품 ID: 3385

- [진격의 거인 MAXIMATIC 여성형 거인](https://www.bnkrmall.co.kr/goods/detail.do?gno=41162366)

```json
{
  "review_id": "R3186",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3187 — MAXIMATIC 옷코츠 유타 사멸회유 (1개)

상품 ID: 3669

- [주술회전 MAXIMATIC 옷코츠 유타 사멸회유](https://www.bnkrmall.co.kr/goods/detail.do?gno=34991880)

```json
{
  "review_id": "R3187",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3188 — MAXIMATIC 옷코츠 유타 사멸회유ii (1개)

상품 ID: 3290

- [주술회전 MAXIMATIC 옷코츠 유타 사멸회유ii](https://www.bnkrmall.co.kr/goods/detail.do?gno=97174466)

```json
{
  "review_id": "R3188",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3189 — MAXIMATIC 요호 쿠라마 (1개)

상품 ID: 3869

- [유유백서 MAXIMATIC 요호 쿠라마](https://www.bnkrmall.co.kr/goods/detail.do?gno=31518895)

```json
{
  "review_id": "R3189",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3190 — MAXIMATIC 우라메시 유스케 (1개)

상품 ID: 3934

- [유유백서 MAXIMATIC 우라메시 유스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=34560571)

```json
{
  "review_id": "R3190",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3191 — MAXIMATIC 우라하라 키스케 (1개)

상품 ID: 3512

- [블리치 MAXIMATIC 우라하라 키스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=33288601)

```json
{
  "review_id": "R3191",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3192 — MAXIMATIC 우르키오라 시파 (1개)

상품 ID: 3647

- [블리치 MAXIMATIC 우르키오라 시파](https://www.bnkrmall.co.kr/goods/detail.do?gno=50377996)

```json
{
  "review_id": "R3192",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3193 — MAXIMATIC 우즈이 텐겐 (1개)

상품 ID: 4027

- [귀멸의 칼날 MAXIMATIC 우즈이 텐겐](https://www.bnkrmall.co.kr/goods/detail.do?gno=39794035)

```json
{
  "review_id": "R3193",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3194 — MAXIMATIC 이레이저 헤드 (1개)

상품 ID: 3415

- [나의 히어로 아카데미아 MAXIMATIC 이레이저 헤드](https://www.bnkrmall.co.kr/goods/detail.do?gno=11187643)

```json
{
  "review_id": "R3194",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3195 — MAXIMATIC 이시고리 류 (1개)

상품 ID: 3320

- [주술회전 MAXIMATIC 이시고리 류](https://www.bnkrmall.co.kr/goods/detail.do?gno=5796396)

```json
{
  "review_id": "R3195",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3196 — MAXIMATIC 이타도리 유지･후시구로 메구미 (A:이타도리 유지) (1개)

상품 ID: 3820

- [주술회전 MAXIMATIC 이타도리 유지･후시구로 메구미 (A:이타도리 유지)](https://www.bnkrmall.co.kr/goods/detail.do?gno=62600836)

```json
{
  "review_id": "R3196",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3197 — MAXIMATIC 이타도리 유지･후시구로 메구미 (B:후시구로 메구미) (1개)

상품 ID: 3819

- [주술회전 MAXIMATIC 이타도리 유지･후시구로 메구미 (B:후시구로 메구미)](https://www.bnkrmall.co.kr/goods/detail.do?gno=64492094)

```json
{
  "review_id": "R3197",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3198 — MAXIMATIC 이타도리 유지 사멸회유 (1개)

상품 ID: 3657

- [주술회전 MAXIMATIC 이타도리 유지 사멸회유](https://www.bnkrmall.co.kr/goods/detail.do?gno=37480000)

```json
{
  "review_id": "R3198",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3199 — MAXIMATIC 이타도리 유지 사멸회유Ⅱ (1개)

상품 ID: 3525

- [주술회전 MAXIMATIC 이타도리 유지 사멸회유Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=78861523)

```json
{
  "review_id": "R3199",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3200 — MAXIMATIC 자라키 켄파치 (1개)

상품 ID: 3279

- [블리치 MAXIMATIC 자라키 켄파치](https://www.bnkrmall.co.kr/goods/detail.do?gno=96065302)

```json
{
  "review_id": "R3200",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3201 — MAXIMATIC 전율의 타츠마키 (1개)

상품 ID: 3233

- [원펀맨 MAXIMATIC 전율의 타츠마키](https://www.bnkrmall.co.kr/goods/detail.do?gno=95866084)

```json
{
  "review_id": "R3201",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3202 — MAXIMATIC 진격의 거인 (1개)

상품 ID: 3366

- [진격의 거인 MAXIMATIC 진격의 거인](https://www.bnkrmall.co.kr/goods/detail.do?gno=71412853)

```json
{
  "review_id": "R3202",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3203 — MAXIMATIC 쵸소우 (VER.A) (1개)

상품 ID: 3936

- [주술회전 MAXIMATIC 쵸소우 (VER.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=8298828)

```json
{
  "review_id": "R3203",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3204 — MAXIMATIC 쵸소우 (VER.B) (1개)

상품 ID: 3935

- [주술회전 MAXIMATIC 쵸소우 (VER.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=40699485)

```json
{
  "review_id": "R3204",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3205 — MAXIMATIC 쵸소우 사멸회유 (1개)

상품 ID: 3668

- [주술회전 MAXIMATIC 쵸소우 사멸회유](https://www.bnkrmall.co.kr/goods/detail.do?gno=46037166)

```json
{
  "review_id": "R3205",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3206 — MAXIMATIC 카마도 탄지로 Ⅲ (1개)

상품 ID: 3505

- [귀멸의 칼날 MAXIMATIC 카마도 탄지로 Ⅲ](https://www.bnkrmall.co.kr/goods/detail.do?gno=44109029)

```json
{
  "review_id": "R3206",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3207 — MAXIMATIC 칸로지 미츠리 (1개)

상품 ID: 3987

- [귀멸의 칼날 MAXIMATIC 칸로지 미츠리](https://www.bnkrmall.co.kr/goods/detail.do?gno=80492004)

```json
{
  "review_id": "R3207",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3208 — MAXIMATIC 코쵸우 시노부 (1개)

상품 ID: 3863

- [귀멸의 칼날 MAXIMATIC 코쵸우 시노부](https://www.bnkrmall.co.kr/goods/detail.do?gno=9037008)

```json
{
  "review_id": "R3208",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3209 — MAXIMATIC 쿠로사키 이치고 (1개)

상품 ID: 4087

- [블리치 MAXIMATIC 쿠로사키 이치고](https://www.bnkrmall.co.kr/goods/detail.do?gno=76293579)

```json
{
  "review_id": "R3209",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3210 — MAXIMATIC 타카바 후미히코 (1개)

상품 ID: 3383

- [주술회전 MAXIMATIC 타카바 후미히코](https://www.bnkrmall.co.kr/goods/detail.do?gno=81093690)

```json
{
  "review_id": "R3210",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3211 — MAXIMATIC 토도로키 쇼토 (1개)

상품 ID: 3911

- [나의 히어로 아카데미아 MAXIMATIC 토도로키 쇼토](https://www.bnkrmall.co.kr/goods/detail.do?gno=3497119)

```json
{
  "review_id": "R3211",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3212 — MAXIMATIC 토도로키 쇼토Ⅱ (1개)

상품 ID: 3619

- [나의 히어로 아카데미아 MAXIMATIC 토도로키 쇼토Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=33532943)

```json
{
  "review_id": "R3212",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3213 — MAXIMATIC 토미오카 기유 (1개)

상품 ID: 4098

- [귀멸의 칼날 MAXIMATIC 토미오카 기유](https://www.bnkrmall.co.kr/goods/detail.do?gno=8731547)

```json
{
  "review_id": "R3213",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3214 — MAXIMATIC 토미오카 기유 Ⅱ (1개)

상품 ID: 3504

- [귀멸의 칼날 MAXIMATIC 토미오카 기유 Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=44583088)

```json
{
  "review_id": "R3214",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3215 — MAXIMATIC 트라팔가 로우 I (1개)

상품 ID: 4602

- [원피스 MAXIMATIC 트라팔가 로우 I](https://www.bnkrmall.co.kr/goods/detail.do?gno=56073)

```json
{
  "review_id": "R3215",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3216 — MAXIMATIC 페른 (1개)

상품 ID: 3670

- [장송의 프리렌 MAXIMATIC 페른](https://www.bnkrmall.co.kr/goods/detail.do?gno=92345547)

```json
{
  "review_id": "R3216",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3217 — MAXIMATIC 프리렌 (1개)

상품 ID: 3696

- [장송의 프리렌 MAXIMATIC 프리렌](https://www.bnkrmall.co.kr/goods/detail.do?gno=80822103)

```json
{
  "review_id": "R3217",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3218 — MAXIMATIC 프리렌Ⅱ (1개)

상품 ID: 3623

- [장송의 프리렌 MAXIMATIC 프리렌Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=72790126)

```json
{
  "review_id": "R3218",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3219 — MAXIMATIC 후시구로 메구미 사멸회유 (1개)

상품 ID: 3418

- [주술회전 MAXIMATIC 후시구로 메구미 사멸회유](https://www.bnkrmall.co.kr/goods/detail.do?gno=83877816)

```json
{
  "review_id": "R3219",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3220 — MAXIMATIC 히구루마 히로미 (1개)

상품 ID: 3531

- [주술회전 MAXIMATIC 히구루마 히로미](https://www.bnkrmall.co.kr/goods/detail.do?gno=40899210)

```json
{
  "review_id": "R3220",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3221 — MAXIMATIC 히에이 (1개)

상품 ID: 3741

- [유유백서 MAXIMATIC 히에이](https://www.bnkrmall.co.kr/goods/detail.do?gno=29896449)

```json
{
  "review_id": "R3221",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3222 — MAXIMATIC 히츠가야 토시로 (1개)

상품 ID: 3572

- [블리치 MAXIMATIC 히츠가야 토시로](https://www.bnkrmall.co.kr/goods/detail.do?gno=20497663)

```json
{
  "review_id": "R3222",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3223 — MAXIMATIC 히츠가야 토시로 (TBA) (1개)

상품 ID: 3427

- [블리치 MAXIMATIC 히츠가야 토시로 (TBA)](https://www.bnkrmall.co.kr/goods/detail.do?gno=71852913)

```json
{
  "review_id": "R3223",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3224 — MAXIMATIC 힘멜 (1개)

상품 ID: 3622

- [장송의 프리렌 MAXIMATIC 힘멜](https://www.bnkrmall.co.kr/goods/detail.do?gno=30807082)

```json
{
  "review_id": "R3224",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3225 — MEGA CAT PROJECT NARUTO-ナルト- ニャルト! 缶バッジコレクション (1개)

상품 ID: 1380

- [MEGA CAT PROJECT NARUTO-ナルト- ニャルト! 缶バッジコレクション【再販】](https://megahobby.jp/products/item/5376/)

```json
{
  "review_id": "R3225",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3226 — MEGA CAT PROJECT NARUTO-ナルト- 疾風伝 ニャルト! 缶バッジコレクション 2 (1개)

상품 ID: 1385

- [MEGA CAT PROJECT NARUTO-ナルト- 疾風伝 ニャルト! 缶バッジコレクション 2](https://megahobby.jp/products/item/5759/)

```json
{
  "review_id": "R3226",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3227 — MEGA CAT PROJECT ワンピース ニャンピースニャーン! 缶バッジコレクション (1개)

상품 ID: 1374

- [MEGA CAT PROJECT ワンピース ニャンピースニャーン! 缶バッジコレクション【再販】](https://megahobby.jp/products/item/5023/)

```json
{
  "review_id": "R3227",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3228 — MEGA CAT PROJECT 僕のヒーローアカデミア ヒロアカニャンコNO.02 (1개)

상품 ID: 1376

- [MEGA CAT PROJECT 僕のヒーローアカデミア ヒロアカニャンコNO.02](https://megahobby.jp/products/item/5164/)

```json
{
  "review_id": "R3228",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3229 — MEGA CAT PROJECT 銀魂 にゃん魂!ニャーニャーニャーニャー缶バッジコレクション (1개)

상품 ID: 1382

- [MEGA CAT PROJECT 銀魂 にゃん魂!ニャーニャーニャーニャー缶バッジコレクション](https://megahobby.jp/products/item/5429/)

```json
{
  "review_id": "R3229",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3230 — MEGA EGG FIGURE デジモンアドベンチャー おやすみデジコレ！ (1개)

상품 ID: 1335

- [MEGA EGG FIGURE デジモンアドベンチャー おやすみデジコレ！](https://megahobby.jp/products/item/6063/)

```json
{
  "review_id": "R3230",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3231 — MEIKO (1개)

상품 ID: 904

- [MEIKO](https://megahobby.jp/products/item/5320/)

```json
{
  "review_id": "R3231",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3232 — melffy figure (1개)

상품 ID: 5280

- [melffy figureーコットンキャンディー](https://furyuprize.com/item/22302)

```json
{
  "review_id": "R3232",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3233 — MEMORABLE SAGA SPECIAL 우즈마키 나루토 (1개)

상품 ID: 3896

- [나루토 질풍전 MEMORABLE SAGA SPECIAL 우즈마키 나루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=75090041)

```json
{
  "review_id": "R3233",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3234 — MEMORABLE SAGA SPECIAL 우치하 사스케 (1개)

상품 ID: 3421

- [나루토 질풍전 MEMORABLE SAGA SPECIAL 우치하 사스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=45064775)

```json
{
  "review_id": "R3234",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3235 — MEMORABLE SAGA SPECIAL 우치하 이타치 (1개)

상품 ID: 3874

- [나루토 질풍전 MEMORABLE SAGA SPECIAL 우치하 이타치](https://www.bnkrmall.co.kr/goods/detail.do?gno=63903450)

```json
{
  "review_id": "R3235",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3236 — MEMORABLE SAGA 나라 시카마루 (1개)

상품 ID: 3954

- [나루토 MEMORABLE SAGA 나라 시카마루](https://www.bnkrmall.co.kr/goods/detail.do?gno=96137526)

```json
{
  "review_id": "R3236",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3237 — MEMORABLE SAGA 록 리 (1개)

상품 ID: 4238

- [나루토 MEMORABLE SAGA 록 리](https://www.bnkrmall.co.kr/goods/detail.do?gno=54649277)

```json
{
  "review_id": "R3237",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3238 — MEMORABLE SAGA 아키미치 쵸지 (1개)

상품 ID: 4104

- [나루토 MEMORABLE SAGA 아키미치 쵸지](https://www.bnkrmall.co.kr/goods/detail.do?gno=58618277)

```json
{
  "review_id": "R3238",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3239 — MEMORABLE SAGA 우즈마키 나루토 (1개)

상품 ID: 4253

- [나루토 MEMORABLE SAGA 우즈마키 나루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=70200285)

```json
{
  "review_id": "R3239",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3240 — MEMORABLE SAGA 우즈마키 나루토Ⅱ (1개)

상품 ID: 3887

- [나루토 MEMORABLE SAGA 우즈마키 나루토Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=8124490)

```json
{
  "review_id": "R3240",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3241 — MEMORABLE SAGA 우치하 사스케&우치하 이타치 (1개)

상품 ID: 3508

- [나루토 질풍전 MEMORABLE SAGA 우치하 사스케&우치하 이타치](https://www.bnkrmall.co.kr/goods/detail.do?gno=18260437)

```json
{
  "review_id": "R3241",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3242 — MEMORABLE SAGA 우치하 사스케Ⅱ (1개)

상품 ID: 4005

- [나루토 MEMORABLE SAGA 우치하 사스케Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=25325139)

```json
{
  "review_id": "R3242",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3243 — MEMORABLE SAGA 하쿠 (1개)

상품 ID: 4248

- [나루토 MEMORABLE SAGA 하쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=74649661)

```json
{
  "review_id": "R3243",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3244 — MEMORABLE SAGA 휴우가 네지 (1개)

상품 ID: 4225

- [나루토 MEMORABLE SAGA 휴우가 네지](https://www.bnkrmall.co.kr/goods/detail.do?gno=71674857)

```json
{
  "review_id": "R3244",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3245 — MEM쵸 『POP IN 2』VER. (1개)

상품 ID: 3918

- [【최애의 아이】 MEM쵸 피규어 『POP IN 2』VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=62629742)

```json
{
  "review_id": "R3245",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3246 — MEM쵸 브라이덜 드레스 (1개)

상품 ID: 3991

- [【최애의 아이】 MEM쵸 브라이덜 드레스 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=48412747)

```json
{
  "review_id": "R3246",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3247 — MEM쵸 사복 데이트 (1개)

상품 ID: 4132

- [【최애의 아이】 MEM쵸 사복 데이트 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=19042141)

```json
{
  "review_id": "R3247",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3248 — mofamofy (1개)

상품 ID: 1938

- [mofamofy 시나모롤](https://www.bnkrmall.co.kr/goods/detail.do?gno=61316709)

```json
{
  "review_id": "R3248",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3249 — mofamofy 구치파치 (1개)

상품 ID: 1747

- [mofamofy 구치파치](https://www.bnkrmall.co.kr/goods/detail.do?gno=20313837)

```json
{
  "review_id": "R3249",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3250 — mofamofy 꿀벌냥 (1개)

상품 ID: 1962

- [mofamofy 꿀벌냥](https://www.bnkrmall.co.kr/goods/detail.do?gno=59389254)

```json
{
  "review_id": "R3250",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3251 — mofamofy 마메치 (1개)

상품 ID: 1748

- [mofamofy 마메치](https://www.bnkrmall.co.kr/goods/detail.do?gno=50414063)

```json
{
  "review_id": "R3251",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3252 — mofamofy 마이멜로디 -파스텔 컬러 ver. (1개)

상품 ID: 1727

- [mofamofy 마이멜로디 -파스텔 컬러 ver.-](https://www.bnkrmall.co.kr/goods/detail.do?gno=71967070)

```json
{
  "review_id": "R3252",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3253 — mofamofy 상어냥 (1개)

상품 ID: 1963

- [mofamofy 상어냥](https://www.bnkrmall.co.kr/goods/detail.do?gno=43756789)

```json
{
  "review_id": "R3253",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3254 — mofamofy 쿠로미 (1개)

상품 ID: 1939

- [mofamofy 쿠로미](https://www.bnkrmall.co.kr/goods/detail.do?gno=26048981)

```json
{
  "review_id": "R3254",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3255 — mofamofy 쿠로미 -파스텔 컬러 ver. (1개)

상품 ID: 1725

- [mofamofy 쿠로미 -파스텔 컬러 ver.-](https://www.bnkrmall.co.kr/goods/detail.do?gno=1584454)

```json
{
  "review_id": "R3255",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3256 — mofamofy 토니토니 쵸파 (1개)

상품 ID: 1756

- [mofamofy 토니토니 쵸파](https://www.bnkrmall.co.kr/goods/detail.do?gno=81840216)

```json
{
  "review_id": "R3256",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3257 — mofamofy 폼폼푸린 -파스텔 컬러 ver. (1개)

상품 ID: 1726

- [mofamofy 폼폼푸린 -파스텔 컬러 ver.-](https://www.bnkrmall.co.kr/goods/detail.do?gno=52386418)

```json
{
  "review_id": "R3257",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3258 — mofamofy 헬로키티 (1개)

상품 ID: 1937

- [mofamofy 헬로키티](https://www.bnkrmall.co.kr/goods/detail.do?gno=66798802)

```json
{
  "review_id": "R3258",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3259 — MONYOGIRL (1개)

상품 ID: 1318

- [MONYOGIRL](https://megahobby.jp/products/item/6038/)

```json
{
  "review_id": "R3259",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3260 — N-202d ティタニア朱雀【初回限定特典付き】 (1개)

상품 ID: 411

- [N-202d ティタニア朱雀【初回限定特典付き】](https://megahobby.jp/products/item/4266/)

```json
{
  "review_id": "R3260",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3261 — N-202d ティタニア玄武 (1개)

상품 ID: 175

- [N-202d ティタニア玄武](https://megahobby.jp/products/item/3701/)

```json
{
  "review_id": "R3261",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3262 — N-202d ティタニア玄武(ver1.1) (1개)

상품 ID: 280

- [N-202d ティタニア玄武(ver1.1) ](https://megahobby.jp/products/item/3993/)

```json
{
  "review_id": "R3262",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3263 — N-202d ティタニア白虎 (1개)

상품 ID: 193

- [N-202d ティタニア白虎](https://megahobby.jp/products/item/3752/)

```json
{
  "review_id": "R3263",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3264 — N-202d ティタニア白虎(ver1.1) (1개)

상품 ID: 278

- [N-202d ティタニア白虎(ver1.1) ](https://megahobby.jp/products/item/3991/)

```json
{
  "review_id": "R3264",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3265 — N-202d ティタニア青龍 (1개)

상품 ID: 180

- [N-202d ティタニア青龍](https://megahobby.jp/products/item/3724/)

```json
{
  "review_id": "R3265",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3266 — N-202d ティタニア青龍(ver1.1) (1개)

상품 ID: 279

- [N-202d ティタニア青龍(ver1.1) ](https://megahobby.jp/products/item/3992/)

```json
{
  "review_id": "R3266",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3267 — N-212d ティタニア デルタ(スカウト装備 砂漠戦仕様) (1개)

상품 ID: 608

- [N-212d ティタニア デルタ(スカウト装備 砂漠戦仕様)](https://megahobby.jp/products/item/4664/)

```json
{
  "review_id": "R3267",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3268 — N-212d ティタニア デルタ(ストライカー装備 夜間戦仕様) (1개)

상품 ID: 607

- [N-212d ティタニア デルタ(ストライカー装備 夜間戦仕様)](https://megahobby.jp/products/item/4663/)

```json
{
  "review_id": "R3268",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3269 — NARUTO-ナルト- うずまきナルト GO！ (1개)

상품 ID: 623

- [NARUTO-ナルト-　 うずまきナルト　GO！](https://megahobby.jp/products/item/4680/)

```json
{
  "review_id": "R3269",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3270 — NARUTO-ナルト- うちはサスケ GO！ (1개)

상품 ID: 705

- [NARUTO-ナルト-　 うちはサスケ　GO！](https://megahobby.jp/products/item/4864/)

```json
{
  "review_id": "R3270",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3271 — NARUTO -ナルト- トコトコニャルト！ うずまきナルト (1개)

상품 ID: 672

- [NARUTO -ナルト- トコトコニャルト！ うずまきナルト](https://megahobby.jp/products/item/4794/)

```json
{
  "review_id": "R3271",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3272 — NARUTO-ナルト- ニャルト！ HappyCAT2026 (1개)

상품 ID: 1251

- [NARUTO-ナルト- ニャルト！ HappyCAT2026](https://megahobby.jp/products/item/5909/)

```json
{
  "review_id": "R3272",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3273 — NARUTO-ナルト- ニャルト！MEGACAT DINER (1개)

상품 ID: 828

- [NARUTO-ナルト- ニャルト！MEGACAT DINER](https://megahobby.jp/products/item/5165/)

```json
{
  "review_id": "R3273",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3274 — NARUTO-ナルト- ニャルト！ カラフル☆招き猫FORTUNE (1개)

상품 ID: 741

- [NARUTO-ナルト- ニャルト！ カラフル☆招き猫FORTUNE](https://megahobby.jp/products/item/4946/)

```json
{
  "review_id": "R3274",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3275 — NARUTO-ナルト- ニャルト！サスケく～んこっちにいらっしゃ～い編 (1개)

상품 ID: 919

- [NARUTO-ナルト- ニャルト！サスケく～んこっちにいらっしゃ～い編【再販】](https://megahobby.jp/products/item/5335/)

```json
{
  "review_id": "R3275",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3276 — NARUTO-ナルト- ニャルト！ ニャンとも大きなニャルト！REBOOT うずまきナルト 金のニャルトver. (1개)

상품 ID: 837

- [NARUTO-ナルト- ニャルト！ ニャンとも大きなニャルト！REBOOT うずまきナルト 金のニャルトver.](https://megahobby.jp/products/item/5178/)

```json
{
  "review_id": "R3276",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3277 — NARUTO-ナルト- ニャルト！ ピンズコレクション ①うずまきナルト②はたけカカシ③春野サクラ④うずまきナルト＆うちはサスケ (1개)

상품 ID: 580

- [NARUTO-ナルト- ニャルト！ ピンズコレクション ①うずまきナルト②はたけカカシ③春野サクラ④うずまきナルト＆うちはサスケ](https://megahobby.jp/products/item/4612/)

```json
{
  "review_id": "R3277",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3278 — NARUTO-ナルト- ニャルト！ 招き猫FORTUNE (1개)

상품 ID: 375

- [NARUTO-ナルト- ニャルト！　招き猫FORTUNE](https://megahobby.jp/products/item/4178/)

```json
{
  "review_id": "R3278",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3279 — NARUTO-ナルト- ニャルト！ 招き猫FORTUNE もういっちょ！ (1개)

상품 ID: 541

- [NARUTO-ナルト- ニャルト！ 招き猫FORTUNE　もういっちょ！](https://megahobby.jp/products/item/4540/)

```json
{
  "review_id": "R3279",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3280 — NARUTO-ナルト- ニャルト！ 木ノ葉の愉快なニャンコたち編REBOOT (1개)

상품 ID: 1116

- [NARUTO-ナルト- ニャルト！ 木ノ葉の愉快なニャンコたち編REBOOT](https://megahobby.jp/products/item/5700/)

```json
{
  "review_id": "R3280",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3281 — NARUTO-ナルト- ニャルト！ 缶バッジコレクション (1개)

상품 ID: 459

- [NARUTO-ナルト-  ニャルト！　缶バッジコレクション](https://megahobby.jp/products/item/4357/)

```json
{
  "review_id": "R3281",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3282 — NARUTO-ナルト- ニャルト！ 限定品 HAPPY・FRIEND 2024LIMITED (1개)

상품 ID: 839

- [NARUTO-ナルト- ニャルト！ 限定品　HAPPY・FRIEND 2024LIMITED](https://megahobby.jp/products/item/5180/)

```json
{
  "review_id": "R3282",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3283 — NARUTO-ナルト- ニャンとも大きなニャルト！REBOOT ①うずまきナルト ②うちはサスケ ③はたけカカシ ④うちはイタチ (1개)

상품 ID: 6155

- [NARUTO-ナルト- ニャンとも大きなニャルト！REBOOT ①うずまきナルト　②うちはサスケ　③はたけカカシ　④うちはイタチ【再販】](https://megahobby.jp/products/item/6162/)

```json
{
  "review_id": "R3283",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3284 — NARUTO-ナルト- 春野サクラGO！ (1개)

상품 ID: 721

- [ NARUTO-ナルト-  春野サクラGO！](https://megahobby.jp/products/item/4901/)

```json
{
  "review_id": "R3284",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3285 — NARUTO -ナルト- 木ノ葉の愉快なニャンコたち編 (1개)

상품 ID: 149

- [NARUTO　-ナルト-　 木ノ葉の愉快なニャンコたち編【再販】](https://megahobby.jp/products/item/3655/)

```json
{
  "review_id": "R3285",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3286 — NARUTO-ナルト- 疾風伝 (1개)

상품 ID: 630

- [   NARUTO-ナルト- 疾風伝](https://megahobby.jp/products/item/4688/)

```json
{
  "review_id": "R3286",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3287 — NARUTO-ナルト- 疾風伝 うずまきナルト (1개)

상품 ID: 132

- [NARUTO-ナルト- 疾風伝 うずまきナルト【再販】](https://megahobby.jp/products/item/3485/)

```json
{
  "review_id": "R3287",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3288 — NARUTO-ナルト- 疾風伝 うずまきナルト(六道仙人モード) (1개)

상품 ID: 702

- [NARUTO-ナルト- 疾風伝 うずまきナルト(六道仙人モード)](https://megahobby.jp/products/item/4861/)

```json
{
  "review_id": "R3288",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3289 — NARUTO-ナルト- 疾風伝 うずまきナルト にかっとver. (1개)

상품 ID: 1303

- [NARUTO-ナルト- 疾風伝 うずまきナルト にかっとver.](https://megahobby.jp/products/item/6023/)

```json
{
  "review_id": "R3289",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3290 — NARUTO-ナルト- 疾風伝 うちはイタチ (1개)

상품 ID: 163

- [NARUTO-ナルト- 疾風伝 うちはイタチ【再販】](https://megahobby.jp/products/item/3671/)

```json
{
  "review_id": "R3290",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3291 — NARUTO-ナルト- 疾風伝 うちはサスケ (1개)

상품 ID: 162

- [NARUTO-ナルト- 疾風伝 うちはサスケ【再販】](https://megahobby.jp/products/item/3670/)

```json
{
  "review_id": "R3291",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3292 — NARUTO-ナルト- 疾風伝 おでかけニャルト！ 2025LIMITED (1개)

상품 ID: 836

- [NARUTO-ナルト- 疾風伝 おでかけニャルト！ 2025LIMITED](https://megahobby.jp/products/item/5177/)

```json
{
  "review_id": "R3292",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3293 — NARUTO-ナルト- 疾風伝 おやすみニャルト！ (1개)

상품 ID: 875

- [NARUTO-ナルト-　疾風伝 おやすみニャルト！](https://megahobby.jp/products/item/5246/)

```json
{
  "review_id": "R3293",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3294 — NARUTO-ナルト- 疾風伝 おやすみニャルト！ あつまれ&quot;暁&quot;編 その1 (1개)

상품 ID: 1333

- [NARUTO-ナルト- 疾風伝 おやすみニャルト！ あつまれ&quot;暁&quot;編　その1](https://megahobby.jp/products/item/6061/)

```json
{
  "review_id": "R3294",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3295 — NARUTO-ナルト- 疾風伝 おやすみニャルト！ あつまれ&quot;暁&quot;編 その2 (1개)

상품 ID: 117

- [NARUTO-ナルト- 疾風伝 おやすみニャルト！ あつまれ&quot;暁&quot;編　その2](https://megahobby.jp/products/item/6112/)

```json
{
  "review_id": "R3295",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3296 — NARUTO-ナルト- 疾風伝 てのひらイタチ (1개)

상품 ID: 1247

- [NARUTO-ナルト- 疾風伝 てのひらイタチ](https://megahobby.jp/products/item/5882/)

```json
{
  "review_id": "R3296",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3297 — NARUTO-ナルト- 疾風伝 てのひらサスケ (1개)

상품 ID: 852

- [NARUTO-ナルト- 疾風伝 てのひらサスケ](https://megahobby.jp/products/item/5222/)

```json
{
  "review_id": "R3297",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3298 — NARUTO-ナルト- 疾風伝 てのひらナルトくん (1개)

상품 ID: 706

- [NARUTO-ナルト- 疾風伝 てのひらナルトくん](https://megahobby.jp/products/item/4865/)

```json
{
  "review_id": "R3298",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3299 — NARUTO-ナルト- 疾風伝 とりあえずお茶にしよってばよ！編 (1개)

상품 ID: 126

- [NARUTO-ナルト- 疾風伝 とりあえずお茶にしよってばよ！編【再販】](https://megahobby.jp/products/item/3067/)

```json
{
  "review_id": "R3299",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3300 — NARUTO-ナルト- 疾風伝 はたけカカシ (1개)

상품 ID: 131

- [NARUTO-ナルト- 疾風伝 はたけカカシ【再販】](https://megahobby.jp/products/item/3484/)

```json
{
  "review_id": "R3300",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3301 — NARUTO-ナルト- 疾風伝 ニャルト！”暁”と全面対決！ 木ノ葉隠れの里の攻防編！ (1개)

상품 ID: 440

- [NARUTO-ナルト- 疾風伝 ニャルト！”暁”と全面対決！ 木ノ葉隠れの里の攻防編！【再販】](https://megahobby.jp/products/item/4323/)

```json
{
  "review_id": "R3301",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3302 — NARUTO-ナルト- 疾風伝 ニャルト！ 招き猫FORTUNE うずまきナルトと仲間たち編 (1개)

상품 ID: 716

- [NARUTO-ナルト- 疾風伝 ニャルト！ 招き猫FORTUNE　うずまきナルトと仲間たち編](https://megahobby.jp/products/item/4896/)

```json
{
  "review_id": "R3302",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3303 — NARUTO-ナルト- 疾風伝 ロック・リー (1개)

상품 ID: 1341

- [NARUTO-ナルト- 疾風伝 ロック・リー](https://megahobby.jp/products/item/6069/)

```json
{
  "review_id": "R3303",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3304 — NARUTO-ナルト- 疾風伝 奈良シカマル (1개)

상품 ID: 245

- [NARUTO-ナルト- 疾風伝 奈良シカマル](https://megahobby.jp/products/item/3905/)

```json
{
  "review_id": "R3304",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3305 — NARUTO-ナルト-疾風伝 山中いの (1개)

상품 ID: 1149

- [NARUTO-ナルト-疾風伝 山中いの【再販】](https://megahobby.jp/products/item/5753/)

```json
{
  "review_id": "R3305",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3306 — NARUTO-ナルト- 疾風伝 新たな時代だってばよ！編 (1개)

상품 ID: 164

- [ NARUTO-ナルト- 疾風伝 新たな時代だってばよ！編【再販】](https://megahobby.jp/products/item/3673/)

```json
{
  "review_id": "R3306",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3307 — NARUTO-ナルト- 疾風伝 日向ネジ (1개)

상품 ID: 1340

- [NARUTO-ナルト- 疾風伝 日向ネジ](https://megahobby.jp/products/item/6068/)

```json
{
  "review_id": "R3307",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3308 — NARUTO-ナルト- 疾風伝 木ノ葉のブレイクタイム～改！～ (1개)

상품 ID: 538

- [NARUTO-ナルト- 疾風伝 木ノ葉のブレイクタイム～改！～【再販】](https://megahobby.jp/products/item/4532/)

```json
{
  "review_id": "R3308",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3309 — NARUTO－ナルト－ 疾風伝 決戦！“暁”戦突入編 (1개)

상품 ID: 600

- [NARUTO－ナルト－ 疾風伝 決戦！“暁”戦突入編【再販】](https://megahobby.jp/products/item/4656/)

```json
{
  "review_id": "R3309",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3310 — NARUTO-ナルト- 疾風伝 第七班集合！ (1개)

상품 ID: 649

- [ NARUTO-ナルト- 疾風伝  第七班集合！](https://megahobby.jp/products/item/4740/)

```json
{
  "review_id": "R3310",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3311 — NARUTO-ナルト- 疾風伝 自来也 (1개)

상품 ID: 1302

- [NARUTO-ナルト- 疾風伝 自来也](https://megahobby.jp/products/item/6022/)

```json
{
  "review_id": "R3311",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3312 — NARUTO ₋ナルト₋ 疾風伝 春野サクラ Ver.2 (1개)

상품 ID: 1075

- [NARUTO ₋ナルト₋ 疾風伝 春野サクラ Ver.2【再販】](https://megahobby.jp/products/item/5616/)

```json
{
  "review_id": "R3312",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3313 — Netflix Live Action Series BIG Fluffy Puffy 쵸파 (1개)

상품 ID: 3474

- [Netflix Live Action Series 원피스 BIG Fluffy Puffy 쵸파](https://www.bnkrmall.co.kr/goods/detail.do?gno=84197940)

```json
{
  "review_id": "R3313",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3314 — NieR:Automata Ver1.1a コラボ ２B (1개)

상품 ID: 793

- [NieR:Automata Ver1.1a コラボ ２B](https://megahobby.jp/products/item/5042/)

```json
{
  "review_id": "R3314",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3315 — Noir Edge Collection 데이다라&사소리 (A.데이다라) (1개)

상품 ID: 3372

- [나루토 질풍전 Noir Edge Collection 데이다라&사소리 (A.데이다라)](https://www.bnkrmall.co.kr/goods/detail.do?gno=49068349)

```json
{
  "review_id": "R3315",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3316 — Noir Edge Collection 데이다라&사소리 (B.사소리) (1개)

상품 ID: 3371

- [나루토 질풍전 Noir Edge Collection 데이다라&사소리 (B.사소리)](https://www.bnkrmall.co.kr/goods/detail.do?gno=77577592)

```json
{
  "review_id": "R3316",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3317 — Noir Edge Collection 미도리야 이즈쿠 (1개)

상품 ID: 3667

- [나의 히어로 아카데미아 Noir Edge Collection 미도리야 이즈쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=68286609)

```json
{
  "review_id": "R3317",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3318 — Noir Edge Collection 오로치마루&호시가키 키사메 (A.오로치마루) (1개)

상품 ID: 3238

- [나루토 질풍전 Noir Edge Collection 오로치마루&호시가키 키사메 (A.오로치마루)](https://www.bnkrmall.co.kr/goods/detail.do?gno=42959868)

```json
{
  "review_id": "R3318",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3319 — Noir Edge Collection 오로치마루&호시가키 키사메 (B.호시가키 키사메) (1개)

상품 ID: 3237

- [나루토 질풍전 Noir Edge Collection 오로치마루&호시가키 키사메 (B.호시가키 키사메)](https://www.bnkrmall.co.kr/goods/detail.do?gno=96098146)

```json
{
  "review_id": "R3319",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3320 — Noir Edge Collection 우즈마키 나루토 (1개)

상품 ID: 3545

- [나루토 질풍전 Noir Edge Collection 우즈마키 나루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=845017)

```json
{
  "review_id": "R3320",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3321 — Noir Edge Collection 우치하 마다라(토비)&제츠 (A.우치하 마다라(토비)) (1개)

상품 ID: 3300

- [나루토 질풍전 Noir Edge Collection 우치하 마다라(토비)&제츠 (A.우치하 마다라(토비))](https://www.bnkrmall.co.kr/goods/detail.do?gno=18714667)

```json
{
  "review_id": "R3321",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3322 — Noir Edge Collection 우치하 마다라(토비)&제츠 (B.제츠) (1개)

상품 ID: 3299

- [나루토 질풍전 Noir Edge Collection 우치하 마다라(토비)&제츠 (B.제츠)](https://www.bnkrmall.co.kr/goods/detail.do?gno=94023734)

```json
{
  "review_id": "R3322",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3323 — Noir Edge Collection 우치하 이타치 (1개)

상품 ID: 3424

- [나루토 질풍전 Noir Edge Collection 우치하 이타치](https://www.bnkrmall.co.kr/goods/detail.do?gno=83027505)

```json
{
  "review_id": "R3323",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3324 — Noir Edge Collection 토가 히미코 (1개)

상품 ID: 3530

- [나의 히어로 아카데미아 Noir Edge Collection 토가 히미코](https://www.bnkrmall.co.kr/goods/detail.do?gno=58654015)

```json
{
  "review_id": "R3324",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3325 — Noir Edge Collection 페인&코난 (A.페인) (1개)

상품 ID: 3298

- [나루토 질풍전 Noir Edge Collection 페인&코난 (A.페인)](https://www.bnkrmall.co.kr/goods/detail.do?gno=92519748)

```json
{
  "review_id": "R3325",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3326 — Noir Edge Collection 페인&코난 (B.코난) (1개)

상품 ID: 3297

- [나루토 질풍전 Noir Edge Collection 페인&코난 (B.코난)](https://www.bnkrmall.co.kr/goods/detail.do?gno=87790995)

```json
{
  "review_id": "R3326",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3327 — Noir Edge Collection 히단&카쿠즈 (A.히단) (1개)

상품 ID: 3370

- [나루토 질풍전 Noir Edge Collection 히단&카쿠즈 (A.히단)](https://www.bnkrmall.co.kr/goods/detail.do?gno=75541740)

```json
{
  "review_id": "R3327",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3328 — Noir Edge Collection 히단&카쿠즈 (B.카쿠즈) (1개)

상품 ID: 3369

- [나루토 질풍전 Noir Edge Collection 히단&카쿠즈 (B.카쿠즈)](https://www.bnkrmall.co.kr/goods/detail.do?gno=3579185)

```json
{
  "review_id": "R3328",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3329 — OMORI SITTING 오모리&오브리 (A.오모리) (1개)

상품 ID: 3307

- [OMORI SITTING 피규어 오모리&오브리 (A.오모리)](https://www.bnkrmall.co.kr/goods/detail.do?gno=18745212)

```json
{
  "review_id": "R3329",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3330 — OMORI SITTING 오모리&오브리 (B.오브리) (1개)

상품 ID: 3306

- [OMORI SITTING 피규어 오모리&오브리 (B.오브리)](https://www.bnkrmall.co.kr/goods/detail.do?gno=10448076)

```json
{
  "review_id": "R3330",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3331 — ONE PIECE (1개)

상품 ID: 1054

- [ ONE PIECE](https://megahobby.jp/products/item/5569/)

```json
{
  "review_id": "R3331",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3332 — ONE PIECE BUSTERCALL Chunky Monkey.D.Luffy (1개)

상품 ID: 4648

- [ONE PIECE BUSTERCALL Chunky Monkey.D.Luffy](https://www.bnkrmall.co.kr/goods/detail.do?gno=55145)

```json
{
  "review_id": "R3332",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3333 — ONE PIECE BUSTERCALL Chunky Tony Tony.Chopper (1개)

상품 ID: 4647

- [ONE PIECE BUSTERCALL Chunky Tony Tony.Chopper](https://www.bnkrmall.co.kr/goods/detail.do?gno=55146)

```json
{
  "review_id": "R3333",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3334 — ONE PIECE LOGBOX RE BIRTH ワノ国編 参 (1개)

상품 ID: 883

- [ONE PIECE LOGBOX RE BIRTH ワノ国編 参　【再販】](https://megahobby.jp/products/item/5282/)

```json
{
  "review_id": "R3334",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3335 — ONE PIECE “白ひげ” エドワード・ニューゲート Ver.1.5 (1개)

상품 ID: 1362

- [ONE PIECE “白ひげ” エドワード・ニューゲート Ver.1.5](https://megahobby.jp/products/item/6126/)

```json
{
  "review_id": "R3335",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3336 — ONE PIECE クロコダイル (1개)

상품 ID: 632

- [ONE PIECE クロコダイル](https://megahobby.jp/products/item/4690/)

```json
{
  "review_id": "R3336",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3337 — ONE PIECE コラソン (1개)

상품 ID: 868

- [ONE PIECE コラソン](https://megahobby.jp/products/item/5239/)

```json
{
  "review_id": "R3337",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3338 — ONE PIECE サンジ 未来島Ver. (1개)

상품 ID: 733

- [ONE PIECE サンジ 未来島Ver.](https://megahobby.jp/products/item/4938/)

```json
{
  "review_id": "R3338",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3339 — ONE PIECE シャンクス (1개)

상품 ID: 587

- [ONE PIECE シャンクス](https://megahobby.jp/products/item/4619/)

```json
{
  "review_id": "R3339",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3340 — ONE PIECE シャンクス 幼少期Ver. (1개)

상품 ID: 1241

- [ONE PIECE シャンクス 幼少期Ver.](https://megahobby.jp/products/item/5876/)

```json
{
  "review_id": "R3340",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3341 — ONE PIECE ゾロ十郎 (1개)

상품 ID: 161

- [ONE PIECE ゾロ十郎](https://megahobby.jp/products/item/3669/)

```json
{
  "review_id": "R3341",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3342 — ONE PIECE トニートニー・チョッパー ワクワクVer. (1개)

상품 ID: 1119

- [ONE PIECE トニートニー・チョッパー ワクワクVer.](https://megahobby.jp/products/item/5703/)

```json
{
  "review_id": "R3342",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3343 — ONE PIECE トラファルガー・ロー 幼少期Ver. (1개)

상품 ID: 867

- [ONE PIECE トラファルガー・ロー 幼少期Ver.](https://megahobby.jp/products/item/5238/)

```json
{
  "review_id": "R3343",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3344 — ONE PIECE ドンキホーテ・ドフラミンゴ (1개)

상품 ID: 1012

- [ONE PIECE ドンキホーテ・ドフラミンゴ](https://megahobby.jp/products/item/5491/)

```json
{
  "review_id": "R3344",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3345 — ONE PIECE ナミ（Summer Vacation) (1개)

상품 ID: 843

- [ONE PIECE ナミ（Summer Vacation)【再販】](https://megahobby.jp/products/item/5209/)

```json
{
  "review_id": "R3345",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3346 — ONE PIECE バギー 幼少期Ver. (1개)

상품 ID: 1240

- [ONE PIECE バギー 幼少期Ver.](https://megahobby.jp/products/item/5875/)

```json
{
  "review_id": "R3346",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3347 — ONE PIECE ビッグ・マム (1개)

상품 ID: 449

- [ONE PIECE ビッグ・マム](https://megahobby.jp/products/item/4337/)

```json
{
  "review_id": "R3347",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3348 — ONE PIECE ペローナ (1개)

상품 ID: 1196

- [ONE PIECE ペローナ【再販】](https://megahobby.jp/products/item/5827/)

```json
{
  "review_id": "R3348",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3349 — ONE PIECE ペローナ【３月発売分】 (1개)

상품 ID: 698

- [ONE PIECE ペローナ【３月発売分】](https://megahobby.jp/products/item/4857/)

```json
{
  "review_id": "R3349",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3350 — ONE PIECE ボア・ハンコック (1개)

상품 ID: 1013

- [ONE PIECE ボア・ハンコック](https://megahobby.jp/products/item/5492/)

```json
{
  "review_id": "R3350",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3351 — ONE PIECE ポートガス・D・エース (1개)

상품 ID: 1197

- [ONE PIECE ポートガス・D・エース【再販】](https://megahobby.jp/products/item/5828/)

```json
{
  "review_id": "R3351",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3352 — ONE PIECE ポートガス・D・エース【３月発売分】 (1개)

상품 ID: 699

- [ONE PIECE ポートガス・D・エース【３月発売分】](https://megahobby.jp/products/item/4858/)

```json
{
  "review_id": "R3352",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3353 — ONE PIECE マルコ (1개)

상품 ID: 311

- [ONE PIECE マルコ](https://megahobby.jp/products/item/4065/)

```json
{
  "review_id": "R3353",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3354 — ONE PIECE モンキー・D・ルフィ (1개)

상품 ID: 202

- [ONE PIECE モンキー・D・ルフィ【再販】](https://megahobby.jp/products/item/3790/)

```json
{
  "review_id": "R3354",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3355 — ONE PIECE モンキー・D・ルフィ ギア4 バウンドマン (1개)

상품 ID: 889

- [ONE PIECE モンキー・D・ルフィ ギア4 バウンドマン](https://megahobby.jp/products/item/5305/)

```json
{
  "review_id": "R3355",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3356 — ONE PIECE ヤマト (1개)

상품 ID: 400

- [ONE PIECE ヤマト](https://megahobby.jp/products/item/4234/)

```json
{
  "review_id": "R3356",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3357 — ONE PIECE ルフィ太郎 (1개)

상품 ID: 140

- [ONE PIECE ルフィ太郎](https://megahobby.jp/products/item/3607/)

```json
{
  "review_id": "R3357",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3358 — ONE PIECE ロブ・ルッチVer.1.5 (1개)

상품 ID: 890

- [ONE PIECE ロブ・ルッチVer.1.5](https://megahobby.jp/products/item/5306/)

```json
{
  "review_id": "R3358",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3359 — ONE PIECE ロロノア・ゾロ 未来島Ver. (1개)

상품 ID: 734

- [ONE PIECE ロロノア・ゾロ 未来島Ver.](https://megahobby.jp/products/item/4939/)

```json
{
  "review_id": "R3359",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3360 — ONE PIECE 海賊たちのティータイム (1개)

상품 ID: 370

- [ONE PIECE 海賊たちのティータイム【再販】](https://megahobby.jp/products/item/4173/)

```json
{
  "review_id": "R3360",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3361 — ONE PIECE 海賊たちのバカンス (1개)

상품 ID: 814

- [ONE PIECE  海賊たちのバカンス【再販】](https://megahobby.jp/products/item/5149/)

```json
{
  "review_id": "R3361",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3362 — ONE PIECE 海賊たちの宴 (1개)

상품 ID: 519

- [ONE PIECE 海賊たちの宴【再販】](https://megahobby.jp/products/item/4497/)

```json
{
  "review_id": "R3362",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3363 — ONE PIECE 百獣のカイドウ (1개)

상품 ID: 450

- [ONE PIECE 百獣のカイドウ](https://megahobby.jp/products/item/4338/)

```json
{
  "review_id": "R3363",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3364 — ONE PIECE 赤髪のシャンクスVer.1.5 (1개)

상품 ID: 570

- [ONE PIECE 赤髪のシャンクスVer.1.5](https://megahobby.jp/products/item/4589/)

```json
{
  "review_id": "R3364",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3365 — One Punch Life 사이타마 (1개)

상품 ID: 3759

- [원펀맨 One Punch Life 사이타마](https://www.bnkrmall.co.kr/goods/detail.do?gno=47601447)

```json
{
  "review_id": "R3365",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3366 — One Punch Life 사이타마 낮잠 (1개)

상품 ID: 3367

- [원펀맨 One Punch Life 사이타마 낮잠](https://www.bnkrmall.co.kr/goods/detail.do?gno=31706557)

```json
{
  "review_id": "R3366",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3367 — Otherworlder- vol.5 (베니마루) (1개)

상품 ID: 4548

- [전생했더니 슬라임이었던 건에 대하여 -Otherworlder- vol.5 (베니마루)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56768)

```json
{
  "review_id": "R3367",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3368 — Otherworlder- vol.5 (슈나) (1개)

상품 ID: 4557

- [전생했더니 슬라임이었던 건에 대하여 -Otherworlder- vol.5 (슈나)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56675)

```json
{
  "review_id": "R3368",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3369 — OTHERWORLDER PLUS 마왕 리무루 템페스트 Special ver. (1개)

상품 ID: 3343

- [전생했더니 슬라임이었던 건에 대하여 OTHERWORLDER PLUS 마왕 리무루 템페스트 Special ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=38906276)

```json
{
  "review_id": "R3369",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3370 — OTHERWORLDER PLUS 밀림 드래곤 폼 스페셜 VER. (1개)

상품 ID: 4042

- [전생했더니 슬라임이었던 건에 대하여 OTHERWORLDER PLUS 밀림 드래곤 폼 스페셜 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=45953269)

```json
{
  "review_id": "R3370",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3371 — OTHERWORLDER VOL.11 (B:하쿠로우) (1개)

상품 ID: 4595

- [전생했더니 슬라임이었던 건에 대하여 OTHERWORLDER VOL.11 (B:하쿠로우)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56282)

```json
{
  "review_id": "R3371",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3372 — OTHERWORLDER Vol.6 (밀림) (1개)

상품 ID: 4547

- [전생했더니 슬라임이었던 건에 대하여 OTHERWORLDER Vol.6 (밀림)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56771)

```json
{
  "review_id": "R3372",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3373 — OTHERWORLDER VOL.7 (시온) (1개)

상품 ID: 4523

- [전생했더니 슬라임이었던 건에 대하여 OTHERWORLDER VOL.7 (시온)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56870)

```json
{
  "review_id": "R3373",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3374 — OTHERWORLDER VOL.8 (B:란가) (1개)

상품 ID: 4655

- [전생했더니 슬라임이었던 건에 대하여 OTHERWORLDER VOL.8 (B:란가)](https://www.bnkrmall.co.kr/goods/detail.do?gno=54961)

```json
{
  "review_id": "R3374",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3375 — OTHERWORLDER VOL.9 (B:디아블로) (1개)

상품 ID: 4644

- [전생했더니 슬라임이었던 건에 대하여 OTHERWORLDER VOL.9 (B:디아블로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=55239)

```json
{
  "review_id": "R3375",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3376 — PALDOLCE COLLECTION VOL.1 (VER.A) (쵸파) (1개)

상품 ID: 3986

- [원피스 PALDOLCE COLLECTION VOL.1 (VER.A) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=79781719)

```json
{
  "review_id": "R3376",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3377 — PALDOLCE COLLECTION VOL.1 (VER.B) (쵸파) (1개)

상품 ID: 4143

- [원피스 PALDOLCE COLLECTION VOL.1 (VER.B) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=37130748)

```json
{
  "review_id": "R3377",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3378 — PALDOLCE COLLECTION VOL.1 (VER.C) (쵸파) (1개)

상품 ID: 4142

- [원피스 PALDOLCE COLLECTION VOL.1 (VER.C) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=44200457)

```json
{
  "review_id": "R3378",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3379 — PALDOLCE COLLECTION VOL.2 (VER.A) (쵸파) (1개)

상품 ID: 4055

- [원피스 PALDOLCE COLLECTION VOL.2 (VER.A) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=96061729)

```json
{
  "review_id": "R3379",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3380 — PALDOLCE COLLECTION VOL.2 (VER.B) (쵸파) (1개)

상품 ID: 4054

- [원피스 PALDOLCE COLLECTION VOL.2 (VER.B) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=2163622)

```json
{
  "review_id": "R3380",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3381 — PALDOLCE COLLECTION VOL.2 (VER.C) (쵸파) (1개)

상품 ID: 4053

- [원피스 PALDOLCE COLLECTION VOL.2 (VER.C) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=84149508)

```json
{
  "review_id": "R3381",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3382 — PALDOLCE COLLECTION VOL.3 (VER.A) (쵸파) (1개)

상품 ID: 3982

- [원피스 PALDOLCE COLLECTION VOL.3 (VER.A) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=60643755)

```json
{
  "review_id": "R3382",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3383 — PALDOLCE COLLECTION VOL.3 (VER.B) (쵸파) (1개)

상품 ID: 3981

- [원피스 PALDOLCE COLLECTION VOL.3 (VER.B) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=9783413)

```json
{
  "review_id": "R3383",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3384 — PALDOLCE COLLECTION VOL.3 (VER.C) (쵸파) (1개)

상품 ID: 3980

- [원피스 PALDOLCE COLLECTION VOL.3 (VER.C) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=52890858)

```json
{
  "review_id": "R3384",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3385 — PALDOLCE COLLECTION VOL.4 (VER.A) (쵸파) (1개)

상품 ID: 3907

- [원피스 PALDOLCE COLLECTION VOL.4 (VER.A) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=47455005)

```json
{
  "review_id": "R3385",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3386 — PALDOLCE COLLECTION VOL.4 (VER.B) (쵸파) (1개)

상품 ID: 3906

- [원피스 PALDOLCE COLLECTION VOL.4 (VER.B) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=79407520)

```json
{
  "review_id": "R3386",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3387 — PALDOLCE COLLECTION VOL.4 (VER.C) (쵸파) (1개)

상품 ID: 3905

- [원피스 PALDOLCE COLLECTION VOL.4 (VER.C) (쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=66436927)

```json
{
  "review_id": "R3387",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3388 — PALDOLCE COLLECTION 쵸파 베포&하트 해적단 (A:토니토니 쵸파) (1개)

상품 ID: 3414

- [원피스 PALDOLCE COLLECTION 쵸파 베포&하트 해적단 (A:토니토니 쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=65955023)

```json
{
  "review_id": "R3388",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3389 — PALDOLCE COLLECTION 쵸파 베포&하트 해적단 (B:토니토니 쵸파) (1개)

상품 ID: 3413

- [원피스 PALDOLCE COLLECTION 쵸파 베포&하트 해적단 (B:토니토니 쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=95266688)

```json
{
  "review_id": "R3389",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3390 — PALDOLCE COLLECTION 쵸파 베포&하트 해적단 (C:베포) (1개)

상품 ID: 3412

- [원피스 PALDOLCE COLLECTION 쵸파 베포&하트 해적단 (C:베포)](https://www.bnkrmall.co.kr/goods/detail.do?gno=18212351)

```json
{
  "review_id": "R3390",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3391 — PALDOLCE COLLECTION 쵸파와 베포와 해적선 (A: 토니토니 쵸파) (1개)

상품 ID: 3361

- [원피스 PALDOLCE COLLECTION 쵸파와 베포와 해적선 (A: 토니토니 쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=39394199)

```json
{
  "review_id": "R3391",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3392 — PALDOLCE COLLECTION 쵸파와 베포와 해적선 (B: 토니토니 쵸파) (1개)

상품 ID: 3360

- [원피스 PALDOLCE COLLECTION 쵸파와 베포와 해적선 (B: 토니토니 쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=85933543)

```json
{
  "review_id": "R3392",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3393 — PALDOLCE COLLECTION 쵸파와 베포와 해적선 (C: 베포) (1개)

상품 ID: 3359

- [원피스 PALDOLCE COLLECTION 쵸파와 베포와 해적선 (C: 베포)](https://www.bnkrmall.co.kr/goods/detail.do?gno=16291938)

```json
{
  "review_id": "R3393",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3394 — PANEL SPECTACLE SPECIAL (A:우즈마키 나루토) (1개)

상품 ID: 4223

- [나루토 질풍전 PANEL SPECTACLE SPECIAL (A:우즈마키 나루토)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59309381)

```json
{
  "review_id": "R3394",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3395 — PANEL SPECTACLE SPECIAL (B:우치하 사스케) (1개)

상품 ID: 4222

- [나루토 질풍전 PANEL SPECTACLE SPECIAL (B:우치하 사스케)](https://www.bnkrmall.co.kr/goods/detail.do?gno=12554953)

```json
{
  "review_id": "R3395",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3396 — PANEL SPECTACLE SPECIAL (C:하루노 사쿠라) (1개)

상품 ID: 4221

- [나루토 질풍전 PANEL SPECTACLE SPECIAL (C:하루노 사쿠라)](https://www.bnkrmall.co.kr/goods/detail.do?gno=94648630)

```json
{
  "review_id": "R3396",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3397 — PANEL SPECTACLE 나미카제 미나토 (1개)

상품 ID: 3858

- [나루토 질풍전 PANEL SPECTACLE 나미카제 미나토](https://www.bnkrmall.co.kr/goods/detail.do?gno=65027565)

```json
{
  "review_id": "R3397",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3398 — PANEL SPECTACLE 사루토비 히루젠 (1개)

상품 ID: 4004

- [나루토 질풍전 PANEL SPECTACLE 사루토비 히루젠](https://www.bnkrmall.co.kr/goods/detail.do?gno=63941841)

```json
{
  "review_id": "R3398",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3399 — PANEL SPECTACLE 센쥬 토비라마 (1개)

상품 ID: 4032

- [나루토 질풍전 PANEL SPECTACLE 센쥬 토비라마](https://www.bnkrmall.co.kr/goods/detail.do?gno=89872976)

```json
{
  "review_id": "R3399",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3400 — PANEL SPECTACLE 센쥬 하시라마 (1개)

상품 ID: 3926

- [나루토 질풍전 PANEL SPECTACLE 센쥬 하시라마](https://www.bnkrmall.co.kr/goods/detail.do?gno=25107156)

```json
{
  "review_id": "R3400",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3401 — PANEL SPECTACLE 우즈마키 나루토 (1개)

상품 ID: 4321

- [나루토 질풍전 PANEL SPECTACLE 우즈마키 나루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=77049627)

```json
{
  "review_id": "R3401",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3402 — PANEL SPECTACLE 우즈마키 나루토 (시간을 초월한 출진) (1개)

상품 ID: 4024

- [나루토 질풍전 PANEL SPECTACLE 우즈마키 나루토 (시간을 초월한 출진)](https://www.bnkrmall.co.kr/goods/detail.do?gno=67751072)

```json
{
  "review_id": "R3402",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3403 — PANEL SPECTACLE 우치하 사스케 (하늘에서 내리는 번개) (1개)

상품 ID: 3897

- [나루토 질풍전 PANEL SPECTACLE 우치하 사스케 (하늘에서 내리는 번개)](https://www.bnkrmall.co.kr/goods/detail.do?gno=70935394)

```json
{
  "review_id": "R3403",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3404 — Portrelic 우치하 사스케&우치하 이타치 (1개)

상품 ID: 3390

- [나루토 질풍전 Portrelic 우치하 사스케&우치하 이타치](https://www.bnkrmall.co.kr/goods/detail.do?gno=52518463)

```json
{
  "review_id": "R3404",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3405 — PREMIUM 우즈마키 나루토 [THE ANIME] (1개)

상품 ID: 3314

- [나루토 질풍전 PREMIUM 우즈마키 나루토 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=87196620)

```json
{
  "review_id": "R3405",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3406 — PREMIUM 우즈마키 나루토 [THE BRUSH] (1개)

상품 ID: 3313

- [나루토 질풍전 PREMIUM 우즈마키 나루토 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=99895305)

```json
{
  "review_id": "R3406",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3407 — PREMIUM 우즈마키 나루토 [THE METALLIC] (1개)

상품 ID: 3312

- [나루토 질풍전 PREMIUM 우즈마키 나루토 (THE METALLIC)](https://www.bnkrmall.co.kr/goods/detail.do?gno=88539548)

```json
{
  "review_id": "R3407",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3408 — PROFESSIONAL 機動戦士ガンダム ジオン公国軍一般兵士01 (1개)

상품 ID: 354

- [PROFESSIONAL 機動戦士ガンダム ジオン公国軍一般兵士01](https://megahobby.jp/products/item/4133/)

```json
{
  "review_id": "R3408",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3409 — PROFESSIONAL 機動戦士ガンダム ジオン公国軍一般兵士02 (1개)

상품 ID: 355

- [PROFESSIONAL 機動戦士ガンダム ジオン公国軍一般兵士02](https://megahobby.jp/products/item/4134/)

```json
{
  "review_id": "R3409",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3410 — PROFESSIONAL 機動戦士ガンダム ジオン公国軍一般兵士03 (1개)

상품 ID: 356

- [PROFESSIONAL 機動戦士ガンダム ジオン公国軍一般兵士03](https://megahobby.jp/products/item/4135/)

```json
{
  "review_id": "R3410",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3411 — PROFESSIONAL 機動戦士ガンダム 地球連邦軍一般兵士01 (1개)

상품 ID: 361

- [PROFESSIONAL 機動戦士ガンダム 地球連邦軍一般兵士01](https://megahobby.jp/products/item/4164/)

```json
{
  "review_id": "R3411",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3412 — PROFESSIONAL 機動戦士ガンダム 地球連邦軍一般兵士02 (1개)

상품 ID: 362

- [PROFESSIONAL 機動戦士ガンダム 地球連邦軍一般兵士02](https://megahobby.jp/products/item/4165/)

```json
{
  "review_id": "R3412",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3413 — PROFESSIONAL 機動戦士ガンダム 地球連邦軍一般兵士03 (1개)

상품 ID: 363

- [PROFESSIONAL 機動戦士ガンダム 地球連邦軍一般兵士03](https://megahobby.jp/products/item/4166/)

```json
{
  "review_id": "R3413",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3414 — RAHDX G.A.NEO 機動戦士Vガンダム カテジナ・ルース (1개)

상품 ID: 270

- [RAHDX G.A.NEO　機動戦士Vガンダム 　カテジナ・ルース【再販】](https://megahobby.jp/products/item/3957/)

```json
{
  "review_id": "R3414",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3415 — RAHDXシリーズ G.A.NEO 機動戦士ガンダムZZ エルピー・プル Re. (1개)

상품 ID: 749

- [RAHDXシリーズ G.A.NEO 機動戦士ガンダムZZ エルピー・プル Re.](https://megahobby.jp/products/item/4967/)

```json
{
  "review_id": "R3415",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3416 — Re:ゼロから始める異世界生活 てのひら エミリア (1개)

상품 ID: 514

- [ Re:ゼロから始める異世界生活 てのひら エミリア](https://megahobby.jp/products/item/4478/)

```json
{
  "review_id": "R3416",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3417 — RE:제로부터 시작하는 이세계 생활 DIANACHT COUTURE 렘 (1개)

상품 ID: 4378

- [RE:제로부터 시작하는 이세계 생활 DIANACHT COUTURE 렘](https://www.bnkrmall.co.kr/goods/detail.do?gno=59812)

```json
{
  "review_id": "R3417",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3418 — RE:제로부터 시작하는 이세계 생활 SERENUS COUTURE 람 (1개)

상품 ID: 4348

- [RE:제로부터 시작하는 이세계 생활 SERENUS COUTURE 람](https://www.bnkrmall.co.kr/goods/detail.do?gno=74910192)

```json
{
  "review_id": "R3418",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3419 — RE:제로부터 시작하는 이세계 생활 SERENUS COUTURE 렘 (1개)

상품 ID: 4607

- [RE:제로부터 시작하는 이세계 생활 SERENUS COUTURE 렘](https://www.bnkrmall.co.kr/goods/detail.do?gno=56056)

```json
{
  "review_id": "R3419",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3420 — RE:제로부터 시작하는 이세계 생활 SERENUS COUTURE 렘 VOL.3 (1개)

상품 ID: 4347

- [RE:제로부터 시작하는 이세계 생활 SERENUS COUTURE 렘 VOL.3](https://www.bnkrmall.co.kr/goods/detail.do?gno=56391300)

```json
{
  "review_id": "R3420",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3421 — RE:제로부터 시작하는 이세계 생활 렘 Rem＇s Morning Star Dress (1개)

상품 ID: 4194

- [RE:제로부터 시작하는 이세계 생활 렘 Rem＇s Morning Star Dress](https://www.bnkrmall.co.kr/goods/detail.do?gno=8650233)

```json
{
  "review_id": "R3421",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3422 — Realistic Model Series 機動戦士ガンダム 水星の魔女 Gストラクチャー【GS07-B】MSコンテナ（マテリアルカラーエディション） (1개)

상품 ID: 369

- [Realistic Model Series  機動戦士ガンダム 水星の魔女 Gストラクチャー【GS07-B】MSコンテナ（マテリアルカラーエディション）](https://megahobby.jp/products/item/4172/)

```json
{
  "review_id": "R3422",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3423 — REPOPRIZE 우즈마키 나루토 (1개)

상품 ID: 4192

- [나루토 질풍전 REPOPRIZE 우즈마키 나루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=91716869)

```json
{
  "review_id": "R3423",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3424 — RM Series Gストラクチャー 機動戦士ガンダムSEED (HGシリーズ用）【GS06M】ヘリオポリスバトルステージ（マテリアルカラーエディション） (1개)

상품 ID: 1347

- [RM Series Gストラクチャー 機動戦士ガンダムSEED (HGシリーズ用）【GS06M】ヘリオポリスバトルステージ（マテリアルカラーエディション）](https://megahobby.jp/products/item/6075/)

```json
{
  "review_id": "R3424",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3425 — RM Series Gストラクチャー 機動戦士ガンダムSEED 【GS04M】アークエンジェル艦橋（マテリアルカラーエディション） (1개)

상품 ID: 566

- [RM Series Gストラクチャー 機動戦士ガンダムSEED 【GS04M】アークエンジェル艦橋（マテリアルカラーエディション）](https://megahobby.jp/products/item/4565/)

```json
{
  "review_id": "R3425",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3426 — RM Series Gストラクチャー 機動戦士ガンダム 【GS02M】ニューヤーク市廃墟（マテリアルカラーエディション） (1개)

상품 ID: 624

- [RM Series Gストラクチャー 機動戦士ガンダム 【GS02M】ニューヤーク市廃墟（マテリアルカラーエディション）](https://megahobby.jp/products/item/4681/)

```json
{
  "review_id": "R3426",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3427 — RM Series Gストラクチャー 機動戦士ガンダム 【GS03M】ラストシューティング（マテリアルカラーエディション） (1개)

상품 ID: 1175

- [RM Series Gストラクチャー 機動戦士ガンダム  【GS03M】ラストシューティング（マテリアルカラーエディション）](https://megahobby.jp/products/item/5806/)

```json
{
  "review_id": "R3427",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3428 — RMS Gストラクチャー 機動戦士ガンダム 【GS01M】ジャブローに散る！（マテリアルカラーエディション） (1개)

상품 ID: 742

- [RMS Gストラクチャー 機動戦士ガンダム 【GS01M】ジャブローに散る！（マテリアルカラーエディション）](https://megahobby.jp/products/item/4947/)

```json
{
  "review_id": "R3428",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3429 — RUBIK&#039;S ID ONE PIECE (1개)

상품 ID: 1357

- [RUBIK&#039;S ID ONE PIECE](https://megahobby.jp/products/item/6108/)

```json
{
  "review_id": "R3429",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3430 — RUBIK&#039;S ID たまごっち (1개)

상품 ID: 1299

- [RUBIK&#039;S ID たまごっち](https://megahobby.jp/products/item/6019/)

```json
{
  "review_id": "R3430",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3431 — SAKAMOTO DAYS SAKAMOTO CATS ニャンとも愉快な坂本商店！ (1개)

상품 ID: 717

- [SAKAMOTO DAYS SAKAMOTO CATS　ニャンとも愉快な坂本商店！](https://megahobby.jp/products/item/4897/)

```json
{
  "review_id": "R3431",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3432 — SAKAMOTO DAYS てのひら南雲さん (1개)

상품 ID: 785

- [SAKAMOTO DAYS てのひら南雲さん](https://megahobby.jp/products/item/5009/)

```json
{
  "review_id": "R3432",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3433 — SAKAMOTO DAYS てのひら坂本さん (1개)

상품 ID: 760

- [SAKAMOTO DAYS てのひら坂本さん](https://megahobby.jp/products/item/4978/)

```json
{
  "review_id": "R3433",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3434 — SAKAMOTO DAYS 南雲 (1개)

상품 ID: 755

- [SAKAMOTO DAYS 南雲](https://megahobby.jp/products/item/4973/)

```json
{
  "review_id": "R3434",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3435 — SAKAMOTO DAYS 坂本太郎 (1개)

상품 ID: 730

- [SAKAMOTO DAYS 坂本太郎](https://megahobby.jp/products/item/4935/)

```json
{
  "review_id": "R3435",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3436 — SAKAMOTO DAYS 大佛 (1개)

상품 ID: 910

- [SAKAMOTO DAYS 大佛](https://megahobby.jp/products/item/5326/)

```json
{
  "review_id": "R3436",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3437 — SAKAMOTO DAYS 朝倉シン (1개)

상품 ID: 729

- [SAKAMOTO DAYS 朝倉シン](https://megahobby.jp/products/item/4934/)

```json
{
  "review_id": "R3437",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3438 — SAKAMOTO DAYS 神々廻 (1개)

상품 ID: 909

- [SAKAMOTO DAYS 神々廻](https://megahobby.jp/products/item/5325/)

```json
{
  "review_id": "R3438",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3439 — Sasaki and Peeps (1개)

상품 ID: 14

- [ELSA](https://www.kotobukiya.co.jp/en/product/detail/p4934054062416/)

```json
{
  "review_id": "R3439",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3440 — SCultures BIG 조형왕 정상결전 4 Vol.3 조로 (1개)

상품 ID: 4691

- [원피스 SCultures BIG 조형왕 정상결전 4 Vol.3 조로](https://www.bnkrmall.co.kr/goods/detail.do?gno=15504)

```json
{
  "review_id": "R3440",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3441 — SCultures BIG 조형왕 정상결전 4 Vol.7 에이스 (1개)

상품 ID: 4704

- [원피스 SCultures BIG 조형왕 정상결전 4 Vol.7 에이스](https://www.bnkrmall.co.kr/goods/detail.do?gno=15313)

```json
{
  "review_id": "R3441",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3442 — SCultures BIG 조형왕 정상결전 6 Vol.3 루피 (1개)

상품 ID: 4698

- [원피스 SCultures BIG 조형왕 정상결전 6 Vol.3 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=15453)

```json
{
  "review_id": "R3442",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3443 — SD건담 황극무창 신용사 레드랜더 (1개)

상품 ID: 4643

- [SD건담 황극무창 신용사 레드랜더](https://www.bnkrmall.co.kr/goods/detail.do?gno=55241)

```json
{
  "review_id": "R3443",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3444 — SITTING 아코 (1개)

상품 ID: 3515

- [블루 아카이브 SITTING 피규어 아코](https://www.bnkrmall.co.kr/goods/detail.do?gno=3631811)

```json
{
  "review_id": "R3444",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3445 — SITTING 이오리 (1개)

상품 ID: 3514

- [블루 아카이브 SITTING 피규어 이오리](https://www.bnkrmall.co.kr/goods/detail.do?gno=445054)

```json
{
  "review_id": "R3445",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3446 — SITTING 치나츠 (1개)

상품 ID: 3573

- [블루 아카이브 SITTING 피규어 치나츠](https://www.bnkrmall.co.kr/goods/detail.do?gno=1678159)

```json
{
  "review_id": "R3446",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3447 — SITTING 히나 (1개)

상품 ID: 3574

- [블루 아카이브 SITTING 피규어 히나](https://www.bnkrmall.co.kr/goods/detail.do?gno=44352756)

```json
{
  "review_id": "R3447",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3448 — SOFVIMATES～가부몬～ (1개)

상품 ID: 3779

- [디지몬 어드벤처 SOFVIMATES～가부몬～](https://www.bnkrmall.co.kr/goods/detail.do?gno=67363648)

```json
{
  "review_id": "R3448",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3449 — SOFVIMATES～아구몬～vol.2 (1개)

상품 ID: 3780

- [디지몬 어드벤처 SOFVIMATES～아구몬～vol.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=62053951)

```json
{
  "review_id": "R3449",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3450 — SOFVIMATES 베포 (1개)

상품 ID: 3985

- [원피스 SOFVIMATES 베포](https://www.bnkrmall.co.kr/goods/detail.do?gno=12719207)

```json
{
  "review_id": "R3450",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3451 — SOFVIMATES 아구몬 (1개)

상품 ID: 4419

- [디지몬 어드벤처 SOFVIMATES 아구몬](https://www.bnkrmall.co.kr/goods/detail.do?gno=59292)

```json
{
  "review_id": "R3451",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3452 — SOFVIMATES 쵸파 드레스로사 VER. (1개)

상품 ID: 4075

- [원피스 SOFVIMATES 쵸파 드레스로사 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=89613455)

```json
{
  "review_id": "R3452",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3453 — SOFVIMATES 쵸파 알라바스타 VER. (1개)

상품 ID: 4126

- [원피스 SOFVIMATES 쵸파 알라바스타 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=45039088)

```json
{
  "review_id": "R3453",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3454 — SOFVIMATES 쵸파 어인섬 VER. (1개)

상품 ID: 4166

- [원피스 SOFVIMATES 쵸파 어인섬 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=11020526)

```json
{
  "review_id": "R3454",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3455 — SOFVIMATES 쵸파 에그 헤드 (1개)

상품 ID: 4099

- [원피스 SOFVIMATES 쵸파 에그 헤드](https://www.bnkrmall.co.kr/goods/detail.do?gno=7920848)

```json
{
  "review_id": "R3455",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3456 — SOFVIMATES 쵸파 조VER. (1개)

상품 ID: 3956

- [원피스 SOFVIMATES 쵸파 조VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=2878623)

```json
{
  "review_id": "R3456",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3457 — SOFVIMATES 쵸파 홀케이크 아일랜드 목욕 후VER. (1개)

상품 ID: 3890

- [원피스 SOFVIMATES 쵸파 홀케이크 아일랜드 목욕 후VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=66977441)

```json
{
  "review_id": "R3457",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3458 — SOFVIMATES 카루 (1개)

상품 ID: 4112

- [원피스 SOFVIMATES 카루](https://www.bnkrmall.co.kr/goods/detail.do?gno=30886037)

```json
{
  "review_id": "R3458",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3459 — SOFVIMATES 터보 할멈 (마네키네코) (1개)

상품 ID: 3822

- [단다단 SOFVIMATES 터보 할멈 (마네키네코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=86760549)

```json
{
  "review_id": "R3459",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3460 — SOFVIMATES 테일몬 (1개)

상품 ID: 3755

- [디지몬 어드벤처 SOFVIMATES 테일몬](https://www.bnkrmall.co.kr/goods/detail.do?gno=57678556)

```json
{
  "review_id": "R3460",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3461 — SOFVIMATES 토니토니 쵸파 (1개)

상품 ID: 4181

- [원피스 SOFVIMATES 토니토니 쵸파](https://www.bnkrmall.co.kr/goods/detail.do?gno=91957403)

```json
{
  "review_id": "R3461",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3462 — SOFVIMATES 파타몬 (1개)

상품 ID: 3754

- [디지몬 어드벤처 SOFVIMATES 파타몬](https://www.bnkrmall.co.kr/goods/detail.do?gno=16824964)

```json
{
  "review_id": "R3462",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3463 — SOFVIMATES 황금 전보벌레 (1개)

상품 ID: 3855

- [원피스 SOFVIMATES 황금 전보벌레](https://www.bnkrmall.co.kr/goods/detail.do?gno=57978190)

```json
{
  "review_id": "R3463",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3464 — SOFVIMATE 쵸파에몽 (1개)

상품 ID: 3692

- [원피스 SOFVIMATE 쵸파에몽](https://www.bnkrmall.co.kr/goods/detail.do?gno=87699199)

```json
{
  "review_id": "R3464",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3465 — SOFVIMATE 쿵푸 듀공 (1개)

상품 ID: 4052

- [원피스 SOFVIMATE 쿵푸 듀공](https://www.bnkrmall.co.kr/goods/detail.do?gno=79715226)

```json
{
  "review_id": "R3465",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3466 — SOLID AND SOULS 야마모토 겐류사이 시게쿠니 (1개)

상품 ID: 4392

- [블리치 SOLID AND SOULS 야마모토 겐류사이 시게쿠니](https://www.bnkrmall.co.kr/goods/detail.do?gno=59556)

```json
{
  "review_id": "R3466",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3467 — SOLID AND SOULS 이시다 우류 (1개)

상품 ID: 4395

- [블리치 SOLID AND SOULS 이시다 우류](https://www.bnkrmall.co.kr/goods/detail.do?gno=59553)

```json
{
  "review_id": "R3467",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3468 — SOLID AND SOULS 자라키 켄파치 (1개)

상품 ID: 4375

- [블리치 SOLID AND SOULS 자라키 켄파치](https://www.bnkrmall.co.kr/goods/detail.do?gno=59817)

```json
{
  "review_id": "R3468",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3469 — SOLID AND SOULS 쿠로사키 이치고 (1개)

상품 ID: 4426

- [블리치 SOLID AND SOULS 쿠로사키 이치고](https://www.bnkrmall.co.kr/goods/detail.do?gno=59247)

```json
{
  "review_id": "R3469",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3470 — SOLID AND SOULS 쿠로사키 이치고Ⅱ (1개)

상품 ID: 4329

- [블리치 SOLID AND SOULS 쿠로사키 이치고Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=69560024)

```json
{
  "review_id": "R3470",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3471 — SOLID AND SOULS 쿠로츠치 마유리 (1개)

상품 ID: 4119

- [블리치 SOLID AND SOULS 쿠로츠치 마유리](https://www.bnkrmall.co.kr/goods/detail.do?gno=64352922)

```json
{
  "review_id": "R3471",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3472 — SOLID AND SOULS 히츠가야 토시로 (1개)

상품 ID: 4376

- [블리치 SOLID AND SOULS 히츠가야 토시로](https://www.bnkrmall.co.kr/goods/detail.do?gno=59816)

```json
{
  "review_id": "R3472",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3473 — SOLID SCENE COLLECTION 나구모 (1개)

상품 ID: 3491

- [사카모토 데이즈 SOLID SCENE COLLECTION 나구모](https://www.bnkrmall.co.kr/goods/detail.do?gno=1431710)

```json
{
  "review_id": "R3473",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3474 — SOLID SCENE COLLECTION 아사쿠라 신 (1개)

상품 ID: 3873

- [사카모토 데이즈 SOLID SCENE COLLECTION 아사쿠라 신](https://www.bnkrmall.co.kr/goods/detail.do?gno=12815023)

```json
{
  "review_id": "R3474",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3475 — Soul Entered Model 쿠로사키 이치고 (1개)

상품 ID: 4560

- [블리치 Soul Entered Model 쿠로사키 이치고](https://www.bnkrmall.co.kr/goods/detail.do?gno=56672)

```json
{
  "review_id": "R3475",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3476 — SPY×FAMILY Fluffy Puffy 본드 포저 vol.2 (ver.A) (1개)

상품 ID: 3824

- [SPY×FAMILY Fluffy Puffy 본드 포저 vol.2 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=37488811)

```json
{
  "review_id": "R3476",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3477 — SPY×FAMILY Fluffy Puffy 본드 포저 vol.2 (ver.B) (1개)

상품 ID: 3823

- [SPY×FAMILY Fluffy Puffy 본드 포저 vol.2 (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=99166144)

```json
{
  "review_id": "R3477",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3478 — SPY×FAMILY PALDOLCE COLLECTION VOL.1 (A:아냐 포저) (1개)

상품 ID: 4276

- [SPY×FAMILY PALDOLCE COLLECTION VOL.1 (A:아냐 포저)](https://www.bnkrmall.co.kr/goods/detail.do?gno=55174802)

```json
{
  "review_id": "R3478",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3479 — SPY×FAMILY PALDOLCE COLLECTION VOL.1 (B:아냐 포저) (1개)

상품 ID: 4275

- [SPY×FAMILY PALDOLCE COLLECTION VOL.1 (B:아냐 포저)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58323984)

```json
{
  "review_id": "R3479",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3480 — SPY×FAMILY PALDOLCE COLLECTION VOL.1 (C:본드 포저) (1개)

상품 ID: 4274

- [SPY×FAMILY PALDOLCE COLLECTION VOL.1 (C:본드 포저)](https://www.bnkrmall.co.kr/goods/detail.do?gno=48524793)

```json
{
  "review_id": "R3480",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3481 — SPY×FAMILY てのひらヨルさん (1개)

상품 ID: 269

- [SPY×FAMILY てのひらヨルさん](https://megahobby.jp/products/item/3956/)

```json
{
  "review_id": "R3481",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3482 — SPY×FAMILY てのひらロイドさん (1개)

상품 ID: 268

- [SPY×FAMILY てのひらロイドさん](https://megahobby.jp/products/item/3955/)

```json
{
  "review_id": "R3482",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3483 — SPY×FAMILY ふかふかスクイーズパン編 (1개)

상품 ID: 187

- [　SPY×FAMILY　ふかふかスクイーズパン編](https://megahobby.jp/products/item/3735/)

```json
{
  "review_id": "R3483",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3484 — SPY×FAMILY アーニャすぺしゃる (1개)

상품 ID: 304

- [SPY×FAMILY アーニャすぺしゃる](https://megahobby.jp/products/item/4034/)

```json
{
  "review_id": "R3484",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3485 — SPY×FAMILY ヨル・フォージャー (1개)

상품 ID: 286

- [SPY×FAMILY ヨル・フォージャー](https://megahobby.jp/products/item/3999/)

```json
{
  "review_id": "R3485",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3486 — SPY×FAMILY ロイド・フォージャー (1개)

상품 ID: 287

- [SPY×FAMILY ロイド・フォージャー](https://megahobby.jp/products/item/4000/)

```json
{
  "review_id": "R3486",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3487 — SPY×FAMILY 箱入りSPY×FAMILY3 (1개)

상품 ID: 1040

- [SPY×FAMILY 箱入りSPY×FAMILY3【再販】](https://megahobby.jp/products/item/5541/)

```json
{
  "review_id": "R3487",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3488 — SPY×FAMILY 가족사진 로이드 포저 (1개)

상품 ID: 4301

- [SPY×FAMILY 가족사진 피규어 로이드 포저](https://www.bnkrmall.co.kr/goods/detail.do?gno=91314635)

```json
{
  "review_id": "R3488",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3489 — SPY×FAMILY 가족사진 아냐 포저X본드 포저 (1개)

상품 ID: 4258

- [SPY×FAMILY 가족사진 피규어 아냐 포저X본드 포저](https://www.bnkrmall.co.kr/goods/detail.do?gno=3553842)

```json
{
  "review_id": "R3489",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3490 — SPY×FAMILY 가족사진 요르 포저 (1개)

상품 ID: 4272

- [SPY×FAMILY 가족사진 피규어 요르 포저](https://www.bnkrmall.co.kr/goods/detail.do?gno=2644127)

```json
{
  "review_id": "R3490",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3491 — SPY×FAMILY 마스코트 vol.1 (1개)

상품 ID: 4264

- [SPY×FAMILY 마스코트 피규어 vol.1](https://www.bnkrmall.co.kr/goods/detail.do?gno=30121343)

```json
{
  "review_id": "R3491",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3492 — SPY×FAMILY 브레이크 타임 콜렉션 로이드 포저 (1개)

상품 ID: 4160

- [SPY×FAMILY 브레이크 타임 콜렉션 로이드 포저](https://www.bnkrmall.co.kr/goods/detail.do?gno=44166826)

```json
{
  "review_id": "R3492",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3493 — SPY×FAMILY 브레이크 타임 콜렉션 아냐 포저 & 본드 포저 (1개)

상품 ID: 4211

- [SPY×FAMILY 브레이크 타임 콜렉션 아냐 포저 & 본드 포저](https://www.bnkrmall.co.kr/goods/detail.do?gno=76612900)

```json
{
  "review_id": "R3493",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3494 — SPY×FAMILY 브레이크 타임 콜렉션 아냐 포저 & 본드 포저Ⅱ (1개)

상품 ID: 4068

- [SPY×FAMILY 브레이크 타임 콜렉션 아냐 포저 & 본드 포저Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=60957292)

```json
{
  "review_id": "R3494",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3495 — SPY×FAMILY 브레이크 타임 콜렉션 아냐 포저 & 펭귄 (1개)

상품 ID: 4138

- [SPY×FAMILY 브레이크 타임 콜렉션 아냐 포저 & 펭귄](https://www.bnkrmall.co.kr/goods/detail.do?gno=96815798)

```json
{
  "review_id": "R3495",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3496 — SPY×FAMILY 브레이크 타임 콜렉션 아냐 포저 파자마 VER. (1개)

상품 ID: 4179

- [SPY×FAMILY 브레이크 타임 콜렉션 아냐 포저 파자마 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=46927680)

```json
{
  "review_id": "R3496",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3497 — SPY×FAMILY 브레이크 타임 콜렉션 요르 포저 (1개)

상품 ID: 4159

- [SPY×FAMILY 브레이크 타임 콜렉션 요르 포저](https://www.bnkrmall.co.kr/goods/detail.do?gno=87770804)

```json
{
  "review_id": "R3497",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3498 — SPY×FAMILY 피그라이프 VOL.1 (1개)

상품 ID: 3944

- [SPY×FAMILY 피그라이프 VOL.1](https://www.bnkrmall.co.kr/goods/detail.do?gno=26505310)

```json
{
  "review_id": "R3498",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3499 — STAND ALONE COMPLEX トコトコタチコマりた～んず2025 (1개)

상품 ID: 761

- [STAND ALONE COMPLEX トコトコタチコマりた～んず2025](https://megahobby.jp/products/item/4983/)

```json
{
  "review_id": "R3499",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3500 — sweets flavor 2026 나기 세이시로 (1개)

상품 ID: 3507

- [블루 록 피규어 sweets flavor 2026 나기 세이시로](https://www.bnkrmall.co.kr/goods/detail.do?gno=64760275)

```json
{
  "review_id": "R3500",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3501 — sweets flavor 2026 미카게 레오 (1개)

상품 ID: 3506

- [블루 록 피규어 sweets flavor 2026 미카게 레오](https://www.bnkrmall.co.kr/goods/detail.do?gno=17782782)

```json
{
  "review_id": "R3501",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3502 — sweets flavor 2026 이사기 요이치 (1개)

상품 ID: 3571

- [블루 록 피규어 sweets flavor 2026 이사기 요이치](https://www.bnkrmall.co.kr/goods/detail.do?gno=2865340)

```json
{
  "review_id": "R3502",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3503 — sweets flavor 2026 이토시 린 (1개)

상품 ID: 3570

- [블루 록 피규어 sweets flavor 2026 이토시 린](https://www.bnkrmall.co.kr/goods/detail.do?gno=98865496)

```json
{
  "review_id": "R3503",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3504 — SWEETS FLAVOR 나기 세이시로 (1개)

상품 ID: 3938

- [블루 록 피규어 SWEETS FLAVOR 나기 세이시로](https://www.bnkrmall.co.kr/goods/detail.do?gno=96881477)

```json
{
  "review_id": "R3504",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3505 — SWEETS FLAVOR 미카게 레오 (1개)

상품 ID: 3487

- [블루 록 피규어 SWEETS FLAVOR 미카게 레오](https://www.bnkrmall.co.kr/goods/detail.do?gno=68635591)

```json
{
  "review_id": "R3505",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3506 — SWEETS FLAVOR 이사기 요이치 (1개)

상품 ID: 3914

- [블루 록 피규어 SWEETS FLAVOR 이사기 요이치](https://www.bnkrmall.co.kr/goods/detail.do?gno=89373733)

```json
{
  "review_id": "R3506",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3507 — SWEETS FLAVOR 이토시 린 (1개)

상품 ID: 3490

- [블루 록 피규어 SWEETS FLAVOR 이토시 린](https://www.bnkrmall.co.kr/goods/detail.do?gno=33526530)

```json
{
  "review_id": "R3507",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3508 — Tamashii Art 손오공&용 (1개)

상품 ID: 1868

- [Tamashii Art 드래곤볼 손오공&용](https://www.bnkrmall.co.kr/goods/detail.do?gno=79656722)

```json
{
  "review_id": "R3508",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3509 — Texture 오챠코&이즈쿠 (미도리야 이즈쿠) (1개)

상품 ID: 4494

- [나의 히어로 아카데미아 Texture 오챠코&이즈쿠 (미도리야 이즈쿠)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57303)

```json
{
  "review_id": "R3509",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3510 — The Animation 아로나 (1개)

상품 ID: 3711

- [블루 아카이브 The Animation 아로나 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=95073484)

```json
{
  "review_id": "R3510",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3511 — THE FINAL SEASON 리바이 (1개)

상품 ID: 4619

- [진격의 거인 THE FINAL SEASON 리바이](https://www.bnkrmall.co.kr/goods/detail.do?gno=55743)

```json
{
  "review_id": "R3511",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3512 — THE FINAL SEASON 리바이 스페셜 (1개)

상품 ID: 4472

- [진격의 거인 THE FINAL SEASON 리바이 스페셜](https://www.bnkrmall.co.kr/goods/detail.do?gno=58589)

```json
{
  "review_id": "R3512",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3513 — THE FINAL SEASON 엘런 예거&리바이 (A:엘런 예거) (1개)

상품 ID: 4432

- [진격의 거인 THE FINAL SEASON 엘런 예거&리바이 (A:엘런 예거)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59241)

```json
{
  "review_id": "R3513",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3514 — THE FINAL SEASON 엘런 예거&리바이 (B:리바이) (1개)

상품 ID: 4431

- [진격의 거인 THE FINAL SEASON 엘런 예거&리바이 (B:리바이)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59242)

```json
{
  "review_id": "R3514",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3515 — THE MOVIE YOU＇RE NEXT VOL.3 (1개)

상품 ID: 4129

- [나의 히어로 아카데미아 THE MOVIE YOU＇RE NEXT 피규어 VOL.3](https://www.bnkrmall.co.kr/goods/detail.do?gno=64411785)

```json
{
  "review_id": "R3515",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3516 — THE MOVIE YOU＇RE NEXT 티저 비쥬얼 미도리아 이즈쿠 (1개)

상품 ID: 4022

- [나의 히어로 아카데미아 THE MOVIE YOU＇RE NEXT 티저 비쥬얼 미도리아 이즈쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=12722761)

```json
{
  "review_id": "R3516",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3517 — THEORAMA SOUL 롤로노아 조로 (1개)

상품 ID: 3330

- [원피스 THEORAMA SOUL 롤로노아 조로](https://www.bnkrmall.co.kr/goods/detail.do?gno=99625973)

```json
{
  "review_id": "R3517",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3518 — THEORAMA SOUL 몽키 D. 루피 기어5 (1개)

상품 ID: 3311

- [원피스 THEORAMA SOUL 몽키 D. 루피 기어5](https://www.bnkrmall.co.kr/goods/detail.do?gno=57361244)

```json
{
  "review_id": "R3518",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3519 — THEORAMA SOUL 몽키 D 루피 (1개)

상품 ID: 3441

- [원피스 THEORAMA SOUL 몽키 D 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=97163680)

```json
{
  "review_id": "R3519",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3520 — THEORAMA SOUL 샹크스 (1개)

상품 ID: 3612

- [원피스 THEORAMA SOUL 샹크스](https://www.bnkrmall.co.kr/goods/detail.do?gno=78898576)

```json
{
  "review_id": "R3520",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3521 — THE출항 LOGIA 볼사리노 스페셜 에디션 (1개)

상품 ID: 3752

- [원피스 THE출항 LOGIA 볼사리노 스페셜 에디션](https://www.bnkrmall.co.kr/goods/detail.do?gno=81307586)

```json
{
  "review_id": "R3521",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3522 — THE출항 LOGIA 사보 스페셜 에디션 (1개)

상품 ID: 3842

- [원피스 THE출항 LOGIA 사보 스페셜 에디션](https://www.bnkrmall.co.kr/goods/detail.do?gno=67598757)

```json
{
  "review_id": "R3522",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3523 — THE출항 LOGIA 사카즈키 스페셜 에디션 (1개)

상품 ID: 3835

- [원피스 THE출항 LOGIA 사카즈키 스페셜 에디션](https://www.bnkrmall.co.kr/goods/detail.do?gno=89657015)

```json
{
  "review_id": "R3523",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3524 — THE출항 LOGIA 쿠잔 스페셜 에디션 (1개)

상품 ID: 3834

- [원피스 THE출항 LOGIA 쿠잔 스페셜 에디션](https://www.bnkrmall.co.kr/goods/detail.do?gno=19813805)

```json
{
  "review_id": "R3524",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3525 — THE출항 LOGIA 포트거스 D 에이스 SPECIAL EDITION (1개)

상품 ID: 3611

- [원피스 THE출항 LOGIA 포트거스 D 에이스 SPECIAL EDITION](https://www.bnkrmall.co.kr/goods/detail.do?gno=28570199)

```json
{
  "review_id": "R3525",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3526 — THE출항 나미 (1개)

상품 ID: 4231

- [원피스 THE출항 나미](https://www.bnkrmall.co.kr/goods/detail.do?gno=73435821)

```json
{
  "review_id": "R3526",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3527 — THE출항 나미 에그 헤드 VER. (1개)

상품 ID: 3816

- [원피스 THE출항 나미 에그 헤드 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=76127468)

```json
{
  "review_id": "R3527",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3528 — THE 출항 니코 로빈 (1개)

상품 ID: 4208

- [원피스 THE 출항 니코 로빈](https://www.bnkrmall.co.kr/goods/detail.do?gno=94288563)

```json
{
  "review_id": "R3528",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3529 — THE출항 니코 로빈 에그 헤드 Ver. (1개)

상품 ID: 3868

- [원피스 THE출항 니코 로빈 에그 헤드 Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=12387574)

```json
{
  "review_id": "R3529",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3530 — THE출항 롤로노아 조로 (1개)

상품 ID: 4307

- [원피스 THE출항 롤로노아 조로](https://www.bnkrmall.co.kr/goods/detail.do?gno=63574601)

```json
{
  "review_id": "R3530",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3531 — THE출항 롤로노아 조로 에그 헤드 VER. (1개)

상품 ID: 4026

- [원피스 THE출항 롤로노아 조로 에그 헤드 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=2030870)

```json
{
  "review_id": "R3531",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3532 — THE출항 몽키 D 루피 (1개)

상품 ID: 4324

- [원피스 THE출항 몽키 D 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=22691655)

```json
{
  "review_id": "R3532",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3533 — THE출항 몽키 D 루피 에그 헤드 VER. (1개)

상품 ID: 4051

- [원피스 THE출항 몽키 D 루피 에그 헤드 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=84484285)

```json
{
  "review_id": "R3533",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3534 — THE출항 벤 베크맨 (1개)

상품 ID: 4216

- [원피스 THE출항 벤 베크맨](https://www.bnkrmall.co.kr/goods/detail.do?gno=9649213)

```json
{
  "review_id": "R3534",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3535 — THE출항 상디 (1개)

상품 ID: 4298

- [원피스 THE출항 상디](https://www.bnkrmall.co.kr/goods/detail.do?gno=77698757)

```json
{
  "review_id": "R3535",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3536 — THE출항 상디 에그 헤드 VER. (1개)

상품 ID: 3998

- [원피스 THE출항 상디 에그 헤드 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=50334487)

```json
{
  "review_id": "R3536",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3537 — THE출항 샹크스 스페셜 에디션 (1개)

상품 ID: 4065

- [원피스 THE출항 샹크스 스페셜 에디션](https://www.bnkrmall.co.kr/goods/detail.do?gno=50903646)

```json
{
  "review_id": "R3537",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3538 — THE출항 야솝 (1개)

상품 ID: 3767

- [원피스 THE출항 야솝](https://www.bnkrmall.co.kr/goods/detail.do?gno=23497602)

```json
{
  "review_id": "R3538",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3539 — THE출항 쥬라큘 미호크 (1개)

상품 ID: 4125

- [원피스 THE출항 쥬라큘 미호크](https://www.bnkrmall.co.kr/goods/detail.do?gno=98447896)

```json
{
  "review_id": "R3539",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3540 — THE출항 코비 (1개)

상품 ID: 3712

- [원피스 THE출항 코비](https://www.bnkrmall.co.kr/goods/detail.do?gno=86788987)

```json
{
  "review_id": "R3540",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3541 — THE출항 크로커다일 (1개)

상품 ID: 4111

- [원피스 THE출항 크로커다일](https://www.bnkrmall.co.kr/goods/detail.do?gno=90903223)

```json
{
  "review_id": "R3541",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3542 — THE출항 트라팔가 로우 (1개)

상품 ID: 4284

- [원피스 THE출항 트라팔가 로우](https://www.bnkrmall.co.kr/goods/detail.do?gno=57784289)

```json
{
  "review_id": "R3542",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3543 — TIGER &amp; BUNNY バーナビー・ブルックス Jr. (1개)

상품 ID: 984

- [TIGER &amp; BUNNY バーナビー・ブルックス Jr.](https://megahobby.jp/products/item/5436/)

```json
{
  "review_id": "R3543",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3544 — TIGER &amp; BUNNY 鏑木・T・虎徹 (1개)

상품 ID: 985

- [TIGER &amp; BUNNY 鏑木・T・虎徹](https://megahobby.jp/products/item/5437/)

```json
{
  "review_id": "R3544",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3545 — TinyTAN DNA 모니터 탑 RM (ver.A) (1개)

상품 ID: 3349

- [TinyTAN DNA 모니터 탑 피규어 RM (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=96832381)

```json
{
  "review_id": "R3545",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3546 — TinyTAN DNA 모니터 탑 뷔 (ver.A) (1개)

상품 ID: 3582

- [TinyTAN DNA 모니터 탑 피규어 뷔 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=25282293)

```json
{
  "review_id": "R3546",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3547 — TinyTAN DNA 모니터 탑 슈가 (ver.A) (1개)

상품 ID: 3286

- [TinyTAN DNA 모니터 탑 피규어 슈가 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=51294684)

```json
{
  "review_id": "R3547",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3548 — TinyTAN DNA 모니터 탑 정국 (ver.A) (1개)

상품 ID: 3581

- [TinyTAN DNA 모니터 탑 피규어 정국 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=2400399)

```json
{
  "review_id": "R3548",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3549 — TinyTAN DNA 모니터 탑 제이홉 (ver.A) (1개)

상품 ID: 3285

- [TinyTAN DNA 모니터 탑 피규어 제이홉 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=60491961)

```json
{
  "review_id": "R3549",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3550 — TinyTAN DNA 모니터 탑 지민 (ver.A) (1개)

상품 ID: 3583

- [TinyTAN DNA 모니터 탑 피규어 지민 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=33525423)

```json
{
  "review_id": "R3550",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3551 — TinyTAN DNA 모니터 탑 진 (ver.A) (1개)

상품 ID: 3348

- [TinyTAN DNA 모니터 탑 피규어 진 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=50652838)

```json
{
  "review_id": "R3551",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3552 — Trapeze (1개)

상품 ID: 5771

- [VOCALOID Trapeze-初音ミク-（全3種）](https://www.suruga-ya.jp/product/detail/602242514)

```json
{
  "review_id": "R3552",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3553 — TVアニメ『BLEACH』 市丸ギン (1개)

상품 ID: 1342

- [TVアニメ『BLEACH』 市丸ギン](https://megahobby.jp/products/item/6070/)

```json
{
  "review_id": "R3553",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3554 — TVアニメ『BLEACH』 藍染惣右介 (1개)

상품 ID: 1343

- [TVアニメ『BLEACH』 藍染惣右介](https://megahobby.jp/products/item/6071/)

```json
{
  "review_id": "R3554",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3555 — TVアニメ『BLEACH 千年血戦篇』 平子真子 (1개)

상품 ID: 1306

- [TVアニメ『BLEACH 千年血戦篇』 平子真子](https://megahobby.jp/products/item/6026/)

```json
{
  "review_id": "R3555",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3556 — TVアニメ『BLEACH 千年血戦篇』 日番谷冬獅郎 (1개)

상품 ID: 1305

- [TVアニメ『BLEACH 千年血戦篇』 日番谷冬獅郎](https://megahobby.jp/products/item/6025/)

```json
{
  "review_id": "R3556",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3557 — TVアニメ『BLEACH 千年血戦篇』 朽木白哉 (1개)

상품 ID: 1256

- [TVアニメ『BLEACH 千年血戦篇』 朽木白哉【再販】](https://megahobby.jp/products/item/5939/)

```json
{
  "review_id": "R3557",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3558 — TVアニメ『BLEACH 千年血戦篇』 黒崎一護 (1개)

상품 ID: 1257

- [TVアニメ『BLEACH 千年血戦篇』 黒崎一護【再販】](https://megahobby.jp/products/item/5940/)

```json
{
  "review_id": "R3558",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3559 — TVアニメ『ウィッチウォッチ』 てのひらニコちゃん (1개)

상품 ID: 879

- [TVアニメ『ウィッチウォッチ』 てのひらニコちゃん](https://megahobby.jp/products/item/5251/)

```json
{
  "review_id": "R3559",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3560 — TVアニメ『ウィッチウォッチ』 若月ニコ (1개)

상품 ID: 873

- [TVアニメ『ウィッチウォッチ』 若月ニコ](https://megahobby.jp/products/item/5244/)

```json
{
  "review_id": "R3560",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3561 — TVアニメ『ダンダダン』 (1개)

상품 ID: 917

- [TVアニメ『ダンダダン』](https://megahobby.jp/products/item/5333/)

```json
{
  "review_id": "R3561",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3562 — TVアニメ『ダンダダン』 てのひら アイラ (1개)

상품 ID: 807

- [TVアニメ『ダンダダン』  てのひら アイラ](https://megahobby.jp/products/item/5056/)

```json
{
  "review_id": "R3562",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3563 — TVアニメ『ダンダダン』 てのひら モモ (1개)

상품 ID: 693

- [TVアニメ『ダンダダン』  てのひら モモ](https://megahobby.jp/products/item/4835/)

```json
{
  "review_id": "R3563",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3564 — TVアニメ『ダンダダン』 アイラ (1개)

상품 ID: 956

- [TVアニメ『ダンダダン』 アイラ](https://megahobby.jp/products/item/5404/)

```json
{
  "review_id": "R3564",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3565 — TVアニメ『ダンダダン』 オカルン (1개)

상품 ID: 711

- [TVアニメ『ダンダダン』 オカルン](https://megahobby.jp/products/item/4871/)

```json
{
  "review_id": "R3565",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3566 — TVアニメ『ダンダダン』 ジジ (1개)

상품 ID: 955

- [TVアニメ『ダンダダン』 ジジ](https://megahobby.jp/products/item/5403/)

```json
{
  "review_id": "R3566",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3567 — TVアニメ『ダンダダン』 モモ (1개)

상품 ID: 712

- [TVアニメ『ダンダダン』 モモ](https://megahobby.jp/products/item/4872/)

```json
{
  "review_id": "R3567",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3568 — TVアニメ『チェンソーマン』 デンジ (1개)

상품 ID: 1288

- [TVアニメ『チェンソーマン』 デンジ【再販】](https://megahobby.jp/products/item/6005/)

```json
{
  "review_id": "R3568",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3569 — TV애니메이션 20주년 기념 우즈마키 나루토 소년 (1개)

상품 ID: 4397

- [나루토 TV애니메이션 20주년 기념 피규어 우즈마키 나루토 소년](https://www.bnkrmall.co.kr/goods/detail.do?gno=59551)

```json
{
  "review_id": "R3569",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3570 — TV애니메이션 20주년 기념 우즈마키 나루토 호카게 (1개)

상품 ID: 4396

- [나루토 TV애니메이션 20주년 기념 피규어 우즈마키 나루토 호카게](https://www.bnkrmall.co.kr/goods/detail.do?gno=59552)

```json
{
  "review_id": "R3570",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3571 — VAKIT プラトーン 装甲騎兵ボトムズ 灰色の魔女 (1개)

상품 ID: 1325

- [VAKIT プラトーン 装甲騎兵ボトムズ 灰色の魔女](https://megahobby.jp/products/item/6047/)

```json
{
  "review_id": "R3571",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3572 — VAKIT 機動戦士ガンダム ジオンの再興 ドワッジG型 (1개)

상품 ID: 4799

- [VAKIT  機動戦士ガンダム ジオンの再興 ドワッジG型](https://megahobby.jp/products/item/6193/)

```json
{
  "review_id": "R3572",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3573 — VAKIT 機動戦士ガンダム 新MS戦記 ギラ・ドーガ （一般機） (1개)

상품 ID: 1204

- [VAKIT  機動戦士ガンダム 新MS戦記 ギラ・ドーガ （一般機）](https://megahobby.jp/products/item/5838/)

```json
{
  "review_id": "R3573",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3574 — VAKIT 機動戦士ガンダム 新MS戦記 ギラ・ドーガ （隊長機） (1개)

상품 ID: 1203

- [VAKIT  機動戦士ガンダム 新MS戦記 ギラ・ドーガ （隊長機）](https://megahobby.jp/products/item/5837/)

```json
{
  "review_id": "R3574",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3575 — VA PIECE SAND LAND サンドランド国王軍戦車隊104号車 (1개)

상품 ID: 389

- [VA PIECE SAND LAND サンドランド国王軍戦車隊104号車](https://megahobby.jp/products/item/4223/)

```json
{
  "review_id": "R3575",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3576 — VOL.11 (우즈이 텐겐) (1개)

상품 ID: 4569

- [귀멸의 칼날 피규어 VOL.11 (우즈이 텐겐)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56591)

```json
{
  "review_id": "R3576",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3577 — Vol.14 (시나즈가와 사네미) (1개)

상품 ID: 4642

- [귀멸의 칼날 피규어 Vol.14 (시나즈가와 사네미)](https://www.bnkrmall.co.kr/goods/detail.do?gno=55244)

```json
{
  "review_id": "R3577",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3578 — Vol.15 (이구로 오바나이) (1개)

상품 ID: 4641

- [귀멸의 칼날 피규어 Vol.15 (이구로 오바나이)](https://www.bnkrmall.co.kr/goods/detail.do?gno=55245)

```json
{
  "review_id": "R3578",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3579 — Vol.16 (히메지마 교메이) (1개)

상품 ID: 4640

- [귀멸의 칼날 피규어 Vol.16 (히메지마 교메이)](https://www.bnkrmall.co.kr/goods/detail.do?gno=55246)

```json
{
  "review_id": "R3579",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3580 — Vol.17 (A:히메지마 교메이) (1개)

상품 ID: 4566

- [귀멸의 칼날 피규어 Vol.17 (A:히메지마 교메이)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56600)

```json
{
  "review_id": "R3580",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3581 — Vol.18 (B:카마도 탄지로) (1개)

상품 ID: 4565

- [귀멸의 칼날 피규어 Vol.18 (B:카마도 탄지로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56602)

```json
{
  "review_id": "R3581",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3582 — VOL.19 (A:카마도 탄지로) (1개)

상품 ID: 4597

- [귀멸의 칼날 피규어 VOL.19 (A:카마도 탄지로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56098)

```json
{
  "review_id": "R3582",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3583 — VOL.19 (B:사비토) (1개)

상품 ID: 4601

- [귀멸의 칼날 피규어 VOL.19 (B:사비토)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56080)

```json
{
  "review_id": "R3583",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3584 — Vol.1【BOX販売商品】 (1개)

상품 ID: 4931

- [ブルーロック　ラバー前髪クリップVol.1【BOX販売商品】](https://taito-goods.jp/shop/g/g70101340/)

```json
{
  "review_id": "R3584",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3585 — VOL.20 (A:사비토) (1개)

상품 ID: 4538

- [귀멸의 칼날 피규어 VOL.20 (A:사비토)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56795)

```json
{
  "review_id": "R3585",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3586 — VOL.20 (B:마코모) (1개)

상품 ID: 4537

- [귀멸의 칼날 피규어 VOL.20 (B:마코모)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56796)

```json
{
  "review_id": "R3586",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3587 — VOL.24 (A:칸자키 아오이) (1개)

상품 ID: 4461

- [귀멸의 칼날 피규어 VOL.24 (A:칸자키 아오이)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58832)

```json
{
  "review_id": "R3587",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3588 — VOL.24 (B:우로코다키 사콘지) (1개)

상품 ID: 4466

- [귀멸의 칼날 피규어 VOL.24 (B:우로코다키 사콘지)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58825)

```json
{
  "review_id": "R3588",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3589 — VOL.25 (렌고쿠 센쥬로) (1개)

상품 ID: 4424

- [귀멸의 칼날 피규어 VOL.25 (렌고쿠 센쥬로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59283)

```json
{
  "review_id": "R3589",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3590 — VOL.26 (B:카마도 네즈코) (1개)

상품 ID: 4411

- [귀멸의 칼날 피규어 VOL.26 (B:카마도 네즈코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59521)

```json
{
  "review_id": "R3590",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3591 — VOL.27 (A:카마도 네즈코) (1개)

상품 ID: 4350

- [귀멸의 칼날 피규어 VOL.27 (A:카마도 네즈코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59973)

```json
{
  "review_id": "R3591",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3592 — VOL.27 (B:무라타) (1개)

상품 ID: 4349

- [귀멸의 칼날 피규어 VOL.27 (B:무라타)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59974)

```json
{
  "review_id": "R3592",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3593 — VOL.28 (1개)

상품 ID: 4359

- [귀멸의 칼날 피규어 VOL.28](https://www.bnkrmall.co.kr/goods/detail.do?gno=59959)

```json
{
  "review_id": "R3593",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3594 — VOL.29 (B:우부야시키 카가야) (1개)

상품 ID: 4343

- [귀멸의 칼날 피규어 VOL.29 (B:우부야시키 카가야)](https://www.bnkrmall.co.kr/goods/detail.do?gno=66455712)

```json
{
  "review_id": "R3594",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3595 — Vol.2【BOX販売商品】 (1개)

상품 ID: 4932

- [ブルーロック　ラバー前髪クリップVol.2【BOX販売商品】](https://taito-goods.jp/shop/g/g70101350/)

```json
{
  "review_id": "R3595",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3596 — VOL.30 (1개)

상품 ID: 4342

- [귀멸의 칼날 피규어 VOL.30](https://www.bnkrmall.co.kr/goods/detail.do?gno=30727946)

```json
{
  "review_id": "R3596",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3597 — VOL.31 (1개)

상품 ID: 4337

- [귀멸의 칼날 피규어 VOL.31](https://www.bnkrmall.co.kr/goods/detail.do?gno=87224703)

```json
{
  "review_id": "R3597",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3598 — VOL.32 (1개)

상품 ID: 4336

- [귀멸의 칼날 피규어 VOL.32](https://www.bnkrmall.co.kr/goods/detail.do?gno=99774060)

```json
{
  "review_id": "R3598",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3599 — VOL.33 (1개)

상품 ID: 4327

- [귀멸의 칼날 피규어 VOL.33](https://www.bnkrmall.co.kr/goods/detail.do?gno=42617726)

```json
{
  "review_id": "R3599",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3600 — VOL.34 (1개)

상품 ID: 4326

- [귀멸의 칼날 피규어 VOL.34](https://www.bnkrmall.co.kr/goods/detail.do?gno=54532698)

```json
{
  "review_id": "R3600",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3601 — VOL.35 (B:하가네즈카 호타루) (1개)

상품 ID: 4312

- [귀멸의 칼날 피규어 VOL.35 (B:하가네즈카 호타루)](https://www.bnkrmall.co.kr/goods/detail.do?gno=81851189)

```json
{
  "review_id": "R3601",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3602 — VOL.36 (A:우부야시키 카가야) (1개)

상품 ID: 4310

- [귀멸의 칼날 피규어 VOL.36 (A:우부야시키 카가야)](https://www.bnkrmall.co.kr/goods/detail.do?gno=36330117)

```json
{
  "review_id": "R3602",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3603 — VOL.36 (B:겐야) (1개)

상품 ID: 4309

- [귀멸의 칼날 피규어 VOL.36 (B:겐야)](https://www.bnkrmall.co.kr/goods/detail.do?gno=3292810)

```json
{
  "review_id": "R3603",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3604 — VOL.37 (B:코쵸우 시노부) (1개)

상품 ID: 4308

- [귀멸의 칼날 피규어 VOL.37 (B:코쵸우 시노부)](https://www.bnkrmall.co.kr/goods/detail.do?gno=48999579)

```json
{
  "review_id": "R3604",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3605 — VOL.38 (A:겐야) (1개)

상품 ID: 4300

- [귀멸의 칼날 피규어 VOL.38 (A:겐야)](https://www.bnkrmall.co.kr/goods/detail.do?gno=83550081)

```json
{
  "review_id": "R3605",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3606 — VOL.38 (B:코테츠) (1개)

상품 ID: 4299

- [귀멸의 칼날 피규어 VOL.38 (B:코테츠)](https://www.bnkrmall.co.kr/goods/detail.do?gno=75689234)

```json
{
  "review_id": "R3606",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3607 — VOL.39 (1개)

상품 ID: 4294

- [귀멸의 칼날 피규어 VOL.39](https://www.bnkrmall.co.kr/goods/detail.do?gno=46173712)

```json
{
  "review_id": "R3607",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3608 — Vol.4 (하시비라 이노스케) (1개)

상품 ID: 4592

- [귀멸의 칼날 피규어 Vol.4 (하시비라 이노스케)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56287)

```json
{
  "review_id": "R3608",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3609 — VOL.40 (B:코쵸우 카나에) (1개)

상품 ID: 4288

- [귀멸의 칼날 피규어 VOL.40 (B:코쵸우 카나에)](https://www.bnkrmall.co.kr/goods/detail.do?gno=40038299)

```json
{
  "review_id": "R3609",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3610 — VOL.41 (B:고토) (1개)

상품 ID: 4266

- [귀멸의 칼날 피규어 VOL.41 (B:고토)](https://www.bnkrmall.co.kr/goods/detail.do?gno=97192598)

```json
{
  "review_id": "R3610",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3611 — VOL.42 (B:칸로지 미츠리) (1개)

상품 ID: 4257

- [귀멸의 칼날 피규어 VOL.42 (B:칸로지 미츠리)](https://www.bnkrmall.co.kr/goods/detail.do?gno=92494336)

```json
{
  "review_id": "R3611",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3612 — VOL.43 (B:렌고쿠 쿄쥬로) (1개)

상품 ID: 4227

- [귀멸의 칼날 피규어 VOL.43 (B:렌고쿠 쿄쥬로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=78073056)

```json
{
  "review_id": "R3612",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3613 — VOL.44 (A:토키토 무이치로) (1개)

상품 ID: 4226

- [귀멸의 칼날 피규어 VOL.44 (A:토키토 무이치로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=93701482)

```json
{
  "review_id": "R3613",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3614 — VOL.44 (B:시나즈가와 겐야) (1개)

상품 ID: 4320

- [귀멸의 칼날 피규어 VOL.44 (B:시나즈가와 겐야)](https://www.bnkrmall.co.kr/goods/detail.do?gno=18041923)

```json
{
  "review_id": "R3614",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3615 — VOL.45 (A:카마도 네즈코) (1개)

상품 ID: 4205

- [귀멸의 칼날 피규어 VOL.45 (A:카마도 네즈코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=3959480)

```json
{
  "review_id": "R3615",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3616 — VOL.45 (B:칸로지 미츠리) (1개)

상품 ID: 4204

- [귀멸의 칼날 피규어 VOL.45 (B:칸로지 미츠리)](https://www.bnkrmall.co.kr/goods/detail.do?gno=23905149)

```json
{
  "review_id": "R3616",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3617 — VOL.47 (B:코쵸우 시노부) (1개)

상품 ID: 4198

- [귀멸의 칼날 피규어 VOL.47 (B:코쵸우 시노부)](https://www.bnkrmall.co.kr/goods/detail.do?gno=6777100)

```json
{
  "review_id": "R3617",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3618 — VOL.48 (츠유리 카나오) (1개)

상품 ID: 4297

- [귀멸의 칼날 피규어 VOL.48 (츠유리 카나오)](https://www.bnkrmall.co.kr/goods/detail.do?gno=12784930)

```json
{
  "review_id": "R3618",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3619 — VOL.49 (칸로지 미츠리) (1개)

상품 ID: 4186

- [귀멸의 칼날 피규어 VOL.49 (칸로지 미츠리)](https://www.bnkrmall.co.kr/goods/detail.do?gno=36166698)

```json
{
  "review_id": "R3619",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3620 — Vol.5 (토미오카 기유) (1개)

상품 ID: 4606

- [귀멸의 칼날 피규어 Vol.5 (토미오카 기유)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56063)

```json
{
  "review_id": "R3620",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3621 — VOL.50 (토키토 무이치로) (1개)

상품 ID: 4185

- [귀멸의 칼날 피규어 VOL.50 (토키토 무이치로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59099493)

```json
{
  "review_id": "R3621",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3622 — vol.51 (1개)

상품 ID: 3273

- [귀멸의 칼날 피규어 vol.51](https://www.bnkrmall.co.kr/goods/detail.do?gno=62597781)

```json
{
  "review_id": "R3622",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3623 — vol.52 (1개)

상품 ID: 3272

- [귀멸의 칼날 피규어 vol.52](https://www.bnkrmall.co.kr/goods/detail.do?gno=42270402)

```json
{
  "review_id": "R3623",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3624 — Vol.7 (츠유리 카나오) (1개)

상품 ID: 4483

- [귀멸의 칼날 피규어 Vol.7 (츠유리 카나오)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58289)

```json
{
  "review_id": "R3624",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3625 — VTuber인데 방송 끄는 걸 깜빡했더니 전설이 되어있었다 슈와짱 (1개)

상품 ID: 4153

- [VTuber인데 방송 끄는 걸 깜빡했더니 전설이 되어있었다 슈와짱 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=91101685)

```json
{
  "review_id": "R3625",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3626 — WALLSTAR ONE PIECE ナミ（エルバフ編） (1개)

상품 ID: 1363

- [WALLSTAR ONE PIECE ナミ（エルバフ編）](https://megahobby.jp/products/item/6127/)

```json
{
  "review_id": "R3626",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3627 — WALLSTAR ONE PIECE モンキー・D・ルフィ（エルバフ編） (1개)

상품 ID: 1364

- [WALLSTAR ONE PIECE モンキー・D・ルフィ（エルバフ編）](https://megahobby.jp/products/item/6128/)

```json
{
  "review_id": "R3627",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3628 — WALLSTAR ONE PIECE モンキー・D・ルフィ ギア5 (1개)

상품 ID: 1351

- [WALLSTAR ONE PIECE モンキー・D・ルフィ ギア5](https://megahobby.jp/products/item/6079/)

```json
{
  "review_id": "R3628",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3629 — WALLSTAR ONE PIECE ロロノア・ゾロ (1개)

상품 ID: 1350

- [WALLSTAR ONE PIECE ロロノア・ゾロ](https://megahobby.jp/products/item/6078/)

```json
{
  "review_id": "R3629",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3630 — WICKED ウィキッド エルファバ (1개)

상품 ID: 1025

- [WICKED ウィキッド エルファバ](https://megahobby.jp/products/item/5526/)

```json
{
  "review_id": "R3630",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3631 — WICKED ウィキッド グリンダ (1개)

상품 ID: 1026

- [WICKED ウィキッド グリンダ](https://megahobby.jp/products/item/5527/)

```json
{
  "review_id": "R3631",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3632 — WIND BREAKER (1개)

상품 ID: 820

- [WIND BREAKER](https://megahobby.jp/products/item/5156/)

```json
{
  "review_id": "R3632",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3633 — WIND BREAKER 兎耳山丁子 (1개)

상품 ID: 732

- [WIND BREAKER 兎耳山丁子](https://megahobby.jp/products/item/4937/)

```json
{
  "review_id": "R3633",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3634 — WIND BREAKER 十亀条 (1개)

상품 ID: 731

- [WIND BREAKER 十亀条](https://megahobby.jp/products/item/4936/)

```json
{
  "review_id": "R3634",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3635 — WIND BREAKER 梅宮一 (1개)

상품 ID: 559

- [WIND BREAKER 梅宮一](https://megahobby.jp/products/item/4558/)

```json
{
  "review_id": "R3635",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3636 — WIND BREAKER 梶蓮 (1개)

상품 ID: 583

- [WIND BREAKER 梶蓮](https://megahobby.jp/products/item/4615/)

```json
{
  "review_id": "R3636",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3637 — WIND BREAKER 蘇枋隼飛 (1개)

상품 ID: 584

- [WIND BREAKER 蘇枋隼飛](https://megahobby.jp/products/item/4616/)

```json
{
  "review_id": "R3637",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3638 — WIND BREAKER 사쿠라 하루카 CHATTING TIME (1개)

상품 ID: 3488

- [WIND BREAKER 사쿠라 하루카 CHATTING TIME](https://www.bnkrmall.co.kr/goods/detail.do?gno=45979055)

```json
{
  "review_id": "R3638",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3639 — WIND BREAKER 스오 하야토 CHATTING TIME (1개)

상품 ID: 3900

- [WIND BREAKER 스오 하야토 CHATTING TIME](https://www.bnkrmall.co.kr/goods/detail.do?gno=28986006)

```json
{
  "review_id": "R3639",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3640 — WIND BREAKER 우메미야 하지메 CHATTING TIME (1개)

상품 ID: 3901

- [WIND BREAKER 우메미야 하지메 CHATTING TIME](https://www.bnkrmall.co.kr/goods/detail.do?gno=73940417)

```json
{
  "review_id": "R3640",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3641 — WIND BREAKER 카지 렌 CHATTING TIME (1개)

상품 ID: 3919

- [WIND BREAKER 카지 렌 CHATTING TIME](https://www.bnkrmall.co.kr/goods/detail.do?gno=31913026)

```json
{
  "review_id": "R3641",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3642 — W 영웅용상 가면라이더 W 사이클론 조커 VER.A (1개)

상품 ID: 4464

- [가면라이더 W 영웅용상 가면라이더 W 사이클론 조커 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=58828)

```json
{
  "review_id": "R3642",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3643 — W 영웅용상 가면라이더 W 팡 조커 VER.A (1개)

상품 ID: 4444

- [가면라이더 W 영웅용상 가면라이더 W 팡 조커 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=59220)

```json
{
  "review_id": "R3643",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3644 — W 영웅용상 가면라이더 스컬 (1개)

상품 ID: 4379

- [가면라이더 W 영웅용상 가면라이더 스컬](https://www.bnkrmall.co.kr/goods/detail.do?gno=59811)

```json
{
  "review_id": "R3644",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3645 — YAIBA : 쿠로가네&카게토라 (A:야이바 쿠로가네) (1개)

상품 ID: 3880

- [YAIBA : 쿠로가네&카게토라 피규어 (A:야이바 쿠로가네)](https://www.bnkrmall.co.kr/goods/detail.do?gno=38697652)

```json
{
  "review_id": "R3645",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3646 — YAIBA : 쿠로가네&카게토라 (B:카게토라) (1개)

상품 ID: 3879

- [YAIBA : 쿠로가네&카게토라 피규어 (B:카게토라)](https://www.bnkrmall.co.kr/goods/detail.do?gno=33054530)

```json
{
  "review_id": "R3646",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3647 — YAIBA 쿠로가네 야이바 (1개)

상품 ID: 3808

- [YAIBA 쿠로가네 야이바 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=83873470)

```json
{
  "review_id": "R3647",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3648 — ZZ 엘피 플 (1개)

상품 ID: 4261

- [기동전사 건담 ZZ 엘피 플 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=35376303)

```json
{
  "review_id": "R3648",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3649 — ~LEGEND&#039;s FACES COLLECTION~ ゴジラ(2026) (1개)

상품 ID: 6156

- [~LEGEND&#039;s FACES COLLECTION~   ゴジラ(2026)](https://megahobby.jp/products/item/6192/)

```json
{
  "review_id": "R3649",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3650 — ~LEGEND&#039;s FACES COLLECTION~ ゴジラ(2026) 熱線放射時Ver. (1개)

상품 ID: 6157

- [~LEGEND&#039;s FACES COLLECTION~  ゴジラ(2026) 熱線放射時Ver.](https://megahobby.jp/products/item/6191/)

```json
{
  "review_id": "R3650",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3651 — ~LEGEND&#039;s FACES COLLECTION~ 新世紀GPXサイバーフォーミュラ ナビゲーションサイバーシステム アスラーダ(スーパーアスラーダ01Ver.) (1개)

상품 ID: 1369

- [~LEGEND&#039;s FACES COLLECTION~  新世紀GPXサイバーフォーミュラ ナビゲーションサイバーシステム アスラーダ(スーパーアスラーダ01Ver.)](https://megahobby.jp/products/item/6134/)

```json
{
  "review_id": "R3651",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3652 — ×メカトロウィーゴ しるふぃーⅡ (1개)

상품 ID: 561

- [×メカトロウィーゴ　  しるふぃーⅡ](https://megahobby.jp/products/item/4560/)

```json
{
  "review_id": "R3652",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3653 — 「聖戦士ダンバイン」 ダンバイン：RE (1개)

상품 ID: 120

- [「聖戦士ダンバイン」　ダンバイン：RE](https://megahobby.jp/products/item/1867/)

```json
{
  "review_id": "R3653",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3654 — 『Re:ゼロから始める異世界生活』 てのひらエミリア (1개)

상품 ID: 973

- [『Re:ゼロから始める異世界生活』 てのひらエミリア【再販】](https://megahobby.jp/products/item/5423/)

```json
{
  "review_id": "R3654",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3655 — 『Re:ゼロから始める異世界生活』 てのひらラム (1개)

상품 ID: 1163

- [ 『Re:ゼロから始める異世界生活』 てのひらラム](https://megahobby.jp/products/item/5768/)

```json
{
  "review_id": "R3655",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3656 — 『ゆるキャン△ SEASON３』 てのひらリンちゃん (1개)

상품 ID: 670

- [ 『ゆるキャン△ SEASON３』 てのひらリンちゃん](https://megahobby.jp/products/item/4792/)

```json
{
  "review_id": "R3656",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3657 — 『ゆるキャン△ SEASON３』 てのひら綾乃ちゃん (1개)

상품 ID: 669

- [ 『ゆるキャン△ SEASON３』 てのひら綾乃ちゃん](https://megahobby.jp/products/item/4791/)

```json
{
  "review_id": "R3657",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3658 — 『ディズニー ツイステッドワンダーランド』 カリム・アルアジーム (1개)

상품 ID: 1141

- [『ディズニー ツイステッドワンダーランド』 カリム・アルアジーム【再販】](https://megahobby.jp/products/item/5745/)

```json
{
  "review_id": "R3658",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3659 — 『ディズニー ツイステッドワンダーランド』 リドル・ローズハート (1개)

상품 ID: 1129

- [『ディズニー ツイステッドワンダーランド』 リドル・ローズハート【再販】](https://megahobby.jp/products/item/5716/)

```json
{
  "review_id": "R3659",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3660 — 『ディズニー ツイステッドワンダーランド』 レオナ・キングスカラー (1개)

상품 ID: 1127

- [『ディズニー ツイステッドワンダーランド』 レオナ・キングスカラー【再販】](https://megahobby.jp/products/item/5714/)

```json
{
  "review_id": "R3660",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3661 — 『メタルギア ソリッド』 メタルギアREX：RE (1개)

상품 ID: 744

- [『メタルギア ソリッド』 メタルギアREX：RE](https://megahobby.jp/products/item/4962/)

```json
{
  "review_id": "R3661",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3662 — 『機動戦士Gundam GQuuuuuuX』 (1개)

상품 ID: 1069

- [ 『機動戦士Gundam GQuuuuuuX』](https://megahobby.jp/products/item/5587/)

```json
{
  "review_id": "R3662",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3663 — 『機動戦士ガンダム 水星の魔女』 エラン・ケレス (強化人士5号) (1개)

상품 ID: 315

- [『機動戦士ガンダム 水星の魔女』 エラン・ケレス (強化人士5号)](https://megahobby.jp/products/item/4069/)

```json
{
  "review_id": "R3663",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3664 — 『機動戦士ガンダム 水星の魔女』 グエル・ジェターク (1개)

상품 ID: 316

- [『機動戦士ガンダム 水星の魔女』 グエル・ジェターク](https://megahobby.jp/products/item/4070/)

```json
{
  "review_id": "R3664",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3665 — 『機動戦士ガンダム 水星の魔女』 シャディク・ゼネリ (1개)

상품 ID: 314

- [『機動戦士ガンダム 水星の魔女』 シャディク・ゼネリ](https://megahobby.jp/products/item/4068/)

```json
{
  "review_id": "R3665",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3666 — 『機動戦士ガンダム 水星の魔女』 スレッタ・マーキュリー (1개)

상품 ID: 303

- [『機動戦士ガンダム 水星の魔女』 スレッタ・マーキュリー](https://megahobby.jp/products/item/4033/)

```json
{
  "review_id": "R3666",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3667 — 『機動戦士ガンダム 水星の魔女』 チュアチュリー・パンランチ (1개)

상품 ID: 343

- [『機動戦士ガンダム 水星の魔女』 チュアチュリー・パンランチ](https://megahobby.jp/products/item/4122/)

```json
{
  "review_id": "R3667",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3668 — 『機動戦士ガンダム 水星の魔女』 ニカ・ナナウラ (1개)

상품 ID: 344

- [『機動戦士ガンダム 水星の魔女』 ニカ・ナナウラ](https://megahobby.jp/products/item/4123/)

```json
{
  "review_id": "R3668",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3669 — 『機動戦士ガンダム 水星の魔女』 ミオリネ・レンブラン (1개)

상품 ID: 302

- [『機動戦士ガンダム 水星の魔女』 ミオリネ・レンブラン](https://megahobby.jp/products/item/4032/)

```json
{
  "review_id": "R3669",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3670 — 『機動戦士ガンダム 鉄血のオルフェンズ』 オルガ・イツカ (1개)

상품 ID: 1093

- [『機動戦士ガンダム 鉄血のオルフェンズ』 オルガ・イツカ](https://megahobby.jp/products/item/5634/)

```json
{
  "review_id": "R3670",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3671 — 『機動戦士ガンダム 鉄血のオルフェンズ』 三日月・オーガス (1개)

상품 ID: 1097

- [『機動戦士ガンダム 鉄血のオルフェンズ』 三日月・オーガス](https://megahobby.jp/products/item/5638/)

```json
{
  "review_id": "R3671",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3672 — 『無職転生Ⅱ ～異世界行ったら本気だす～』 てのひらエリス (1개)

상품 ID: 1052

- [『無職転生Ⅱ ～異世界行ったら本気だす～』 てのひらエリス【再販】](https://megahobby.jp/products/item/5567/)

```json
{
  "review_id": "R3672",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3673 — 『生徒会にも穴はある！』 てのひらこまろちゃん (1개)

상품 ID: 1366

- [『生徒会にも穴はある！』 てのひらこまろちゃん](https://megahobby.jp/products/item/6130/)

```json
{
  "review_id": "R3673",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3674 — 『신 고질라』 아트 비네트 고질라(2016) 제4형태 상륙 이미지 ver. (1개)

상품 ID: 3336

- [『신 고질라』 아트 비네트 고질라(2016) 제4형태 상륙 이미지 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=36324290)

```json
{
  "review_id": "R3674",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3675 — 【100着限定】 ふわもこスンスンルームウェア (1개)

상품 ID: 4945

- [【100着限定】パペットスンスン　ふわもこスンスンルームウェア](https://taito-goods.jp/shop/g/g70101210/)

```json
{
  "review_id": "R3675",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3676 — 【300個限定】 スンスンとおでかけバックパック (1개)

상품 ID: 4946

- [【300個限定】パペットスンスン　スンスンとおでかけバックパック](https://taito-goods.jp/shop/g/g70101220/)

```json
{
  "review_id": "R3676",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3677 — 【推しの子】 アイ (1개)

상품 ID: 323

- [【推しの子】 アイ](https://megahobby.jp/products/item/4077/)

```json
{
  "review_id": "R3677",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3678 — 【推しの子】 アクア (1개)

상품 ID: 346

- [【推しの子】 アクア](https://megahobby.jp/products/item/4125/)

```json
{
  "review_id": "R3678",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3679 — 【推しの子】 ルビー (1개)

상품 ID: 322

- [【推しの子】 ルビー](https://megahobby.jp/products/item/4076/)

```json
{
  "review_id": "R3679",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3680 — 【推しの子】 有馬かな (1개)

상품 ID: 345

- [【推しの子】 有馬かな](https://megahobby.jp/products/item/4124/)

```json
{
  "review_id": "R3680",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3681 — うるぎゅっと THE RIBBON HERO マスコット サファイア リボンの騎士ver. (1개)

상품 ID: 4802

- [うるぎゅっと　THE RIBBON HERO　マスコット　サファイア　リボンの騎士ver.](https://taito-goods.jp/shop/g/g70101490/)

```json
{
  "review_id": "R3681",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3682 — うるぎゅっと THE RIBBON HERO マスコット サファイア 私服ver. (1개)

상품 ID: 4803

- [うるぎゅっと　THE RIBBON HERO　マスコット　サファイア　私服ver.](https://taito-goods.jp/shop/g/g70101491/)

```json
{
  "review_id": "R3682",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3683 — うる星やつら ラム (1개)

상품 ID: 417

- [うる星やつら ラム](https://megahobby.jp/products/item/4272/)

```json
{
  "review_id": "R3683",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3684 — うる星やつら 諸星あたる (1개)

상품 ID: 418

- [うる星やつら 諸星あたる](https://megahobby.jp/products/item/4273/)

```json
{
  "review_id": "R3684",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3685 — おでかけポーチ (1개)

상품 ID: 1199

- [おでかけポーチ【再販】](https://megahobby.jp/products/item/5830/)

```json
{
  "review_id": "R3685",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3686 — お兄ちゃんはおしまい！ てのひら みはりちゃん (1개)

상품 ID: 989

- [お兄ちゃんはおしまい！ てのひら　みはりちゃん](https://megahobby.jp/products/item/5441/)

```json
{
  "review_id": "R3686",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3687 — しゅごキャラ！ 日奈森あむ (1개)

상품 ID: 1178

- [しゅごキャラ！ 日奈森あむ](https://megahobby.jp/products/item/5809/)

```json
{
  "review_id": "R3687",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3688 — すたんだーど 機動戦士Gundam GQuuuuuuX ハロ (1개)

상품 ID: 967

- [すたんだーど  機動戦士Gundam GQuuuuuuX ハロ](https://megahobby.jp/products/item/5415/)

```json
{
  "review_id": "R3688",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3689 — すたんだーど 銀魂 ギンザベス (1개)

상품 ID: 988

- [すたんだーど 銀魂 ギンザベス](https://megahobby.jp/products/item/5440/)

```json
{
  "review_id": "R3689",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3690 — その他コレクションアイテム 3年Z組銀八先生×大川ぶくぶ 3年Z組銀八先生 青春☆缶バッジコレクション (1개)

상품 ID: 1378

- [その他コレクションアイテム 3年Z組銀八先生×大川ぶくぶ 3年Z組銀八先生 青春☆缶バッジコレクション](https://megahobby.jp/products/item/5235/)

```json
{
  "review_id": "R3690",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3691 — その着せ替え人形は恋をする てのひら 海夢ちゃん (1개)

상품 ID: 622

- [ その着せ替え人形は恋をする てのひら 海夢ちゃん](https://megahobby.jp/products/item/4679/)

```json
{
  "review_id": "R3691",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3692 — ちびコレクト vol.1 パックマン×サンリオキャラクターズ (1개)

상품 ID: 177

- [ちびコレクト フィギュアvol.1  パックマン×サンリオキャラクターズ ](https://megahobby.jp/products/item/3703/)

```json
{
  "review_id": "R3692",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3693 — ちみメガシリーズ NARUTO-ナルト- 疾風伝 マスコットコレクション【1】 (1개)

상품 ID: 1331

- [ちみメガシリーズ NARUTO-ナルト- 疾風伝 マスコットコレクション【1】](https://megahobby.jp/products/item/6059/)

```json
{
  "review_id": "R3693",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3694 — とびマス NARUTO-ナルト- 疾風伝 (1개)

상품 ID: 1359

- [とびマス NARUTO-ナルト- 疾風伝](https://megahobby.jp/products/item/6110/)

```json
{
  "review_id": "R3694",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3695 — とびマス サンリオキャラクターズ (1개)

상품 ID: 123

- [とびマス  サンリオキャラクターズ](https://megahobby.jp/products/item/2138/)

```json
{
  "review_id": "R3695",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3696 — とびマス ドラゴンボールvol.2 (1개)

상품 ID: 1150

- [とびマス  ドラゴンボールvol.2](https://megahobby.jp/products/item/5754/)

```json
{
  "review_id": "R3696",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3697 — とびマス ドラゴンボールvol.3 (1개)

상품 ID: 1296

- [とびマス  ドラゴンボールvol.3](https://megahobby.jp/products/item/6016/)

```json
{
  "review_id": "R3697",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3698 — とびマス 僕のヒーローアカデミア (1개)

상품 ID: 1330

- [とびマス 僕のヒーローアカデミア](https://megahobby.jp/products/item/6058/)

```json
{
  "review_id": "R3698",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3699 — とびマス 呪術廻戦 (1개)

상품 ID: 1329

- [とびマス 呪術廻戦](https://megahobby.jp/products/item/6057/)

```json
{
  "review_id": "R3699",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3700 — とびマス 星のカービィ (1개)

상품 ID: 1077

- [とびマス  星のカービィ](https://megahobby.jp/products/item/5618/)

```json
{
  "review_id": "R3700",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3701 — とびマス 進撃の巨人 (1개)

상품 ID: 1297

- [とびマス  進撃の巨人](https://megahobby.jp/products/item/6017/)

```json
{
  "review_id": "R3701",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3702 — ぴたきゅっと。 たまごっち (1개)

상품 ID: 1358

- [ぴたきゅっと。 たまごっち](https://megahobby.jp/products/item/6109/)

```json
{
  "review_id": "R3702",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3703 — ふかふかスクイーズパン 地獄楽 (1개)

상품 ID: 575

- [ふかふかスクイーズパン  地獄楽](https://megahobby.jp/products/item/4607/)

```json
{
  "review_id": "R3703",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3704 — ぷらっとこれくしょん WIND BREAKER (1개)

상품 ID: 794

- [ぷらっとこれくしょん  WIND BREAKER](https://megahobby.jp/products/item/5043/)

```json
{
  "review_id": "R3704",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3705 — ぼっち・ざ・ろっく！ てのひら ひとりちゃん (1개)

상품 ID: 378

- [ ぼっち・ざ・ろっく！ てのひら　ひとりちゃん](https://megahobby.jp/products/item/4181/)

```json
{
  "review_id": "R3705",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3706 — ぼっち・ざ・ろっく！ 伊地知虹夏 (1개)

상품 ID: 448

- [ぼっち・ざ・ろっく！ 伊地知虹夏](https://megahobby.jp/products/item/4336/)

```json
{
  "review_id": "R3706",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3707 — ぼっち・ざ・ろっく！ 喜多郁代 (1개)

상품 ID: 437

- [ぼっち・ざ・ろっく！ 喜多郁代](https://megahobby.jp/products/item/4312/)

```json
{
  "review_id": "R3707",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3708 — ぼっち・ざ・ろっく！ 山田リョウ (1개)

상품 ID: 447

- [ぼっち・ざ・ろっく！ 山田リョウ](https://megahobby.jp/products/item/4335/)

```json
{
  "review_id": "R3708",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3709 — らいと アイカツ！×プリパラTHEMOVIE-出会いのキセキ！- 大空あかり (1개)

상품 ID: 1101

- [らいと アイカツ！×プリパラTHEMOVIE-出会いのキセキ！- 大空あかり](https://megahobby.jp/products/item/5642/)

```json
{
  "review_id": "R3709",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3710 — らいと アイカツ！×プリパラ THE MOVIE -出会いのキセキ！- 真中らぁら (1개)

상품 ID: 1124

- [らいと アイカツ！×プリパラ THE MOVIE -出会いのキセキ！- 真中らぁら](https://megahobby.jp/products/item/5708/)

```json
{
  "review_id": "R3710",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3711 — らいと アポカリプスホテル ヤチヨ (1개)

상품 ID: 1125

- [らいと アポカリプスホテル ヤチヨ](https://megahobby.jp/products/item/5709/)

```json
{
  "review_id": "R3711",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3712 — らいと 機動戦士Gundam GQuuuuuuX アマテ・ユズリハ（マチュ） パイロットスーツVer. (1개)

상품 ID: 832

- [らいと 機動戦士Gundam GQuuuuuuX アマテ・ユズリハ（マチュ） パイロットスーツVer.](https://megahobby.jp/products/item/5169/)

```json
{
  "review_id": "R3712",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3713 — らいと 機動戦士Gundam GQuuuuuuX シャリア・ブル (1개)

상품 ID: 1248

- [らいと 機動戦士Gundam GQuuuuuuX シャリア・ブル](https://megahobby.jp/products/item/5883/)

```json
{
  "review_id": "R3713",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3714 — らいと 機動戦士Gundam GQuuuuuuX ドゥー・ムラサメ パイロットスーツVer. (1개)

상품 ID: 1004

- [らいと 機動戦士Gundam GQuuuuuuX ドゥー・ムラサメ　パイロットスーツVer.](https://megahobby.jp/products/item/5483/)

```json
{
  "review_id": "R3714",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3715 — らいと 機動戦士Gundam GQuuuuuuX ニャアン パイロットスーツVer. (1개)

상품 ID: 1020

- [らいと 機動戦士Gundam GQuuuuuuX ニャアン　パイロットスーツVer.](https://megahobby.jp/products/item/5499/)

```json
{
  "review_id": "R3715",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3716 — らいと 機動戦士ガンダムSEED FREEDOM アスラン・ザラ パイロットスーツVer. (1개)

상품 ID: 1249

- [らいと 機動戦士ガンダムSEED FREEDOM アスラン・ザラ　パイロットスーツVer.](https://megahobby.jp/products/item/5884/)

```json
{
  "review_id": "R3716",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3717 — らいと 機動戦士ガンダムSEED FREEDOM キラ・ヤマト パイロットスーツVer. (1개)

상품 ID: 1169

- [らいと 機動戦士ガンダムSEED FREEDOM キラ・ヤマト　パイロットスーツVer.](https://megahobby.jp/products/item/5800/)

```json
{
  "review_id": "R3717",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3718 — らいと 機動戦士ガンダムSEED FREEDOM ラクス・クライン 水着Ver. (1개)

상품 ID: 1367

- [らいと 機動戦士ガンダムSEED FREEDOM ラクス・クライン 水着Ver.](https://megahobby.jp/products/item/6131/)

```json
{
  "review_id": "R3718",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3719 — るきゃっぷ 銀魂 定春 (1개)

상품 ID: 1118

- [るきゃっぷ 銀魂 定春](https://megahobby.jp/products/item/5702/)

```json
{
  "review_id": "R3719",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3720 — アイドリッシュセブン 七瀬陸 (1개)

상품 ID: 779

- [アイドリッシュセブン 七瀬陸](https://megahobby.jp/products/item/5003/)

```json
{
  "review_id": "R3720",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3721 — アイドリッシュセブン 九条天 (1개)

상품 ID: 778

- [アイドリッシュセブン 九条天](https://megahobby.jp/products/item/5002/)

```json
{
  "review_id": "R3721",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3722 — アイドルマスター シャイニーカラーズ 芹沢あさひ (1개)

상품 ID: 510

- [アイドルマスター シャイニーカラーズ 芹沢あさひ](https://megahobby.jp/products/item/4474/)

```json
{
  "review_id": "R3722",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3723 — アイドルマスター シャイニーカラーズ 黛 冬優子 (1개)

상품 ID: 509

- [アイドルマスター シャイニーカラーズ 黛 冬優子](https://megahobby.jp/products/item/4473/)

```json
{
  "review_id": "R3723",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3724 — アクリルマスコット 銀魂 エリザベス12星座 autumn＆winter (1개)

상품 ID: 861

- [アクリルマスコット 銀魂 エリザベス12星座　autumn＆winter](https://megahobby.jp/products/item/5231/)

```json
{
  "review_id": "R3724",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3725 — アクリルマスコット 銀魂 エリザベス12星座 spring＆summer (1개)

상품 ID: 817

- [アクリルマスコット 銀魂 エリザベス12星座　spring＆summer](https://megahobby.jp/products/item/5152/)

```json
{
  "review_id": "R3725",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3726 — アニメ『ケロロ軍曹☆』 てのひら夏美＆ギロロ (1개)

상품 ID: 1365

- [アニメ『ケロロ軍曹☆』 てのひら夏美＆ギロロ](https://megahobby.jp/products/item/6129/)

```json
{
  "review_id": "R3726",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3727 — アニメ『呪術廻戦』 ５周年 (1개)

상품 ID: 1193

- [アニメ『呪術廻戦』 ５周年](https://megahobby.jp/products/item/5824/)

```json
{
  "review_id": "R3727",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3728 — アリス・ギア・アイギス バージニア・グリンベレー (1개)

상품 ID: 212

- [アリス・ギア・アイギス バージニア・グリンベレー](https://megahobby.jp/products/item/3815/)

```json
{
  "review_id": "R3728",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3729 — アームにスンスンロンT (1개)

상품 ID: 4947

- [パペットスンスン アームにスンスンロンT](https://taito-goods.jp/shop/g/g70101230/)

```json
{
  "review_id": "R3729",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3730 — イーブイ (1개)

상품 ID: 641

- [イーブイ](https://megahobby.jp/products/item/4728/)

```json
{
  "review_id": "R3730",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3731 — ウマ娘 プリティーダービー ゴールドシップ (1개)

상품 ID: 554

- [ウマ娘 プリティーダービー ゴールドシップ](https://megahobby.jp/products/item/4553/)

```json
{
  "review_id": "R3731",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3732 — ウマ娘 プリティーダービー サイレンススズカ (1개)

상품 ID: 441

- [ウマ娘 プリティーダービー サイレンススズカ](https://megahobby.jp/products/item/4329/)

```json
{
  "review_id": "R3732",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3733 — ウマ娘 プリティーダービー スペシャルウィーク (1개)

상품 ID: 442

- [ウマ娘 プリティーダービー スペシャルウィーク](https://megahobby.jp/products/item/4330/)

```json
{
  "review_id": "R3733",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3734 — ウマ娘 プリティーダービー ダイワスカーレット (1개)

상품 ID: 553

- [ウマ娘 プリティーダービー ダイワスカーレット](https://megahobby.jp/products/item/4552/)

```json
{
  "review_id": "R3734",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3735 — ウマ娘 プリティーダービー トウカイテイオー (1개)

상품 ID: 231

- [ウマ娘 プリティーダービー トウカイテイオー](https://megahobby.jp/products/item/3863/)

```json
{
  "review_id": "R3735",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3736 — ウマ娘 プリティーダービー ミホノブルボン (1개)

상품 ID: 424

- [ウマ娘 プリティーダービー ミホノブルボン](https://megahobby.jp/products/item/4298/)

```json
{
  "review_id": "R3736",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3737 — ウマ娘 プリティーダービー メジロマックイーン (1개)

상품 ID: 232

- [ウマ娘 プリティーダービー メジロマックイーン](https://megahobby.jp/products/item/3864/)

```json
{
  "review_id": "R3737",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3738 — ウマ娘 プリティーダービー ライスシャワー (1개)

상품 ID: 423

- [ウマ娘 プリティーダービー ライスシャワー](https://megahobby.jp/products/item/4297/)

```json
{
  "review_id": "R3738",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3739 — ウルトラセブン （バトルイメージカラーEd.） (1개)

상품 ID: 878

- [ウルトラセブン （バトルイメージカラーEd.）](https://megahobby.jp/products/item/5250/)

```json
{
  "review_id": "R3739",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3740 — ウルトラマンティガ（マルチタイプ） バトルイメージカラーエディション (1개)

상품 ID: 1171

- [ウルトラマンティガ（マルチタイプ） バトルイメージカラーエディション](https://megahobby.jp/products/item/5802/)

```json
{
  "review_id": "R3740",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3741 — カグラバチ 六平千鉱 (1개)

상품 ID: 1160

- [カグラバチ 六平千鉱](https://megahobby.jp/products/item/5765/)

```json
{
  "review_id": "R3741",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3742 — カグラバチ 漣伯理 (1개)

상품 ID: 1159

- [カグラバチ 漣伯理](https://megahobby.jp/products/item/5764/)

```json
{
  "review_id": "R3742",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3743 — カラころーＣlear Candy Figures－ テレビアニメ『春夏秋冬代行者 春の舞』 (1개)

상품 ID: 1219

- [カラころーＣlear Candy Figures－  テレビアニメ『春夏秋冬代行者 春の舞』](https://megahobby.jp/products/item/5854/)

```json
{
  "review_id": "R3743",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3744 — カラころーＣlear Candy Figures－ 僕のヒーローアカデミア (1개)

상품 ID: 1191

- [カラころーＣlear Candy Figures－  僕のヒーローアカデミア](https://megahobby.jp/products/item/5822/)

```json
{
  "review_id": "R3744",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3745 — カラころーＣlearCandyFigures－ 銀魂 (1개)

상품 ID: 1055

- [カラころーＣlearCandyFigures－   銀魂](https://megahobby.jp/products/item/5571/)

```json
{
  "review_id": "R3745",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3746 — カードキャプターさくら 木之本桜 (1개)

상품 ID: 470

- [カードキャプターさくら 木之本桜](https://megahobby.jp/products/item/4377/)

```json
{
  "review_id": "R3746",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3747 — クレヨンしんちゃん (1개)

상품 ID: 940

- [クレヨンしんちゃん](https://megahobby.jp/products/item/5388/)

```json
{
  "review_id": "R3747",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3748 — ケロロ軍曹 ケロロ (1개)

상품 ID: 901

- [ケロロ軍曹 ケロロ](https://megahobby.jp/products/item/5317/)

```json
{
  "review_id": "R3748",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3749 — ケロロ軍曹 タママ (1개)

상품 ID: 902

- [ケロロ軍曹 タママ](https://megahobby.jp/products/item/5318/)

```json
{
  "review_id": "R3749",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3750 — コレクション 3年Z組銀八先生 vol.1 (1개)

상품 ID: 932

- [コレクション  3年Z組銀八先生　vol.1](https://megahobby.jp/products/item/5380/)

```json
{
  "review_id": "R3750",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3751 — コレクション 3年Z組銀八先生 vol.2 (1개)

상품 ID: 1073

- [コレクション  3年Z組銀八先生 vol.2](https://megahobby.jp/products/item/5612/)

```json
{
  "review_id": "R3751",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3752 — コレクション HUNTER×HUNTER (1개)

상품 ID: 1294

- [コレクション  HUNTER×HUNTER](https://megahobby.jp/products/item/6014/)

```json
{
  "review_id": "R3752",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3753 — コレクション NARUTO-ナルト (1개)

상품 ID: 1030

- [コレクション  NARUTO-ナルト-](https://megahobby.jp/products/item/5531/)

```json
{
  "review_id": "R3753",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3754 — コレクション ONE PIECE エッグヘッド編 (1개)

상품 ID: 914

- [コレクション ONE PIECE エッグヘッド編](https://megahobby.jp/products/item/5330/)

```json
{
  "review_id": "R3754",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3755 — コレクション SAKAMOTO DAYS (1개)

상품 ID: 773

- [コレクション SAKAMOTO DAYS](https://megahobby.jp/products/item/4997/)

```json
{
  "review_id": "R3755",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3756 — コレクション TVアニメ『しゅごキャラ！』 (1개)

상품 ID: 1295

- [コレクション  TVアニメ『しゅごキャラ！』](https://megahobby.jp/products/item/6015/)

```json
{
  "review_id": "R3756",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3757 — コレクション WIND BREAKER Vol.2 (1개)

상품 ID: 819

- [コレクション WIND BREAKER Vol.2](https://megahobby.jp/products/item/5155/)

```json
{
  "review_id": "R3757",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3758 — コレクション たまごっち (1개)

상품 ID: 1154

- [コレクション たまごっち](https://megahobby.jp/products/item/5758/)

```json
{
  "review_id": "R3758",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3759 — コレクション チェンソーマン (1개)

상품 ID: 916

- [コレクション チェンソーマン](https://megahobby.jp/products/item/5332/)

```json
{
  "review_id": "R3759",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3760 — コレクション テレビアニメ『春夏秋冬代行者 春の舞』 (1개)

상품 ID: 1189

- [コレクション  テレビアニメ『春夏秋冬代行者 春の舞』](https://megahobby.jp/products/item/5820/)

```json
{
  "review_id": "R3760",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3761 — コレクション ブルーロック vol.2 (1개)

상품 ID: 947

- [コレクション ブルーロック vol.2](https://megahobby.jp/products/item/5395/)

```json
{
  "review_id": "R3761",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3762 — コレクション 僕のヒーローアカデミア (1개)

상품 ID: 860

- [コレクション 僕のヒーローアカデミア ](https://megahobby.jp/products/item/5230/)

```json
{
  "review_id": "R3762",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3763 — コレクション 名探偵コナン (1개)

상품 ID: 1276

- [コレクション  名探偵コナン](https://megahobby.jp/products/item/5963/)

```json
{
  "review_id": "R3763",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3764 — コレクション 呪術廻戦 (1개)

상품 ID: 1328

- [コレクション 呪術廻戦](https://megahobby.jp/products/item/6056/)

```json
{
  "review_id": "R3764",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3765 — コレクション 呪術廻戦 vol.2 (1개)

상품 ID: 789

- [コレクション 呪術廻戦 vol.2【再販】](https://megahobby.jp/products/item/5037/)

```json
{
  "review_id": "R3765",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3766 — コレクション 忍たま乱太郎 Vol.1 (1개)

상품 ID: 1079

- [コレクション 忍たま乱太郎 Vol.1](https://megahobby.jp/products/item/5620/)

```json
{
  "review_id": "R3766",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3767 — コレクション 忍たま乱太郎 Vol.2 (1개)

상품 ID: 1112

- [コレクション 忍たま乱太郎 Vol.2](https://megahobby.jp/products/item/5696/)

```json
{
  "review_id": "R3767",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3768 — コレクション 新テニスの王子様 Vol.1 (1개)

상품 ID: 1223

- [コレクション  新テニスの王子様 Vol.1](https://megahobby.jp/products/item/5858/)

```json
{
  "review_id": "R3768",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3769 — コレクション 新テニスの王子様 Vol.2 (1개)

상품 ID: 1262

- [コレクション  新テニスの王子様 Vol.2](https://megahobby.jp/products/item/5946/)

```json
{
  "review_id": "R3769",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3770 — コレクション 機動戦士Gundam GQuuuuuuX (1개)

상품 ID: 796

- [コレクション  機動戦士Gundam GQuuuuuuX](https://megahobby.jp/products/item/5045/)

```json
{
  "review_id": "R3770",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3771 — コレクション 葬送のフリーレン (1개)

상품 ID: 1360

- [コレクション 葬送のフリーレン](https://megahobby.jp/products/item/6111/)

```json
{
  "review_id": "R3771",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3772 — コレクション 進撃の巨人 (1개)

상품 ID: 1224

- [コレクション  進撃の巨人](https://megahobby.jp/products/item/5859/)

```json
{
  "review_id": "R3772",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3773 — コレクション 銀河特急 ミルキー☆サブウェイ (1개)

상품 ID: 1190

- [コレクション  銀河特急 ミルキー☆サブウェイ](https://megahobby.jp/products/item/5821/)

```json
{
  "review_id": "R3773",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3774 — コレクション 銀魂 vol.2 (1개)

상품 ID: 915

- [コレクション 銀魂 vol.2](https://megahobby.jp/products/item/5331/)

```json
{
  "review_id": "R3774",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3775 — コレクション 鬼滅の刃 (1개)

상품 ID: 859

- [コレクション 鬼滅の刃 ](https://megahobby.jp/products/item/5229/)

```json
{
  "review_id": "R3775",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3776 — コードギアス 反逆のルルーシュ コードギニャス (1개)

상품 ID: 1226

- [コードギアス 反逆のルルーシュ コードギニャス](https://megahobby.jp/products/item/5861/)

```json
{
  "review_id": "R3776",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3777 — コードギアス 反逆のルルーシュ ルルーシュ・ランペルージ (1개)

상품 ID: 983

- [コードギアス 反逆のルルーシュ ルルーシュ・ランペルージ](https://megahobby.jp/products/item/5435/)

```json
{
  "review_id": "R3777",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3778 — コードギアス 反逆のルルーシュ 枢木スザク (1개)

상품 ID: 982

- [コードギアス 反逆のルルーシュ 枢木スザク](https://megahobby.jp/products/item/5434/)

```json
{
  "review_id": "R3778",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3779 — ゴジラ(1962)富士山麓決戦Ver.【ゴジラ・ストア限定】 (1개)

상품 ID: 993

- [ゴジラ(1962)富士山麓決戦Ver.【ゴジラ・ストア限定】](https://megahobby.jp/products/item/5450/)

```json
{
  "review_id": "R3779",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3780 — ゴジラ(2023) 海神作戦時イメージカラーVer. (1개)

상품 ID: 709

- [ゴジラ(2023) 海神作戦時イメージカラーVer.](https://megahobby.jp/products/item/4869/)

```json
{
  "review_id": "R3780",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3781 — サンリオキャラクターズ ハニーキャンディ (1개)

상품 ID: 975

- [サンリオキャラクターズ ハニーキャンディ](https://megahobby.jp/products/item/5425/)

```json
{
  "review_id": "R3781",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3782 — シリーズ ドラゴンボールZ コレクション01 (1개)

상품 ID: 1332

- [シリーズ ドラゴンボールZ コレクション01](https://megahobby.jp/products/item/6060/)

```json
{
  "review_id": "R3782",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3783 — シリーズ ワンピース グランドラインコレクションVol.2 (1개)

상품 ID: 1003

- [シリーズ ワンピース グランドラインコレクションVol.2【再販】](https://megahobby.jp/products/item/5482/)

```json
{
  "review_id": "R3783",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3784 — ジョジョの奇妙な冒険 ストーンオーシャン S・F (1개)

상품 ID: 312

- [ジョジョの奇妙な冒険 ストーンオーシャン S・F](https://megahobby.jp/products/item/4066/)

```json
{
  "review_id": "R3784",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3785 — ジョジョの奇妙な冒険 ストーンオーシャン 空条徐倫 (1개)

상품 ID: 313

- [ジョジョの奇妙な冒険 ストーンオーシャン 空条徐倫](https://megahobby.jp/products/item/4067/)

```json
{
  "review_id": "R3785",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3786 — スピリテイル (1개)

상품 ID: 4865

- [ブラック★★ロックシューター DAWN FALL エンプレス【ブラックロックシューター】～ティザービジュアル ver. (Art by huke)～ スケールフィギュア【完全受注生産】](https://taito-goods.jp/shop/g/g50101270/)

```json
{
  "review_id": "R3786",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3787 — スンスンと一緒Tシャツ ブラック (1개)

상품 ID: 4949

- [パペットスンスン　スンスンと一緒Tシャツ ブラック](https://taito-goods.jp/shop/g/g70101250/)

```json
{
  "review_id": "R3787",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3788 — スンスンと一緒Tシャツ ホワイト (1개)

상품 ID: 4948

- [パペットスンスン　スンスンと一緒Tシャツ ホワイト](https://taito-goods.jp/shop/g/g70101240/)

```json
{
  "review_id": "R3788",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3789 — ダンガンロンパ 希望の学園と絶望の高校生 江ノ島盾子 (1개)

상품 ID: 6150

- [ダンガンロンパ 希望の学園と絶望の高校生 江ノ島盾子](https://megahobby.jp/products/item/6187/)

```json
{
  "review_id": "R3789",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3790 — ダンガンロンパ 希望の学園と絶望の高校生 苗木誠 (1개)

상품 ID: 6149

- [ダンガンロンパ 希望の学園と絶望の高校生 苗木誠](https://megahobby.jp/products/item/6188/)

```json
{
  "review_id": "R3790",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3791 — ダンジョン飯 てのひら マルシル (1개)

상품 ID: 651

- [ ダンジョン飯 てのひら マルシル](https://megahobby.jp/products/item/4742/)

```json
{
  "review_id": "R3791",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3792 — チェンソーマン デンジ (1개)

상품 ID: 219

- [チェンソーマン デンジ](https://megahobby.jp/products/item/3846/)

```json
{
  "review_id": "R3792",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3793 — チェンソーマン 早川アキ (1개)

상품 ID: 226

- [チェンソーマン 早川アキ](https://megahobby.jp/products/item/3858/)

```json
{
  "review_id": "R3793",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3794 — チャーム・パティスリー 星のカービィ カービィのクッキータイム (1개)

상품 ID: 125

- [チャーム・パティスリー 星のカービィ カービィのクッキータイム【再販】](https://megahobby.jp/products/item/3025/)

```json
{
  "review_id": "R3794",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3795 — デジコレ！MIX (1개)

상품 ID: 133

- [デジコレ！MIX【再販】](https://megahobby.jp/products/item/3539/)

```json
{
  "review_id": "R3795",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3796 — デジモンアドベンチャー (1개)

상품 ID: 1109

- [デジモンアドベンチャー](https://megahobby.jp/products/item/5692/)

```json
{
  "review_id": "R3796",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3797 — デジモンアドベンチャー アグモン (1개)

상품 ID: 434

- [デジモンアドベンチャー アグモン【再販】](https://megahobby.jp/products/item/4309/)

```json
{
  "review_id": "R3797",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3798 — デジモンアドベンチャー テイルモン (1개)

상품 ID: 430

- [デジモンアドベンチャー テイルモン【再販】](https://megahobby.jp/products/item/4305/)

```json
{
  "review_id": "R3798",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3799 — デジモンアドベンチャー テントモン (1개)

상품 ID: 612

- [デジモンアドベンチャー テントモン](https://megahobby.jp/products/item/4668/)

```json
{
  "review_id": "R3799",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3800 — デジモンアドベンチャー パルモン (1개)

상품 ID: 611

- [デジモンアドベンチャー パルモン](https://megahobby.jp/products/item/4667/)

```json
{
  "review_id": "R3800",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3801 — ドラゴンボール 06 孫悟空＆ブルマ -限定復刻仕様版 (1개)

상품 ID: 1319

- [ドラゴンボール 06 孫悟空＆ブルマ -限定復刻仕様版-](https://megahobby.jp/products/item/6039/)

```json
{
  "review_id": "R3801",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3802 — ドラゴンボールDAIMA ベジータ(ミニ) (1개)

상품 ID: 723

- [ドラゴンボールDAIMA ベジータ(ミニ)](https://megahobby.jp/products/item/4903/)

```json
{
  "review_id": "R3802",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3803 — ドラゴンボールDAIMA 孫悟空(ミニ) (1개)

상품 ID: 724

- [ドラゴンボールDAIMA 孫悟空(ミニ)](https://megahobby.jp/products/item/4909/)

```json
{
  "review_id": "R3803",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3804 — ドラゴンボールDAIMA 超サイヤ人 ベジータ(ミニ) (1개)

상품 ID: 1234

- [ドラゴンボールDAIMA 超サイヤ人 ベジータ(ミニ)](https://megahobby.jp/products/item/5869/)

```json
{
  "review_id": "R3804",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3805 — ドラゴンボールDAIMA 超サイヤ人 孫悟空(ミニ) (1개)

상품 ID: 1235

- [ドラゴンボールDAIMA 超サイヤ人 孫悟空(ミニ)](https://megahobby.jp/products/item/5870/)

```json
{
  "review_id": "R3805",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3806 — ドラゴンボールZ 03 ブルマ -限定復刻仕様版 (1개)

상품 ID: 898

- [ドラゴンボールZ 03 ブルマ -限定復刻仕様版-](https://megahobby.jp/products/item/5314/)

```json
{
  "review_id": "R3806",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3807 — ドラゴンボールZ 05 孫悟空＆チチ -限定復刻仕様版 (1개)

상품 ID: 1161

- [ドラゴンボールZ 05 孫悟空＆チチ -限定復刻仕様版-](https://megahobby.jp/products/item/5766/)

```json
{
  "review_id": "R3807",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3808 — ドラゴンボールZ 孫悟空 01 -限定復刻仕様版 (1개)

상품 ID: 1033

- [ドラゴンボールZ 孫悟空 01 -限定復刻仕様版-](https://megahobby.jp/products/item/5534/)

```json
{
  "review_id": "R3808",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3809 — ナルト＆サスケ 2023 Limited ver. (1개)

상품 ID: 333

- [ナルト＆サスケ 2023 Limited ver.](https://megahobby.jp/products/item/4111/)

```json
{
  "review_id": "R3809",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3810 — ニャオハ (1개)

상품 ID: 642

- [ニャオハ](https://megahobby.jp/products/item/4729/)

```json
{
  "review_id": "R3810",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3811 — ハイキュ―!! てのひら宮 侑 (1개)

상품 ID: 783

- [ハイキュ―!! てのひら宮 侑](https://megahobby.jp/products/item/5007/)

```json
{
  "review_id": "R3811",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3812 — ハイキュ―!! てのひら宮 治 (1개)

상품 ID: 782

- [ハイキュ―!! てのひら宮 治](https://megahobby.jp/products/item/5006/)

```json
{
  "review_id": "R3812",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3813 — ハイキュ―!! てのひら日向翔陽 (1개)

상품 ID: 602

- [ハイキュ―!! てのひら日向翔陽【再販】](https://megahobby.jp/products/item/4658/)

```json
{
  "review_id": "R3813",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3814 — ハイキュ―!! てのひら月島蛍 (1개)

상품 ID: 758

- [ハイキュ―!! てのひら月島蛍](https://megahobby.jp/products/item/4976/)

```json
{
  "review_id": "R3814",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3815 — ハイキュ―!! 北 信介 ユニフォームVer. (1개)

상품 ID: 754

- [ハイキュ―!! 北 信介 ユニフォームVer.](https://megahobby.jp/products/item/4972/)

```json
{
  "review_id": "R3815",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3816 — ハイキュ―!! 孤爪 研磨 ユニフォームVer. (1개)

상품 ID: 1212

- [ハイキュ―!! 孤爪 研磨　ユニフォームVer.【再販】](https://megahobby.jp/products/item/5846/)

```json
{
  "review_id": "R3816",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3817 — ハイキュ―!! 宮侑 (1개)

상품 ID: 300

- [ハイキュ―!! 宮侑](https://megahobby.jp/products/item/4030/)

```json
{
  "review_id": "R3817",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3818 — ハイキュ―!! 宮 侑 ユニフォームVer. (1개)

상품 ID: 634

- [ハイキュ―!! 宮 侑 ユニフォームVer.](https://megahobby.jp/products/item/4692/)

```json
{
  "review_id": "R3818",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3819 — ハイキュ―!! 宮治 (1개)

상품 ID: 299

- [ハイキュ―!! 宮治](https://megahobby.jp/products/item/4029/)

```json
{
  "review_id": "R3819",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3820 — ハイキュ―!! 宮 治 ユニフォームVer. (1개)

상품 ID: 633

- [ハイキュ―!! 宮 治 ユニフォームVer.](https://megahobby.jp/products/item/4691/)

```json
{
  "review_id": "R3820",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3821 — ハイキュ―!! 岩泉 一 ユニフォームVer. (1개)

상품 ID: 615

- [ハイキュ―!! 岩泉 一 ユニフォームVer.](https://megahobby.jp/products/item/4671/)

```json
{
  "review_id": "R3821",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3822 — ハイキュ―!! 日向翔陽 (1개)

상품 ID: 763

- [ハイキュ―!! 日向翔陽【再販】](https://megahobby.jp/products/item/4986/)

```json
{
  "review_id": "R3822",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3823 — ハイキュ―!! 月島 蛍 ユニフォームVer. (1개)

상품 ID: 529

- [ハイキュ―!! 月島 蛍 ユニフォームVer.](https://megahobby.jp/products/item/4507/)

```json
{
  "review_id": "R3823",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3824 — ハイキュ―!! 木兎光太郎 ユニフォームVer. (1개)

상품 ID: 690

- [ハイキュ―!! 木兎光太郎 ユニフォームVer.](https://megahobby.jp/products/item/4832/)

```json
{
  "review_id": "R3824",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3825 — ハイキュ―!! 東峰 旭 (1개)

상품 ID: 1242

- [ハイキュ―!! 東峰 旭](https://megahobby.jp/products/item/5877/)

```json
{
  "review_id": "R3825",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3826 — ハイキュ―!! 澤村大地 (1개)

상품 ID: 1183

- [ハイキュ―!! 澤村大地](https://megahobby.jp/products/item/5814/)

```json
{
  "review_id": "R3826",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3827 — ハイキュ―!! 田中龍之介 ユニフォームVer. (1개)

상품 ID: 719

- [ハイキュ―!! 田中龍之介 ユニフォームVer.](https://megahobby.jp/products/item/4899/)

```json
{
  "review_id": "R3827",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3828 — ハイキュ―!! 菅原孝支 (1개)

상품 ID: 1184

- [ハイキュ―!! 菅原孝支](https://megahobby.jp/products/item/5815/)

```json
{
  "review_id": "R3828",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3829 — ハイキュ―!! 西谷 夕 (1개)

상품 ID: 1243

- [ハイキュ―!! 西谷 夕](https://megahobby.jp/products/item/5878/)

```json
{
  "review_id": "R3829",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3830 — ハイキュ―!! 西谷 夕 ユニフォームVer. (1개)

상품 ID: 720

- [ハイキュ―!! 西谷 夕 ユニフォームVer.](https://megahobby.jp/products/item/4900/)

```json
{
  "review_id": "R3830",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3831 — ハイキュ―!! 角名倫太郎 ユニフォームVer. (1개)

상품 ID: 753

- [ハイキュ―!! 角名倫太郎 ユニフォームVer.](https://megahobby.jp/products/item/4971/)

```json
{
  "review_id": "R3831",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3832 — ハイキュ―!! 赤葦京治 ユニフォームVer. (1개)

상품 ID: 689

- [ハイキュ―!! 赤葦京治 ユニフォームVer.](https://megahobby.jp/products/item/4831/)

```json
{
  "review_id": "R3832",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3833 — ハイキュ―!! 黒尾 鉄朗 ユニフォームVer. (1개)

상품 ID: 1213

- [ハイキュ―!! 黒尾 鉄朗　ユニフォームVer.【再販】](https://megahobby.jp/products/item/5847/)

```json
{
  "review_id": "R3833",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3834 — ハイキュー‼ てのひら及川 徹 (1개)

상품 ID: 564

- [ハイキュー‼ てのひら及川 徹](https://megahobby.jp/products/item/4563/)

```json
{
  "review_id": "R3834",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3835 — ハイキュー‼ てのひら孤爪 研磨 (1개)

상품 ID: 515

- [ハイキュー‼ てのひら孤爪 研磨](https://megahobby.jp/products/item/4479/)

```json
{
  "review_id": "R3835",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3836 — ハイキュー‼ てのひら影山飛雄 セカンドユニフォームver. (1개)

상품 ID: 900

- [ハイキュー‼ てのひら影山飛雄 セカンドユニフォームver.](https://megahobby.jp/products/item/5316/)

```json
{
  "review_id": "R3836",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3837 — ハイキュー!! てのひら日向翔陽 (1개)

상품 ID: 326

- [ハイキュー!! てのひら日向翔陽](https://megahobby.jp/products/item/4080/)

```json
{
  "review_id": "R3837",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3838 — ハイキュー‼ てのひら日向翔陽 セカンドユニフォームver. (1개)

상품 ID: 899

- [ハイキュー‼ てのひら日向翔陽 セカンドユニフォームver.](https://megahobby.jp/products/item/5315/)

```json
{
  "review_id": "R3838",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3839 — ハイキュー‼ てのひら黒尾鉄朗 (1개)

상품 ID: 535

- [ハイキュー‼ てのひら黒尾鉄朗](https://megahobby.jp/products/item/4513/)

```json
{
  "review_id": "R3839",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3840 — ハイキュー!! 孤爪 研磨 ユニフォームVer. (1개)

상품 ID: 558

- [ハイキュー!! 孤爪 研磨 ユニフォームVer.](https://megahobby.jp/products/item/4557/)

```json
{
  "review_id": "R3840",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3841 — ハイキュー!! 宮 侑 (1개)

상품 ID: 1002

- [ハイキュー!! 宮 侑【再販】](https://megahobby.jp/products/item/5481/)

```json
{
  "review_id": "R3841",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3842 — ハイキュー!! 宮 治 (1개)

상품 ID: 1001

- [ハイキュー!! 宮 治【再販】](https://megahobby.jp/products/item/5480/)

```json
{
  "review_id": "R3842",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3843 — ハイキュー!! 山口 忠 (1개)

상품 ID: 952

- [ハイキュー!! 山口 忠](https://megahobby.jp/products/item/5400/)

```json
{
  "review_id": "R3843",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3844 — ハイキュー!! 日向翔陽 (1개)

상품 ID: 189

- [ハイキュー!!  日向翔陽](https://megahobby.jp/products/item/3747/)

```json
{
  "review_id": "R3844",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3845 — ハイキュー!! 月島 蛍 (1개)

상품 ID: 953

- [ハイキュー!! 月島 蛍](https://megahobby.jp/products/item/5401/)

```json
{
  "review_id": "R3845",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3846 — ハイキュー‼ 頂のブレイクタイム! (1개)

상품 ID: 1080

- [ハイキュー‼ 頂のブレイクタイム!](https://megahobby.jp/products/item/5621/)

```json
{
  "review_id": "R3846",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3847 — ハイキュー!! 黒尾 鉄朗 ユニフォームVer. (1개)

상품 ID: 557

- [ハイキュー!! 黒尾 鉄朗 ユニフォームVer.](https://megahobby.jp/products/item/4556/)

```json
{
  "review_id": "R3847",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3848 — ハリー・ポッター ハリー・ポッター (1개)

상품 ID: 340

- [ハリー・ポッター ハリー・ポッター](https://megahobby.jp/products/item/4119/)

```json
{
  "review_id": "R3848",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3849 — ハリー・ポッター ハーマイオニー・グレンジャー (1개)

상품 ID: 339

- [ハリー・ポッター ハーマイオニー・グレンジャー](https://megahobby.jp/products/item/4118/)

```json
{
  "review_id": "R3849",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3850 — バリエーションズ 新世紀GPXサイバーフォーミュラ アスラーダV.S.X-R (1개)

상품 ID: 743

- [バリエーションズ 新世紀GPXサイバーフォーミュラ アスラーダV.S.X-R](https://megahobby.jp/products/item/4948/)

```json
{
  "review_id": "R3850",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3851 — バリエーションズ 新世紀GPXサイバーフォーミュラ ヴィジョンアスラーダ (1개)

상품 ID: 256

- [バリエーションズ 新世紀GPXサイバーフォーミュラ ヴィジョンアスラーダ](https://megahobby.jp/products/item/3925/)

```json
{
  "review_id": "R3851",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3852 — パックマン (1개)

상품 ID: 1260

- [パックマン](https://megahobby.jp/products/item/5944/)

```json
{
  "review_id": "R3852",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3853 — パン SPY×FAMILY (1개)

상품 ID: 168

- [パン  SPY×FAMILY](https://megahobby.jp/products/item/3694/)

```json
{
  "review_id": "R3853",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3854 — パン 僕のヒーローアカデミア (1개)

상품 ID: 380

- [パン  僕のヒーローアカデミア](https://megahobby.jp/products/item/4190/)

```json
{
  "review_id": "R3854",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3855 — ピカチュウ (1개)

상품 ID: 643

- [ピカチュウ](https://megahobby.jp/products/item/4730/)

```json
{
  "review_id": "R3855",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3856 — ファンタスティック・ビースト ジェイコブ・コワルスキー (1개)

상품 ID: 435

- [ファンタスティック・ビースト ジェイコブ・コワルスキー](https://megahobby.jp/products/item/4310/)

```json
{
  "review_id": "R3856",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3857 — ファンタスティック・ビースト ニュート・スキャマンダー (1개)

상품 ID: 436

- [ファンタスティック・ビースト ニュート・スキャマンダー](https://megahobby.jp/products/item/4311/)

```json
{
  "review_id": "R3857",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3858 — ブルーアーカイブ シロコ (1개)

상품 ID: 801

- [ブルーアーカイブ シロコ](https://megahobby.jp/products/item/5050/)

```json
{
  "review_id": "R3858",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3859 — ブルーアーカイブ ホシノ (1개)

상품 ID: 800

- [ブルーアーカイブ ホシノ](https://megahobby.jp/products/item/5049/)

```json
{
  "review_id": "R3859",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3860 — ブルーロック (1개)

상품 ID: 697

- [  ブルーロック](https://megahobby.jp/products/item/4856/)

```json
{
  "review_id": "R3860",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3861 — ブルーロック てのひら凪 誠士郎 Repaint Ver. (1개)

상품 ID: 830

- [ブルーロック てのひら凪 誠士郎 Repaint Ver.](https://megahobby.jp/products/item/5167/)

```json
{
  "review_id": "R3861",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3862 — ブルーロック てのひら御影 玲王 (1개)

상품 ID: 831

- [ブルーロック てのひら御影 玲王](https://megahobby.jp/products/item/5168/)

```json
{
  "review_id": "R3862",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3863 — ブルーロック てのひら潔 世一 (1개)

상품 ID: 809

- [ブルーロック てのひら潔 世一](https://megahobby.jp/products/item/5058/)

```json
{
  "review_id": "R3863",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3864 — ブルーロック てのひら糸師 凛 (1개)

상품 ID: 808

- [ブルーロック てのひら糸師 凛](https://megahobby.jp/products/item/5057/)

```json
{
  "review_id": "R3864",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3865 — ブルーロック 凪 誠士郎 ver.2 (1개)

상품 ID: 505

- [ブルーロック 凪 誠士郎 ver.2](https://megahobby.jp/products/item/4469/)

```json
{
  "review_id": "R3865",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3866 — ブルーロック 凪 誠士郎 日本代表戦ver. (1개)

상품 ID: 751

- [ブルーロック 凪 誠士郎 日本代表戦ver.](https://megahobby.jp/products/item/4969/)

```json
{
  "review_id": "R3866",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3867 — ブルーロック 千切豹馬 二次選考ver. (1개)

상품 ID: 700

- [ブルーロック 千切豹馬 二次選考ver.](https://megahobby.jp/products/item/4859/)

```json
{
  "review_id": "R3867",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3868 — ブルーロック 國神錬介 二次選考ver. (1개)

상품 ID: 701

- [ブルーロック 國神錬介 二次選考ver.](https://megahobby.jp/products/item/4860/)

```json
{
  "review_id": "R3868",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3869 — ブルーロック 御影玲王 (1개)

상품 ID: 506

- [ブルーロック 御影玲王](https://megahobby.jp/products/item/4470/)

```json
{
  "review_id": "R3869",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3870 — ブルーロック 御影玲王 日本代表戦ver. (1개)

상품 ID: 797

- [ブルーロック 御影玲王 日本代表戦ver.](https://megahobby.jp/products/item/5046/)

```json
{
  "review_id": "R3870",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3871 — ブルーロック 氷織 羊 (1개)

상품 ID: 775

- [ブルーロック 氷織 羊](https://megahobby.jp/products/item/4999/)

```json
{
  "review_id": "R3871",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3872 — ブルーロック 潔 世一 日本代表戦ver. (1개)

상품 ID: 752

- [ブルーロック 潔 世一 日本代表戦ver.](https://megahobby.jp/products/item/4970/)

```json
{
  "review_id": "R3872",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3873 — ブルーロック 烏 旅人 (1개)

상품 ID: 774

- [ブルーロック 烏 旅人](https://megahobby.jp/products/item/4998/)

```json
{
  "review_id": "R3873",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3874 — ブルーロック 糸師 冴 日本代表戦ver. (1개)

상품 ID: 739

- [ブルーロック 糸師 冴 日本代表戦ver.](https://megahobby.jp/products/item/4944/)

```json
{
  "review_id": "R3874",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3875 — ブルーロック 糸師 凛 (1개)

상품 ID: 528

- [ブルーロック 糸師 凛](https://megahobby.jp/products/item/4506/)

```json
{
  "review_id": "R3875",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3876 — ブルーロック 糸師 凛 日本代表戦ver. (1개)

상품 ID: 740

- [ブルーロック 糸師 凛 日本代表戦ver.](https://megahobby.jp/products/item/4945/)

```json
{
  "review_id": "R3876",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3877 — プチラマEX ゴジラ 01 (1개)

상품 ID: 1259

- [プチラマEX ゴジラ 01](https://megahobby.jp/products/item/5943/)

```json
{
  "review_id": "R3877",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3878 — プチラマEX ゴジラー1.0 ゼロからマイナス1 (1개)

상품 ID: 925

- [プチラマEX ゴジラー1.0 ゼロからマイナス1 【再販】](https://megahobby.jp/products/item/5341/)

```json
{
  "review_id": "R3878",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3879 — ヘドラ (1개)

상품 ID: 1298

- [ヘドラ](https://megahobby.jp/products/item/6018/)

```json
{
  "review_id": "R3879",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3880 — ペルソナ３ リロード アイギス (1개)

상품 ID: 1279

- [ペルソナ３ リロード アイギス](https://megahobby.jp/products/item/5966/)

```json
{
  "review_id": "R3880",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3881 — ペルソナ３ リロード 主人公 (1개)

상품 ID: 1280

- [ペルソナ３ リロード 主人公](https://megahobby.jp/products/item/5967/)

```json
{
  "review_id": "R3881",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3882 — ペルソナ5 ザ・ロイヤル モルガナ (1개)

상품 ID: 1309

- [ペルソナ5 ザ・ロイヤル モルガナ](https://megahobby.jp/products/item/6029/)

```json
{
  "review_id": "R3882",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3883 — ペルソナ5 ザ・ロイヤル 主人公 (1개)

상품 ID: 1310

- [ペルソナ5 ザ・ロイヤル 主人公](https://megahobby.jp/products/item/6030/)

```json
{
  "review_id": "R3883",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3884 — ペルソナ5 ザ・ロイヤル 明智吾郎 (1개)

상품 ID: 1339

- [ペルソナ5 ザ・ロイヤル 明智吾郎](https://megahobby.jp/products/item/6067/)

```json
{
  "review_id": "R3884",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3885 — ペルソナ5 ザ・ロイヤル 芳澤かすみ (1개)

상품 ID: 1338

- [ペルソナ5 ザ・ロイヤル 芳澤かすみ](https://megahobby.jp/products/item/6066/)

```json
{
  "review_id": "R3885",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3886 — ホロライブ 戌神ころね (1개)

상품 ID: 347

- [ホロライブ 戌神ころね](https://megahobby.jp/products/item/4126/)

```json
{
  "review_id": "R3886",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3887 — ホロライブ 猫又おかゆ (1개)

상품 ID: 348

- [ホロライブ 猫又おかゆ](https://megahobby.jp/products/item/4127/)

```json
{
  "review_id": "R3887",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3888 — ポケットモンスター ディアルガ&amp;パルキア (1개)

상품 ID: 155

- [ポケットモンスター ディアルガ&amp;パルキア](https://megahobby.jp/products/item/3662/)

```json
{
  "review_id": "R3888",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3889 — ポケットモンスター メガリザードンＸ＆メガリザードンＹ (1개)

상품 ID: 1021

- [ポケットモンスター メガリザードンＸ＆メガリザードンＹ](https://megahobby.jp/products/item/5500/)

```json
{
  "review_id": "R3889",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3890 — ポッチャマ (1개)

상품 ID: 644

- [ポッチャマ](https://megahobby.jp/products/item/4731/)

```json
{
  "review_id": "R3890",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3891 — ポンチョ NARUTO-ナルト- 疾風伝 パックン (1개)

상품 ID: 1300

- [ポンチョ NARUTO-ナルト- 疾風伝 パックン](https://megahobby.jp/products/item/6020/)

```json
{
  "review_id": "R3891",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3892 — ポンチョ NARUTO-ナルト- 疾風伝 九喇嘛 (1개)

상품 ID: 1301

- [ポンチョ NARUTO-ナルト- 疾風伝 九喇嘛](https://megahobby.jp/products/item/6021/)

```json
{
  "review_id": "R3892",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3893 — ポンチョ アニメ『呪術廻戦』 5周年 乙骨憂太 劇場版 呪術廻戦 0 (1개)

상품 ID: 1186

- [ポンチョ アニメ『呪術廻戦』 5周年 乙骨憂太 劇場版 呪術廻戦 0](https://megahobby.jp/products/item/5817/)

```json
{
  "review_id": "R3893",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3894 — ポンチョ アニメ『呪術廻戦』 5周年 五条悟 (1개)

상품 ID: 1228

- [ポンチョ アニメ『呪術廻戦』 5周年 五条悟](https://megahobby.jp/products/item/5863/)

```json
{
  "review_id": "R3894",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3895 — ポンチョ アニメ『呪術廻戦』 5周年 五条悟 高専ver. (1개)

상품 ID: 1132

- [ポンチョ アニメ『呪術廻戦』 5周年 五条悟 高専ver. ](https://megahobby.jp/products/item/5719/)

```json
{
  "review_id": "R3895",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3896 — ポンチョ アニメ『呪術廻戦』 5周年 伏黒恵 (1개)

상품 ID: 1230

- [ポンチョ アニメ『呪術廻戦』 5周年 伏黒恵](https://megahobby.jp/products/item/5865/)

```json
{
  "review_id": "R3896",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3897 — ポンチョ アニメ『呪術廻戦』 5周年 夏油傑 高専ver. (1개)

상품 ID: 1133

- [ポンチョ アニメ『呪術廻戦』 5周年 夏油傑 高専ver.](https://megahobby.jp/products/item/5721/)

```json
{
  "review_id": "R3897",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3898 — ポンチョ アニメ『呪術廻戦』 5周年 狗巻棘 劇場版 呪術廻戦 0 (1개)

상품 ID: 1187

- [ポンチョ アニメ『呪術廻戦』 5周年 狗巻棘 劇場版 呪術廻戦 0](https://megahobby.jp/products/item/5818/)

```json
{
  "review_id": "R3898",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3899 — ポンチョ アニメ『呪術廻戦』 5周年 虎杖悠仁 (1개)

상품 ID: 1231

- [ポンチョ アニメ『呪術廻戦』 5周年 虎杖悠仁](https://megahobby.jp/products/item/5866/)

```json
{
  "review_id": "R3899",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3900 — ポンチョ アニメ『呪術廻戦』 5周年 釘崎野薔薇 (1개)

상품 ID: 1229

- [ポンチョ アニメ『呪術廻戦』 5周年 釘崎野薔薇](https://megahobby.jp/products/item/5864/)

```json
{
  "review_id": "R3900",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3901 — ポンチョ ハイキュー!! アカアシフクロウ (1개)

상품 ID: 1058

- [ポンチョ  ハイキュー!!  アカアシフクロウ](https://megahobby.jp/products/item/5576/)

```json
{
  "review_id": "R3901",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3902 — ポンチョ ハイキュー!! サムキツネ (1개)

상품 ID: 1010

- [ポンチョ ハイキュー!! サムキツネ](https://megahobby.jp/products/item/5489/)

```json
{
  "review_id": "R3902",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3903 — ポンチョ ハイキュー!! ツキガラス (1개)

상품 ID: 951

- [ポンチョ ハイキュー!! ツキガラス](https://megahobby.jp/products/item/5399/)

```json
{
  "review_id": "R3903",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3904 — ポンチョ ハイキュー!! ツムキツネ (1개)

상품 ID: 1011

- [ポンチョ ハイキュー!! ツムキツネ](https://megahobby.jp/products/item/5490/)

```json
{
  "review_id": "R3904",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3905 — ポンチョ ハイキュー!! ボクトフクロウ (1개)

상품 ID: 1059

- [ポンチョ  ハイキュー!!  ボクトフクロウ](https://megahobby.jp/products/item/5577/)

```json
{
  "review_id": "R3905",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3906 — ポンチョ ハイキュー!! ヤマグチガラス (1개)

상품 ID: 950

- [ポンチョ ハイキュー!! ヤマグチガラス](https://megahobby.jp/products/item/5398/)

```json
{
  "review_id": "R3906",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3907 — ポンチョ 僕のヒーローアカデミア デクシープ (1개)

상품 ID: 1267

- [ポンチョ 僕のヒーローアカデミア デクシープ](https://megahobby.jp/products/item/5951/)

```json
{
  "review_id": "R3907",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3908 — ポンチョ 僕のヒーローアカデミア バクドッグ (1개)

상품 ID: 1266

- [ポンチョ 僕のヒーローアカデミア バクドッグ](https://megahobby.jp/products/item/5950/)

```json
{
  "review_id": "R3908",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3909 — ポンチョ 銀魂 エリザベス (1개)

상품 ID: 1117

- [ポンチョ 銀魂 エリザベス](https://megahobby.jp/products/item/5701/)

```json
{
  "review_id": "R3909",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3910 — マシンビルド シリーズ マシンロボ クロノスの大逆襲 バトルロボ (1개)

상품 ID: 426

- [マシンビルド　シリーズ  マシンロボ　クロノスの大逆襲  バトルロボ](https://megahobby.jp/products/item/4301/)

```json
{
  "review_id": "R3910",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3911 — マシンビルドシリーズ マシンロボ クロノスの大逆襲 ブルージェット (1개)

상품 ID: 259

- [マシンビルドシリーズ　マシンロボ　クロノスの大逆襲　ブルージェット](https://megahobby.jp/products/item/3946/)

```json
{
  "review_id": "R3911",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3912 — マシンビルドシリーズ マシンロボ クロノスの大逆襲 ロッドドリル (1개)

상품 ID: 194

- [マシンビルドシリーズ　 マシンロボ　クロノスの大逆襲　 ロッドドリル](https://megahobby.jp/products/item/3753/)

```json
{
  "review_id": "R3912",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3913 — マシンビルド 機動戦士ガンダム スキウレ (1개)

상품 ID: 404

- [マシンビルド 機動戦士ガンダム スキウレ](https://megahobby.jp/products/item/4259/)

```json
{
  "review_id": "R3913",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3914 — マシンビルド 機動戦士ガンダム 逆襲のシャア α・アジール (1개)

상품 ID: 625

- [マシンビルド 機動戦士ガンダム 逆襲のシャア α・アジール](https://megahobby.jp/products/item/4682/)

```json
{
  "review_id": "R3914",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3915 — マシンビルド 機動武闘伝Gガンダム ブッドキャリアー (1개)

상품 ID: 666

- [マシンビルド 機動武闘伝Gガンダム ブッドキャリアー](https://megahobby.jp/products/item/4788/)

```json
{
  "review_id": "R3915",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3916 — マスコット HUNTER×HUNTER(再販) (1개)

상품 ID: 257

- [マスコット HUNTER×HUNTER(再販)](https://megahobby.jp/products/item/3944/)

```json
{
  "review_id": "R3916",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3917 — マスコット NARUTO-ナルト- 疾風伝 (1개)

상품 ID: 274

- [マスコット NARUTO-ナルト- 疾風伝【再販】](https://megahobby.jp/products/item/3987/)

```json
{
  "review_id": "R3917",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3918 — マスコット NARUTO-ナルト- 疾風伝 vol.2 (1개)

상품 ID: 478

- [マスコット NARUTO-ナルト- 疾風伝 vol.2【再販】](https://megahobby.jp/products/item/4400/)

```json
{
  "review_id": "R3918",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3919 — マスコット NARUTO-ナルト- 疾風伝 vol.3 (1개)

상품 ID: 152

- [マスコット NARUTO-ナルト- 疾風伝 vol.3](https://megahobby.jp/products/item/3658/)

```json
{
  "review_id": "R3919",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3920 — マスコット NARUTO-ナルト- 疾風伝 vol.4 (1개)

상품 ID: 409

- [マスコット NARUTO-ナルト- 疾風伝 vol.4](https://megahobby.jp/products/item/4264/)

```json
{
  "review_id": "R3920",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3921 — マスコット ONE PIECE ワノ国編 (1개)

상품 ID: 204

- [マスコット ONE PIECE ワノ国編](https://megahobby.jp/products/item/3792/)

```json
{
  "review_id": "R3921",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3922 — マスコット SPY×FAMILY (1개)

상품 ID: 157

- [マスコット SPY×FAMILY](https://megahobby.jp/products/item/3665/)

```json
{
  "review_id": "R3922",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3923 — マスコット TVアニメ『ダンダダン』 (1개)

상품 ID: 686

- [マスコット TVアニメ『ダンダダン』](https://megahobby.jp/products/item/4828/)

```json
{
  "review_id": "R3923",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3924 — マスコット WIND BREAKER (1개)

상품 ID: 548

- [マスコット WIND BREAKER](https://megahobby.jp/products/item/4547/)

```json
{
  "review_id": "R3924",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3925 — マスコット 『機動戦士ガンダム 水星の魔女』 (1개)

상품 ID: 301

- [マスコット 『機動戦士ガンダム 水星の魔女』](https://megahobby.jp/products/item/4031/)

```json
{
  "review_id": "R3925",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3926 — マスコット 【推しの子】 (1개)

상품 ID: 321

- [マスコット 【推しの子】](https://megahobby.jp/products/item/4075/)

```json
{
  "review_id": "R3926",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3927 — マスコット お昼のショッカーさん (1개)

상품 ID: 236

- [マスコット お昼のショッカーさん](https://megahobby.jp/products/item/3886/)

```json
{
  "review_id": "R3927",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3928 — マスコット チェンソーマン (1개)

상품 ID: 221

- [マスコット チェンソーマン](https://megahobby.jp/products/item/3848/)

```json
{
  "review_id": "R3928",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3929 — マスコット ハイキュー!! vol.3 (1개)

상품 ID: 428

- [マスコット ハイキュー!! vol.3](https://megahobby.jp/products/item/4303/)

```json
{
  "review_id": "R3929",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3930 — マスコット ブルーロック (1개)

상품 ID: 237

- [マスコット ブルーロック](https://megahobby.jp/products/item/3887/)

```json
{
  "review_id": "R3930",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3931 — マスコット マッシュル-MASHLE (1개)

상품 ID: 336

- [マスコット マッシュル-MASHLE-](https://megahobby.jp/products/item/4115/)

```json
{
  "review_id": "R3931",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3932 — マスコット モブサイコ100 Ⅲ (1개)

상품 ID: 358

- [マスコット モブサイコ100 Ⅲ](https://megahobby.jp/products/item/4137/)

```json
{
  "review_id": "R3932",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3933 — マスコット 僕のヒーローアカデミア (1개)

상품 ID: 374

- [マスコット 僕のヒーローアカデミア](https://megahobby.jp/products/item/4177/)

```json
{
  "review_id": "R3933",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3934 — マスコット 呪術廻戦 (1개)

상품 ID: 452

- [マスコット 呪術廻戦【再販】](https://megahobby.jp/products/item/4340/)

```json
{
  "review_id": "R3934",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3935 — マスコット 呪術廻戦 vol.2 (1개)

상품 ID: 373

- [マスコット 呪術廻戦　vol.2](https://megahobby.jp/products/item/4176/)

```json
{
  "review_id": "R3935",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3936 — マスコット 地獄楽 (1개)

상품 ID: 307

- [マスコット 地獄楽](https://megahobby.jp/products/item/4061/)

```json
{
  "review_id": "R3936",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3937 — マスコット 夏目友人帳 (1개)

상품 ID: 391

- [マスコット 夏目友人帳【再販】](https://megahobby.jp/products/item/4225/)

```json
{
  "review_id": "R3937",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3938 — マスコット 怪獣8号 (1개)

상품 ID: 579

- [マスコット 怪獣8号](https://megahobby.jp/products/item/4611/)

```json
{
  "review_id": "R3938",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3939 — マスコット 東京リベンジャーズ (1개)

상품 ID: 210

- [マスコット 東京リベンジャーズ](https://megahobby.jp/products/item/3813/)

```json
{
  "review_id": "R3939",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3940 — マスコット 葬送のフリーレン (1개)

상품 ID: 471

- [マスコット 葬送のフリーレン](https://megahobby.jp/products/item/4378/)

```json
{
  "review_id": "R3940",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3941 — マスコット 銀魂 (1개)

상품 ID: 188

- [マスコット 銀魂【再販】](https://megahobby.jp/products/item/3740/)

```json
{
  "review_id": "R3941",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3942 — マスコット 鬼滅の刃 Vol.2 (1개)

상품 ID: 176

- [マスコット 鬼滅の刃　Vol.2【再販】](https://megahobby.jp/products/item/3702/)

```json
{
  "review_id": "R3942",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3943 — マスコット 鬼滅の刃 Vol.3 (1개)

상품 ID: 196

- [マスコット 鬼滅の刃　Vol.3【再販】](https://megahobby.jp/products/item/3784/)

```json
{
  "review_id": "R3943",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3944 — マスコット 鬼滅の刃 Vol.4 (1개)

상품 ID: 241

- [マスコット 鬼滅の刃　Vol.4](https://megahobby.jp/products/item/3901/)

```json
{
  "review_id": "R3944",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3945 — マッシュル-MASHLE- バディコレ編 (1개)

상품 ID: 465

- [ マッシュル-MASHLE- バディコレ編](https://megahobby.jp/products/item/4372/)

```json
{
  "review_id": "R3945",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3946 — マッシュル-MASHLE- マッシュ・バーンデッド (1개)

상품 ID: 466

- [マッシュル-MASHLE- マッシュ・バーンデッド](https://megahobby.jp/products/item/4373/)

```json
{
  "review_id": "R3946",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3947 — マッシュル-MASHLE- ランス・クラウン (1개)

상품 ID: 467

- [マッシュル-MASHLE- ランス・クラウン](https://megahobby.jp/products/item/4374/)

```json
{
  "review_id": "R3947",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3948 — ミニチュアコレクション 僕のヒーローアカデミア (1개)

상품 ID: 1361

- [ミニチュアコレクション  僕のヒーローアカデミア](https://megahobby.jp/products/item/6113/)

```json
{
  "review_id": "R3948",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3949 — ミニチュアコレクション 銀魂 (1개)

상품 ID: 1268

- [ミニチュアコレクション 銀魂](https://megahobby.jp/products/item/5952/)

```json
{
  "review_id": "R3949",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3950 — ミニチュアコレクション 鬼滅の刃 (1개)

상품 ID: 1205

- [ミニチュアコレクション  鬼滅の刃](https://megahobby.jp/products/item/5839/)

```json
{
  "review_id": "R3950",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3951 — メタリック缶バッジ【BOX販売商品】 (1개)

상품 ID: 4950

- [ブルーロック　メタリック缶バッジ【BOX販売商品】](https://taito-goods.jp/shop/g/g70101260/)

```json
{
  "review_id": "R3951",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3952 — モンスターハンター アイルー (1개)

상품 ID: 1158

- [モンスターハンター アイルー](https://megahobby.jp/products/item/5763/)

```json
{
  "review_id": "R3952",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3953 — ヤマトガールズコレクション 宇宙戦艦ヤマト2202 愛の戦士たち 森雪プライベートコーデRe. (1개)

상품 ID: 897

- [ヤマトガールズコレクション 宇宙戦艦ヤマト2202 愛の戦士たち 森雪プライベートコーデRe.](https://megahobby.jp/products/item/5313/)

```json
{
  "review_id": "R3953",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3954 — ヤマトガールズコレクション 宇宙戦艦ヤマト ヤマトよ永遠に REBEL3199 森雪デザリアムスーツVer. (1개)

상품 ID: 1275

- [ヤマトガールズコレクション 宇宙戦艦ヤマト ヤマトよ永遠に REBEL3199 森雪デザリアムスーツVer.](https://megahobby.jp/products/item/5961/)

```json
{
  "review_id": "R3954",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3955 — リコリス・リコイル 井ノ上たきな (1개)

상품 ID: 318

- [リコリス・リコイル 井ノ上たきな](https://megahobby.jp/products/item/4072/)

```json
{
  "review_id": "R3955",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3956 — リコリス・リコイル 錦木千束 (1개)

상품 ID: 319

- [リコリス・リコイル 錦木千束](https://megahobby.jp/products/item/4073/)

```json
{
  "review_id": "R3956",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3957 — ルカリオ (1개)

상품 ID: 645

- [ルカリオ](https://megahobby.jp/products/item/4732/)

```json
{
  "review_id": "R3957",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3958 — ルパン三世 LUPIN THE GALLERY Punk at dawn！ (1개)

상품 ID: 627

- [ルパン三世 LUPIN THE GALLERY Punk at dawn！](https://megahobby.jp/products/item/4684/)

```json
{
  "review_id": "R3958",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3959 — ワンパンマン サイタマ (1개)

상품 ID: 962

- [ワンパンマン サイタマ](https://megahobby.jp/products/item/5410/)

```json
{
  "review_id": "R3959",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3960 — ワンパンマン ジェノス (1개)

상품 ID: 961

- [ワンパンマン ジェノス](https://megahobby.jp/products/item/5409/)

```json
{
  "review_id": "R3960",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3961 — ワンピース ”NEO-DX” バーソロミュー・くま【限定復刻版】(あみあみ限定) (1개)

상품 ID: 653

- [ワンピース ”NEO-DX” バーソロミュー・くま【限定復刻版】(あみあみ限定)](https://megahobby.jp/products/item/4754/)

```json
{
  "review_id": "R3961",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3962 — ワンピース おでかけニャンピースニャーン！ 2025LIMITED (1개)

상품 ID: 835

- [ワンピース おでかけニャンピースニャーン！ 2025LIMITED](https://megahobby.jp/products/item/5176/)

```json
{
  "review_id": "R3962",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3963 — ワンピース おやすみニャンピースニャーン！好敵手編 (1개)

상품 ID: 1155

- [ワンピース おやすみニャンピースニャーン！好敵手編](https://megahobby.jp/products/item/5760/)

```json
{
  "review_id": "R3963",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3964 — ワンピース ウタ RUN!RUN!RUN! (1개)

상품 ID: 324

- [ワンピース ウタ　RUN!RUN!RUN!](https://megahobby.jp/products/item/4078/)

```json
{
  "review_id": "R3964",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3965 — ワンピース グランドラインコレクションVol.2 (1개)

상품 ID: 772

- [ワンピース グランドラインコレクションVol.2](https://megahobby.jp/products/item/4996/)

```json
{
  "review_id": "R3965",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3966 — ワンピース グランドラインコレクションVol.3 (1개)

상품 ID: 1220

- [ワンピース グランドラインコレクションVol.3](https://megahobby.jp/products/item/5855/)

```json
{
  "review_id": "R3966",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3967 — ワンピース サボ RUN！RUN！RUN！ (1개)

상품 ID: 455

- [ワンピース サボ　RUN！RUN！RUN！](https://megahobby.jp/products/item/4343/)

```json
{
  "review_id": "R3967",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3968 — ワンピース サンジ RUN!RUN!RUN! (1개)

상품 ID: 383

- [ワンピース サンジ RUN!RUN!RUN!](https://megahobby.jp/products/item/4217/)

```json
{
  "review_id": "R3968",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3969 — ワンピース シャンクス RUN！RUN！RUN！ (1개)

상품 ID: 563

- [ワンピース シャンクス　RUN！RUN！RUN！](https://megahobby.jp/products/item/4562/)

```json
{
  "review_id": "R3969",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3970 — ワンピース トコトコニャンピースニャーン！ モンキー・D・ルフィ (1개)

상품 ID: 673

- [ワンピース トコトコニャンピースニャーン！ モンキー・D・ルフィ](https://megahobby.jp/products/item/4795/)

```json
{
  "review_id": "R3970",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3971 — ワンピース トラファルガー・ロー RUN!RUN!RUN! (1개)

상품 ID: 377

- [ワンピース トラファルガー・ロー RUN!RUN!RUN!](https://megahobby.jp/products/item/4180/)

```json
{
  "review_id": "R3971",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3972 — ワンピース ナミ RUN！RUN！RUN！ (1개)

상품 ID: 499

- [ワンピース ナミ　 RUN！RUN！RUN！](https://megahobby.jp/products/item/4436/)

```json
{
  "review_id": "R3972",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3973 — ワンピース ニコ・ロビン RUN！RUN！RUN！ (1개)

상품 ID: 485

- [ワンピース ニコ・ロビン　RUN！RUN！RUN！](https://megahobby.jp/products/item/4407/)

```json
{
  "review_id": "R3973",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3974 — ワンピース ニャンピースニャーン！DINER！ (1개)

상품 ID: 1265

- [ワンピース ニャンピースニャーン！DINER！](https://megahobby.jp/products/item/5949/)

```json
{
  "review_id": "R3974",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3975 — ワンピース ニャンピースニャーン！ HappyCAT2026 (1개)

상품 ID: 1252

- [ワンピース ニャンピースニャーン！ HappyCAT2026](https://megahobby.jp/products/item/5910/)

```json
{
  "review_id": "R3975",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3976 — ワンピース ニャンピースニャーン！つまめるニャンピースニャーン！ (1개)

상품 ID: 543

- [ワンピース ニャンピースニャーン！つまめるニャンピースニャーン！](https://megahobby.jp/products/item/4542/)

```json
{
  "review_id": "R3976",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3977 — ワンピース ニャンピースニャーン！ エッグヘッド編 (1개)

상품 ID: 874

- [ワンピース ニャンピースニャーン！　エッグヘッド編](https://megahobby.jp/products/item/5245/)

```json
{
  "review_id": "R3977",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3978 — ワンピース ニャンピースニャーン！ペタリ！ (1개)

상품 ID: 1056

- [ワンピース ニャンピースニャーン！ペタリ！](https://megahobby.jp/products/item/5574/)

```json
{
  "review_id": "R3978",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3979 — ワンピース ニャンピースニャーン！ ルフィVS海軍編 (1개)

상품 ID: 532

- [ワンピース ニャンピースニャーン！　ルフィVS海軍編](https://megahobby.jp/products/item/4510/)

```json
{
  "review_id": "R3979",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3980 — ワンピース ニャンピースニャーン！ ルフィと頂上戦争編 (1개)

상품 ID: 581

- [ワンピース ニャンピースニャーン！　ルフィと頂上戦争編](https://megahobby.jp/products/item/4613/)

```json
{
  "review_id": "R3980",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3981 — ワンピース ニャンピースニャーン！ 招き猫FORTUNE LUCKY☆CAT PIRATES (1개)

상품 ID: 650

- [ワンピース ニャンピースニャーン！ 招き猫FORTUNE LUCKY☆CAT PIRATES](https://megahobby.jp/products/item/4741/)

```json
{
  "review_id": "R3981",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3982 — ワンピース ニャンピースニャーン！ 海賊王におれはなるニャン！ (1개)

상품 ID: 291

- [ワンピース ニャンピースニャーン！　海賊王におれはなるニャン！【再販】](https://megahobby.jp/products/item/4016/)

```json
{
  "review_id": "R3982",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3983 — ワンピース ニャンピースニャーン！ 缶バッジコレクション (1개)

상품 ID: 591

- [ワンピース ニャンピースニャーン！　缶バッジコレクション](https://megahobby.jp/products/item/4623/)

```json
{
  "review_id": "R3983",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3984 — ワンピース ニャンピースニャーン！ 限定品 HAPPY・TRIO 2024LIMITED (1개)

상품 ID: 838

- [ワンピース ニャンピースニャーン！ 限定品　HAPPY・TRIO 2024LIMITED](https://megahobby.jp/products/item/5179/)

```json
{
  "review_id": "R3984",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3985 — ワンピース ネフェルタリ・ビビ RUN！RUN！RUN！ (1개)

상품 ID: 536

- [ワンピース ネフェルタリ・ビビ　RUN！RUN！RUN！](https://megahobby.jp/products/item/4514/)

```json
{
  "review_id": "R3985",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3986 — ワンピース ポートガス・D・エース RUN！RUN！RUN！ (1개)

상품 ID: 431

- [ワンピース ポートガス・D・エース RUN！RUN！RUN！](https://megahobby.jp/products/item/4306/)

```json
{
  "review_id": "R3986",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3987 — ワンピース モンキー・D・ルフィ RUN!RUN!RUN! (1개)

상품 ID: 240

- [ワンピース モンキー・D・ルフィ RUN!RUN!RUN!](https://megahobby.jp/products/item/3890/)

```json
{
  "review_id": "R3987",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3988 — ワンピース ヤマト RUN!RUN!RUN! (1개)

상품 ID: 290

- [ワンピース ヤマト　RUN!RUN!RUN!](https://megahobby.jp/products/item/4010/)

```json
{
  "review_id": "R3988",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3989 — ワンピース ロロノア・ゾロ RUN!RUN!RUN! (1개)

상품 ID: 255

- [ワンピース ロロノア・ゾロ 　 RUN!RUN!RUN!](https://megahobby.jp/products/item/3924/)

```json
{
  "review_id": "R3989",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3990 — ヴァリアブルアクション 新世紀GPXサイバーフォーミュラSIN 凰呀 AN‐21 -Livery Edition- DXセット (1개)

상품 ID: 1372

- [ヴァリアブルアクション 新世紀GPXサイバーフォーミュラSIN 凰呀 AN‐21 -Livery Edition- DXセット](https://megahobby.jp/products/item/3749/)

```json
{
  "review_id": "R3990",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3991 — 僕のヒーローアカデミア (1개)

상품 ID: 1082

- [僕のヒーローアカデミア](https://megahobby.jp/products/item/5623/)

```json
{
  "review_id": "R3991",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3992 — 僕のヒーローアカデミア おやすみヒロアカニャンコ (1개)

상품 ID: 1334

- [僕のヒーローアカデミア おやすみヒロアカニャンコ](https://megahobby.jp/products/item/6062/)

```json
{
  "review_id": "R3992",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3993 — 僕のヒーローアカデミア てのひら爆豪勝己 (1개)

상품 ID: 351

- [僕のヒーローアカデミア てのひら爆豪勝己](https://megahobby.jp/products/item/4130/)

```json
{
  "review_id": "R3993",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3994 — 僕のヒーローアカデミア てのひら緑谷出久 (1개)

상품 ID: 325

- [僕のヒーローアカデミア てのひら緑谷出久](https://megahobby.jp/products/item/4079/)

```json
{
  "review_id": "R3994",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3995 — 僕のヒーローアカデミア てのひら轟焦凍 (1개)

상품 ID: 385

- [僕のヒーローアカデミア てのひら轟焦凍](https://megahobby.jp/products/item/4219/)

```json
{
  "review_id": "R3995",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3996 — 僕のヒーローアカデミア てのひら麗日お茶子 (1개)

상품 ID: 384

- [僕のヒーローアカデミア てのひら麗日お茶子](https://megahobby.jp/products/item/4218/)

```json
{
  "review_id": "R3996",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3997 — 僕のヒーローアカデミア ひとやすみティータイム (1개)

상품 ID: 1290

- [僕のヒーローアカデミア ひとやすみティータイム](https://megahobby.jp/products/item/6010/)

```json
{
  "review_id": "R3997",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3998 — 僕のヒーローアカデミア ヒロアカニャンコNO.02 (1개)

상품 ID: 1135

- [僕のヒーローアカデミア ヒロアカニャンコNO.02【再販】](https://megahobby.jp/products/item/5739/)

```json
{
  "review_id": "R3998",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R3999 — 僕のヒーローアカデミア ホークス (1개)

상품 ID: 736

- [僕のヒーローアカデミア ホークス](https://megahobby.jp/products/item/4941/)

```json
{
  "review_id": "R3999",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4000 — 僕のヒーローアカデミア 切島鋭児郎 (1개)

상품 ID: 907

- [僕のヒーローアカデミア 切島鋭児郎](https://megahobby.jp/products/item/5323/)

```json
{
  "review_id": "R4000",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4001 — 僕のヒーローアカデミア 死柄木弔 (1개)

상품 ID: 688

- [僕のヒーローアカデミア 死柄木弔](https://megahobby.jp/products/item/4830/)

```json
{
  "review_id": "R4001",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4002 — 僕のヒーローアカデミア 爆豪勝己 私服ver. (1개)

상품 ID: 1232

- [僕のヒーローアカデミア 爆豪勝己　私服ver.](https://megahobby.jp/products/item/5867/)

```json
{
  "review_id": "R4002",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4003 — 僕のヒーローアカデミア 相澤消太 (1개)

상품 ID: 908

- [僕のヒーローアカデミア 相澤消太](https://megahobby.jp/products/item/5324/)

```json
{
  "review_id": "R4003",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4004 — 僕のヒーローアカデミア 緑谷出久 私服ver. (1개)

상품 ID: 1233

- [僕のヒーローアカデミア 緑谷出久　私服ver.](https://megahobby.jp/products/item/5868/)

```json
{
  "review_id": "R4004",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4005 — 僕のヒーローアカデミア 荼毘 (1개)

상품 ID: 735

- [僕のヒーローアカデミア 荼毘](https://megahobby.jp/products/item/4940/)

```json
{
  "review_id": "R4005",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4006 — 僕のヒーローアカデミア 麗日お茶子 (1개)

상품 ID: 469

- [僕のヒーローアカデミア 麗日お茶子](https://megahobby.jp/products/item/4376/)

```json
{
  "review_id": "R4006",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4007 — 凪 誠士郎 (1개)

상품 ID: 4924

- [ブルーロック　SPOOK SHOWマスコット　凪 誠士郎](https://taito-goods.jp/shop/g/g70101460/)

```json
{
  "review_id": "R4007",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4008 — 刀剣乱舞ONLINE 三日月宗近 (1개)

상품 ID: 1315

- [刀剣乱舞ONLINE 三日月宗近](https://megahobby.jp/products/item/6035/)

```json
{
  "review_id": "R4008",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4009 — 刀剣乱舞ONLINE 加州清光 (1개)

상품 ID: 1314

- [刀剣乱舞ONLINE 加州清光](https://megahobby.jp/products/item/6034/)

```json
{
  "review_id": "R4009",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4010 — 刀剣乱舞ONLINE 燭台切光忠 (1개)

상품 ID: 4801

- [刀剣乱舞ONLINE 燭台切光忠](https://megahobby.jp/products/item/6180/)

```json
{
  "review_id": "R4010",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4011 — 刀剣乱舞ONLINE 鶴丸国永 (1개)

상품 ID: 6139

- [刀剣乱舞ONLINE 鶴丸国永](https://megahobby.jp/products/item/6179/)

```json
{
  "review_id": "R4011",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4012 — 劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラーちびムーン (1개)

상품 ID: 264

- [劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラーちびムーン](https://megahobby.jp/products/item/3951/)

```json
{
  "review_id": "R4012",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4013 — 劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラージュピター (1개)

상품 ID: 390

- [劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラージュピター](https://megahobby.jp/products/item/4224/)

```json
{
  "review_id": "R4013",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4014 — 劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラーマーキュリー (1개)

상품 ID: 283

- [劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラーマーキュリー](https://megahobby.jp/products/item/3996/)

```json
{
  "review_id": "R4014",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4015 — 劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラーマーズ (1개)

상품 ID: 282

- [劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラーマーズ](https://megahobby.jp/products/item/3995/)

```json
{
  "review_id": "R4015",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4016 — 劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラームーン (1개)

상품 ID: 265

- [劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラームーン](https://megahobby.jp/products/item/3952/)

```json
{
  "review_id": "R4016",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4017 — 劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラーヴィーナス (1개)

상품 ID: 332

- [劇場版「美少女戦士セーラームーンCosmos」 エターナルセーラーヴィーナス](https://megahobby.jp/products/item/4107/)

```json
{
  "review_id": "R4017",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4018 — 劇場版『チェンソーマン レゼ篇』 BREAK TIME CAFÉ (1개)

상품 ID: 6152

- [劇場版『チェンソーマン レゼ篇』 BREAK TIME CAFÉ](https://megahobby.jp/products/item/6171/)

```json
{
  "review_id": "R4018",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4019 — 劇場版『チェンソーマン レゼ篇』 デンジ 私服Ver. (1개)

상품 ID: 812

- [劇場版『チェンソーマン レゼ篇』 デンジ 私服Ver.](https://megahobby.jp/products/item/5076/)

```json
{
  "review_id": "R4019",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4020 — 劇場版『チェンソーマン レゼ篇』 天使の悪魔 (1개)

상품 ID: 1014

- [劇場版『チェンソーマン レゼ篇』 天使の悪魔](https://megahobby.jp/products/item/5493/)

```json
{
  "review_id": "R4020",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4021 — 劇場版『チェンソーマン レゼ篇』 早川アキ にっこりVer. (1개)

상품 ID: 1015

- [劇場版『チェンソーマン レゼ篇』 早川アキ にっこりVer.](https://megahobby.jp/products/item/5494/)

```json
{
  "review_id": "R4021",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4022 — 劇場版ブルーロック -EPISODE 凪- てのひら凪 誠士郎 (1개)

상품 ID: 534

- [劇場版ブルーロック -EPISODE 凪- てのひら凪 誠士郎](https://megahobby.jp/products/item/4512/)

```json
{
  "review_id": "R4022",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4023 — 劇場版 呪術廻戦 ０ 乙骨憂太 (1개)

상품 ID: 598

- [劇場版 呪術廻戦 ０ 乙骨憂太【再販】](https://megahobby.jp/products/item/4630/)

```json
{
  "review_id": "R4023",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4024 — 劇場版 呪術廻戦 ０ 夏油傑 (1개)

상품 ID: 597

- [劇場版 呪術廻戦 ０ 夏油傑【再販】](https://megahobby.jp/products/item/4629/)

```json
{
  "review_id": "R4024",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4025 — 劇場版 呪術廻戦 0 狗巻棘 (1개)

상품 ID: 1185

- [劇場版 呪術廻戦 0 狗巻棘](https://megahobby.jp/products/item/5816/)

```json
{
  "review_id": "R4025",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4026 — 劇場版忍たま乱太郎 てのひら天鬼 (1개)

상품 ID: 725

- [劇場版忍たま乱太郎 てのひら天鬼](https://megahobby.jp/products/item/4910/)

```json
{
  "review_id": "R4026",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4027 — 劇場版 忍たま乱太郎 土井半助 (1개)

상품 ID: 777

- [劇場版 忍たま乱太郎 土井半助](https://megahobby.jp/products/item/5001/)

```json
{
  "review_id": "R4027",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4028 — 劇場版 忍たま乱太郎 山田利吉 (1개)

상품 ID: 776

- [劇場版 忍たま乱太郎 山田利吉](https://megahobby.jp/products/item/5000/)

```json
{
  "review_id": "R4028",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4029 — 千切 豹馬 (1개)

상품 ID: 4922

- [ブルーロック　SPOOK SHOWマスコット　千切 豹馬](https://taito-goods.jp/shop/g/g70101450/)

```json
{
  "review_id": "R4029",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4030 — 原神 ゴロー (1개)

상품 ID: 1064

- [ 原神 ゴロー](https://megahobby.jp/products/item/5582/)

```json
{
  "review_id": "R4030",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4031 — 原神 楓原万葉 (1개)

상품 ID: 1065

- [原神 楓原万葉](https://megahobby.jp/products/item/5583/)

```json
{
  "review_id": "R4031",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4032 — 名探偵コナン (1개)

상품 ID: 1225

- [名探偵コナン](https://megahobby.jp/products/item/5860/)

```json
{
  "review_id": "R4032",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4033 — 名探偵コナン 怪盗キッド (1개)

상품 ID: 1245

- [名探偵コナン 怪盗キッド](https://megahobby.jp/products/item/5880/)

```json
{
  "review_id": "R4033",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4034 — 名探偵コナン 江戸川コナン (1개)

상품 ID: 1246

- [名探偵コナン 江戸川コナン](https://megahobby.jp/products/item/5881/)

```json
{
  "review_id": "R4034",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4035 — 呪術廻戦 おやすみ呪術ニャンコ (1개)

상품 ID: 1057

- [呪術廻戦 おやすみ呪術ニャンコ](https://megahobby.jp/products/item/5575/)

```json
{
  "review_id": "R4035",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4036 — 呪術廻戦 トコトコ編 懐玉・玉折 (1개)

상품 ID: 427

- [ 呪術廻戦 トコトコ編　懐玉・玉折　](https://megahobby.jp/products/item/4302/)

```json
{
  "review_id": "R4036",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4037 — 呪術廻戦 バディコレ編 懐玉・玉折 (1개)

상품 ID: 406

- [ 呪術廻戦 バディコレ編　懐玉・玉折](https://megahobby.jp/products/item/4261/)

```json
{
  "review_id": "R4037",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4038 — 呪術廻戦 七海建人 高専ver. (1개)

상품 ID: 568

- [呪術廻戦 七海建人 高専ver.](https://megahobby.jp/products/item/4587/)

```json
{
  "review_id": "R4038",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4039 — 呪術廻戦 乙骨憂太 ver.2 (1개)

상품 ID: 1062

- [呪術廻戦 乙骨憂太 ver.2](https://megahobby.jp/products/item/5580/)

```json
{
  "review_id": "R4039",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4040 — 呪術廻戦 五条悟 (1개)

상품 ID: 599

- [呪術廻戦 五条悟【再販】](https://megahobby.jp/products/item/4655/)

```json
{
  "review_id": "R4040",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4041 — 呪術廻戦 五条悟 スーツver. (1개)

상품 ID: 494

- [呪術廻戦 五条悟 スーツver.](https://megahobby.jp/products/item/4427/)

```json
{
  "review_id": "R4041",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4042 — 呪術廻戦 五条悟 沖縄ver. (1개)

상품 ID: 799

- [呪術廻戦 五条悟 沖縄ver.](https://megahobby.jp/products/item/5048/)

```json
{
  "review_id": "R4042",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4043 — 呪術廻戦 伏黒恵 (1개)

상품 ID: 664

- [呪術廻戦 伏黒恵【再販】](https://megahobby.jp/products/item/4786/)

```json
{
  "review_id": "R4043",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4044 — 呪術廻戦 伏黒恵 ver.2 (1개)

상품 ID: 1088

- [呪術廻戦 伏黒恵 ver.2](https://megahobby.jp/products/item/5629/)

```json
{
  "review_id": "R4044",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4045 — 呪術廻戦 伏黒恵 ほほえみver. (1개)

상품 ID: 443

- [ 呪術廻戦 伏黒恵　ほほえみver.](https://megahobby.jp/products/item/4331/)

```json
{
  "review_id": "R4045",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4046 — 呪術廻戦 呪術ニャンコ招き猫ニャン！ (1개)

상품 ID: 948

- [呪術廻戦 呪術ニャンコ招き猫ニャン！](https://megahobby.jp/products/item/5396/)

```json
{
  "review_id": "R4046",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4047 — 呪術廻戦 夏油傑 スーツver. (1개)

상품 ID: 493

- [呪術廻戦 夏油傑 スーツver.](https://megahobby.jp/products/item/4426/)

```json
{
  "review_id": "R4047",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4048 — 呪術廻戦 夏油傑 沖縄ver. (1개)

상품 ID: 798

- [呪術廻戦 夏油傑 沖縄ver.](https://megahobby.jp/products/item/5047/)

```json
{
  "review_id": "R4048",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4049 — 呪術廻戦 家入硝子 高専ver. (1개)

상품 ID: 569

- [呪術廻戦 家入硝子 高専ver.](https://megahobby.jp/products/item/4588/)

```json
{
  "review_id": "R4049",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4050 — 呪術廻戦 懐玉・玉折 (1개)

상품 ID: 810

- [呪術廻戦 懐玉・玉折](https://megahobby.jp/products/item/5059/)

```json
{
  "review_id": "R4050",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4051 — 呪術廻戦 死滅回游 (1개)

상품 ID: 1110

- [呪術廻戦 死滅回游](https://megahobby.jp/products/item/5693/)

```json
{
  "review_id": "R4051",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4052 — 呪術廻戦 灰原雄 (1개)

상품 ID: 821

- [呪術廻戦 灰原雄](https://megahobby.jp/products/item/5157/)

```json
{
  "review_id": "R4052",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4053 — 呪術廻戦 狗巻棘 (1개)

상품 ID: 491

- [呪術廻戦 狗巻棘【再販】](https://megahobby.jp/products/item/4424/)

```json
{
  "review_id": "R4053",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4054 — 呪術廻戦 禪院直哉 (1개)

상품 ID: 1089

- [呪術廻戦 禪院直哉](https://megahobby.jp/products/item/5630/)

```json
{
  "review_id": "R4054",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4055 — 呪術廻戦 虎杖悠仁 (1개)

상품 ID: 665

- [呪術廻戦 虎杖悠仁【再販】](https://megahobby.jp/products/item/4787/)

```json
{
  "review_id": "R4055",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4056 — 呪術廻戦 虎杖悠仁 ver.2 (1개)

상품 ID: 1063

- [呪術廻戦 虎杖悠仁 ver.2](https://megahobby.jp/products/item/5581/)

```json
{
  "review_id": "R4056",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4057 — 呪術廻戦 虎杖悠仁 ニカっとver. (1개)

상품 ID: 444

- [呪術廻戦 虎杖悠仁　ニカっとver.](https://megahobby.jp/products/item/4332/)

```json
{
  "review_id": "R4057",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4058 — 呪術廻戦 釘崎野薔薇 (1개)

상품 ID: 1215

- [呪術廻戦 釘崎野薔薇【再販】](https://megahobby.jp/products/item/5849/)

```json
{
  "review_id": "R4058",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4059 — 國神 錬介 (1개)

상품 ID: 4923

- [ブルーロック　SPOOK SHOWマスコット　國神 錬介](https://taito-goods.jp/shop/g/g70101440/)

```json
{
  "review_id": "R4059",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4060 — 地獄楽 亜左 弔兵衛 (1개)

상품 ID: 298

- [地獄楽 亜左 弔兵衛](https://megahobby.jp/products/item/4028/)

```json
{
  "review_id": "R4060",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4061 — 地獄楽 山田浅ェ門 佐切 (1개)

상품 ID: 288

- [地獄楽 山田浅ェ門 佐切](https://megahobby.jp/products/item/4001/)

```json
{
  "review_id": "R4061",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4062 — 地獄楽 山田浅ェ門 桐馬 (1개)

상품 ID: 297

- [地獄楽 山田浅ェ門 桐馬](https://megahobby.jp/products/item/4027/)

```json
{
  "review_id": "R4062",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4063 — 地獄楽 画眉丸 (1개)

상품 ID: 289

- [地獄楽 画眉丸](https://megahobby.jp/products/item/4002/)

```json
{
  "review_id": "R4063",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4064 — 学園アイドルマスター (1개)

상품 ID: 1162

- [学園アイドルマスター](https://megahobby.jp/products/item/5767/)

```json
{
  "review_id": "R4064",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4065 — 宇宙戦艦ヤマト2202 愛の戦士たち 宇宙戦艦ヤマト2202 Re.（アステロイドリング付き） (1개)

상품 ID: 748

- [宇宙戦艦ヤマト2202 愛の戦士たち 宇宙戦艦ヤマト2202 Re.（アステロイドリング付き）](https://megahobby.jp/products/item/4966/)

```json
{
  "review_id": "R4065",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4066 — 宇宙戦艦ヤマト2202 愛の戦士たち 零式52型空間艦上戦闘機コスモゼロα1 (1개)

상품 ID: 549

- [宇宙戦艦ヤマト2202 愛の戦士たち 零式52型空間艦上戦闘機コスモゼロα1【再販】](https://megahobby.jp/products/item/4548/)

```json
{
  "review_id": "R4066",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4067 — 家庭教師ヒットマンREBORN! てのひらツナくん＆リボーン (1개)

상품 ID: 1019

- [家庭教師ヒットマンREBORN! てのひらツナくん＆リボーン](https://megahobby.jp/products/item/5498/)

```json
{
  "review_id": "R4067",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4068 — 家庭教師ヒットマンREBORN! てのひら雲雀さん＆ヒバード (1개)

상품 ID: 1018

- [家庭教師ヒットマンREBORN! てのひら雲雀さん＆ヒバード](https://megahobby.jp/products/item/5497/)

```json
{
  "review_id": "R4068",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4069 — 崩壊：スターレイル アベンチュリン (1개)

상품 ID: 1095

- [崩壊：スターレイル アベンチュリン](https://megahobby.jp/products/item/5636/)

```json
{
  "review_id": "R4069",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4070 — 崩壊：スターレイル カカワーシャ (1개)

상품 ID: 1096

- [崩壊：スターレイル カカワーシャ](https://megahobby.jp/products/item/5637/)

```json
{
  "review_id": "R4070",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4071 — 崩壊：スターレイル カフカ (1개)

상품 ID: 4797

- [崩壊：スターレイル カフカ](https://megahobby.jp/products/item/6184/)

```json
{
  "review_id": "R4071",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4072 — 崩壊：スターレイル マダム・ヘルタ (1개)

상품 ID: 4798

- [崩壊：スターレイル マダム・ヘルタ](https://megahobby.jp/products/item/6183/)

```json
{
  "review_id": "R4072",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4073 — 巡音ルカ (1개)

상품 ID: 1023

- [ 巡音ルカ](https://megahobby.jp/products/item/5524/)

```json
{
  "review_id": "R4073",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4074 — 幽☆遊☆白書 てのひら浦飯幽助 (1개)

상품 ID: 533

- [幽☆遊☆白書 てのひら浦飯幽助](https://megahobby.jp/products/item/4511/)

```json
{
  "review_id": "R4074",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4075 — 幽☆遊☆白書 てのひら蔵馬 (1개)

상품 ID: 565

- [幽☆遊☆白書 てのひら蔵馬](https://megahobby.jp/products/item/4564/)

```json
{
  "review_id": "R4075",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4076 — 幽☆遊☆白書 てのひら飛影 (1개)

상품 ID: 592

- [幽☆遊☆白書 てのひら飛影](https://megahobby.jp/products/item/4624/)

```json
{
  "review_id": "R4076",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4077 — 御影 玲王 (1개)

상품 ID: 4925

- [ブルーロック　SPOOK SHOWマスコット　御影 玲王](https://taito-goods.jp/shop/g/g70101470/)

```json
{
  "review_id": "R4077",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4078 — 忍たま乱太郎 てのひら利吉さん (1개)

상품 ID: 1022

- [忍たま乱太郎 てのひら利吉さん](https://megahobby.jp/products/item/5523/)

```json
{
  "review_id": "R4078",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4079 — 忍たま乱太郎 てのひら土井先生 (1개)

상품 ID: 1170

- [忍たま乱太郎 てのひら土井先生](https://megahobby.jp/products/item/5801/)

```json
{
  "review_id": "R4079",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4080 — 忍たま乱太郎 てのひら雑渡さん (1개)

상품 ID: 1070

- [忍たま乱太郎 てのひら雑渡さん](https://megahobby.jp/products/item/5588/)

```json
{
  "review_id": "R4080",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4081 — 忍たま乱太郎 雑渡昆奈門 (1개)

상품 ID: 1016

- [忍たま乱太郎 雑渡昆奈門](https://megahobby.jp/products/item/5495/)

```json
{
  "review_id": "R4081",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4082 — 怪獣8号 鳴海弦 (1개)

상품 ID: 954

- [怪獣8号 鳴海弦](https://megahobby.jp/products/item/5402/)

```json
{
  "review_id": "R4082",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4083 — 怪獣8号 鳴海弦 やるきver. (1개)

상품 ID: 1304

- [怪獣8号 鳴海弦 やるきver.](https://megahobby.jp/products/item/6024/)

```json
{
  "review_id": "R4083",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4084 — 文豪ストレイドッグス (1개)

상품 ID: 946

- [文豪ストレイドッグス](https://megahobby.jp/products/item/5394/)

```json
{
  "review_id": "R4084",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4085 — 文豪ストレイドッグス 中原中也 (1개)

상품 ID: 959

- [文豪ストレイドッグス 中原中也](https://megahobby.jp/products/item/5407/)

```json
{
  "review_id": "R4085",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4086 — 文豪ストレイドッグス 中島敦 (1개)

상품 ID: 805

- [文豪ストレイドッグス 中島敦](https://megahobby.jp/products/item/5054/)

```json
{
  "review_id": "R4086",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4087 — 文豪ストレイドッグス 太宰治 (1개)

상품 ID: 804

- [文豪ストレイドッグス 太宰治](https://megahobby.jp/products/item/5053/)

```json
{
  "review_id": "R4087",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4088 — 文豪ストレイドッグス 芥川龍之介 (1개)

상품 ID: 960

- [文豪ストレイドッグス 芥川龍之介](https://megahobby.jp/products/item/5408/)

```json
{
  "review_id": "R4088",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4089 — 斉木楠雄のΨ難 斉木楠雄 (1개)

상품 ID: 1313

- [斉木楠雄のΨ難 斉木楠雄](https://megahobby.jp/products/item/6033/)

```json
{
  "review_id": "R4089",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4090 — 斉木楠雄のΨ難 海藤瞬 (1개)

상품 ID: 1337

- [斉木楠雄のΨ難 海藤瞬](https://megahobby.jp/products/item/6065/)

```json
{
  "review_id": "R4090",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4091 — 斉木楠雄のΨ難 窪谷須亜蓮 (1개)

상품 ID: 1336

- [斉木楠雄のΨ難 窪谷須亜蓮](https://megahobby.jp/products/item/6064/)

```json
{
  "review_id": "R4091",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4092 — 新テニスの王子様 不二周助 (1개)

상품 ID: 1237

- [新テニスの王子様 不二周助](https://megahobby.jp/products/item/5872/)

```json
{
  "review_id": "R4092",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4093 — 新テニスの王子様 幸村精市 (1개)

상품 ID: 1182

- [新テニスの王子様 幸村精市](https://megahobby.jp/products/item/5813/)

```json
{
  "review_id": "R4093",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4094 — 新テニスの王子様 手塚国光 (1개)

상품 ID: 1181

- [新テニスの王子様 手塚国光](https://megahobby.jp/products/item/5812/)

```json
{
  "review_id": "R4094",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4095 — 新テニスの王子様 王子様のティータイム Again! (1개)

상품 ID: 1152

- [新テニスの王子様 王子様のティータイム Again!](https://megahobby.jp/products/item/5756/)

```json
{
  "review_id": "R4095",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4096 — 新テニスの王子様 白石蔵ノ介 (1개)

상품 ID: 1236

- [新テニスの王子様 白石蔵ノ介](https://megahobby.jp/products/item/5871/)

```json
{
  "review_id": "R4096",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4097 — 新テニスの王子様 越前リョーマ (1개)

상품 ID: 987

- [新テニスの王子様 越前リョーマ](https://megahobby.jp/products/item/5439/)

```json
{
  "review_id": "R4097",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4098 — 新テニスの王子様 越前リョーマ 日本代表Ver. (1개)

상품 ID: 4800

- [新テニスの王子様 越前リョーマ 日本代表Ver.](https://megahobby.jp/products/item/6181/)

```json
{
  "review_id": "R4098",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4099 — 新テニスの王子様 跡部景吾 (1개)

상품 ID: 986

- [新テニスの王子様 跡部景吾](https://megahobby.jp/products/item/5438/)

```json
{
  "review_id": "R4099",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4100 — 新世紀GPXサイバーフォーミュラ11 スーパーアスラーダ AKF-11 (1개)

상품 ID: 127

- [新世紀GPXサイバーフォーミュラ11  スーパーアスラーダ AKF-11](https://megahobby.jp/products/item/3144/)

```json
{
  "review_id": "R4100",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4101 — 新世紀GPXサイバーフォーミュラ11 スーパーアスラーダAKF-11 -Livery Edition (1개)

상품 ID: 516

- [新世紀GPXサイバーフォーミュラ11 スーパーアスラーダAKF-11 -Livery Edition-](https://megahobby.jp/products/item/4480/)

```json
{
  "review_id": "R4101",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4102 — 新世紀GPXサイバーフォーミュラ11 スーパーアスラーダ AKF-11 ~35th Anniversary Color Edition~ (1개)

상품 ID: 1126

- [新世紀GPXサイバーフォーミュラ11 スーパーアスラーダ AKF-11 ~35th Anniversary Color Edition~](https://megahobby.jp/products/item/5710/)

```json
{
  "review_id": "R4102",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4103 — 新世紀GPXサイバーフォーミュラSAGA ガーランドSF-03 -Livery Edition (1개)

상품 ID: 327

- [新世紀GPXサイバーフォーミュラSAGA ガーランドSF-03 -Livery Edition-](https://megahobby.jp/products/item/4081/)

```json
{
  "review_id": "R4103",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4104 — 新世紀GPXサイバーフォーミュラSIN νアスラーダAKF-0/G (1개)

상품 ID: 628

- [新世紀GPXサイバーフォーミュラSIN νアスラーダAKF-0/G](https://megahobby.jp/products/item/4685/)

```json
{
  "review_id": "R4104",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4105 — 新世紀GPXサイバーフォーミュラSIN エクスペリオンZ/A-10 加賀機 (1개)

상품 ID: 969

- [新世紀GPXサイバーフォーミュラSIN エクスペリオンZ/A-10 加賀機](https://megahobby.jp/products/item/5418/)

```json
{
  "review_id": "R4105",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4106 — 新世紀GPXサイバーフォーミュラSIN 凰呀AN-21 (1개)

상품 ID: 379

- [新世紀GPXサイバーフォーミュラSIN 凰呀AN-21【再販】](https://megahobby.jp/products/item/4183/)

```json
{
  "review_id": "R4106",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4107 — 新世紀GPXサイバーフォーミュラ イシュザーク (1개)

상품 ID: 934

- [新世紀GPXサイバーフォーミュラ イシュザーク【リニューアル再販】](https://megahobby.jp/products/item/5382/)

```json
{
  "review_id": "R4107",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4108 — 新世紀GPXサイバーフォーミュラ スーパーアスラーダ01（サーキットモード） (1개)

상품 ID: 935

- [新世紀GPXサイバーフォーミュラ スーパーアスラーダ01（サーキットモード）【リニューアル再販】](https://megahobby.jp/products/item/5383/)

```json
{
  "review_id": "R4108",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4109 — 新世紀GPXサイバーフォーミュラ ナイトセイバー005 (1개)

상품 ID: 933

- [新世紀GPXサイバーフォーミュラ ナイトセイバー005【リニューアル再販】](https://megahobby.jp/products/item/5381/)

```json
{
  "review_id": "R4109",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4110 — 新世紀GPXサイバーフォーミュラ ナイトセイバー005 -Livery Edition (1개)

상품 ID: 842

- [新世紀GPXサイバーフォーミュラ ナイトセイバー005 -Livery Edition-](https://megahobby.jp/products/item/5208/)

```json
{
  "review_id": "R4110",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4111 — 新機動戦記ガンダムW ニャンダムW ニャンコ化計画任務完了！ (1개)

상품 ID: 876

- [新機動戦記ガンダムW ニャンダムW　ニャンコ化計画任務完了！](https://megahobby.jp/products/item/5247/)

```json
{
  "review_id": "R4111",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4112 — 映画「鬼太郎誕生 ゲゲゲの謎」 てのひら鬼太郎の父 (1개)

상품 ID: 593

- [ 映画「鬼太郎誕生 ゲゲゲの謎」 てのひら鬼太郎の父](https://megahobby.jp/products/item/4625/)

```json
{
  "review_id": "R4112",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4113 — 東京リベンジャーズ 佐野万次郎 (1개)

상품 ID: 247

- [東京リベンジャーズ 佐野万次郎](https://megahobby.jp/products/item/3907/)

```json
{
  "review_id": "R4113",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4114 — 東京リベンジャーズ 松野千冬 (1개)

상품 ID: 308

- [東京リベンジャーズ 松野千冬](https://megahobby.jp/products/item/4062/)

```json
{
  "review_id": "R4114",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4115 — 東京リベンジャーズ 花垣武道 (1개)

상품 ID: 309

- [東京リベンジャーズ 花垣武道](https://megahobby.jp/products/item/4063/)

```json
{
  "review_id": "R4115",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4116 — 東京リベンジャーズ 龍宮寺堅 (1개)

상품 ID: 246

- [東京リベンジャーズ 龍宮寺堅](https://megahobby.jp/products/item/3906/)

```json
{
  "review_id": "R4116",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4117 — 機動戦士Gundam GQuuuuuuX (1개)

상품 ID: 816

- [機動戦士Gundam GQuuuuuuX](https://megahobby.jp/products/item/5151/)

```json
{
  "review_id": "R4117",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4118 — 機動戦士Gundam GQuuuuuuX アマテ・ユズリハ(マチュ) (1개)

상품 ID: 803

- [機動戦士Gundam GQuuuuuuX アマテ・ユズリハ(マチュ)](https://megahobby.jp/products/item/5052/)

```json
{
  "review_id": "R4118",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4119 — 機動戦士Gundam GQuuuuuuX アマテ・ユズリハ(マチュ)パイロットスーツVer. (1개)

상품 ID: 822

- [機動戦士Gundam GQuuuuuuX アマテ・ユズリハ(マチュ)パイロットスーツVer.](https://megahobby.jp/products/item/5158/)

```json
{
  "review_id": "R4119",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4120 — 機動戦士Gundam GQuuuuuuX シャア・アズナブル (1개)

상품 ID: 871

- [機動戦士Gundam GQuuuuuuX シャア・アズナブル](https://megahobby.jp/products/item/5242/)

```json
{
  "review_id": "R4120",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4121 — 機動戦士Gundam GQuuuuuuX シャリア・ブル (1개)

상품 ID: 872

- [機動戦士Gundam GQuuuuuuX シャリア・ブル](https://megahobby.jp/products/item/5243/)

```json
{
  "review_id": "R4121",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4122 — 機動戦士Gundam GQuuuuuuX シュウジ・イトウ (1개)

상품 ID: 823

- [機動戦士Gundam GQuuuuuuX シュウジ・イトウ](https://megahobby.jp/products/item/5159/)

```json
{
  "review_id": "R4122",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4123 — 機動戦士Gundam GQuuuuuuX ニャアン (1개)

상품 ID: 802

- [機動戦士Gundam GQuuuuuuX ニャアン](https://megahobby.jp/products/item/5051/)

```json
{
  "review_id": "R4123",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4124 — 機動戦士Vガンダム リーンホースJr.Re. (1개)

상품 ID: 562

- [機動戦士Vガンダム リーンホースJr.Re.](https://megahobby.jp/products/item/4561/)

```json
{
  "review_id": "R4124",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4125 — 機動戦士Zガンダム アーガマRe. (1개)

상품 ID: 387

- [機動戦士Zガンダム アーガマRe.](https://megahobby.jp/products/item/4221/)

```json
{
  "review_id": "R4125",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4126 — 機動戦士Zガンダム カミーユ・ビダン【限定復刻版】 (1개)

상품 ID: 896

- [機動戦士Zガンダム カミーユ・ビダン【限定復刻版】](https://megahobby.jp/products/item/5312/)

```json
{
  "review_id": "R4126",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4127 — 機動戦士Zガンダム ハマーン・カーン (1개)

상품 ID: 151

- [機動戦士Zガンダム ハマーン・カーン【再販】](https://megahobby.jp/products/item/3657/)

```json
{
  "review_id": "R4127",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4128 — 機動戦士Zガンダム パプテマス・シロッコ (1개)

상품 ID: 171

- [機動戦士Zガンダム  パプテマス・シロッコ](https://megahobby.jp/products/item/3697/)

```json
{
  "review_id": "R4128",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4129 — 機動戦士Zガンダム フォウ・ムラサメ (1개)

상품 ID: 1258

- [機動戦士Zガンダム フォウ・ムラサメ【再販】](https://megahobby.jp/products/item/5942/)

```json
{
  "review_id": "R4129",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4130 — 機動戦士Zガンダム フォウ・ムラサメ -蘇るZの魂 (1개)

상품 ID: 885

- [機動戦士Zガンダム フォウ・ムラサメ -蘇るZの魂-](https://megahobby.jp/products/item/5301/)

```json
{
  "review_id": "R4130",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4131 — 機動戦士ガンダム0080 ポケットの中の戦争 クリスチーナ・マッケンジー -INTO THE SKY (1개)

상품 ID: 1194

- [機動戦士ガンダム0080 ポケットの中の戦争 クリスチーナ・マッケンジー -INTO THE SKY-【再販】](https://megahobby.jp/products/item/5825/)

```json
{
  "review_id": "R4131",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4132 — 機動戦士ガンダムSEED FREEDOM カガリ・ユラ・アスハ (1개)

상품 ID: 869

- [機動戦士ガンダムSEED FREEDOM  カガリ・ユラ・アスハ](https://megahobby.jp/products/item/5240/)

```json
{
  "review_id": "R4132",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4133 — 機動戦士ガンダムSEED FREEDOM カガリ・ユラ・アスハ パイロットスーツVer. (1개)

상품 ID: 1349

- [機動戦士ガンダムSEED FREEDOM カガリ・ユラ・アスハ　パイロットスーツVer.](https://megahobby.jp/products/item/6077/)

```json
{
  "review_id": "R4133",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4134 — 機動戦士ガンダムSEED FREEDOM ラクス・クライン (1개)

상품 ID: 870

- [機動戦士ガンダムSEED FREEDOM  ラクス・クライン](https://megahobby.jp/products/item/5241/)

```json
{
  "review_id": "R4134",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4135 — 機動戦士ガンダムSEED FREEDOM ラクス・クライン 陣羽織Ver. (1개)

상품 ID: 1368

- [機動戦士ガンダムSEED FREEDOM ラクス・クライン 陣羽織Ver.](https://megahobby.jp/products/item/6132/)

```json
{
  "review_id": "R4135",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4136 — 機動戦士ガンダムSEED FREEDOM ルナマリア・ホーク (1개)

상품 ID: 972

- [機動戦士ガンダムSEED FREEDOM ルナマリア・ホーク](https://megahobby.jp/products/item/5422/)

```json
{
  "review_id": "R4136",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4137 — 機動戦士ガンダムSEED 機動戦士ニャンダムSEED 偽りのニャンコ (1개)

상품 ID: 1188

- [機動戦士ガンダムSEED 機動戦士ニャンダムSEED　 偽りのニャンコ](https://megahobby.jp/products/item/5819/)

```json
{
  "review_id": "R4137",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4138 — 機動戦士ガンダム THE ORIGIN ムサイ改型ワルキューレRe. (1개)

상품 ID: 497

- [機動戦士ガンダム THE ORIGIN ムサイ改型ワルキューレRe.](https://megahobby.jp/products/item/4432/)

```json
{
  "review_id": "R4138",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4139 — 機動戦士ガンダムUC ネェル・アーガマ（最終章Ver.）Re. (1개)

상품 ID: 648

- [機動戦士ガンダムUC ネェル・アーガマ（最終章Ver.）Re.](https://megahobby.jp/products/item/4739/)

```json
{
  "review_id": "R4139",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4140 — 機動戦士ガンダムUC レウルーラRe. (1개)

상품 ID: 484

- [機動戦士ガンダムUC レウルーラRe.](https://megahobby.jp/products/item/4406/)

```json
{
  "review_id": "R4140",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4141 — 機動戦士ガンダム アッガイ (1개)

상품 ID: 616

- [機動戦士ガンダム アッガイ](https://megahobby.jp/products/item/4673/)

```json
{
  "review_id": "R4141",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4142 — 機動戦士ガンダム シャア・アズナブル～めぐりあい～ (1개)

상품 ID: 567

- [機動戦士ガンダム シャア・アズナブル～めぐりあい～](https://megahobby.jp/products/item/4566/)

```json
{
  "review_id": "R4142",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4143 — 機動戦士ガンダム マチルダ・アジャン feat.ことぶきつかさ (1개)

상품 ID: 118

- [機動戦士ガンダム マチルダ・アジャン feat.ことぶきつかさ](https://megahobby.jp/products/item/6133/)

```json
{
  "review_id": "R4143",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4144 — 機動戦士ガンダム 機動戦士ニャンダム☆LUCKYCAT (1개)

상품 ID: 1009

- [機動戦士ガンダム 機動戦士ニャンダム☆LUCKYCAT](https://megahobby.jp/products/item/5488/)

```json
{
  "review_id": "R4144",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4145 — 機動戦士ガンダム 水星の魔女 てのひらエランくん (1개)

상품 ID: 451

- [ 機動戦士ガンダム　水星の魔女 てのひらエランくん](https://megahobby.jp/products/item/4339/)

```json
{
  "review_id": "R4145",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4146 — 機動戦士ガンダム 水星の魔女 てのひらグエルくん (1개)

상품 ID: 454

- [機動戦士ガンダム　水星の魔女 てのひらグエルくん](https://megahobby.jp/products/item/4342/)

```json
{
  "review_id": "R4146",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4147 — 機動戦士ガンダム 水星の魔女 てのひらシャディクくん (1개)

상품 ID: 453

- [機動戦士ガンダム　水星の魔女 てのひらシャディクくん](https://megahobby.jp/products/item/4341/)

```json
{
  "review_id": "R4147",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4148 — 機動戦士ガンダム 水星の魔女 てのひらスレッタちゃん (1개)

상품 ID: 433

- [機動戦士ガンダム　水星の魔女 てのひらスレッタちゃん](https://megahobby.jp/products/item/4308/)

```json
{
  "review_id": "R4148",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4149 — 機動戦士ガンダム 水星の魔女 てのひらチュチュちゃん (1개)

상품 ID: 474

- [機動戦士ガンダム　水星の魔女 てのひらチュチュちゃん](https://megahobby.jp/products/item/4381/)

```json
{
  "review_id": "R4149",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4150 — 機動戦士ガンダム 水星の魔女 てのひらニカちゃん (1개)

상품 ID: 473

- [機動戦士ガンダム　水星の魔女 てのひらニカちゃん](https://megahobby.jp/products/item/4380/)

```json
{
  "review_id": "R4150",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4151 — 機動戦士ガンダム 水星の魔女 てのひらミオリネさん (1개)

상품 ID: 432

- [機動戦士ガンダム　水星の魔女 てのひらミオリネさん](https://megahobby.jp/products/item/4307/)

```json
{
  "review_id": "R4151",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4152 — 機動戦士ガンダム第08MS小隊 アイナ・サハリン ～Snow Night Ver.～ (1개)

상품 ID: 1053

- [機動戦士ガンダム第08MS小隊 アイナ・サハリン ～Snow Night Ver.～](https://megahobby.jp/products/item/5568/)

```json
{
  "review_id": "R4152",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4153 — 機動戦士ガンダム 逆襲のシャア アムロ・レイ (1개)

상품 ID: 271

- [機動戦士ガンダム 逆襲のシャア アムロ・レイ 【再販】](https://megahobby.jp/products/item/3984/)

```json
{
  "review_id": "R4153",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4154 — 機動戦士ガンダム 逆襲のシャア アムロ・レイ 【限定復刻版】 (1개)

상품 ID: 858

- [機動戦士ガンダム 逆襲のシャア アムロ・レイ 【限定復刻版】](https://megahobby.jp/products/item/5228/)

```json
{
  "review_id": "R4154",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4155 — 機動戦士ガンダム 逆襲のシャア シャア・アズナブル総帥 (1개)

상품 ID: 833

- [機動戦士ガンダム 逆襲のシャア シャア・アズナブル総帥](https://megahobby.jp/products/item/5170/)

```json
{
  "review_id": "R4155",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4156 — 機動戦士ガンダム 逆襲のシャア ラー・カイラムRe. (1개)

상품 ID: 364

- [機動戦士ガンダム 逆襲のシャア ラー・カイラムRe.【再販】](https://megahobby.jp/products/item/4167/)

```json
{
  "review_id": "R4156",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4157 — 機動武闘伝Gガンダム ドモン・カッシュ (1개)

상품 ID: 726

- [機動武闘伝Gガンダム ドモン・カッシュ【再販】](https://megahobby.jp/products/item/4931/)

```json
{
  "review_id": "R4157",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4158 — 潔 世一 (1개)

상품 ID: 4920

- [ブルーロック　SPOOK SHOWマスコット　潔 世一](https://taito-goods.jp/shop/g/g70101420/)

```json
{
  "review_id": "R4158",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4159 — 無職転生Ⅲ ～異世界行ったら本気だす～ てのひらエリス 添い寝だニャンVer. (1개)

상품 ID: 1281

- [無職転生Ⅲ ～異世界行ったら本気だす～ てのひらエリス 添い寝だニャンVer.](https://megahobby.jp/products/item/5968/)

```json
{
  "review_id": "R4159",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4160 — 無職転生Ⅱ ～異世界行ったら本気だす～ てのひら エリス (1개)

상품 ID: 590

- [ 無職転生Ⅱ ～異世界行ったら本気だす～ てのひら エリス](https://megahobby.jp/products/item/4622/)

```json
{
  "review_id": "R4160",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4161 — 無職転生Ⅱ ～異世界行ったら本気だす～ てのひらシルフィエット (1개)

상품 ID: 877

- [無職転生Ⅱ ～異世界行ったら本気だす～ てのひらシルフィエット](https://megahobby.jp/products/item/5248/)

```json
{
  "review_id": "R4161",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4162 — 無職転生 ～異世界行ったら本気だす～ てのひらロキシー のぞき見Ver. (1개)

상품 ID: 1098

- [無職転生 ～異世界行ったら本気だす～ てのひらロキシー のぞき見Ver.](https://megahobby.jp/products/item/5639/)

```json
{
  "review_id": "R4162",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4163 — 盾の勇者の成り上がり てのひら ラフタリア 幼少化Ver. (1개)

상품 ID: 475

- [ 盾の勇者の成り上がり てのひら ラフタリア 幼少化Ver.](https://megahobby.jp/products/item/4382/)

```json
{
  "review_id": "R4163",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4164 — 真夜中ぱんチ てのひら りぶ (1개)

상품 ID: 691

- [ 真夜中ぱんチ てのひら りぶ](https://megahobby.jp/products/item/4833/)

```json
{
  "review_id": "R4164",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4165 — 缶バッジコレクション 銀魂 名場面編 (1개)

상품 ID: 881

- [缶バッジコレクション 銀魂 名場面編【再販】](https://megahobby.jp/products/item/5258/)

```json
{
  "review_id": "R4165",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4166 — 缶バッジ 呪術廻戦 呪術ニャンコ 缶バッジコレクション (1개)

상품 ID: 1377

- [缶バッジ  呪術廻戦 呪術ニャンコ 缶バッジコレクション](https://megahobby.jp/products/item/5174/)

```json
{
  "review_id": "R4166",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4167 — 缶バッジ 銀魂×大川ぶくぶ 銀魂 オシャンティ☆缶バッジコレクション (1개)

상품 ID: 1375

- [缶バッジ 銀魂×大川ぶくぶ 銀魂 オシャンティ☆缶バッジコレクション](https://megahobby.jp/products/item/5153/)

```json
{
  "review_id": "R4167",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4168 — 美少女戦士セーラームーン スーパーセーラーちびムーン (1개)

상품 ID: 147

- [美少女戦士セーラームーン スーパーセーラーちびムーン](https://megahobby.jp/products/item/3653/)

```json
{
  "review_id": "R4168",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4169 — 美少女戦士セーラームーン スーパーセーラームーン (1개)

상품 ID: 148

- [美少女戦士セーラームーン スーパーセーラームーン](https://megahobby.jp/products/item/3654/)

```json
{
  "review_id": "R4169",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4170 — 美少女戦士セーラームーン セーニャームーン 月にかわっておしおきニャ！2024ver. (1개)

상품 ID: 396

- [美少女戦士セーラームーン セーニャームーン　月にかわっておしおきニャ！2024ver.](https://megahobby.jp/products/item/4230/)

```json
{
  "review_id": "R4170",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4171 — 美少女戦士セーラームーン 月にかわっておしおきニャ！２ (1개)

상품 ID: 146

- [美少女戦士セーラームーン 月にかわっておしおきニャ！２](https://megahobby.jp/products/item/3652/)

```json
{
  "review_id": "R4171",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4172 — 葬送のフリーレン シュタルク (1개)

상품 ID: 613

- [葬送のフリーレン シュタルク](https://megahobby.jp/products/item/4669/)

```json
{
  "review_id": "R4172",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4173 — 葬送のフリーレン ヒンメル (1개)

상품 ID: 1086

- [葬送のフリーレン ヒンメル](https://megahobby.jp/products/item/5627/)

```json
{
  "review_id": "R4173",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4174 — 葬送のフリーレン フェルン (1개)

상품 ID: 614

- [葬送のフリーレン フェルン](https://megahobby.jp/products/item/4670/)

```json
{
  "review_id": "R4174",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4175 — 葬送のフリーレン フリーレン しょぼしょぼVer. (1개)

상품 ID: 1090

- [葬送のフリーレン フリーレン しょぼしょぼVer.](https://megahobby.jp/products/item/5631/)

```json
{
  "review_id": "R4175",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4176 — 薬屋のひとりごと 壬氏 (1개)

상품 ID: 756

- [薬屋のひとりごと 壬氏](https://megahobby.jp/products/item/4974/)

```json
{
  "review_id": "R4176",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4177 — 薬屋のひとりごと 猫猫 (1개)

상품 ID: 757

- [薬屋のひとりごと 猫猫](https://megahobby.jp/products/item/4975/)

```json
{
  "review_id": "R4177",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4178 — 薬屋のひとりごと 瓶の中の薬屋にゃんこ (1개)

상품 ID: 6140

- [薬屋のひとりごと 瓶の中の薬屋にゃんこ](https://megahobby.jp/products/item/6178/)

```json
{
  "review_id": "R4178",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4179 — 蜂楽 廻 (1개)

상품 ID: 4921

- [ブルーロック　SPOOK SHOWマスコット　蜂楽 廻](https://taito-goods.jp/shop/g/g70101430/)

```json
{
  "review_id": "R4179",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4180 — 解体パズルFANTASY サンリオキャラクターズ トロピカルチェリーMix (1개)

상품 ID: 1078

- [解体パズルFANTASY サンリオキャラクターズ トロピカルチェリーMix](https://megahobby.jp/products/item/5619/)

```json
{
  "review_id": "R4180",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4181 — 超かぐや姫！ かぐや (1개)

상품 ID: 1316

- [超かぐや姫！ かぐや](https://megahobby.jp/products/item/6036/)

```json
{
  "review_id": "R4181",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4182 — 超かぐや姫！ 酒寄彩葉 (1개)

상품 ID: 1317

- [超かぐや姫！ 酒寄彩葉](https://megahobby.jp/products/item/6037/)

```json
{
  "review_id": "R4182",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4183 — 超力ロボガラット ジャンブー リニューアルVer. (1개)

상품 ID: 429

- [超力ロボガラット ジャンブー リニューアルVer.【再販】](https://megahobby.jp/products/item/4304/)

```json
{
  "review_id": "R4183",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4184 — 超時空世紀オーガス オーガス (1개)

상품 ID: 381

- [超時空世紀オーガス オーガス【再販】](https://megahobby.jp/products/item/4214/)

```json
{
  "review_id": "R4184",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4185 — 超時空世紀オーガス オーガスⅡ オルソン・スペシャル リニューアルVer. (1개)

상품 ID: 550

- [超時空世紀オーガス オーガスⅡ オルソン・スペシャル リニューアルVer.](https://megahobby.jp/products/item/4549/)

```json
{
  "review_id": "R4185",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4186 — 逃げ上手の若君 北条時行 (1개)

상품 ID: 715

- [逃げ上手の若君 北条時行](https://megahobby.jp/products/item/4891/)

```json
{
  "review_id": "R4186",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4187 — 逃げ上手の若君 諏訪頼重 (1개)

상품 ID: 124

- [逃げ上手の若君 諏訪頼重](https://megahobby.jp/products/item/2689/)

```json
{
  "review_id": "R4187",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4188 — 進撃の巨人 アルミン・アルレルト (1개)

상품 ID: 1122

- [進撃の巨人 アルミン・アルレルト](https://megahobby.jp/products/item/5706/)

```json
{
  "review_id": "R4188",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4189 — 進撃の巨人 エルヴィン・スミス (1개)

상품 ID: 1060

- [進撃の巨人 エルヴィン・スミス](https://megahobby.jp/products/item/5578/)

```json
{
  "review_id": "R4189",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4190 — 進撃の巨人 エレン・イェーガー (1개)

상품 ID: 827

- [進撃の巨人 エレン・イェーガー](https://megahobby.jp/products/item/5163/)

```json
{
  "review_id": "R4190",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4191 — 進撃の巨人 エレン・イェーガー むむっとVer. (1개)

상품 ID: 1121

- [進撃の巨人 エレン・イェーガー むむっとVer.](https://megahobby.jp/products/item/5705/)

```json
{
  "review_id": "R4191",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4192 — 進撃の巨人 ハンジ・ゾエ (1개)

상품 ID: 1061

- [進撃の巨人 ハンジ・ゾエ](https://megahobby.jp/products/item/5579/)

```json
{
  "review_id": "R4192",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4193 — 進撃の巨人 ミカサ・アッカーマン (1개)

상품 ID: 1085

- [進撃の巨人 ミカサ・アッカーマン](https://megahobby.jp/products/item/5626/)

```json
{
  "review_id": "R4193",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4194 — 進撃の巨人 リヴァイ (1개)

상품 ID: 826

- [進撃の巨人 リヴァイ](https://megahobby.jp/products/item/5162/)

```json
{
  "review_id": "R4194",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4195 — 進撃の巨人 リヴァイ お掃除Ver. (1개)

상품 ID: 1087

- [進撃の巨人 リヴァイ お掃除Ver.](https://megahobby.jp/products/item/5628/)

```json
{
  "review_id": "R4195",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4196 — 進撃の巨人 調査兵団マント (1개)

상품 ID: 1084

- [進撃の巨人 調査兵団マント](https://megahobby.jp/products/item/5625/)

```json
{
  "review_id": "R4196",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4197 — 遊☆戯☆王デュエルモンスターズ オシリスの天空竜 (1개)

상품 ID: 537

- [ 遊☆戯☆王デュエルモンスターズ オシリスの天空竜](https://megahobby.jp/products/item/4515/)

```json
{
  "review_id": "R4197",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4198 — 遊☆戯☆王デュエルモンスターズ オベリスクの巨神兵 (1개)

상품 ID: 588

- [ 遊☆戯☆王デュエルモンスターズ オベリスクの巨神兵](https://megahobby.jp/products/item/4620/)

```json
{
  "review_id": "R4198",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4199 — 遊☆戯☆王デュエルモンスターズ ブラック・マジシャン (1개)

상품 ID: 518

- [ 遊☆戯☆王デュエルモンスターズ ブラック・マジシャン](https://megahobby.jp/products/item/4489/)

```json
{
  "review_id": "R4199",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4200 — 遊☆戯☆王デュエルモンスターズ ブラック・マジシャン・ガール (1개)

상품 ID: 284

- [遊☆戯☆王デュエルモンスターズ ブラック・マジシャン・ガール](https://megahobby.jp/products/item/3997/)

```json
{
  "review_id": "R4200",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4201 — 遊☆戯☆王デュエルモンスターズ ラーの翼神竜 (1개)

상품 ID: 676

- [ 遊☆戯☆王デュエルモンスターズ ラーの翼神竜](https://megahobby.jp/products/item/4798/)

```json
{
  "review_id": "R4201",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4202 — 遊☆戯☆王デュエルモンスターズ 真紅眼の黒竜 (1개)

상품 ID: 677

- [ 遊☆戯☆王デュエルモンスターズ 真紅眼の黒竜](https://megahobby.jp/products/item/4799/)

```json
{
  "review_id": "R4202",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4203 — 遊☆戯☆王デュエルモンスターズ 闇遊戯 (1개)

상품 ID: 285

- [遊☆戯☆王デュエルモンスターズ 闇遊戯](https://megahobby.jp/products/item/3998/)

```json
{
  "review_id": "R4203",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4204 — 遊☆戯☆王デュエルモンスターズ 青眼の白龍 (1개)

상품 ID: 589

- [ 遊☆戯☆王デュエルモンスターズ 青眼の白龍](https://megahobby.jp/products/item/4621/)

```json
{
  "review_id": "R4204",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4205 — 重兵装型女子高生 第二分隊 伍 (1개)

상품 ID: 331

- [重兵装型女子高生 第二分隊　伍](https://megahobby.jp/products/item/4106/)

```json
{
  "review_id": "R4205",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4206 — 銀河特急 ミルキー☆サブウェイ (1개)

상품 ID: 1151

- [銀河特急 ミルキー☆サブウェイ](https://megahobby.jp/products/item/5755/)

```json
{
  "review_id": "R4206",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4207 — 銀河特急 ミルキー☆サブウェイ アカネ (1개)

상품 ID: 1308

- [銀河特急 ミルキー☆サブウェイ アカネ](https://megahobby.jp/products/item/6028/)

```json
{
  "review_id": "R4207",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4208 — 銀河特急 ミルキー☆サブウェイ カナタ (1개)

상품 ID: 1307

- [銀河特急 ミルキー☆サブウェイ カナタ](https://megahobby.jp/products/item/6027/)

```json
{
  "review_id": "R4208",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4209 — 銀河特急 ミルキー☆サブウェイ カート (1개)

상품 ID: 1239

- [銀河特急 ミルキー☆サブウェイ カート](https://megahobby.jp/products/item/5874/)

```json
{
  "review_id": "R4209",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4210 — 銀河特急 ミルキー☆サブウェイ チハル (1개)

상품 ID: 1179

- [銀河特急 ミルキー☆サブウェイ チハル](https://megahobby.jp/products/item/5810/)

```json
{
  "review_id": "R4210",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4211 — 銀河特急 ミルキー☆サブウェイ マキナ (1개)

상품 ID: 1180

- [銀河特急 ミルキー☆サブウェイ マキナ](https://megahobby.jp/products/item/5811/)

```json
{
  "review_id": "R4211",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4212 — 銀河特急 ミルキー☆サブウェイ マックス (1개)

상품 ID: 1238

- [銀河特急 ミルキー☆サブウェイ マックス](https://megahobby.jp/products/item/5873/)

```json
{
  "review_id": "R4212",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4213 — 銀魂 YOROZUYA CAFE (1개)

상품 ID: 882

- [銀魂 YOROZUYA CAFE【再販】](https://megahobby.jp/products/item/5281/)

```json
{
  "review_id": "R4213",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4214 — 銀魂×大川ぶくぶ 銀魂 オシャンティ☆アクリルマスコット (1개)

상품 ID: 675

- [銀魂×大川ぶくぶ 銀魂 オシャンティ☆アクリルマスコット【再販】](https://megahobby.jp/products/item/4797/)

```json
{
  "review_id": "R4214",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4215 — 銀魂×大川ぶくぶ 銀魂 銀さん大好き☆コレクション (1개)

상품 ID: 1007

- [銀魂×大川ぶくぶ 銀魂 銀さん大好き☆コレクション](https://megahobby.jp/products/item/5486/)

```json
{
  "review_id": "R4215",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4216 — 銀魂 ちょいと一服しませんか？ (1개)

상품 ID: 119

- [銀魂 ちょいと一服しませんか？【再販】](https://megahobby.jp/products/item/1861/)

```json
{
  "review_id": "R4216",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4217 — 銀魂 てのひら土方さん (1개)

상품 ID: 784

- [銀魂 てのひら土方さん](https://megahobby.jp/products/item/5008/)

```json
{
  "review_id": "R4217",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4218 — 銀魂 てのひら桂さん (1개)

상품 ID: 6159

- [銀魂 てのひら桂さん](https://megahobby.jp/products/item/6189/)

```json
{
  "review_id": "R4218",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4219 — 銀魂 てのひら沖田さん (1개)

상품 ID: 1123

- [銀魂 てのひら沖田さん](https://megahobby.jp/products/item/5707/)

```json
{
  "review_id": "R4219",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4220 — 銀魂 てのひら神楽ちゃん (1개)

상품 ID: 6158

- [銀魂 てのひら神楽ちゃん](https://megahobby.jp/products/item/6190/)

```json
{
  "review_id": "R4220",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4221 — 銀魂 てのひら銀さん (1개)

상품 ID: 759

- [銀魂 てのひら銀さん](https://megahobby.jp/products/item/4977/)

```json
{
  "review_id": "R4221",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4222 — 銀魂 てのひら高杉さん (1개)

상품 ID: 1099

- [銀魂 てのひら高杉さん](https://megahobby.jp/products/item/5640/)

```json
{
  "review_id": "R4222",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4223 — 銀魂 エリザベス (1개)

상품 ID: 1092

- [銀魂 エリザベス](https://megahobby.jp/products/item/5633/)

```json
{
  "review_id": "R4223",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4224 — 銀魂 志村新八 (1개)

상품 ID: 1094

- [銀魂 志村新八](https://megahobby.jp/products/item/5635/)

```json
{
  "review_id": "R4224",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4225 — 銀魂 桂小太郎 (1개)

상품 ID: 1091

- [銀魂 桂小太郎](https://megahobby.jp/products/item/5632/)

```json
{
  "review_id": "R4225",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4226 — 銀魂 神威 (1개)

상품 ID: 824

- [銀魂 神威](https://megahobby.jp/products/item/5160/)

```json
{
  "review_id": "R4226",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4227 — 銀魂 自由すぎる銀魂茶屋 (1개)

상품 ID: 121

- [銀魂 自由すぎる銀魂茶屋【再販】](https://megahobby.jp/products/item/1894/)

```json
{
  "review_id": "R4227",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4228 — 銀魂 高杉晋助 (1개)

상품 ID: 825

- [銀魂 高杉晋助](https://megahobby.jp/products/item/5161/)

```json
{
  "review_id": "R4228",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4229 — 鋼の錬金術師 FULLMETAL ALCHEMIST エドワード・エルリック (1개)

상품 ID: 1272

- [鋼の錬金術師 FULLMETAL ALCHEMIST エドワード・エルリック](https://megahobby.jp/products/item/5956/)

```json
{
  "review_id": "R4229",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4230 — 鋼の錬金術師 FULLMETAL ALCHEMIST ロイ・マスタング (1개)

상품 ID: 1271

- [鋼の錬金術師 FULLMETAL ALCHEMIST ロイ・マスタング](https://megahobby.jp/products/item/5955/)

```json
{
  "review_id": "R4230",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4231 — 鏡音リン (1개)

상품 ID: 981

- [鏡音リン](https://megahobby.jp/products/item/5433/)

```json
{
  "review_id": "R4231",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4232 — 鏡音レン (1개)

상품 ID: 980

- [鏡音レン](https://megahobby.jp/products/item/5432/)

```json
{
  "review_id": "R4232",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4233 — 鬼滅の刃 (1개)

상품 ID: 1044

- [鬼滅の刃【再販】](https://megahobby.jp/products/item/5559/)

```json
{
  "review_id": "R4233",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4234 — 鬼滅の刃 てのひら宇髄さん (1개)

상품 ID: 159

- [鬼滅の刃 てのひら宇髄さん](https://megahobby.jp/products/item/3667/)

```json
{
  "review_id": "R4234",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4235 — 鬼滅の刃 てのひら悲鳴嶼さん (1개)

상품 ID: 229

- [鬼滅の刃 てのひら悲鳴嶼さん](https://megahobby.jp/products/item/3861/)

```json
{
  "review_id": "R4235",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4236 — 鬼滅の刃 てのひら義勇さん (1개)

상품 ID: 1147

- [鬼滅の刃 てのひら義勇さん【再販】](https://megahobby.jp/products/item/5751/)

```json
{
  "review_id": "R4236",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4237 — 鬼滅の刃 不死川実弥 (1개)

상품 ID: 851

- [鬼滅の刃 不死川実弥【再販】](https://megahobby.jp/products/item/5219/)

```json
{
  "review_id": "R4237",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4238 — 鬼滅の刃 伊黒小芭内 (1개)

상품 ID: 920

- [鬼滅の刃 伊黒小芭内【再販】](https://megahobby.jp/products/item/5336/)

```json
{
  "review_id": "R4238",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4239 — 鬼滅の刃 冨岡義勇 (1개)

상품 ID: 128

- [鬼滅の刃 冨岡義勇【再販】](https://megahobby.jp/products/item/3464/)

```json
{
  "review_id": "R4239",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4240 — 鬼滅の刃 嘴平伊之助 (1개)

상품 ID: 197

- [鬼滅の刃 嘴平伊之助【再販】](https://megahobby.jp/products/item/3785/)

```json
{
  "review_id": "R4240",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4241 — 鬼滅の刃 宇髄天元 (1개)

상품 ID: 145

- [鬼滅の刃 宇髄天元](https://megahobby.jp/products/item/3631/)

```json
{
  "review_id": "R4241",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4242 — 鬼滅の刃 宇髄天元 元音柱ver. (1개)

상품 ID: 1244

- [鬼滅の刃 宇髄天元　元音柱ver.](https://megahobby.jp/products/item/5879/)

```json
{
  "review_id": "R4242",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4243 — 鬼滅の刃 恋雪 (1개)

상품 ID: 1269

- [鬼滅の刃 恋雪](https://megahobby.jp/products/item/5953/)

```json
{
  "review_id": "R4243",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4244 — 鬼滅の刃 我妻善逸 (1개)

상품 ID: 198

- [鬼滅の刃 我妻善逸【再販】](https://megahobby.jp/products/item/3786/)

```json
{
  "review_id": "R4244",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4245 — 鬼滅の刃 時透無一郎 (1개)

상품 ID: 275

- [鬼滅の刃 時透無一郎【再販】](https://megahobby.jp/products/item/3988/)

```json
{
  "review_id": "R4245",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4246 — 鬼滅の刃 栗花落カナヲ (1개)

상품 ID: 134

- [鬼滅の刃 栗花落カナヲ【再販】](https://megahobby.jp/products/item/3540/)

```json
{
  "review_id": "R4246",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4247 — 鬼滅の刃 炭治郎と仲間たちマスコットコレクション【1】 (1개)

상품 ID: 1042

- [鬼滅の刃 炭治郎と仲間たちマスコットコレクション【1】](https://megahobby.jp/products/item/5557/)

```json
{
  "review_id": "R4247",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4248 — 鬼滅の刃 炭治郎と仲間たちマスコットコレクション【2】 (1개)

상품 ID: 1041

- [ 鬼滅の刃 炭治郎と仲間たちマスコットコレクション【2】](https://megahobby.jp/products/item/5556/)

```json
{
  "review_id": "R4248",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4249 — 鬼滅の刃 煉獄杏寿郎 (1개)

상품 ID: 135

- [鬼滅の刃 煉獄杏寿郎【再販】](https://megahobby.jp/products/item/3541/)

```json
{
  "review_id": "R4249",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4250 — 鬼滅の刃 狛治 (1개)

상품 ID: 1270

- [鬼滅の刃 狛治](https://megahobby.jp/products/item/5954/)

```json
{
  "review_id": "R4250",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4251 — 鬼滅の刃 猗窩座 (1개)

상품 ID: 927

- [鬼滅の刃 猗窩座](https://megahobby.jp/products/item/5343/)

```json
{
  "review_id": "R4251",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4252 — 鬼滅の刃 玄弥 (1개)

상품 ID: 1035

- [鬼滅の刃 玄弥【再販】](https://megahobby.jp/products/item/5536/)

```json
{
  "review_id": "R4252",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4253 — 鬼滅の刃 甘露寺蜜璃 (1개)

상품 ID: 276

- [鬼滅の刃 甘露寺蜜璃【再販】](https://megahobby.jp/products/item/3989/)

```json
{
  "review_id": "R4253",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4254 — 鬼滅の刃 竈門炭治郎 (1개)

상품 ID: 200

- [鬼滅の刃 竈門炭治郎【再販】](https://megahobby.jp/products/item/3788/)

```json
{
  "review_id": "R4254",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4255 — 鬼滅の刃 竈門炭治郎 きりっとver. (1개)

상품 ID: 483

- [鬼滅の刃 竈門炭治郎 きりっとver.](https://megahobby.jp/products/item/4405/)

```json
{
  "review_id": "R4255",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4256 — 鬼滅の刃 竈門炭治郎 最終選別ver. (1개)

상품 ID: 1106

- [鬼滅の刃 竈門炭治郎 最終選別ver.【再販】](https://megahobby.jp/products/item/5689/)

```json
{
  "review_id": "R4256",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4257 — 鬼滅の刃 竈門禰豆子 (1개)

상품 ID: 199

- [鬼滅の刃 竈門禰豆子【再販】](https://megahobby.jp/products/item/3787/)

```json
{
  "review_id": "R4257",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4258 — 鬼滅の刃 竈門禰豆子 太陽克服ver. (1개)

상품 ID: 482

- [鬼滅の刃 竈門禰豆子 太陽克服ver.](https://megahobby.jp/products/item/4404/)

```json
{
  "review_id": "R4258",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4259 — 鬼滅の刃 胡蝶しのぶ (1개)

상품 ID: 129

- [鬼滅の刃 胡蝶しのぶ【再販】](https://megahobby.jp/products/item/3465/)

```json
{
  "review_id": "R4259",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4260 — 鬼滅の刃 胡蝶しのぶ にっこりver. (1개)

상품 ID: 957

- [鬼滅の刃 胡蝶しのぶ にっこりver.](https://megahobby.jp/products/item/5405/)

```json
{
  "review_id": "R4260",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4261 — 鬼滅の刃 鬼滅の刃ニャンコ招き猫ver.壱 (1개)

상품 ID: 1083

- [鬼滅の刃 鬼滅の刃ニャンコ招き猫ver.壱](https://megahobby.jp/products/item/5624/)

```json
{
  "review_id": "R4261",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4262 — 鬼滅の刃 鬼滅の刃ニャンコ招き猫ver.弐 (1개)

상품 ID: 1115

- [鬼滅の刃 鬼滅の刃ニャンコ招き猫ver.弐](https://megahobby.jp/products/item/5699/)

```json
{
  "review_id": "R4262",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4263 — 魔入りました！入間くん オペラ (1개)

상품 ID: 1311

- [魔入りました！入間くん オペラ](https://megahobby.jp/products/item/6031/)

```json
{
  "review_id": "R4263",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4264 — 魔入りました！入間くん 鈴木入間 (1개)

상품 ID: 1312

- [魔入りました！入間くん 鈴木入間](https://megahobby.jp/products/item/6032/)

```json
{
  "review_id": "R4264",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4265 — 魔法少女にあこがれて てのひら マジアベーゼ (1개)

상품 ID: 674

- [ 魔法少女にあこがれて てのひら マジアベーゼ](https://megahobby.jp/products/item/4796/)

```json
{
  "review_id": "R4265",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4266 — 魔法少女まどか☆マギカ 暁美ほむら (1개)

상품 ID: 1177

- [魔法少女まどか☆マギカ 暁美ほむら](https://megahobby.jp/products/item/5808/)

```json
{
  "review_id": "R4266",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4267 — 魔法少女まどか☆マギカ 鹿目まどか (1개)

상품 ID: 1176

- [魔法少女まどか☆マギカ 鹿目まどか](https://megahobby.jp/products/item/5807/)

```json
{
  "review_id": "R4267",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4268 — 가이아 영웅용상 울트라맨 가이아 스프림 버전 (1개)

상품 ID: 4571

- [울트라맨 가이아 영웅용상 울트라맨 가이아 스프림 버전](https://www.bnkrmall.co.kr/goods/detail.do?gno=56584)

```json
{
  "review_id": "R4268",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4269 — 개구리 중사 케로로 히나타 가 청소 대작전 vol.1 (A.케로로) (1개)

상품 ID: 3431

- [개구리 중사 케로로 피규어 히나타 가 청소 대작전 vol.1 (A.케로로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=52272224)

```json
{
  "review_id": "R4269",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4270 — 개구리 중사 케로로 히나타 가 청소 대작전 vol.1 (B.기로로) (1개)

상품 ID: 3430

- [개구리 중사 케로로 피규어 히나타 가 청소 대작전 vol.1 (B.기로로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=69789401)

```json
{
  "review_id": "R4270",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4271 — 개구리 중사 케로로 히나타 가 청소 대작전 vol.2 (A.타마마) (1개)

상품 ID: 3429

- [개구리 중사 케로로 피규어 히나타 가 청소 대작전 vol.2 (A.타마마)](https://www.bnkrmall.co.kr/goods/detail.do?gno=93424136)

```json
{
  "review_id": "R4271",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4272 — 개구리 중사 케로로 히나타 가 청소 대작전 vol.2 (B.쿠루루) (1개)

상품 ID: 3428

- [개구리 중사 케로로 피규어 히나타 가 청소 대작전 vol.2 (B.쿠루루)](https://www.bnkrmall.co.kr/goods/detail.do?gno=68667493)

```json
{
  "review_id": "R4272",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4273 — 개구리 중사 케로로 히나타 가 청소 대작전 vol.3 (A.도로로) (1개)

상품 ID: 3403

- [개구리 중사 케로로 피규어 히나타 가 청소 대작전 vol.3 (A.도로로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=85746970)

```json
{
  "review_id": "R4273",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4274 — 개구리 중사 케로로 히나타 가 청소 대작전 vol.3 (B.케로로) (1개)

상품 ID: 3402

- [개구리 중사 케로로 피규어 히나타 가 청소 대작전 vol.3 (B.케로로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=10550296)

```json
{
  "review_id": "R4274",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4275 — 건담45주년× BANPRESTO EVOLV 건담 콜라보레이션 (1개)

상품 ID: 2531

- [건담45주년×하츠네 미쿠 BANPRESTO EVOLV 건담 콜라보레이션 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=26891967)

```json
{
  "review_id": "R4275",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4276 — 건담45주년× 샤아 자쿠 코스튬 하츠네 미쿠Ver. (1개)

상품 ID: 3658

- [건담45주년×하츠네 미쿠 샤아 자쿠 코스튬 하츠네 미쿠Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=70687085)

```json
{
  "review_id": "R4276",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4277 — 건담45주년× 자쿠 코스튬 하츠네 미쿠Ver. (1개)

상품 ID: 3778

- [건담45주년×하츠네 미쿠 자쿠 코스튬 하츠네 미쿠Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=59222400)

```json
{
  "review_id": "R4277",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4278 — 건담× #HOLOLIVE IF 유니콘 건담×우사다 페코라(누이 아머 Ver.) (1개)

상품 ID: 3308

- [건담×홀로라이브 프로덕션 #HOLOLIVE IF 유니콘 건담×우사다 페코라(누이 아머 Ver.) 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=28333207)

```json
{
  "review_id": "R4278",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4279 — 건담× #HOLOLIVE IF 크로스본 건담 X1×호쇼 마린(누이 아머 Ver.) (1개)

상품 ID: 3309

- [건담×홀로라이브 프로덕션 #HOLOLIVE IF 크로스본 건담 X1×호쇼 마린(누이 아머 Ver.) 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=18023465)

```json
{
  "review_id": "R4279",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4280 — 걸즈 앤 판처 최종장 이터널 로맨스 니시즈미 마호 메이드 수영복 ver. (1개)

상품 ID: 3396

- [걸즈 앤 판처 최종장 이터널 로맨스 니시즈미 마호 메이드 수영복 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=2977917)

```json
{
  "review_id": "R4280",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4281 — 걸즈 앤 판처 최종장 이터널 로맨스 니시즈미 미호 메이드 수영복 ver. (1개)

상품 ID: 3397

- [걸즈 앤 판처 최종장 이터널 로맨스 니시즈미 미호 메이드 수영복 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=40421399)

```json
{
  "review_id": "R4281",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4282 — 걸즈 앤 판처 최종장 이터널 로맨스 니시즈미 시호 메이드 수영복 ver. (1개)

상품 ID: 3303

- [걸즈 앤 판처 최종장 이터널 로맨스 니시즈미 시호 메이드 수영복 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=92047893)

```json
{
  "review_id": "R4282",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4283 — 계왕신(미니) 패널 (1개)

상품 ID: 4057

- [드래곤볼 DAIMA 계왕신(미니) 패널 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=66808085)

```json
{
  "review_id": "R4283",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4284 — 고마 패널 (1개)

상품 ID: 4078

- [드래곤볼 DAIMA 고마 패널 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=12659635)

```json
{
  "review_id": "R4284",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4285 — 고죠 사토루 (1개)

상품 ID: 4632

- [주술회전 고죠 사토루](https://www.bnkrmall.co.kr/goods/detail.do?gno=55275)

```json
{
  "review_id": "R4285",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4286 — 구엘 제타크 (1개)

상품 ID: 4203

- [기동전사 건담 수성의 마녀 구엘 제타크 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=56043960)

```json
{
  "review_id": "R4286",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4287 — 군단 출진 울트라 하이퍼 고양이 축제 요수 가루 (1개)

상품 ID: 3831

- [냥코 대전쟁 군단 출진 피규어 울트라 하이퍼 고양이 축제 요수 가루](https://www.bnkrmall.co.kr/goods/detail.do?gno=61340586)

```json
{
  "review_id": "R4287",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4288 — 그랜드라인 걸즈 온 베케이션 니코 로빈 VER.A (1개)

상품 ID: 4407

- [원피스 그랜드라인 걸즈 온 베케이션 니코 로빈 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=59526)

```json
{
  "review_id": "R4288",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4289 — 그랜드라인 걸즈 온 베케이션 보아 핸콕 VER.A (1개)

상품 ID: 4476

- [원피스 그랜드라인 걸즈 온 베케이션 보아 핸콕 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=58568)

```json
{
  "review_id": "R4289",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4290 — 그랜드라인 저니 나미 (1개)

상품 ID: 4605

- [원피스 그랜드라인 저니 나미](https://www.bnkrmall.co.kr/goods/detail.do?gno=56066)

```json
{
  "review_id": "R4290",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4291 — 그랜드라인 저니 보아 핸콕 (1개)

상품 ID: 4618

- [원피스 그랜드라인 저니 보아 핸콕](https://www.bnkrmall.co.kr/goods/detail.do?gno=55744)

```json
{
  "review_id": "R4291",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4292 — 그랜드라인 저니 스페셜 (A:나미) (1개)

상품 ID: 3689

- [원피스 그랜드라인 저니 스페셜 (A:나미)](https://www.bnkrmall.co.kr/goods/detail.do?gno=70063136)

```json
{
  "review_id": "R4292",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4293 — 그랜드라인 저니 스페셜 (B:보아 핸콕) (1개)

상품 ID: 3687

- [원피스 그랜드라인 저니 스페셜 (B:보아 핸콕)](https://www.bnkrmall.co.kr/goods/detail.do?gno=22420535)

```json
{
  "review_id": "R4293",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4294 — 극장판 (신편) 반역의 이야기 BANPRESTO EVOLVE 악마 호무라 (1개)

상품 ID: 2614

- [극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 BANPRESTO EVOLVE 악마 호무라 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=27852521)

```json
{
  "review_id": "R4294",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4295 — 극장판 (신편) 반역의 이야기 BANPRESTO EVOLVE 얼티밋 마도카 (1개)

상품 ID: 2615

- [극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 BANPRESTO EVOLVE 얼티밋 마도카 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=15510298)

```json
{
  "review_id": "R4295",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4296 — 극장판 0 MAXIMATIC 옷코츠 유타 (1개)

상품 ID: 4002

- [극장판 주술회전 0 MAXIMATIC 옷코츠 유타](https://www.bnkrmall.co.kr/goods/detail.do?gno=27281533)

```json
{
  "review_id": "R4296",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4297 — 극장판 0 고죠 사토루 (1개)

상품 ID: 4593

- [극장판 주술회전 0 고죠 사토루](https://www.bnkrmall.co.kr/goods/detail.do?gno=56286)

```json
{
  "review_id": "R4297",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4298 — 극장판 레제편 -BOMB (1개)

상품 ID: 3871

- [극장판 체인소 맨 레제편 -BOMB-](https://www.bnkrmall.co.kr/goods/detail.do?gno=56292552)

```json
{
  "review_id": "R4298",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4299 — 극장판 레제편 -CHAINSAW MAN (1개)

상품 ID: 3872

- [극장판 체인소 맨 레제편 -CHAINSAW MAN-](https://www.bnkrmall.co.kr/goods/detail.do?gno=95738012)

```json
{
  "review_id": "R4299",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4300 — 극장판 레제편 BIG SOFVIMATES 포치타 (1개)

상품 ID: 3270

- [극장판 체인소 맨 레제편 BIG SOFVIMATES 포치타](https://www.bnkrmall.co.kr/goods/detail.do?gno=36860840)

```json
{
  "review_id": "R4300",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4301 — 극장판 레제편 Fluffy Puffy 댄싱 포치타 (ver.A) (1개)

상품 ID: 3595

- [극장판 체인소 맨 레제편 Fluffy Puffy 댄싱 포치타 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=96557438)

```json
{
  "review_id": "R4301",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4302 — 극장판 레제편 Fluffy Puffy 댄싱 포치타 (ver.B) (1개)

상품 ID: 3594

- [극장판 체인소 맨 레제편 Fluffy Puffy 댄싱 포치타 (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=96185476)

```json
{
  "review_id": "R4302",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4303 — 극장판 레제편 MAXIMATIC BOMB (1개)

상품 ID: 3592

- [극장판 체인소 맨 레제편 MAXIMATIC BOMB](https://www.bnkrmall.co.kr/goods/detail.do?gno=94939581)

```json
{
  "review_id": "R4303",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4304 — 극장판 레제편 MAXIMATIC 체인소 맨 (1개)

상품 ID: 3593

- [극장판 체인소 맨 레제편 MAXIMATIC 체인소 맨](https://www.bnkrmall.co.kr/goods/detail.do?gno=47573767)

```json
{
  "review_id": "R4304",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4305 — 극장판 레제편 Noir Edge Collection 체인소 맨 (1개)

상품 ID: 3608

- [극장판 체인소 맨 레제편 Noir Edge Collection 체인소 맨](https://www.bnkrmall.co.kr/goods/detail.do?gno=36565101)

```json
{
  "review_id": "R4305",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4306 — 극장판 레제편 피그라이프 빔 (1개)

상품 ID: 3540

- [극장판 체인소 맨 레제편 피그라이프 빔](https://www.bnkrmall.co.kr/goods/detail.do?gno=90952600)

```json
{
  "review_id": "R4306",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4307 — 극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 Fluffy Puffy 큐베&과자의 마녀 (A:큐베) (1개)

상품 ID: 3649

- [극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 Fluffy Puffy 큐베&과자의 마녀 (A:큐베)](https://www.bnkrmall.co.kr/goods/detail.do?gno=27507923)

```json
{
  "review_id": "R4307",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4308 — 극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 Fluffy Puffy 큐베&과자의 마녀 (B:과자의 마녀) (1개)

상품 ID: 3648

- [극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 Fluffy Puffy 큐베&과자의 마녀 (B:과자의 마녀)](https://www.bnkrmall.co.kr/goods/detail.do?gno=51979802)

```json
{
  "review_id": "R4308",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4309 — 극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 미키 사야카 (1개)

상품 ID: 3558

- [극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 미키 사야카 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=95468094)

```json
{
  "review_id": "R4309",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4310 — 극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 사쿠라 쿄코 (1개)

상품 ID: 3557

- [극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 사쿠라 쿄코 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=82671465)

```json
{
  "review_id": "R4310",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4311 — 극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 아케미 호무라 (1개)

상품 ID: 3568

- [극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 아케미 호무라 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=7129326)

```json
{
  "review_id": "R4311",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4312 — 극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 카나메 마도카 (1개)

상품 ID: 3569

- [극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 카나메 마도카 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=38755953)

```json
{
  "review_id": "R4312",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4313 — 극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 토모에 마미 (1개)

상품 ID: 3567

- [극장판 마법소녀 마도카 마기카(신편) 반역의 이야기 토모에 마미 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=88190527)

```json
{
  "review_id": "R4313",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4314 — 극장판 마법소녀 마도카 마기카 발푸르기스의 회천 Fluffy Puffy BIG 큐베 (1개)

상품 ID: 3575

- [극장판 마법소녀 마도카 마기카 발푸르기스의 회천 Fluffy Puffy BIG 큐베](https://www.bnkrmall.co.kr/goods/detail.do?gno=88690218)

```json
{
  "review_id": "R4314",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4315 — 극장판 마법소녀 마도카 마기카 발푸르기스의 회천 모모에 나기사 (1개)

상품 ID: 3239

- [극장판 마법소녀 마도카 마기카 발푸르기스의 회천 모모에 나기사 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=82862055)

```json
{
  "review_id": "R4315",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4316 — 극장판 마법소녀 마도카 마기카 발푸르기스의 회천 미키 사야카 (1개)

상품 ID: 3257

- [극장판 마법소녀 마도카 마기카 발푸르기스의 회천 미키 사야카 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=10845136)

```json
{
  "review_id": "R4316",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4317 — 극장판 마법소녀 마도카 마기카 발푸르기스의 회천 사쿠라 쿄코 (1개)

상품 ID: 3255

- [극장판 마법소녀 마도카 마기카 발푸르기스의 회천 사쿠라 쿄코 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=82953282)

```json
{
  "review_id": "R4317",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4318 — 극장판 마법소녀 마도카 마기카 발푸르기스의 회천 아케미 호무라 (1개)

상품 ID: 3258

- [극장판 마법소녀 마도카 마기카 발푸르기스의 회천 아케미 호무라 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=76975032)

```json
{
  "review_id": "R4318",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4319 — 극장판 마법소녀 마도카 마기카 발푸르기스의 회천 아케미 호무라 ii (1개)

상품 ID: 3374

- [극장판 마법소녀 마도카 마기카 발푸르기스의 회천 아케미 호무라 피규어 ii](https://www.bnkrmall.co.kr/goods/detail.do?gno=85351255)

```json
{
  "review_id": "R4319",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4320 — 극장판 마법소녀 마도카 마기카 발푸르기스의 회천 카나메 마도카 (1개)

상품 ID: 3259

- [극장판 마법소녀 마도카 마기카 발푸르기스의 회천 카나메 마도카 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=82904544)

```json
{
  "review_id": "R4320",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4321 — 극장판 마법소녀 마도카 마기카 발푸르기스의 회천 카나메 마도카 ii (1개)

상품 ID: 3375

- [극장판 마법소녀 마도카 마기카 발푸르기스의 회천 카나메 마도카 피규어 ii](https://www.bnkrmall.co.kr/goods/detail.do?gno=20550949)

```json
{
  "review_id": "R4321",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4322 — 극장판 마법소녀 마도카 마기카 발푸르기스의 회천 토모에 마미 (1개)

상품 ID: 3256

- [극장판 마법소녀 마도카 마기카 발푸르기스의 회천 토모에 마미 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=11058575)

```json
{
  "review_id": "R4322",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4323 — 극장판 시티헌터 천사의 눈물(엔젤 더스트) 마키무라 카오리 (1개)

상품 ID: 4006

- [극장판 시티헌터 천사의 눈물(엔젤 더스트) 마키무라 카오리](https://www.bnkrmall.co.kr/goods/detail.do?gno=51281298)

```json
{
  "review_id": "R4323",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4324 — 극장판 시티헌터 천사의 눈물(엔젤 더스트) 사에바 료 (1개)

상품 ID: 4007

- [극장판 시티헌터 천사의 눈물(엔젤 더스트) 사에바 료](https://www.bnkrmall.co.kr/goods/detail.do?gno=31311376)

```json
{
  "review_id": "R4324",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4325 — 극장판 쓰레기장의 결전 (1개)

상품 ID: 3972

- [극장판 하이큐!! 쓰레기장의 결전 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=98009049)

```json
{
  "review_id": "R4325",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4326 — 극장판 청해의 눈물편 리무루 BIG 소프비 (1개)

상품 ID: 3621

- [극장판 전생했더니 슬라임이었던 건에 대하여 청해의 눈물편 리무루 BIG 소프비 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=40156268)

```json
{
  "review_id": "R4326",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4327 — 극장판 청해의 눈물편 마왕 리무루 템페스트 (1개)

상품 ID: 3637

- [극장판 전생했더니 슬라임이었던 건에 대하여 청해의 눈물편 마왕 리무루 템페스트 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=27697798)

```json
{
  "review_id": "R4327",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4328 — 글로리오 패널 (1개)

상품 ID: 3983

- [드래곤볼 DAIMA 글로리오 패널 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=3542665)

```json
{
  "review_id": "R4328",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4329 — 기동문구 자동변형 명함 케이스 블랙 컬러 (1개)

상품 ID: 1674

- [기동문구 자동변형 명함 케이스 블랙 컬러](https://www.bnkrmall.co.kr/goods/detail.do?gno=24415732)

```json
{
  "review_id": "R4329",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4330 — 기동문구 자동변형 명함 케이스 스탠다드 컬러 (1개)

상품 ID: 1675

- [기동문구 자동변형 명함 케이스 스탠다드 컬러](https://www.bnkrmall.co.kr/goods/detail.do?gno=66386296)

```json
{
  "review_id": "R4330",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4331 — 기동문구 자동변형 명함 케이스 토이 컬러 (1개)

상품 ID: 1676

- [기동문구 자동변형 명함 케이스 토이 컬러](https://www.bnkrmall.co.kr/goods/detail.do?gno=14015231)

```json
{
  "review_id": "R4331",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4332 — 기동전사 Gundam GQuuuuuuX 냐안 (1개)

상품 ID: 3803

- [기동전사 Gundam GQuuuuuuX 냐안 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=54220475)

```json
{
  "review_id": "R4332",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4333 — 기동전사 Gundam GQuuuuuuX 냐안 사복 Ver. (1개)

상품 ID: 3775

- [기동전사 Gundam GQuuuuuuX 냐안 피규어 사복 Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=14731010)

```json
{
  "review_id": "R4333",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4334 — 기동전사 Gundam GQuuuuuuX 슈우지 이토 (1개)

상품 ID: 3813

- [기동전사 Gundam GQuuuuuuX 슈우지 이토](https://www.bnkrmall.co.kr/goods/detail.do?gno=71708750)

```json
{
  "review_id": "R4334",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4335 — 기동전사 Gundam GQuuuuuuX 아마테 유즈리하(마츄) (1개)

상품 ID: 3843

- [기동전사 Gundam GQuuuuuuX 아마테 유즈리하(마츄) 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=96345136)

```json
{
  "review_id": "R4335",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4336 — 기동전사 Gundam GQuuuuuuX 아마테 유즈리하(마츄) 사복 Ver. (1개)

상품 ID: 3776

- [기동전사 Gundam GQuuuuuuX 아마테 유즈리하(마츄) 피규어 사복 Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=60891209)

```json
{
  "review_id": "R4336",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4337 — 기동전사 Gundam GQuuuuuuX 아마테 유즈리하(마츄) 파일럿 슈트VER. (1개)

상품 ID: 3804

- [기동전사 Gundam GQuuuuuuX 아마테 유즈리하(마츄) 피규어 파일럿 슈트VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=12974632)

```json
{
  "review_id": "R4337",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4338 — 기동전사 Gundam GQuuuuuuX 한계돌파 GFreD (지프레드) (1개)

상품 ID: 3805

- [기동전사 Gundam GQuuuuuuX 한계돌파 GFreD (지프레드)](https://www.bnkrmall.co.kr/goods/detail.do?gno=82322813)

```json
{
  "review_id": "R4338",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4339 — 기동전사 Gundam GQuuuuuuX 한계돌파 GQuuuuuuX (오메가 사이코뮤 기동 전) (1개)

상품 ID: 3777

- [기동전사 Gundam GQuuuuuuX 한계돌파 GQuuuuuuX (오메가 사이코뮤 기동 전)](https://www.bnkrmall.co.kr/goods/detail.do?gno=99430861)

```json
{
  "review_id": "R4339",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4340 — 기동전사 Gundam GQuuuuuuX 한계돌파 GQuuuuuuX (지쿠악스) (1개)

상품 ID: 3844

- [기동전사 Gundam GQuuuuuuX 한계돌파 GQuuuuuuX (지쿠악스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=13971020)

```json
{
  "review_id": "R4340",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4341 — 기동전사 Gundam GQuuuuuuX 한계돌파 붉은 건담 (1개)

상품 ID: 3814

- [기동전사 Gundam GQuuuuuuX 한계돌파 붉은 건담](https://www.bnkrmall.co.kr/goods/detail.do?gno=20849428)

```json
{
  "review_id": "R4341",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4342 — 기동전사 Gundam GQuuuuuuX 한계돌파 하얀 건담 (1개)

상품 ID: 3791

- [기동전사 Gundam GQuuuuuuX 한계돌파 하얀 건담](https://www.bnkrmall.co.kr/goods/detail.do?gno=87480050)

```json
{
  "review_id": "R4342",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4343 — 기동전사 Z건담 포우 무라사메 VER.A (1개)

상품 ID: 4333

- [기동전사 Z건담 포우 무라사메 피규어 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=91033565)

```json
{
  "review_id": "R4343",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4344 — 길드의 접수원인데, 야근이 싫어서 보스를 혼자 토벌하려고 합니다 아리나 클로버 (1개)

상품 ID: 4034

- [길드의 접수원인데, 야근이 싫어서 보스를 혼자 토벌하려고 합니다 아리나 클로버](https://www.bnkrmall.co.kr/goods/detail.do?gno=98491561)

```json
{
  "review_id": "R4344",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4345 — 나루토 콜로세움 록 리 (1개)

상품 ID: 2929

- [나루토 반프레스토 피규어 콜로세움 록 리](https://www.bnkrmall.co.kr/goods/detail.do?gno=49738473)

```json
{
  "review_id": "R4345",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4346 — 나루토 콜로세움 우즈마키 나루토 (1개)

상품 ID: 2886

- [나루토 반프레스토 피규어 콜로세움 우즈마키 나루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=11839495)

```json
{
  "review_id": "R4346",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4347 — 나루토 콜로세움 츠나데 (1개)

상품 ID: 2942

- [나루토 반프레스토 피규어 콜로세움 츠나데](https://www.bnkrmall.co.kr/goods/detail.do?gno=96030092)

```json
{
  "review_id": "R4347",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4348 — 나루톱99 나미카제 미나토 (1개)

상품 ID: 4193

- [나루토 나루톱99 나미카제 미나토 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=5174726)

```json
{
  "review_id": "R4348",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4349 — 나루톱99 우즈마키 나루토 (1개)

상품 ID: 4280

- [나루토 나루톱99 우즈마키 나루토 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=40310642)

```json
{
  "review_id": "R4349",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4350 — 나루톱99 우치하 시스이 (1개)

상품 ID: 4247

- [나루토 나루톱99 우치하 시스이 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=14076389)

```json
{
  "review_id": "R4350",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4351 — 나루톱99 우치하 이타치 (1개)

상품 ID: 4224

- [나루토 나루톱99 우치하 이타치 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=54561611)

```json
{
  "review_id": "R4351",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4352 — 나루톱99 하루노 사쿠라 (1개)

상품 ID: 4237

- [나루토 나루톱99 하루노 사쿠라 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=78259886)

```json
{
  "review_id": "R4352",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4353 — 나루톱99 하타케 카카시 (1개)

상품 ID: 4265

- [나루토 나루톱99 하타케 카카시 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=81139980)

```json
{
  "review_id": "R4353",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4354 — 나이스 서브!! (A: 히나타 쇼요) (1개)

상품 ID: 3363

- [하이큐!! 피규어 나이스 서브!! (A: 히나타 쇼요)](https://www.bnkrmall.co.kr/goods/detail.do?gno=28993029)

```json
{
  "review_id": "R4354",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4355 — 나이스 서브!! (B: 니시노야 유) (1개)

상품 ID: 3364

- [하이큐!! 피규어 나이스 서브!! (B: 니시노야 유)](https://www.bnkrmall.co.kr/goods/detail.do?gno=63241522)

```json
{
  "review_id": "R4355",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4356 — 나이스 서브!! (C: 스가와라 코시) (1개)

상품 ID: 3362

- [하이큐!! 피규어 나이스 서브!! (C: 스가와라 코시)](https://www.bnkrmall.co.kr/goods/detail.do?gno=1957452)

```json
{
  "review_id": "R4356",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4357 — 나츠메 우인장 BIG SOFVIMATES 냥코 센세 (1개)

상품 ID: 3435

- [나츠메 우인장 BIG SOFVIMATES 냥코 센세](https://www.bnkrmall.co.kr/goods/detail.do?gno=76851249)

```json
{
  "review_id": "R4357",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4358 — 나카노 니노 Animation Original Art Exhibition ver. (1개)

상품 ID: 3876

- [5등분의 신부 나카노 니노 Animation Original Art Exhibition ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=61814168)

```json
{
  "review_id": "R4358",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4359 — 나카노 미쿠 애니메이션 원화전 ver. (1개)

상품 ID: 3849

- [5등분의 신부 나카노 미쿠 피규어 애니메이션 원화전 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=26984541)

```json
{
  "review_id": "R4359",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4360 — 나카노 요츠바 애니메이션 원화전 ver. (1개)

상품 ID: 3848

- [5등분의 신부 나카노 요츠바 피규어 애니메이션 원화전 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=77909062)

```json
{
  "review_id": "R4360",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4361 — 나카노 이츠카 Animation Original Art Exhibition ver. (1개)

상품 ID: 3877

- [5등분의 신부 나카노 이츠카 Animation Original Art Exhibition ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=42594920)

```json
{
  "review_id": "R4361",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4362 — 나카노 이츠키 Animation Original Art Exhibition ver. (1개)

상품 ID: 3821

- [5등분의 신부 나카노 이츠키 Animation Original Art Exhibition ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=62003460)

```json
{
  "review_id": "R4362",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4363 — 냐안 & 콘치 엔딩 ver. (1개)

상품 ID: 3422

- [기동전사 건담 GQuuuuuuX 냐안 & 콘치 피규어 엔딩 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=52865449)

```json
{
  "review_id": "R4363",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4364 — 냥코 군단 출진 VOL.1 (1개)

상품 ID: 4018

- [냥코 대전쟁 냥코 군단 출진 피규어 VOL.1](https://www.bnkrmall.co.kr/goods/detail.do?gno=21089368)

```json
{
  "review_id": "R4364",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4365 — 냥코 군단 출진 VOL.2 (1개)

상품 ID: 4017

- [냥코 대전쟁 냥코 군단 출진 피규어 VOL.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=8981418)

```json
{
  "review_id": "R4365",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4366 — 냥코 군단 출진 VOL.3 (1개)

상품 ID: 3967

- [냥코 대전쟁 냥코 군단 출진 피규어 VOL.3](https://www.bnkrmall.co.kr/goods/detail.do?gno=27364670)

```json
{
  "review_id": "R4366",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4367 — 냥코 군단 출진 VOL.4 (1개)

상품 ID: 3966

- [냥코 대전쟁 냥코 군단 출진 피규어 VOL.4](https://www.bnkrmall.co.kr/goods/detail.do?gno=45323642)

```json
{
  "review_id": "R4367",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4368 — 냥코 군단 출진 고양이 무트 (1개)

상품 ID: 3704

- [냥코 대전쟁 냥코 군단 출진 피규어 고양이 무트](https://www.bnkrmall.co.kr/goods/detail.do?gno=92553123)

```json
{
  "review_id": "R4368",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4369 — 냥코 군단 출진 냥코 성 (1개)

상품 ID: 3635

- [냥코 대전쟁 냥코 군단 출진 피규어 냥코 성](https://www.bnkrmall.co.kr/goods/detail.do?gno=12091526)

```json
{
  "review_id": "R4369",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4370 — 냥코 군단 출진 울트라 하이퍼 고양이 축제 무희 이즈 (1개)

상품 ID: 3809

- [냥코 대전쟁 냥코 군단 출진 피규어 울트라 하이퍼 고양이 축제 무희 이즈](https://www.bnkrmall.co.kr/goods/detail.do?gno=74980159)

```json
{
  "review_id": "R4370",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4371 — 냥코 군단 출진 울트라 하이퍼 고양이 축제 재앙의 캐슬리 (1개)

상품 ID: 3653

- [냥코 대전쟁 냥코 군단 출진 피규어 울트라 하이퍼 고양이 축제 재앙의 캐슬리](https://www.bnkrmall.co.kr/goods/detail.do?gno=66834547)

```json
{
  "review_id": "R4371",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4372 — 뉴건담 입상 RX-93ff 뉴 건담 (1개)

상품 ID: 4139

- [뉴건담 입상 RX-93ff 뉴 건담](https://www.bnkrmall.co.kr/goods/detail.do?gno=41166384)

```json
{
  "review_id": "R4372",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4373 — 뉴 모니터 탑 ~스캔티&니삭스~ (A:스캔티) (1개)

상품 ID: 3284

- [뉴 팬티 & 스타킹 with 가터벨트 모니터 탑 피규어 ~스캔티&니삭스~ (A:스캔티)](https://www.bnkrmall.co.kr/goods/detail.do?gno=17464645)

```json
{
  "review_id": "R4373",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4374 — 뉴 모니터 탑 ~스캔티&니삭스~ (B:니삭스) (1개)

상품 ID: 3283

- [뉴 팬티 & 스타킹 with 가터벨트 모니터 탑 피규어 ~스캔티&니삭스~ (B:니삭스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=37603130)

```json
{
  "review_id": "R4374",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4375 — 뉴 모니터 탑 ~팬티 & 스타킹~ (A: 팬티) (1개)

상품 ID: 3406

- [뉴 팬티 & 스타킹 with 가터벨트 모니터 탑 피규어 ~팬티 & 스타킹~ (A: 팬티)](https://www.bnkrmall.co.kr/goods/detail.do?gno=43412528)

```json
{
  "review_id": "R4375",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4376 — 뉴 모니터 탑 ~팬티 & 스타킹~ (B: 스타킹) (1개)

상품 ID: 3405

- [뉴 팬티 & 스타킹 with 가터벨트 모니터 탑 피규어 ~팬티 & 스타킹~ (B: 스타킹)](https://www.bnkrmall.co.kr/goods/detail.do?gno=17645501)

```json
{
  "review_id": "R4376",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4377 — 뉴 모니터 탑 ~팬티&스타킹 엔젤 ver.~ (A:팬티(엔젤 ver.)) (1개)

상품 ID: 3519

- [뉴 팬티 & 스타킹 with 가터벨트 모니터 탑 피규어 ~팬티&스타킹 엔젤 ver.~ (A:팬티(엔젤 ver.))](https://www.bnkrmall.co.kr/goods/detail.do?gno=84182688)

```json
{
  "review_id": "R4377",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4378 — 뉴 모니터 탑 ~팬티&스타킹 엔젤 ver.~ (B:스타킹(엔젤 ver.)) (1개)

상품 ID: 3518

- [뉴 팬티 & 스타킹 with 가터벨트 모니터 탑 피규어 ~팬티&스타킹 엔젤 ver.~ (B:스타킹(엔젤 ver.))](https://www.bnkrmall.co.kr/goods/detail.do?gno=44335050)

```json
{
  "review_id": "R4378",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4379 — 뉴 모니터 탑 ~폴리에스테르 & 폴리우레탄~ (A: 폴리에스테르) (1개)

상품 ID: 3354

- [뉴 팬티 & 스타킹 with 가터벨트 모니터 탑 피규어 ~폴리에스테르 & 폴리우레탄~ (A: 폴리에스테르)](https://www.bnkrmall.co.kr/goods/detail.do?gno=84556221)

```json
{
  "review_id": "R4379",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4380 — 뉴 모니터 탑 ~폴리에스테르 & 폴리우레탄~ (B: 폴리우레탄) (1개)

상품 ID: 3353

- [뉴 팬티 & 스타킹 with 가터벨트 모니터 탑 피규어 ~폴리에스테르 & 폴리우레탄~ (B: 폴리우레탄)](https://www.bnkrmall.co.kr/goods/detail.do?gno=24284363)

```json
{
  "review_id": "R4380",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4381 — 니시키기 치사토 (두사람의 여행) (1개)

상품 ID: 4089

- [리코리스 리코일 니시키기 치사토 (두사람의 여행)](https://www.bnkrmall.co.kr/goods/detail.do?gno=25792635)

```json
{
  "review_id": "R4381",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4382 — 니카 나나우라 (1개)

상품 ID: 4234

- [기동전사 건담 수성의 마녀 니카 나나우라 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=16516070)

```json
{
  "review_id": "R4382",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4383 — 닌계조형열전 우치하 사스케 (1개)

상품 ID: 3373

- [나루토 닌계조형열전 우치하 사스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=51514236)

```json
{
  "review_id": "R4383",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4384 — 다마고치 SOFVIMATES 구치파치 (1개)

상품 ID: 3243

- [다마고치 SOFVIMATES 구치파치](https://www.bnkrmall.co.kr/goods/detail.do?gno=7034731)

```json
{
  "review_id": "R4384",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4385 — 다크 소울 SCULPT 콜렉션 VOL.4 아스토라 상급 기사 (1개)

상품 ID: 3881

- [다크 소울 SCULPT 콜렉션 VOL.4 아스토라 상급 기사](https://www.bnkrmall.co.kr/goods/detail.do?gno=72348630)

```json
{
  "review_id": "R4385",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4386 — 단간론파 1.2 Reload 모노미 (1개)

상품 ID: 3447

- [단간론파 1.2 Reload 모노미 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=51489897)

```json
{
  "review_id": "R4386",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4387 — 단간론파 1.2 Reload 모노쿠마 (1개)

상품 ID: 3388

- [단간론파 1.2 Reload 모노쿠마 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59157661)

```json
{
  "review_id": "R4387",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4388 — 단간론파1·2 Reload 에노시마 준코 (1개)

상품 ID: 3295

- [단간론파1·2 Reload 에노시마 준코 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=72642561)

```json
{
  "review_id": "R4388",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4389 — 데스 스트랜딩 2: 온 더 비치 모니터 탑 샘 (1개)

상품 ID: 3408

- [데스 스트랜딩 2: 온 더 비치 모니터 탑 피규어 샘](https://www.bnkrmall.co.kr/goods/detail.do?gno=81196873)

```json
{
  "review_id": "R4389",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4390 — 데스 스트랜딩 2: 온 더 비치 모니터 탑 힉스 (1개)

상품 ID: 3356

- [데스 스트랜딩 2: 온 더 비치 모니터 탑 피규어 힉스](https://www.bnkrmall.co.kr/goods/detail.do?gno=40625844)

```json
{
  "review_id": "R4390",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4391 — 데스 스트랜딩 2: 온 더 비치 밸런스 (1개)

상품 ID: 3676

- [데스 스트랜딩 2: 온 더 비치 밸런스 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=61244108)

```json
{
  "review_id": "R4391",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4392 — 데커 영웅용상 울트라맨 데커 플래시 타입 VER.A (1개)

상품 ID: 4430

- [울트라맨 데커 영웅용상 울트라맨 데커 플래시 타입 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=59243)

```json
{
  "review_id": "R4392",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4393 — 도박묵시록 카이지 마천의 지옥 철골 건너기 (1개)

상품 ID: 3607

- [도박묵시록 카이지 마천의 지옥 철골 건너기 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=10115209)

```json
{
  "review_id": "R4393",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4394 — 도쿄 구울 MAXIMATIC 스즈야 쥬조 (1개)

상품 ID: 3596

- [도쿄 구울 MAXIMATIC 스즈야 쥬조](https://www.bnkrmall.co.kr/goods/detail.do?gno=87537408)

```json
{
  "review_id": "R4394",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4395 — 도쿄 구울 MAXIMATIC 카네키 켄 (1개)

상품 ID: 3384

- [도쿄 구울 MAXIMATIC 카네키 켄](https://www.bnkrmall.co.kr/goods/detail.do?gno=23880141)

```json
{
  "review_id": "R4395",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4396 — 동복 성장의 증표 ver. (1개)

상품 ID: 3232

- [장송의 프리렌 피규어 동복 성장의 증표 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=5717071)

```json
{
  "review_id": "R4396",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4397 — 디오라마 고죠 사토루・게토 스구루 슈트VER. SPECIAL (A:고죠 사토루) (1개)

상품 ID: 3951

- [주술회전 디오라마 피규어 고죠 사토루・게토 스구루 슈트VER. SPECIAL (A:고죠 사토루)](https://www.bnkrmall.co.kr/goods/detail.do?gno=95583926)

```json
{
  "review_id": "R4397",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4398 — 디오라마 고죠 사토루・게토 스구루 슈트VER. SPECIAL (B:게토 스구루) (1개)

상품 ID: 3950

- [주술회전 디오라마 피규어 고죠 사토루・게토 스구루 슈트VER. SPECIAL (B:게토 스구루)](https://www.bnkrmall.co.kr/goods/detail.do?gno=63139889)

```json
{
  "review_id": "R4398",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4399 — 디오라마 사이타마 (1개)

상품 ID: 3744

- [원펀맨 디오라마 피규어 사이타마](https://www.bnkrmall.co.kr/goods/detail.do?gno=78587387)

```json
{
  "review_id": "R4399",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4400 — 디지바이스 스탠드! 그레이몬 (1개)

상품 ID: 3318

- [디지몬 어드벤처 디지바이스 스탠드! 그레이몬](https://www.bnkrmall.co.kr/goods/detail.do?gno=32359832)

```json
{
  "review_id": "R4400",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4401 — 디지바이스 스탠드! 아구몬 (1개)

상품 ID: 3319

- [디지몬 어드벤처 디지바이스 스탠드! 아구몬](https://www.bnkrmall.co.kr/goods/detail.do?gno=59143712)

```json
{
  "review_id": "R4401",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4402 — 디지바이스 엔젤몬 (1개)

상품 ID: 3263

- [디지몬 어드벤처 디지바이스 피규어 엔젤몬](https://www.bnkrmall.co.kr/goods/detail.do?gno=38071104)

```json
{
  "review_id": "R4402",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4403 — 디지바이스 파닥몬 (1개)

상품 ID: 3264

- [디지몬 어드벤처 디지바이스 피규어 파닥몬](https://www.bnkrmall.co.kr/goods/detail.do?gno=56518234)

```json
{
  "review_id": "R4403",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4404 — 라라아 슨 VER.A (1개)

상품 ID: 4625

- [기동전사 건담 라라아 슨 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=55489)

```json
{
  "review_id": "R4404",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4405 — 라라아 슨 VER.B (1개)

상품 ID: 4624

- [기동전사 건담 라라아 슨 VER.B](https://www.bnkrmall.co.kr/goods/detail.do?gno=55490)

```json
{
  "review_id": "R4405",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4406 — 라이카게 에이 오카게 집결!! (1개)

상품 ID: 3275

- [나루토 질풍전 라이카게 에이 피규어 오카게 집결!!](https://www.bnkrmall.co.kr/goods/detail.do?gno=87055678)

```json
{
  "review_id": "R4406",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4407 — 라크스 클라인 (1개)

상품 ID: 4178

- [기동전사 건담 SEED FREEDOM 라크스 클라인 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=52408512)

```json
{
  "review_id": "R4407",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4408 — 러브라이브 니지가사키 학원 스쿨 아이돌 동호회 미야시타 아이 (1개)

상품 ID: 4546

- [러브라이브 니지가사키 학원 스쿨 아이돌 동호회 미야시타 아이](https://www.bnkrmall.co.kr/goods/detail.do?gno=56774)

```json
{
  "review_id": "R4408",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4409 — 러브라이브 니지가사키 학원 스쿨 아이돌 동호회 아사카 카린 (1개)

상품 ID: 4542

- [러브라이브 니지가사키 학원 스쿨 아이돌 동호회 아사카 카린](https://www.bnkrmall.co.kr/goods/detail.do?gno=56780)

```json
{
  "review_id": "R4409",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4410 — 러브라이브 니지가사키 학원 스쿨 아이돌 동호회 엠마 베르데 (1개)

상품 ID: 4545

- [러브라이브 니지가사키 학원 스쿨 아이돌 동호회 엠마 베르데](https://www.bnkrmall.co.kr/goods/detail.do?gno=56776)

```json
{
  "review_id": "R4410",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4411 — 러브라이브 니지가사키 학원 스쿨 아이돌 동호회 오사카 시즈쿠 (1개)

상품 ID: 4543

- [러브라이브 니지가사키 학원 스쿨 아이돌 동호회 오사카 시즈쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=56779)

```json
{
  "review_id": "R4411",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4412 — 러브라이브 니지가사키 학원 스쿨 아이돌 동호회 유키 세츠나 (1개)

상품 ID: 4580

- [러브라이브 니지가사키 학원 스쿨 아이돌 동호회 유키 세츠나](https://www.bnkrmall.co.kr/goods/detail.do?gno=56478)

```json
{
  "review_id": "R4412",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4413 — 러브라이브 니지가사키 학원 스쿨 아이돌 동호회 텐노지 리나 (1개)

상품 ID: 4544

- [러브라이브 니지가사키 학원 스쿨 아이돌 동호회 텐노지 리나](https://www.bnkrmall.co.kr/goods/detail.do?gno=56777)

```json
{
  "review_id": "R4413",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4414 — 레이디 파이트 나미 (1개)

상품 ID: 4630

- [원피스 레이디 파이트 나미](https://www.bnkrmall.co.kr/goods/detail.do?gno=55279)

```json
{
  "review_id": "R4414",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4415 — 레이싱 Ver. 반프레스토 클로니클 레이싱 미쿠 2016 (1개)

상품 ID: 3056

- [하츠네 미쿠 레이싱 Ver. 반프레스토 클로니클 레이싱 미쿠 2016](https://www.bnkrmall.co.kr/goods/detail.do?gno=58059895)

```json
{
  "review_id": "R4415",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4416 — 레이싱 Ver. 반프레스토 클로니클 레이싱 미쿠 2017 TEAM UKYO CHEERING Ver. (1개)

상품 ID: 3057

- [하츠네 미쿠 레이싱 Ver. 반프레스토 클로니클 레이싱 미쿠 2017 TEAM UKYO CHEERING Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=79221589)

```json
{
  "review_id": "R4416",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4417 — 레이싱 Ver. 반프레스토 클로니클 레이싱 미쿠 2019 TEAM UKYO CHEERING Ver. (1개)

상품 ID: 3055

- [하츠네 미쿠 레이싱 Ver. 반프레스토 클로니클 레이싱 미쿠 2019 TEAM UKYO CHEERING Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=59200429)

```json
{
  "review_id": "R4417",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4418 — 레전드 콜라보 베지트 (1개)

상품 ID: 4683

- [드래곤볼 레전드 콜라보 베지트](https://www.bnkrmall.co.kr/goods/detail.do?gno=15675)

```json
{
  "review_id": "R4418",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4419 — 레전드 콜라보 손오공 (1개)

상품 ID: 4520

- [드래곤볼 레전드 콜라보 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=57254)

```json
{
  "review_id": "R4419",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4420 — 레전드 콜라보 오천크스 (1개)

상품 ID: 4497

- [드래곤볼 레전드 콜라보 오천크스](https://www.bnkrmall.co.kr/goods/detail.do?gno=57297)

```json
{
  "review_id": "R4420",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4421 — 레졸루션 오브 솔져 Vol.5 (VER.A) (1개)

상품 ID: 4620

- [드래곤볼 Z 레졸루션 오브 솔져 Vol.5 (VER.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=55496)

```json
{
  "review_id": "R4421",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4422 — 로그 파일 셀렉션 FIGHT Vol.1 (조로) (1개)

상품 ID: 4670

- [원피스 로그 파일 셀렉션 FIGHT Vol.1 (조로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15783)

```json
{
  "review_id": "R4422",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4423 — 로그 파일 셀렉션 FIGHT Vol.2 (상디) (1개)

상품 ID: 4667

- [원피스 로그 파일 셀렉션 FIGHT Vol.2 (상디)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15828)

```json
{
  "review_id": "R4423",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4424 — 루나마리아 호크 (1개)

상품 ID: 4096

- [기동전사 건담 SEED FREEDOM 루나마리아 호크 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=95192375)

```json
{
  "review_id": "R4424",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4425 — 루비 AIR FLOW (1개)

상품 ID: 4048

- [【최애의 아이】 루비 AIR FLOW 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=49830115)

```json
{
  "review_id": "R4425",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4426 — 루비 『POP IN 2』VER. (1개)

상품 ID: 3964

- [【최애의 아이】 루비 피규어 『POP IN 2』VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=27647602)

```json
{
  "review_id": "R4426",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4427 — 루비 브라이덜 드레스 (1개)

상품 ID: 3992

- [【최애의 아이】 루비 브라이덜 드레스 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=35334972)

```json
{
  "review_id": "R4427",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4428 — 루비 사복 데이트 (1개)

상품 ID: 4173

- [【최애의 아이】 루비 사복 데이트 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=74844704)

```json
{
  "review_id": "R4428",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4429 — 리무루&란가 소프비 (1개)

상품 ID: 3798

- [전생했더니 슬라임이었던 건에 대하여 리무루&란가 소프비 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=10212553)

```json
{
  "review_id": "R4429",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4430 — 리무루 템페스트 (1개)

상품 ID: 3590

- [전생했더니 슬라임이었던 건에 대하여 리무루 템페스트 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=27965922)

```json
{
  "review_id": "R4430",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4431 — 리바이스 가면 라이더 리바이 (1개)

상품 ID: 4492

- [가면라이더 리바이스 가면 라이더 리바이 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=57422)

```json
{
  "review_id": "R4431",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4432 — 리틀 나이트메어 (A:식스) (1개)

상품 ID: 3941

- [리틀 나이트메어 피규어 (A:식스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=30643393)

```json
{
  "review_id": "R4432",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4433 — 리틀 나이트메어 (B:모노) (1개)

상품 ID: 3940

- [리틀 나이트메어 피규어 (B:모노)](https://www.bnkrmall.co.kr/goods/detail.do?gno=38745526)

```json
{
  "review_id": "R4433",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4434 — 리틀 나이트메어 모니터 탑 Vol.1 (A:식스) (1개)

상품 ID: 3762

- [리틀 나이트메어 모니터 탑 피규어 Vol.1 (A:식스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=43854624)

```json
{
  "review_id": "R4434",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4435 — 리틀 나이트메어 모니터 탑 Vol.2 (B:얼론) (1개)

상품 ID: 3830

- [리틀 나이트메어 모니터 탑 피규어 Vol.2 (B:얼론)](https://www.bnkrmall.co.kr/goods/detail.do?gno=18184014)

```json
{
  "review_id": "R4435",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4436 — 리틀 나이트메어 모니터 탑 Vol.3 (C:모노) (1개)

상품 ID: 3829

- [리틀 나이트메어 모니터 탑 피규어 Vol.3 (C:모노)](https://www.bnkrmall.co.kr/goods/detail.do?gno=6359754)

```json
{
  "review_id": "R4436",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4437 — 리틀 나이트메어 모니터 탑 Vol.4 (D:로우) (1개)

상품 ID: 3828

- [리틀 나이트메어 모니터 탑 피규어 Vol.4 (D:로우)](https://www.bnkrmall.co.kr/goods/detail.do?gno=9400885)

```json
{
  "review_id": "R4437",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4438 — 마법소녀 마도카 마기카 10주년 기념 SERENUS COUTURE 카나메 마도카 (1개)

상품 ID: 4589

- [마법소녀 마도카 마기카 10주년 기념 SERENUS COUTURE 카나메 마도카](https://www.bnkrmall.co.kr/goods/detail.do?gno=56301)

```json
{
  "review_id": "R4438",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4439 — 마스터 스타 피스 엘런 예거 (1개)

상품 ID: 4623

- [진격의 거인 마스터 스타 피스 엘런 예거](https://www.bnkrmall.co.kr/goods/detail.do?gno=55491)

```json
{
  "review_id": "R4439",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4440 — 마오마오 (1개)

상품 ID: 3533

- [약사의 혼잣말 마오마오 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=44595550)

```json
{
  "review_id": "R4440",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4441 — 마오마오 MOON FAIRY (1개)

상품 ID: 3416

- [약사의 혼잣말 마오마오 피규어 MOON FAIRY](https://www.bnkrmall.co.kr/goods/detail.do?gno=70301752)

```json
{
  "review_id": "R4441",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4442 — 마오마오 가든 파티 (1개)

상품 ID: 3703

- [약사의 혼잣말 마오마오 피규어 가든 파티](https://www.bnkrmall.co.kr/goods/detail.do?gno=7257197)

```json
{
  "review_id": "R4442",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4443 — 마오마오 거리 산책 (1개)

상품 ID: 3633

- [약사의 혼잣말 마오마오 피규어 거리 산책](https://www.bnkrmall.co.kr/goods/detail.do?gno=98956040)

```json
{
  "review_id": "R4443",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4444 — 마오마오 여우 마을 (1개)

상품 ID: 3400

- [약사의 혼잣말 마오마오 피규어 여우 마을](https://www.bnkrmall.co.kr/goods/detail.do?gno=935059)

```json
{
  "review_id": "R4444",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4445 — 마오마오 판초 (1개)

상품 ID: 3532

- [약사의 혼잣말 마오마오 피규어 판초](https://www.bnkrmall.co.kr/goods/detail.do?gno=24820922)

```json
{
  "review_id": "R4445",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4446 — 마인 부우 패널 (1개)

상품 ID: 3495

- [드래곤볼 DAIMA 마인 부우 패널 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=75999873)

```json
{
  "review_id": "R4446",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4447 — 마히토 (1개)

상품 ID: 4450

- [주술회전 마히토](https://www.bnkrmall.co.kr/goods/detail.do?gno=59168)

```json
{
  "review_id": "R4447",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4448 — 매거진 꿈의 한 장#2 VOL.1 (포트거스 D 에이스) (1개)

상품 ID: 4529

- [원피스 매거진 피규어 꿈의 한 장#2 VOL.1 (포트거스 D 에이스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56850)

```json
{
  "review_id": "R4448",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4449 — 매거진 꿈의 한 장#2 VOL.2 (사보) (1개)

상품 ID: 4527

- [원피스 매거진 피규어 꿈의 한 장#2 VOL.2 (사보)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56852)

```json
{
  "review_id": "R4449",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4450 — 매거진 꿈의 한 장 Vol.1 스페셜 (A:사보) (1개)

상품 ID: 4510

- [원피스 매거진 피규어 꿈의 한 장 Vol.1 스페셜 (A:사보)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57275)

```json
{
  "review_id": "R4450",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4451 — 매거진 꿈의 한 장 Vol.1 스페셜 (B:몽키 D 루피) (1개)

상품 ID: 4509

- [원피스 매거진 피규어 꿈의 한 장 Vol.1 스페셜 (B:몽키 D 루피)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57276)

```json
{
  "review_id": "R4451",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4452 — 매거진 꿈의 한 장 Vol.1 스페셜 (C:포트거스 D 에이스) (1개)

상품 ID: 4508

- [원피스 매거진 피규어 꿈의 한 장 Vol.1 스페셜 (C:포트거스 D 에이스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57277)

```json
{
  "review_id": "R4452",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4453 — 매거진 꿈의 한 장 Vol.1 스페셜 (D:몽키 D 가프) (1개)

상품 ID: 4507

- [원피스 매거진 피규어 꿈의 한 장 Vol.1 스페셜 (D:몽키 D 가프)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57278)

```json
{
  "review_id": "R4453",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4454 — 매거진 꿈의 한 장 Vol.2 사보 (1개)

상품 ID: 4700

- [원피스 매거진 피규어 꿈의 한 장 Vol.2 사보](https://www.bnkrmall.co.kr/goods/detail.do?gno=15392)

```json
{
  "review_id": "R4454",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4455 — 매거진 꿈의 한 장 Vol.3 루피 (1개)

상품 ID: 4695

- [원피스 매거진 피규어 꿈의 한 장 Vol.3 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=15503)

```json
{
  "review_id": "R4455",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4456 — 매거진 스페셜 에피소드 LUFF VOL.2 (에이스) (1개)

상품 ID: 4657

- [원피스 매거진 피규어 스페셜 에피소드 LUFF VOL.2 (에이스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=18889)

```json
{
  "review_id": "R4456",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4457 — 맨후드 에드워드 뉴게이트 (Ver.A) (1개)

상품 ID: 4511

- [원피스 맨후드 에드워드 뉴게이트 (Ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57274)

```json
{
  "review_id": "R4457",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4458 — 메이린 호크 (1개)

상품 ID: 4094

- [기동전사 건담 SEED FREEDOM 메이린 호크 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=51897625)

```json
{
  "review_id": "R4458",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4459 — 메탈로봇혼 (SIDE MS) 붉은 건담 (1개)

상품 ID: 1986

- [메탈로봇혼 (SIDE MS) 붉은 건담](https://www.bnkrmall.co.kr/goods/detail.do?gno=82030451)

```json
{
  "review_id": "R4459",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4460 — 메탈로봇혼 류오마루 (1개)

상품 ID: 1976

- [메탈로봇혼 류오마루](https://www.bnkrmall.co.kr/goods/detail.do?gno=44253696)

```json
{
  "review_id": "R4460",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4461 — 모니터 탑 아로나 (1개)

상품 ID: 3476

- [블루 아카이브 모니터 탑 피규어 아로나](https://www.bnkrmall.co.kr/goods/detail.do?gno=68633247)

```json
{
  "review_id": "R4461",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4462 — 모니터 탑 프라나 (1개)

상품 ID: 3475

- [블루 아카이브 모니터 탑 피규어 프라나](https://www.bnkrmall.co.kr/goods/detail.do?gno=5446923)

```json
{
  "review_id": "R4462",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4463 — 모리노 린제 (1개)

상품 ID: 4413

- [아이돌마스터 샤이니 컬러즈 모리노 린제](https://www.bnkrmall.co.kr/goods/detail.do?gno=59302)

```json
{
  "review_id": "R4463",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4464 — 모험의 새벽 몽키 D 루피 vol.1 (1개)

상품 ID: 3527

- [원피스 모험의 새벽 몽키 D 루피 vol.1](https://www.bnkrmall.co.kr/goods/detail.do?gno=37262476)

```json
{
  "review_id": "R4464",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4465 — 모험의 새벽 몽키 D 루피 vol.2 (1개)

상품 ID: 3526

- [원피스 모험의 새벽 몽키 D 루피 vol.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=6981044)

```json
{
  "review_id": "R4465",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4466 — 몬스터 헌터 리오레우스 (1개)

상품 ID: 4019

- [몬스터 헌터 리오레우스](https://www.bnkrmall.co.kr/goods/detail.do?gno=455133)

```json
{
  "review_id": "R4466",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4467 — 몬스터 헌터 와일즈 알슈베르도 (1개)

상품 ID: 3479

- [몬스터 헌터 와일즈 피규어 알슈베르도](https://www.bnkrmall.co.kr/goods/detail.do?gno=10940304)

```json
{
  "review_id": "R4467",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4468 — 몬스터 헌터 진오우거 (1개)

상품 ID: 4020

- [몬스터 헌터 진오우거](https://www.bnkrmall.co.kr/goods/detail.do?gno=47548716)

```json
{
  "review_id": "R4468",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4469 — 몬스터 헌터 진좌수 Enshrined Monsters 라잔 (ver.A) (1개)

상품 ID: 3437

- [몬스터 헌터 진좌수 Enshrined Monsters 라잔 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=11336339)

```json
{
  "review_id": "R4469",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4470 — 몬스터 헌터 진좌수 Enshrined Monsters 라잔 (ver.B) (1개)

상품 ID: 3436

- [몬스터 헌터 진좌수 Enshrined Monsters 라잔 (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=74069167)

```json
{
  "review_id": "R4470",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4471 — 몬스터 헌터 진좌수 Enshrined Monsters 티가렉스 (1개)

상품 ID: 3438

- [몬스터 헌터 진좌수 Enshrined Monsters 티가렉스](https://www.bnkrmall.co.kr/goods/detail.do?gno=33587578)

```json
{
  "review_id": "R4471",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4472 — 미도리야 이즈쿠 (1개)

상품 ID: 3483

- [나의 히어로 아카데미아 피규어 미도리야 이즈쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=59235889)

```json
{
  "review_id": "R4472",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4473 — 미도리야 이즈쿠&바쿠고 카츠키 (가칭) (A:미도리야 이즈쿠) (1개)

상품 ID: 3867

- [나의 히어로 아카데미아 피규어 미도리야 이즈쿠&바쿠고 카츠키 (가칭) (A:미도리야 이즈쿠)](https://www.bnkrmall.co.kr/goods/detail.do?gno=68429778)

```json
{
  "review_id": "R4473",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4474 — 미도리야 이즈쿠&바쿠고 카츠키 (가칭) (B:바쿠고 카즈키) (1개)

상품 ID: 3866

- [나의 히어로 아카데미아 피규어 미도리야 이즈쿠&바쿠고 카츠키 (가칭) (B:바쿠고 카즈키)](https://www.bnkrmall.co.kr/goods/detail.do?gno=27111854)

```json
{
  "review_id": "R4474",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4475 — 미도리야 이즈쿠･바쿠고 카츠키 (미도리야 이즈쿠) (1개)

상품 ID: 4363

- [나의 히어로 아카데미아 피규어 미도리야 이즈쿠･바쿠고 카츠키 (미도리야 이즈쿠)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59944)

```json
{
  "review_id": "R4475",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4476 — 미도리야 이즈쿠･바쿠고 카츠키 (바쿠고 카츠키) (1개)

상품 ID: 4362

- [나의 히어로 아카데미아 피규어 미도리야 이즈쿠･바쿠고 카츠키 (바쿠고 카츠키)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59945)

```json
{
  "review_id": "R4476",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4477 — 미야 아츠무 (1개)

상품 ID: 4189

- [하이큐!! 미야 아츠무 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=28574798)

```json
{
  "review_id": "R4477",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4478 — 미오리네 램블랑 (1개)

상품 ID: 4323

- [기동전사 건담 수성의 마녀 미오리네 램블랑 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=54304409)

```json
{
  "review_id": "R4478",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4479 — 미오리네 램블랑 SEASON2 엔딩VER. (1개)

상품 ID: 4156

- [기동전사 건담 수성의 마녀 미오리네 램블랑 피규어 SEASON2 엔딩VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=89566140)

```json
{
  "review_id": "R4479",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4480 — 미즈카게 테루미 메이 오카게 집결!! (1개)

상품 ID: 3345

- [나루토 질풍전 미즈카게 테루미 메이 피규어 오카게 집결!!](https://www.bnkrmall.co.kr/goods/detail.do?gno=21038044)

```json
{
  "review_id": "R4480",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4481 — 밀리언 라이브 CELESTIAL VIVI 키사라기 치하야 (1개)

상품 ID: 4268

- [아이돌마스터 밀리언 라이브 CELESTIAL VIVI 키사라기 치하야](https://www.bnkrmall.co.kr/goods/detail.do?gno=57670346)

```json
{
  "review_id": "R4481",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4482 — 밀리언 라이브 EMOTIONAL LENS 하코자키 세리카 (1개)

상품 ID: 4212

- [아이돌마스터 밀리언 라이브 EMOTIONAL LENS 하코자키 세리카](https://www.bnkrmall.co.kr/goods/detail.do?gno=55447909)

```json
{
  "review_id": "R4482",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4483 — 바치라 메구루 (1개)

상품 ID: 4374

- [블루 록 바치라 메구루 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59820)

```json
{
  "review_id": "R4483",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4484 — 바쿠고 카츠키 (1개)

상품 ID: 3482

- [나의 히어로 아카데미아 피규어 바쿠고 카츠키](https://www.bnkrmall.co.kr/goods/detail.do?gno=23415022)

```json
{
  "review_id": "R4484",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4485 — 바키 (비스켓 올리버 구체 Ver.) (1개)

상품 ID: 3589

- [바키 피규어 (비스켓 올리버 구체 Ver.)](https://www.bnkrmall.co.kr/goods/detail.do?gno=69085349)

```json
{
  "review_id": "R4485",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4486 — 바키 에어 야식 !! 한마 바키 (1개)

상품 ID: 3293

- [바키 에어 야식 피규어!! 한마 바키](https://www.bnkrmall.co.kr/goods/detail.do?gno=93045777)

```json
{
  "review_id": "R4486",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4487 — 바키 에어 야식 !! 한마 유지로 (1개)

상품 ID: 3294

- [바키 에어 야식 피규어!! 한마 유지로](https://www.bnkrmall.co.kr/goods/detail.do?gno=50971431)

```json
{
  "review_id": "R4487",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4488 — 반프레스토 월드 콜로세움 2 Vol.7 (손오공) (1개)

상품 ID: 3218

- [드래곤볼 Z 반프레스토 월드 피규어 콜로세움 2 Vol.7 (손오공)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15452)

```json
{
  "review_id": "R4488",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4489 — 반프레스토 콜로세움 스페셜 올마이트 (1개)

상품 ID: 3201

- [나의 히어로 아카데미아 반프레스토 피규어 콜로세움 스페셜 올마이트](https://www.bnkrmall.co.kr/goods/detail.do?gno=15900)

```json
{
  "review_id": "R4489",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4490 — 반프레스토 콜로세움 지라이야 (1개)

상품 ID: 2959

- [나루토 질풍전 반프레스토 피규어 콜로세움 지라이야](https://www.bnkrmall.co.kr/goods/detail.do?gno=72006859)

```json
{
  "review_id": "R4490",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4491 — 반프레스토 콜로세움 하타케 카카시 (1개)

상품 ID: 2756

- [나루토 질풍전 반프레스토 피규어 콜로세움 하타케 카카시](https://www.bnkrmall.co.kr/goods/detail.do?gno=30124683)

```json
{
  "review_id": "R4491",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4492 — 반프레스토 클로니클 SMSP 바쿠고 카츠키 (1개)

상품 ID: 3081

- [나의 히어로 아카데미아 반프레스토 클로니클 SMSP 바쿠고 카츠키](https://www.bnkrmall.co.kr/goods/detail.do?gno=59800)

```json
{
  "review_id": "R4492",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4493 — 반프레스토 클로니클 SMSP 토도로키 쇼토 (1개)

상품 ID: 3058

- [나의 히어로 아카데미아 반프레스토 클로니클 SMSP 토도로키 쇼토](https://www.bnkrmall.co.kr/goods/detail.do?gno=13645591)

```json
{
  "review_id": "R4493",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4494 — 반프레스토 클로니클 아카데미 VOL.4 시가라키 토무라 (1개)

상품 ID: 3141

- [나의 히어로 아카데미아 반프레스토 클로니클 피규어 아카데미 VOL.4 시가라키 토무라](https://www.bnkrmall.co.kr/goods/detail.do?gno=57651)

```json
{
  "review_id": "R4494",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4495 — 반프레스토 클로니클 아카데미 VOL.5 토가 히미코 (1개)

상품 ID: 3157

- [나의 히어로 아카데미아 반프레스토 클로니클 피규어 아카데미 VOL.5 토가 히미코](https://www.bnkrmall.co.kr/goods/detail.do?gno=56810)

```json
{
  "review_id": "R4495",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4496 — 발로란트 모니터 탑 바이퍼 (1개)

상품 ID: 3634

- [발로란트 모니터 탑 피규어 바이퍼](https://www.bnkrmall.co.kr/goods/detail.do?gno=46581723)

```json
{
  "review_id": "R4496",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4497 — 발로란트 모니터 탑 세이지 (1개)

상품 ID: 3705

- [발로란트 모니터 탑 피규어 세이지](https://www.bnkrmall.co.kr/goods/detail.do?gno=28773832)

```json
{
  "review_id": "R4497",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4498 — 발로란트 모니터 탑 소바 (1개)

상품 ID: 3651

- [발로란트 모니터 탑 피규어 소바](https://www.bnkrmall.co.kr/goods/detail.do?gno=7611382)

```json
{
  "review_id": "R4498",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4499 — 발로란트 모니터 탑 제트 (1개)

상품 ID: 3706

- [발로란트 모니터 탑 피규어 제트](https://www.bnkrmall.co.kr/goods/detail.do?gno=84947941)

```json
{
  "review_id": "R4499",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4500 — 발로란트 모니터 탑 피닉스 (1개)

상품 ID: 3652

- [발로란트 모니터 탑 피규어 피닉스](https://www.bnkrmall.co.kr/goods/detail.do?gno=22523095)

```json
{
  "review_id": "R4500",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4501 — 버닝 파이터 vol.1 (1개)

상품 ID: 4631

- [드래곤볼 Z 버닝 파이터 vol.1](https://www.bnkrmall.co.kr/goods/detail.do?gno=55278)

```json
{
  "review_id": "R4501",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4502 — 베루도라 템페스트 -REPAINT (1개)

상품 ID: 4504

- [전생했더니 슬라임이었던 건에 대하여 베루도라 템페스트 -REPAINT-](https://www.bnkrmall.co.kr/goods/detail.do?gno=57287)

```json
{
  "review_id": "R4502",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4503 — 베지터 (미니) 패널 (1개)

상품 ID: 4076

- [드래곤볼 DAIMA 베지터 (미니) 패널 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=65269502)

```json
{
  "review_id": "R4503",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4504 — 별의 커비 Fluffy Puffy MINE 브레이크 타임 (A:커비) (1개)

상품 ID: 3924

- [별의 커비 Fluffy Puffy MINE 브레이크 타임 (A:커비)](https://www.bnkrmall.co.kr/goods/detail.do?gno=93098441)

```json
{
  "review_id": "R4504",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4505 — 별의 커비 Fluffy Puffy MINE 브레이크 타임 (B:커비) (1개)

상품 ID: 3923

- [별의 커비 Fluffy Puffy MINE 브레이크 타임 (B:커비)](https://www.bnkrmall.co.kr/goods/detail.do?gno=43058270)

```json
{
  "review_id": "R4505",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4506 — 별의 커비 Fluffy Puffy MINE 브레이크 타임 (C:웨이들 디) (1개)

상품 ID: 3922

- [별의 커비 Fluffy Puffy MINE 브레이크 타임 (C:웨이들 디)](https://www.bnkrmall.co.kr/goods/detail.do?gno=40906767)

```json
{
  "review_id": "R4506",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4507 — 별의 커비 Fluffy Puffy MINE 커비들의 눈놀이 (A:커비) (1개)

상품 ID: 3656

- [별의 커비 Fluffy Puffy MINE 커비들의 눈놀이 (A:커비)](https://www.bnkrmall.co.kr/goods/detail.do?gno=53693014)

```json
{
  "review_id": "R4507",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4508 — 별의 커비 Fluffy Puffy MINE 커비들의 눈놀이 (B:웨이들 디) (1개)

상품 ID: 3655

- [별의 커비 Fluffy Puffy MINE 커비들의 눈놀이 (B:웨이들 디)](https://www.bnkrmall.co.kr/goods/detail.do?gno=62241072)

```json
{
  "review_id": "R4508",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4509 — 별의 커비 Fluffy Puffy MINE 커비들의 눈놀이 (C:웨이들 디) (1개)

상품 ID: 3654

- [별의 커비 Fluffy Puffy MINE 커비들의 눈놀이 (C:웨이들 디)](https://www.bnkrmall.co.kr/goods/detail.do?gno=2600012)

```json
{
  "review_id": "R4509",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4510 — 별의 커비 SOFVIMATES 커비 Warp star VER. (1개)

상품 ID: 3833

- [별의 커비 SOFVIMATES 커비 Warp star VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=7152359)

```json
{
  "review_id": "R4510",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4511 — 보루토 NEXT 제너레이션즈 우즈마키 보루토 (1개)

상품 ID: 3723

- [보루토 나루토 NEXT 제너레이션즈 우즈마키 보루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=29292356)

```json
{
  "review_id": "R4511",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4512 — 보루토 NEXT 제너레이션즈 우치하 사스케 (1개)

상품 ID: 3461

- [보루토 나루토 NEXT 제너레이션즈 우치하 사스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=56174310)

```json
{
  "review_id": "R4512",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4513 — 보루토 NEXT 제너레이션즈 피그라이프 호카게 얼굴바위 SPECIAL (ver.A) (1개)

상품 ID: 3627

- [보루토 나루토 NEXT 제너레이션즈 피그라이프 호카게 얼굴바위 SPECIAL (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=47601784)

```json
{
  "review_id": "R4513",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4514 — 보루토 NEXT 제너레이션즈 피그라이프 호카게 얼굴바위 SPECIAL (ver.B) (1개)

상품 ID: 3626

- [보루토 나루토 NEXT 제너레이션즈 피그라이프 호카게 얼굴바위 SPECIAL (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15314555)

```json
{
  "review_id": "R4514",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4515 — 보루토 NGVS 우즈마키 나루토 & 우즈마키 보루토 (A:우즈마키 보루토) (1개)

상품 ID: 4541

- [보루토 나루토 NGVS 우즈마키 나루토 & 우즈마키 보루토 (A:우즈마키 보루토)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56781)

```json
{
  "review_id": "R4515",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4516 — 봇치 더 록! 고토 히토리 (1개)

상품 ID: 4281

- [봇치 더 록! 고토 히토리 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=98950865)

```json
{
  "review_id": "R4516",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4517 — 봇치 더 록! 고토 히토리 VOL.2 (1개)

상품 ID: 4165

- [봇치 더 록! 고토 히토리 피규어 VOL.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=92165529)

```json
{
  "review_id": "R4517",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4518 — 봇치 더 록! 고토 히토리 퀸 오브 웨이 (1개)

상품 ID: 3376

- [봇치 더 록! 고토 히토리 피규어 퀸 오브 웨이](https://www.bnkrmall.co.kr/goods/detail.do?gno=59163599)

```json
{
  "review_id": "R4518",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4519 — 봇치 더 록! 봇치짱 스위츠 컬렉션 (ver.A) (1개)

상품 ID: 3305

- [봇치 더 록! 봇치짱 스위츠 컬렉션 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=96292674)

```json
{
  "review_id": "R4519",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4520 — 봇치 더 록! 봇치짱 스위츠 컬렉션 (ver.B) (1개)

상품 ID: 3304

- [봇치 더 록! 봇치짱 스위츠 컬렉션 (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=1699053)

```json
{
  "review_id": "R4520",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4521 — 봇치 더 록! 승인욕구 몬스터 (1개)

상품 ID: 3730

- [봇치 더 록! 승인욕구 몬스터](https://www.bnkrmall.co.kr/goods/detail.do?gno=65285904)

```json
{
  "review_id": "R4521",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4522 — 봇치 더 록! 야마다 료 VOL.2 (1개)

상품 ID: 4152

- [봇치 더 록! 야마다 료 피규어 VOL.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=64136591)

```json
{
  "review_id": "R4522",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4523 — 봇치 더 록! 이지치 니지카 VOL.2 (1개)

상품 ID: 4164

- [봇치 더 록! 이지치 니지카 피규어 VOL.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=42168736)

```json
{
  "review_id": "R4523",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4524 — 봇치 더 록! 키타 이쿠요 VOL.2 (1개)

상품 ID: 4151

- [봇치 더 록! 키타 이쿠요 피규어 VOL.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=98672135)

```json
{
  "review_id": "R4524",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4525 — 부자 에네르기파 버독 (1개)

상품 ID: 4664

- [드래곤볼 슈퍼 부자 에네르기파 버독](https://www.bnkrmall.co.kr/goods/detail.do?gno=15856)

```json
{
  "review_id": "R4525",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4526 — 부자 에네르기파 손오공 (1개)

상품 ID: 4663

- [드래곤볼 슈퍼 부자 에네르기파 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=15861)

```json
{
  "review_id": "R4526",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4527 — 브레이크 타임 콜렉션 VOL.1 (마오마오) (1개)

상품 ID: 3365

- [약사의 혼잣말 브레이크 타임 콜렉션 VOL.1 (마오마오)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59011167)

```json
{
  "review_id": "R4527",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4528 — 브레이크 타임 콜렉션 VOL.4 (1개)

상품 ID: 3625

- [체인소 맨 브레이크 타임 콜렉션 VOL.4](https://www.bnkrmall.co.kr/goods/detail.do?gno=73495590)

```json
{
  "review_id": "R4528",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4529 — 브레이크 타임 콜렉션 아쿠아 (1개)

상품 ID: 4239

- [【최애의 아이】 브레이크 타임 콜렉션 아쿠아](https://www.bnkrmall.co.kr/goods/detail.do?gno=3595891)

```json
{
  "review_id": "R4529",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4530 — 브레이크 타임 콜렉션 쿠로카와 아카네 (1개)

상품 ID: 4118

- [【최애의 아이】 브레이크 타임 콜렉션 쿠로카와 아카네](https://www.bnkrmall.co.kr/goods/detail.do?gno=90374827)

```json
{
  "review_id": "R4530",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4531 — 블랙 영웅용상 가면라이더 블랙 (1개)

상품 ID: 4282

- [가면라이더 블랙 영웅용상 가면라이더 블랙](https://www.bnkrmall.co.kr/goods/detail.do?gno=36129615)

```json
{
  "review_id": "R4531",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4532 — 블러드 오브 사이언즈 베지터 (1개)

상품 ID: 3891

- [드래곤볼 슈퍼 블러드 오브 사이언즈 베지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=15322059)

```json
{
  "review_id": "R4532",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4533 — 블러드 오브 사이언즈 손오공 (1개)

상품 ID: 3910

- [드래곤볼 슈퍼 블러드 오브 사이언즈 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=21807548)

```json
{
  "review_id": "R4533",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4534 — 블러드 오브 사이언즈 스페셜 VI (1개)

상품 ID: 4210

- [드래곤볼 Z 블러드 오브 사이언즈 스페셜 VI](https://www.bnkrmall.co.kr/goods/detail.do?gno=31109158)

```json
{
  "review_id": "R4534",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4535 — 블러드 오브 사이언즈 스페셜 VIII (초사이어인 베지트) (1개)

상품 ID: 4703

- [드래곤볼 Z 블러드 오브 사이언즈 스페셜 VIII (초사이어인 베지트)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15395)

```json
{
  "review_id": "R4535",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4536 — 블러드 오브 사이언즈 스페셜 XII (1개)

상품 ID: 4408

- [드래곤볼 슈퍼 블러드 오브 사이언즈 스페셜 XII](https://www.bnkrmall.co.kr/goods/detail.do?gno=59525)

```json
{
  "review_id": "R4536",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4537 — 블러드 오브 사이언즈 스페셜 XIX (1개)

상품 ID: 4242

- [드래곤볼 Z 블러드 오브 사이언즈 스페셜 XIX](https://www.bnkrmall.co.kr/goods/detail.do?gno=16119599)

```json
{
  "review_id": "R4537",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4538 — 블러드 오브 사이언즈 오지터&베지트(A:오지터) (1개)

상품 ID: 3838

- [드래곤볼 슈퍼 블러드 오브 사이언즈 오지터&베지트(A:오지터)](https://www.bnkrmall.co.kr/goods/detail.do?gno=81495557)

```json
{
  "review_id": "R4538",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4539 — 블러드 오브 사이언즈 오지터&베지트(B:베지트) (1개)

상품 ID: 3837

- [드래곤볼 슈퍼 블러드 오브 사이언즈 오지터&베지트(B:베지트)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58671228)

```json
{
  "review_id": "R4539",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4540 — 블러드 오브 사이언즈 초사이어인3 손오공 (1개)

상품 ID: 4100

- [드래곤볼 Z 블러드 오브 사이언즈 초사이어인3 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=15743509)

```json
{
  "review_id": "R4540",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4541 — 블러드 오브 사이언즈 초사이어인4 오지터 (1개)

상품 ID: 4058

- [드래곤볼 GT 블러드 오브 사이언즈 초사이어인4 오지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=24996991)

```json
{
  "review_id": "R4541",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4542 — 블러드 오브 사이언즈 초사이어인 갓 초사이어인 진화 베지터 (1개)

상품 ID: 3381

- [드래곤볼 슈퍼 블러드 오브 사이언즈 초사이어인 갓 초사이어인 진화 베지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=79181811)

```json
{
  "review_id": "R4542",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4543 — 블러드 오브 사이언즈 초사이어인 브로리 (1개)

상품 ID: 3494

- [드래곤볼 Z 블러드 오브 사이언즈 초사이어인 브로리](https://www.bnkrmall.co.kr/goods/detail.do?gno=9457836)

```json
{
  "review_id": "R4543",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4544 — 블러드 오브 사이언즈 초사이어인 손오공 (1개)

상품 ID: 3480

- [드래곤볼 Z 블러드 오브 사이언즈 초사이어인 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=4723775)

```json
{
  "review_id": "R4544",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4545 — 블러드 오브 사이언즈 초사이어인 손오반 (1개)

상품 ID: 3606

- [드래곤볼 Z 블러드 오브 사이언즈 초사이어인 손오반](https://www.bnkrmall.co.kr/goods/detail.do?gno=17796794)

```json
{
  "review_id": "R4545",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4546 — 블러드 오브 사이언즈 초사이어인 손오천 (1개)

상품 ID: 3605

- [드래곤볼 Z 블러드 오브 사이언즈 초사이어인 손오천](https://www.bnkrmall.co.kr/goods/detail.do?gno=33788650)

```json
{
  "review_id": "R4546",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4547 — 블러드 오브 사이언즈 초사이어인 트랭크스 (1개)

상품 ID: 4023

- [드래곤볼 Z 블러드 오브 사이언즈 초사이어인 트랭크스](https://www.bnkrmall.co.kr/goods/detail.do?gno=40413451)

```json
{
  "review_id": "R4547",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4548 — 삐뽀사루 겟츄 SOFVIMATES 삐뽀사루 (1개)

상품 ID: 3904

- [삐뽀사루 겟츄 SOFVIMATES 삐뽀사루](https://www.bnkrmall.co.kr/goods/detail.do?gno=58814315)

```json
{
  "review_id": "R4548",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4549 — 사카모토 타로 (전설의 청부업자) (1개)

상품 ID: 4043

- [사카모토 데이즈 사카모토 타로 피규어 (전설의 청부업자)](https://www.bnkrmall.co.kr/goods/detail.do?gno=73447811)

```json
{
  "review_id": "R4549",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4550 — 사쿠라 미쿠 BANPRESTO EVOLVE 사쿠라 미쿠 (1개)

상품 ID: 2382

- [사쿠라 미쿠 BANPRESTO EVOLVE 사쿠라 미쿠 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=32257567)

```json
{
  "review_id": "R4550",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4551 — 산리오캐릭터즈 BIG SOFVIMATES～쿠로미～ (1개)

상품 ID: 3708

- [산리오캐릭터즈 BIG SOFVIMATES～쿠로미～](https://www.bnkrmall.co.kr/goods/detail.do?gno=62613421)

```json
{
  "review_id": "R4551",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4552 — 산리오캐릭터즈 BIG SOFVIMATES 마이멜로디 인어 (ver.A) (1개)

상품 ID: 3678

- [산리오캐릭터즈 BIG SOFVIMATES 마이멜로디 인어 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=96188932)

```json
{
  "review_id": "R4552",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4553 — 산리오캐릭터즈 BIG SOFVIMATES 마이멜로디 인어 (ver.B) (1개)

상품 ID: 3677

- [산리오캐릭터즈 BIG SOFVIMATES 마이멜로디 인어 (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=18651418)

```json
{
  "review_id": "R4553",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4554 — 산리오캐릭터즈 BIG SOFVIMATES 시나모롤 (1개)

상품 ID: 3449

- [산리오캐릭터즈 BIG SOFVIMATES 시나모롤](https://www.bnkrmall.co.kr/goods/detail.do?gno=6731184)

```json
{
  "review_id": "R4554",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4555 — 산리오캐릭터즈 BIG SOFVIMATES 쿠로미 할로윈 ver. (1개)

상품 ID: 3585

- [산리오캐릭터즈 BIG SOFVIMATES 쿠로미 할로윈 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=39156959)

```json
{
  "review_id": "R4555",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4556 — 산리오캐릭터즈 BIG SOFVIMATES 헬로키티 SUMMER VER. (VER.A) (1개)

상품 ID: 3718

- [산리오캐릭터즈 BIG SOFVIMATES 헬로키티 SUMMER VER. (VER.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=44892724)

```json
{
  "review_id": "R4556",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4557 — 산리오캐릭터즈 BIG SOFVIMATES 헬로키티 SUMMER VER. (VER.B) (1개)

상품 ID: 3717

- [산리오캐릭터즈 BIG SOFVIMATES 헬로키티 SUMMER VER. (VER.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=13483456)

```json
{
  "review_id": "R4557",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4558 — 산리오캐릭터즈 BIG SOFVIMATES 헬로키티 tropical summer ver. (ver.A) (1개)

상품 ID: 3322

- [산리오캐릭터즈 BIG SOFVIMATES 헬로키티 tropical summer ver. (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=27708833)

```json
{
  "review_id": "R4558",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4559 — 산리오캐릭터즈 BIG SOFVIMATES 헬로키티 tropical summer ver. (ver.B) (1개)

상품 ID: 3321

- [산리오캐릭터즈 BIG SOFVIMATES 헬로키티 tropical summer ver. (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=64063170)

```json
{
  "review_id": "R4559",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4560 — 산리오캐릭터즈 Fluffy Puffy Mine vol.1 (A:마이멜로디) (1개)

상품 ID: 3749

- [산리오캐릭터즈 Fluffy Puffy Mine vol.1 (A:마이멜로디)](https://www.bnkrmall.co.kr/goods/detail.do?gno=51326507)

```json
{
  "review_id": "R4560",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4561 — 산리오캐릭터즈 Fluffy Puffy Mine vol.1 (B:쿠로미) (1개)

상품 ID: 3748

- [산리오캐릭터즈 Fluffy Puffy Mine vol.1 (B:쿠로미)](https://www.bnkrmall.co.kr/goods/detail.do?gno=93971621)

```json
{
  "review_id": "R4561",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4562 — 산리오캐릭터즈 Fluffy Puffy Mine vol.1 (C:폼폼푸린) (1개)

상품 ID: 3747

- [산리오캐릭터즈 Fluffy Puffy Mine vol.1 (C:폼폼푸린)](https://www.bnkrmall.co.kr/goods/detail.do?gno=85682469)

```json
{
  "review_id": "R4562",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4563 — 산리오캐릭터즈 Fluffy Puffy Mine vol.2 (A:헬로키티) (1개)

상품 ID: 3701

- [산리오캐릭터즈 Fluffy Puffy Mine vol.2 (A:헬로키티)](https://www.bnkrmall.co.kr/goods/detail.do?gno=60620615)

```json
{
  "review_id": "R4563",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4564 — 산리오캐릭터즈 Fluffy Puffy Mine vol.2 (B:시나모롤) (1개)

상품 ID: 3700

- [산리오캐릭터즈 Fluffy Puffy Mine vol.2 (B:시나모롤)](https://www.bnkrmall.co.kr/goods/detail.do?gno=60719170)

```json
{
  "review_id": "R4564",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4565 — 산리오캐릭터즈 Fluffy Puffy Mine vol.2 (C:포챠코) (1개)

상품 ID: 3699

- [산리오캐릭터즈 Fluffy Puffy Mine vol.2 (C:포챠코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=50198257)

```json
{
  "review_id": "R4565",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4566 — 산리오캐릭터즈 Fluffy Puffy Mine 마이멜로디&쿠로미 (A:마이멜로디) (1개)

상품 ID: 3674

- [산리오캐릭터즈 Fluffy Puffy Mine 마이멜로디&쿠로미 (A:마이멜로디)](https://www.bnkrmall.co.kr/goods/detail.do?gno=38511866)

```json
{
  "review_id": "R4566",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4567 — 산리오캐릭터즈 Fluffy Puffy Mine 마이멜로디&쿠로미 (B:쿠로미) (1개)

상품 ID: 3673

- [산리오캐릭터즈 Fluffy Puffy Mine 마이멜로디&쿠로미 (B:쿠로미)](https://www.bnkrmall.co.kr/goods/detail.do?gno=9127346)

```json
{
  "review_id": "R4567",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4568 — 산리오캐릭터즈 Fluffy Puffy 헬로키티&시나모롤 (A:헬로키티) (1개)

상품 ID: 3602

- [산리오캐릭터즈 Fluffy Puffy 헬로키티&시나모롤 (A:헬로키티)](https://www.bnkrmall.co.kr/goods/detail.do?gno=94258191)

```json
{
  "review_id": "R4568",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4569 — 산리오캐릭터즈 Fluffy Puffy 헬로키티&시나모롤 (B:시나모롤) (1개)

상품 ID: 3601

- [산리오캐릭터즈 Fluffy Puffy 헬로키티&시나모롤 (B:시나모롤)](https://www.bnkrmall.co.kr/goods/detail.do?gno=46975609)

```json
{
  "review_id": "R4569",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4570 — 산리오캐릭터즈 SOFVIMATES 라라 (1개)

상품 ID: 3671

- [산리오캐릭터즈 SOFVIMATES 라라](https://www.bnkrmall.co.kr/goods/detail.do?gno=70090653)

```json
{
  "review_id": "R4570",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4571 — 산리오캐릭터즈 SOFVIMATES 마이멜로디 RELAX VER. (1개)

상품 ID: 3745

- [산리오캐릭터즈 SOFVIMATES 마이멜로디 RELAX VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=5214407)

```json
{
  "review_id": "R4571",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4572 — 산리오캐릭터즈 SOFVIMATES 시나모롤 RELAX VER. (1개)

상품 ID: 3746

- [산리오캐릭터즈 SOFVIMATES 시나모롤 RELAX VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=21202571)

```json
{
  "review_id": "R4572",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4573 — 산리오캐릭터즈 SOFVIMATES 챠미키티 (1개)

상품 ID: 3597

- [산리오캐릭터즈 SOFVIMATES 챠미키티](https://www.bnkrmall.co.kr/goods/detail.do?gno=98915617)

```json
{
  "review_id": "R4573",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4574 — 산리오캐릭터즈 SOFVIMATES 키키 (1개)

상품 ID: 3672

- [산리오캐릭터즈 SOFVIMATES 키키](https://www.bnkrmall.co.kr/goods/detail.do?gno=63241276)

```json
{
  "review_id": "R4574",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4575 — 산리오캐릭터즈 SOFVIMATES 페클 (1개)

상품 ID: 3248

- [산리오캐릭터즈 SOFVIMATES 페클](https://www.bnkrmall.co.kr/goods/detail.do?gno=62182591)

```json
{
  "review_id": "R4575",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4576 — 산리오캐릭터즈 SOFVIMATES 포챠코 RELAX VER. (1개)

상품 ID: 3600

- [산리오캐릭터즈 SOFVIMATES 포챠코 RELAX VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=50511698)

```json
{
  "review_id": "R4576",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4577 — 산리오캐릭터즈 SOFVIMATES 폼폼푸린 RELAX VER. (1개)

상품 ID: 3675

- [산리오캐릭터즈 SOFVIMATES 폼폼푸린 RELAX VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=57201545)

```json
{
  "review_id": "R4577",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4578 — 산리오캐릭터즈 단짝 메모리즈 VOL.2 포차코&한교동 (A:포차코) (1개)

상품 ID: 3720

- [산리오캐릭터즈 단짝 메모리즈 VOL.2 포차코&한교동 (A:포차코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59374610)

```json
{
  "review_id": "R4578",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4579 — 산리오캐릭터즈 단짝 메모리즈 VOL.2 포차코&한교동 (B:한교동) (1개)

상품 ID: 3719

- [산리오캐릭터즈 단짝 메모리즈 VOL.2 포차코&한교동 (B:한교동)](https://www.bnkrmall.co.kr/goods/detail.do?gno=67618108)

```json
{
  "review_id": "R4579",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4580 — 산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 시나모롤&폼폼푸린 (A:시나모롤) (1개)

상품 ID: 3556

- [산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 시나모롤&폼폼푸린 (A:시나모롤)](https://www.bnkrmall.co.kr/goods/detail.do?gno=4035415)

```json
{
  "review_id": "R4580",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4581 — 산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 시나모롤&폼폼푸린 (B:폼폼푸린) (1개)

상품 ID: 3524

- [산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 시나모롤&폼폼푸린 (B:폼폼푸린)](https://www.bnkrmall.co.kr/goods/detail.do?gno=43443789)

```json
{
  "review_id": "R4581",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4582 — 산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 쿠로미&우사하나 (A:쿠로미) (1개)

상품 ID: 3326

- [산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 쿠로미&우사하나 (A:쿠로미)](https://www.bnkrmall.co.kr/goods/detail.do?gno=89342656)

```json
{
  "review_id": "R4582",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4583 — 산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 쿠로미&우사하나 (B:우사하나) (1개)

상품 ID: 3325

- [산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 쿠로미&우사하나 (B:우사하나)](https://www.bnkrmall.co.kr/goods/detail.do?gno=24247138)

```json
{
  "review_id": "R4583",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4584 — 산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 헬로키티&마이멜로디 (A:헬로키티) (1개)

상품 ID: 3599

- [산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 헬로키티&마이멜로디 (A:헬로키티)](https://www.bnkrmall.co.kr/goods/detail.do?gno=75669536)

```json
{
  "review_id": "R4584",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4585 — 산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 헬로키티&마이멜로디 (B:마이멜로디) (1개)

상품 ID: 3598

- [산리오캐릭터즈 단짝 메모리즈 집에서 릴렉스 타임 헬로키티&마이멜로디 (B:마이멜로디)](https://www.bnkrmall.co.kr/goods/detail.do?gno=63117195)

```json
{
  "review_id": "R4585",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4586 — 산리오캐릭터즈 단짝 메모리즈 티 파티 포차코&헬로키티 (A:포차코) (1개)

상품 ID: 3523

- [산리오캐릭터즈 단짝 메모리즈 티 파티 포차코&헬로키티 (A:포차코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=26462542)

```json
{
  "review_id": "R4586",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4587 — 산리오캐릭터즈 단짝 메모리즈 티 파티 포차코&헬로키티 (B:헬로키티) (1개)

상품 ID: 3522

- [산리오캐릭터즈 단짝 메모리즈 티 파티 포차코&헬로키티 (B:헬로키티)](https://www.bnkrmall.co.kr/goods/detail.do?gno=99239665)

```json
{
  "review_id": "R4587",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4588 — 산리오캐릭터즈 단짝 메모리즈 티 파티 폼폼푸린&시나모롤 (A:폼폼푸린) (1개)

상품 ID: 3521

- [산리오캐릭터즈 단짝 메모리즈 티 파티 폼폼푸린&시나모롤 (A:폼폼푸린)](https://www.bnkrmall.co.kr/goods/detail.do?gno=66744184)

```json
{
  "review_id": "R4588",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4589 — 산리오캐릭터즈 단짝 메모리즈 티 파티 폼폼푸린&시나모롤 (B:시나모롤) (1개)

상품 ID: 3520

- [산리오캐릭터즈 단짝 메모리즈 티 파티 폼폼푸린&시나모롤 (B:시나모롤)](https://www.bnkrmall.co.kr/goods/detail.do?gno=91746325)

```json
{
  "review_id": "R4589",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4590 — 산리오캐릭터즈 봉제 코스튬 스트랩 헬로키티 베어 ver. (1개)

상품 ID: 3249

- [산리오캐릭터즈 봉제 코스튬 피규어 스트랩 헬로키티 베어 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=40347938)

```json
{
  "review_id": "R4590",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4591 — 산리오캐릭터즈 코스플레이 컬렉션 마이멜로디&쿠로미 (A:마이멜로디) (1개)

상품 ID: 3324

- [산리오캐릭터즈 코스플레이 피규어 컬렉션 마이멜로디&쿠로미 (A:마이멜로디)](https://www.bnkrmall.co.kr/goods/detail.do?gno=19177576)

```json
{
  "review_id": "R4591",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4592 — 산리오캐릭터즈 코스플레이 컬렉션 마이멜로디&쿠로미 (B:쿠로미) (1개)

상품 ID: 3323

- [산리오캐릭터즈 코스플레이 피규어 컬렉션 마이멜로디&쿠로미 (B:쿠로미)](https://www.bnkrmall.co.kr/goods/detail.do?gno=70047043)

```json
{
  "review_id": "R4592",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4593 — 산리오캐릭터즈 쿠로미 컬렉션 키체인 (ver.A) (1개)

상품 ID: 3681

- [산리오캐릭터즈 쿠로미 피규어 컬렉션 키체인 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=66751085)

```json
{
  "review_id": "R4593",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4594 — 산리오캐릭터즈 쿠로미 컬렉션 키체인 (ver.B) (1개)

상품 ID: 3680

- [산리오캐릭터즈 쿠로미 피규어 컬렉션 키체인 (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=39729004)

```json
{
  "review_id": "R4594",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4595 — 산리오캐릭터즈 쿠로미 컬렉션 키체인 (ver.C) (1개)

상품 ID: 3679

- [산리오캐릭터즈 쿠로미 피규어 컬렉션 키체인 (ver.C)](https://www.bnkrmall.co.kr/goods/detail.do?gno=91643677)

```json
{
  "review_id": "R4595",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4596 — 산리오캐릭터즈 쿠로미 콜렉션(ver.A) (1개)

상품 ID: 3698

- [산리오캐릭터즈 쿠로미 피규어 콜렉션(ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=52148151)

```json
{
  "review_id": "R4596",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4597 — 산리오캐릭터즈 쿠로미 콜렉션(ver.B) (1개)

상품 ID: 3710

- [산리오캐릭터즈 쿠로미 피규어 콜렉션(ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=66596796)

```json
{
  "review_id": "R4597",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4598 — 산리오캐릭터즈 쿠로미 콜렉션(ver.C) (1개)

상품 ID: 3709

- [산리오캐릭터즈 쿠로미 피규어 콜렉션(ver.C)](https://www.bnkrmall.co.kr/goods/detail.do?gno=87714153)

```json
{
  "review_id": "R4598",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4599 — 산리오캐릭터즈 클리어 참(A.헬로키티) (1개)

상품 ID: 3500

- [산리오캐릭터즈 클리어 피규어 참(A.헬로키티)](https://www.bnkrmall.co.kr/goods/detail.do?gno=40785316)

```json
{
  "review_id": "R4599",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4600 — 산리오캐릭터즈 클리어 참(B.마이멜로디) (1개)

상품 ID: 3499

- [산리오캐릭터즈 클리어 피규어 참(B.마이멜로디)](https://www.bnkrmall.co.kr/goods/detail.do?gno=45978431)

```json
{
  "review_id": "R4600",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4601 — 산리오캐릭터즈 클리어 참(C.시나모롤) (1개)

상품 ID: 3498

- [산리오캐릭터즈 클리어 피규어 참(C.시나모롤)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57143207)

```json
{
  "review_id": "R4601",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4602 — 산리오캐릭터즈 폼폼푸린 콜렉션 (ver.A) (1개)

상품 ID: 3329

- [산리오캐릭터즈 폼폼푸린 피규어 콜렉션 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=97315605)

```json
{
  "review_id": "R4602",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4603 — 산리오캐릭터즈 폼폼푸린 콜렉션 (ver.B) (1개)

상품 ID: 3328

- [산리오캐릭터즈 폼폼푸린 피규어 콜렉션 (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=98011990)

```json
{
  "review_id": "R4603",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4604 — 산리오캐릭터즈 폼폼푸린 콜렉션 (ver.C) (1개)

상품 ID: 3327

- [산리오캐릭터즈 폼폼푸린 피규어 콜렉션 (ver.C)](https://www.bnkrmall.co.kr/goods/detail.do?gno=25914714)

```json
{
  "review_id": "R4604",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4605 — 산리오캐릭터즈 피그라이프 마이멜로디&마이스윗피아노 (1개)

상품 ID: 3586

- [산리오캐릭터즈 피그라이프 마이멜로디&마이스윗피아노](https://www.bnkrmall.co.kr/goods/detail.do?gno=61983006)

```json
{
  "review_id": "R4605",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4606 — 상냥한 전사 마섬광!! (1개)

상품 ID: 4576

- [드래곤볼 슈퍼 상냥한 전사 마섬광!!](https://www.bnkrmall.co.kr/goods/detail.do?gno=56518)

```json
{
  "review_id": "R4606",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4607 — 샤디크 제네리 (1개)

상품 ID: 4201

- [기동전사 건담 수성의 마녀 샤디크 제네리 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=32590474)

```json
{
  "review_id": "R4607",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4608 — 샤리아 불 (1개)

상품 ID: 3287

- [기동전사 건담 GQuuuuuuX 샤리아 불 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=11986410)

```json
{
  "review_id": "R4608",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4609 — 샤아 아즈나블 (1개)

상품 ID: 3288

- [기동전사 건담 GQuuuuuuX 샤아 아즈나블 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=80382045)

```json
{
  "review_id": "R4609",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4610 — 샹그릴라 프론티어 사이가 레이 (1개)

상품 ID: 3994

- [샹그릴라 프론티어 사이가 레이](https://www.bnkrmall.co.kr/goods/detail.do?gno=68480521)

```json
{
  "review_id": "R4610",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4611 — 샹그릴라 프론티어 아마네 토와 (1개)

상품 ID: 3995

- [샹그릴라 프론티어 아마네 토와](https://www.bnkrmall.co.kr/goods/detail.do?gno=39695505)

```json
{
  "review_id": "R4611",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4612 — 세일러 문 플러피 퍼피 루나/아르테미스 (A:루나) (1개)

상품 ID: 4388

- [세일러 문 플러피 퍼피 루나/아르테미스 (A:루나)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59561)

```json
{
  "review_id": "R4612",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4613 — 세일러 문 플러피 퍼피 루나/아르테미스 (B:아르테미스) (1개)

상품 ID: 4387

- [세일러 문 플러피 퍼피 루나/아르테미스 (B:아르테미스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59562)

```json
{
  "review_id": "R4613",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4614 — 소프비 가마분타 Ⅱ (1개)

상품 ID: 3511

- [나루토 소프비 피규어 가마분타 Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=70673011)

```json
{
  "review_id": "R4614",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4615 — 소프비 가마키치 (1개)

상품 ID: 3898

- [나루토 질풍전 소프비 피규어 가마키치](https://www.bnkrmall.co.kr/goods/detail.do?gno=7481877)

```json
{
  "review_id": "R4615",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4616 — 소프비 만다 (1개)

상품 ID: 3392

- [나루토 소프비 피규어 만다](https://www.bnkrmall.co.kr/goods/detail.do?gno=69691630)

```json
{
  "review_id": "R4616",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4617 — 소프비 수학 & 가마분타 (A:수학) (1개)

상품 ID: 3963

- [나루토 질풍전 소프비 피규어 수학 & 가마분타 (A:수학)](https://www.bnkrmall.co.kr/goods/detail.do?gno=22981264)

```json
{
  "review_id": "R4617",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4618 — 소프비 수학 & 가마분타 (B:가마분타) (1개)

상품 ID: 3962

- [나루토 질풍전 소프비 피규어 수학 & 가마분타 (B:가마분타)](https://www.bnkrmall.co.kr/goods/detail.do?gno=84097915)

```json
{
  "review_id": "R4618",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4619 — 소프비 카츠유 (1개)

상품 ID: 3426

- [나루토 소프비 피규어 카츠유](https://www.bnkrmall.co.kr/goods/detail.do?gno=29352818)

```json
{
  "review_id": "R4619",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4620 — 손오공 (미니) 패널 (1개)

상품 ID: 4077

- [드래곤볼 DAIMA 손오공 (미니) 패널 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=56394349)

```json
{
  "review_id": "R4620",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4621 — 손오공(미니) 패널 Ⅱ (가칭) (1개)

상품 ID: 4056

- [드래곤볼 DAIMA 손오공(미니) 패널 피규어Ⅱ (가칭)](https://www.bnkrmall.co.kr/goods/detail.do?gno=81281348)

```json
{
  "review_id": "R4621",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4622 — 손오공 FES Vol.12 (A:손오공(소년)) (1개)

상품 ID: 4502

- [드래곤볼 슈퍼 손오공 FES Vol.12 (A:손오공(소년))](https://www.bnkrmall.co.kr/goods/detail.do?gno=57290)

```json
{
  "review_id": "R4622",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4623 — 손오공 FES Vol.12 (A:초사이어인 손오공) (1개)

상품 ID: 4503

- [드래곤볼 슈퍼 손오공 FES Vol.12 (A:초사이어인 손오공)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57289)

```json
{
  "review_id": "R4623",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4624 — 손오공 FES Vol.14 (A:손오공) (1개)

상품 ID: 4500

- [드래곤볼 슈퍼 손오공 FES Vol.14 (A:손오공)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57294)

```json
{
  "review_id": "R4624",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4625 — 손오공 FES Vol.14 (B:초사이어인 갓 초사이어인 베지트) (1개)

상품 ID: 4499

- [드래곤볼 슈퍼 손오공 FES Vol.14 (B:초사이어인 갓 초사이어인 베지트)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57295)

```json
{
  "review_id": "R4625",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4626 — 손오공 FES VOL.15 (B:초사이어인 오지터) (1개)

상품 ID: 4578

- [드래곤볼 슈퍼 손오공 FES VOL.15 (B:초사이어인 오지터)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56486)

```json
{
  "review_id": "R4626",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4627 — 손오공 FES VOL.16 (A:초사이어인 손오공(키즈)) (1개)

상품 ID: 4609

- [드래곤볼 슈퍼 손오공 FES VOL.16 (A:초사이어인 손오공(키즈))](https://www.bnkrmall.co.kr/goods/detail.do?gno=56052)

```json
{
  "review_id": "R4627",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4628 — 손오공 FES VOL.16 (B:손오공) (1개)

상품 ID: 4608

- [드래곤볼 슈퍼 손오공 FES VOL.16 (B:손오공)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56053)

```json
{
  "review_id": "R4628",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4629 — 슈퍼 ZENKAI SOLID vol.1 (1개)

상품 ID: 4651

- [드래곤볼 슈퍼 슈퍼 ZENKAI SOLID vol.1](https://www.bnkrmall.co.kr/goods/detail.do?gno=54966)

```json
{
  "review_id": "R4629",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4630 — 슈퍼 ZENKAI SOLID vol.2 (1개)

상품 ID: 4581

- [드래곤볼 슈퍼 슈퍼 ZENKAI SOLID vol.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=56319)

```json
{
  "review_id": "R4630",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4631 — 슈퍼 히어로 CLEARISE 손오반(비스트) (1개)

상품 ID: 4195

- [드래곤볼 슈퍼 슈퍼 히어로 CLEARISE 손오반(비스트)](https://www.bnkrmall.co.kr/goods/detail.do?gno=39394814)

```json
{
  "review_id": "R4631",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4632 — 슈퍼 히어로즈 9주년 초사이어인4 베지터 : 제노 (1개)

상품 ID: 4710

- [슈퍼 드래곤볼 히어로즈 9주년 피규어 초사이어인4 베지터 : 제노](https://www.bnkrmall.co.kr/goods/detail.do?gno=15239)

```json
{
  "review_id": "R4632",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4633 — 슈퍼 히어로 히스토리 박스 Vol.8 (1개)

상품 ID: 4250

- [드래곤볼 슈퍼 슈퍼 히어로 히스토리 박스 Vol.8](https://www.bnkrmall.co.kr/goods/detail.do?gno=38875779)

```json
{
  "review_id": "R4633",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4634 — 스사노오&쿠라마(쿠라마 링크 모드) (A:스사노오) (1개)

상품 ID: 3473

- [나루토 질풍전 스사노오&쿠라마(쿠라마 링크 모드) 피규어 (A:스사노오)](https://www.bnkrmall.co.kr/goods/detail.do?gno=75883099)

```json
{
  "review_id": "R4634",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4635 — 스사노오&쿠라마(쿠라마 링크 모드) (B:쿠라마(쿠라마 링크 모드)) (1개)

상품 ID: 3472

- [나루토 질풍전 스사노오&쿠라마(쿠라마 링크 모드) 피규어 (B:쿠라마(쿠라마 링크 모드))](https://www.bnkrmall.co.kr/goods/detail.do?gno=80514872)

```json
{
  "review_id": "R4635",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4636 — 스위트 스타일 해적 네펠타리 비비 (Ver.A) (1개)

상품 ID: 4562

- [원피스 스위트 스타일 해적 네펠타리 비비 (Ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56668)

```json
{
  "review_id": "R4636",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4637 — 스위트 스타일 해적 네펠타리 비비 (Ver.B) (1개)

상품 ID: 4561

- [원피스 스위트 스타일 해적 네펠타리 비비 (Ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56669)

```json
{
  "review_id": "R4637",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4638 — 스위트 스타일 해적 레베카 (Ver.A) (1개)

상품 ID: 4531

- [원피스 스위트 스타일 해적 레베카 (Ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56848)

```json
{
  "review_id": "R4638",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4639 — 스즈미야 하루히의 우울 나가토 유키 (1개)

상품 ID: 3394

- [스즈미야 하루히의 우울 피규어 나가토 유키](https://www.bnkrmall.co.kr/goods/detail.do?gno=57458834)

```json
{
  "review_id": "R4639",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4640 — 스즈미야 하루히의 우울 스즈미야 하루히 (1개)

상품 ID: 3395

- [스즈미야 하루히의 우울 피규어 스즈미야 하루히](https://www.bnkrmall.co.kr/goods/detail.do?gno=24006916)

```json
{
  "review_id": "R4640",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4641 — 슬레타 머큐리 SEASON2 엔딩VER. (1개)

상품 ID: 4174

- [기동전사 건담 수성의 마녀 슬레타 머큐리 피규어 SEASON2 엔딩VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=67278842)

```json
{
  "review_id": "R4641",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4642 — 승리의 여신 NIKKE 바이퍼 코드 릴 (1개)

상품 ID: 3760

- [승리의 여신 NIKKE 바이퍼 코드 릴 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=81407106)

```json
{
  "review_id": "R4642",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4643 — 승리의 여신 NIKKE 아니스 코드 릴 (1개)

상품 ID: 3782

- [승리의 여신 NIKKE 아니스 코드 릴 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=47662896)

```json
{
  "review_id": "R4643",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4644 — 승리의 여신 NIKKE 피그라이프 레드 후드 (1개)

상품 ID: 3401

- [승리의 여신 NIKKE 피그라이프 레드 후드](https://www.bnkrmall.co.kr/goods/detail.do?gno=1936470)

```json
{
  "review_id": "R4644",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4645 — 시노미야 키코루 [THE METALLIC] (1개)

상품 ID: 4025

- [괴수 8호 시노미야 키코루 (THE METALLIC)](https://www.bnkrmall.co.kr/goods/detail.do?gno=21981580)

```json
{
  "review_id": "R4645",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4646 — 시도 류세이 U-20 일본 대표 (1개)

상품 ID: 3961

- [블루 록 시도 류세이 피규어 U-20 일본 대표](https://www.bnkrmall.co.kr/goods/detail.do?gno=6988219)

```json
{
  "review_id": "R4646",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4647 — 시리즈 진좌수 고대괴수 고모라(ver.A) (1개)

상품 ID: 3379

- [울트라맨 시리즈 진좌수 고대괴수 고모라(ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=70834862)

```json
{
  "review_id": "R4647",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4648 — 시리즈 진좌수 고대괴수 고모라(ver.B) (1개)

상품 ID: 3378

- [울트라맨 시리즈 진좌수 고대괴수 고모라(ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=34368808)

```json
{
  "review_id": "R4648",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4649 — 시리즈 진좌수 우주괴수 에레킹 (ver.A) (1개)

상품 ID: 3241

- [울트라맨 시리즈 진좌수 우주괴수 에레킹 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=54889443)

```json
{
  "review_id": "R4649",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4650 — 시리즈 진좌수 우주괴수 에레킹 (ver.B) (1개)

상품 ID: 3240

- [울트라맨 시리즈 진좌수 우주괴수 에레킹 (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=27981645)

```json
{
  "review_id": "R4650",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4651 — 시온 (가칭) (1개)

상품 ID: 4146

- [전생했더니 슬라임이었던 건에 대하여 시온 피규어 (가칭)](https://www.bnkrmall.co.kr/goods/detail.do?gno=19823443)

```json
{
  "review_id": "R4651",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4652 — 시즌3 시마 린 (1개)

상품 ID: 3915

- [유루캠△ 시즌3 시마 린 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=49170282)

```json
{
  "review_id": "R4652",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4653 — 시즌3 카가미하라 나데시코 (1개)

상품 ID: 3916

- [유루캠△ 시즌3 카가미하라 나데시코 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=93909605)

```json
{
  "review_id": "R4653",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4654 — 시즌3 펜 프렌드 시마 린 (1개)

상품 ID: 4107

- [유루캠△ 시즌3 펜 프렌드 시마 린](https://www.bnkrmall.co.kr/goods/detail.do?gno=88298882)

```json
{
  "review_id": "R4654",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4655 — 시즌3 펜 프렌드 카가미하라 나데시코 (1개)

상품 ID: 4121

- [유루캠△ 시즌3 펜 프렌드 카가미하라 나데시코](https://www.bnkrmall.co.kr/goods/detail.do?gno=4966194)

```json
{
  "review_id": "R4655",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4656 — 시즌3 펜 프렌드 토키 아야노 (1개)

상품 ID: 4120

- [유루캠△ 시즌3 펜 프렌드 토키 아야노](https://www.bnkrmall.co.kr/goods/detail.do?gno=95020241)

```json
{
  "review_id": "R4656",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4657 — 시즌7 미도리아 이즈쿠 COLOR VER. (1개)

상품 ID: 4081

- [나의 히어로 아카데미아 시즌7 피규어 미도리아 이즈쿠 COLOR VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=13830740)

```json
{
  "review_id": "R4657",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4658 — 시즌7 바쿠고 카츠키 (1개)

상품 ID: 4131

- [나의 히어로 아카데미아 시즌7 피규어 바쿠고 카츠키](https://www.bnkrmall.co.kr/goods/detail.do?gno=25840327)

```json
{
  "review_id": "R4658",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4659 — 신데렐라 걸즈 CELESTIAL VIVI 시부야 린 (1개)

상품 ID: 4385

- [아이돌마스터 신데렐라 걸즈 CELESTIAL VIVI 시부야 린](https://www.bnkrmall.co.kr/goods/detail.do?gno=59567)

```json
{
  "review_id": "R4659",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4660 — 신데렐라 걸즈 CELESTIAL VIVI 하야미 카나데 (1개)

상품 ID: 4481

- [아이돌마스터 신데렐라 걸즈 CELESTIAL VIVI 하야미 카나데](https://www.bnkrmall.co.kr/goods/detail.do?gno=58553)

```json
{
  "review_id": "R4660",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4661 — 신데렐라 걸즈 EMOTIONAL LENS 오토쿠라 유우키 (1개)

상품 ID: 4255

- [아이돌마스터 신데렐라 걸즈 EMOTIONAL LENS 오토쿠라 유우키](https://www.bnkrmall.co.kr/goods/detail.do?gno=92426702)

```json
{
  "review_id": "R4661",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4662 — 아기토 영웅용상 가면라이더 아기토 그라운드 폼(Ver.A) (1개)

상품 ID: 4522

- [가면라이더 아기토 영웅용상 가면라이더 아기토 그라운드 폼(Ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56872)

```json
{
  "review_id": "R4662",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4663 — 아리마 카나 AIR FLOW (1개)

상품 ID: 4049

- [【최애의 아이】 아리마 카나 AIR FLOW 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=71614196)

```json
{
  "review_id": "R4663",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4664 — 아리마 카나 『POP IN 2』VER. (1개)

상품 ID: 3939

- [【최애의 아이】 아리마 카나 『POP IN 2』VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=25989806)

```json
{
  "review_id": "R4664",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4665 — 아리마 카나 브라이덜 드레스 (1개)

상품 ID: 4039

- [【최애의 아이】 아리마 카나 브라이덜 드레스 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=22337388)

```json
{
  "review_id": "R4665",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4666 — 아리마 카나 사복 데이트 (1개)

상품 ID: 4249

- [【최애의 아이】 아리마 카나 사복 데이트 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=28790198)

```json
{
  "review_id": "R4666",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4667 — 아리마 카나 츠루기 VER. (1개)

상품 ID: 4037

- [【최애의 아이】 아리마 카나 츠루기 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=44783456)

```json
{
  "review_id": "R4667",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4668 — 아마가미 씨네 인연 맺기 아마가미 아사히 바니 VER. (1개)

상품 ID: 4033

- [아마가미 씨네 인연 맺기 아마가미 아사히 바니 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=78324832)

```json
{
  "review_id": "R4668",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4669 — 아마가미 씨네 인연 맺기 아마가미 야에 바니 VER. (1개)

상품 ID: 4046

- [아마가미 씨네 인연 맺기 아마가미 야에 피규어 바니 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=84756352)

```json
{
  "review_id": "R4669",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4670 — 아마가미 씨네 인연 맺기 아마가미 유나 바니 VER. (1개)

상품 ID: 4012

- [아마가미 씨네 인연 맺기 아마가미 유나 바니 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=68267882)

```json
{
  "review_id": "R4670",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4671 — 아마테 유즈리하 & 하로 엔딩 ver. (1개)

상품 ID: 3409

- [기동전사 건담 GQuuuuuuX 아마테 유즈리하 & 하로 피규어 엔딩 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=35846150)

```json
{
  "review_id": "R4671",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4672 — 아스란 자라 (1개)

상품 ID: 4176

- [기동전사 건담 SEED FREEDOM 아스란 자라 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=10985080)

```json
{
  "review_id": "R4672",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4673 — 아시로 미나 [THE METALLIC] (1개)

상품 ID: 4071

- [괴수 8호 아시로 미나 (THE METALLIC)](https://www.bnkrmall.co.kr/goods/detail.do?gno=23830630)

```json
{
  "review_id": "R4673",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4674 — 아이 -사인은 B (1개)

상품 ID: 4162

- [【최애의 아이】 아이 -사인은 B- 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=84917074)

```json
{
  "review_id": "R4674",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4675 — 아이 브라이덜 드레스 (1개)

상품 ID: 4070

- [【최애의 아이】 아이 브라이덜 드레스 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=56477654)

```json
{
  "review_id": "R4675",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4676 — 아쿠아 AIR FLOW (1개)

상품 ID: 4047

- [【최애의 아이】 아쿠아 AIR FLOW 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=45442059)

```json
{
  "review_id": "R4676",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4677 — 앉은 자세 아로나 (1개)

상품 ID: 3883

- [블루 아카이브 앉은 자세 피규어 아로나](https://www.bnkrmall.co.kr/goods/detail.do?gno=13906876)

```json
{
  "review_id": "R4677",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4678 — 앉은 자세 페른 (1개)

상품 ID: 4044

- [장송의 프리렌 앉은 자세 피규어 페른](https://www.bnkrmall.co.kr/goods/detail.do?gno=71729485)

```json
{
  "review_id": "R4678",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4679 — 앉은 자세 프라나 (1개)

상품 ID: 3882

- [블루 아카이브 앉은 자세 피규어 프라나](https://www.bnkrmall.co.kr/goods/detail.do?gno=62241553)

```json
{
  "review_id": "R4679",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4680 — 앉은 자세 프리렌 (1개)

상품 ID: 4045

- [장송의 프리렌 앉은 자세 피규어 프리렌](https://www.bnkrmall.co.kr/goods/detail.do?gno=21656575)

```json
{
  "review_id": "R4680",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4681 — 암흑무술대회 도구로 동생 100% (1개)

상품 ID: 4080

- [유유백서 암흑무술대회 도구로 동생 100%](https://www.bnkrmall.co.kr/goods/detail.do?gno=61166614)

```json
{
  "review_id": "R4681",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4682 — 암흑무술대회 요호 쿠라마 (1개)

상품 ID: 4001

- [유유백서 암흑무술대회 요호 쿠라마](https://www.bnkrmall.co.kr/goods/detail.do?gno=26375960)

```json
{
  "review_id": "R4682",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4683 — 암흑무술대회 쿠라마 (1개)

상품 ID: 4167

- [유유백서 암흑무술대회 쿠라마](https://www.bnkrmall.co.kr/goods/detail.do?gno=95659159)

```json
{
  "review_id": "R4683",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4684 — 암흑무술대회 쿠와바라 카즈마 (1개)

상품 ID: 4128

- [유유백서 암흑무술대회 쿠와바라 카즈마](https://www.bnkrmall.co.kr/goods/detail.do?gno=61953123)

```json
{
  "review_id": "R4684",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4685 — 암흑무술대회 히에이 흑룡파 이펙트 VER. (1개)

상품 ID: 4059

- [유유백서 암흑무술대회 히에이 흑룡파 이펙트 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=70069582)

```json
{
  "review_id": "R4685",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4686 — 앨리시제이션 WAR OF UNDERWORLD 지신 테라리아 리파 (1개)

상품 ID: 4628

- [소드 아트 온라인 앨리시제이션 WAR OF UNDERWORLD 지신 테라리아 리파](https://www.bnkrmall.co.kr/goods/detail.do?gno=55480)

```json
{
  "review_id": "R4686",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4687 — 앨리시제이션 WAR OF UNDERWORLD 키리토 (1개)

상품 ID: 4462

- [소드 아트 온라인 앨리시제이션 WAR OF UNDERWORLD 키리토 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=58831)

```json
{
  "review_id": "R4687",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4688 — 어느 카페의 페른 (1개)

상품 ID: 3291

- [장송의 프리렌 피규어 어느 카페의 페른](https://www.bnkrmall.co.kr/goods/detail.do?gno=66358619)

```json
{
  "review_id": "R4688",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4689 — 어느 카페의 프리렌 (1개)

상품 ID: 3292

- [장송의 프리렌 피규어 어느 카페의 프리렌](https://www.bnkrmall.co.kr/goods/detail.do?gno=9083617)

```json
{
  "review_id": "R4689",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4690 — 어몽 어스 BIG SOFVIMATES vol.1 (A:레드) (1개)

상품 ID: 3555

- [어몽 어스 BIG SOFVIMATES vol.1 (A:레드)](https://www.bnkrmall.co.kr/goods/detail.do?gno=27481491)

```json
{
  "review_id": "R4690",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4691 — 어몽 어스 BIG SOFVIMATES vol.1 (B:블루) (1개)

상품 ID: 3554

- [어몽 어스 BIG SOFVIMATES vol.1 (B:블루)](https://www.bnkrmall.co.kr/goods/detail.do?gno=94007181)

```json
{
  "review_id": "R4691",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4692 — 어몽 어스 모니터 탑 vol.1 (A:레드) (1개)

상품 ID: 3773

- [어몽 어스 모니터 탑 피규어 vol.1 (A:레드)](https://www.bnkrmall.co.kr/goods/detail.do?gno=30624209)

```json
{
  "review_id": "R4692",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4693 — 어몽 어스 모니터 탑 vol.1 (B:블루) (1개)

상품 ID: 3772

- [어몽 어스 모니터 탑 피규어 vol.1 (B:블루)](https://www.bnkrmall.co.kr/goods/detail.do?gno=18670083)

```json
{
  "review_id": "R4693",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4694 — 어몽 어스 모니터 탑 vol.1 (C:옐로우) (1개)

상품 ID: 3771

- [어몽 어스 모니터 탑 피규어 vol.1 (C:옐로우)](https://www.bnkrmall.co.kr/goods/detail.do?gno=74952521)

```json
{
  "review_id": "R4694",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4695 — 어몽 어스 모니터 탑 vol.1 (D:핑크) (1개)

상품 ID: 3468

- [어몽 어스 모니터 탑 피규어 vol.1 (D:핑크)](https://www.bnkrmall.co.kr/goods/detail.do?gno=76368258)

```json
{
  "review_id": "R4695",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4696 — 에이지 오브 히어로즈 CREATY&DEKU (야오요로즈 모모) (1개)

상품 ID: 4575

- [나의 히어로 아카데미아 에이지 오브 히어로즈 CREATY&DEKU (야오요로즈 모모)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56519)

```json
{
  "review_id": "R4696",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4697 — 에이지 오브 히어로즈 데쿠Ⅲ (1개)

상품 ID: 4251

- [나의 히어로 아카데미아 에이지 오브 히어로즈 데쿠Ⅲ](https://www.bnkrmall.co.kr/goods/detail.do?gno=94950548)

```json
{
  "review_id": "R4697",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4698 — 에이지 오브 히어로즈 르밀리옹 스페셜 (1개)

상품 ID: 4458

- [나의 히어로 아카데미아 에이지 오브 히어로즈 르밀리옹 스페셜](https://www.bnkrmall.co.kr/goods/detail.do?gno=58836)

```json
{
  "review_id": "R4698",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4699 — 에이지 오브 히어로즈 엔데버&쇼토 (엔데버) (1개)

상품 ID: 4711

- [나의 히어로 아카데미아 에이지 오브 히어로즈 엔데버&쇼토 (엔데버)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15238)

```json
{
  "review_id": "R4699",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4700 — 에이지 오브 히어로즈 엔데버 스페셜 (1개)

상품 ID: 4283

- [나의 히어로 아카데미아 에이지 오브 히어로즈 엔데버 스페셜](https://www.bnkrmall.co.kr/goods/detail.do?gno=11473865)

```json
{
  "review_id": "R4700",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4701 — 에이지 오브 히어로즈 올마이트 (1개)

상품 ID: 4480

- [나의 히어로 아카데미아 에이지 오브 히어로즈 올마이트](https://www.bnkrmall.co.kr/goods/detail.do?gno=58554)

```json
{
  "review_id": "R4701",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4702 — 에이지 오브 히어로즈 올마이트 스페셜 VER.A (1개)

상품 ID: 4482

- [나의 히어로 아카데미아 에이지 오브 히어로즈 올마이트 스페셜 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=58552)

```json
{
  "review_id": "R4702",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4703 — 엘란 케레스 (강화 인간 5호) (1개)

상품 ID: 4202

- [기동전사 건담 수성의 마녀 엘란 케레스 (강화 인간 5호) 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=73352841)

```json
{
  "review_id": "R4703",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4704 — 열일의 황금향 BIG Fluffy Puffy 나나치 (1개)

상품 ID: 3722

- [메이드 인 어비스 열일의 황금향 BIG Fluffy Puffy 나나치](https://www.bnkrmall.co.kr/goods/detail.do?gno=44050378)

```json
{
  "review_id": "R4704",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4705 — 열일의 황금향 BIG Fluffy Puffy 미티 (1개)

상품 ID: 3721

- [메이드 인 어비스 열일의 황금향 BIG Fluffy Puffy 미티](https://www.bnkrmall.co.kr/goods/detail.do?gno=37856953)

```json
{
  "review_id": "R4705",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4706 — 열일의 황금향 소프비 나나치 (1개)

상품 ID: 3975

- [메이드 인 어비스 열일의 황금향 소프비 피규어 나나치](https://www.bnkrmall.co.kr/goods/detail.do?gno=88427592)

```json
{
  "review_id": "R4706",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4707 — 영웅용상 가면라이더 덴오 소드 폼 VER.A (1개)

상품 ID: 4599

- [가면라이더 영웅용상 가면라이더 덴오 소드 폼 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=56094)

```json
{
  "review_id": "R4707",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4708 — 영웅용상 가면라이더 쿠우가 마이티 폼 (1개)

상품 ID: 4696

- [가면라이더 영웅용상 가면라이더 쿠우가 마이티 폼](https://www.bnkrmall.co.kr/goods/detail.do?gno=15499)

```json
{
  "review_id": "R4708",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4709 — 영웅용상 스카이라이더 VER.A (1개)

상품 ID: 4532

- [가면라이더 영웅용상 스카이라이더 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=56845)

```json
{
  "review_id": "R4709",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4710 — 오드리 번 (1개)

상품 ID: 4213

- [기동전사 건담 UC 오드리 번 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=49442234)

```json
{
  "review_id": "R4710",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4711 — 오로치마루 (1개)

상품 ID: 3391

- [나루토 오로치마루 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=64924373)

```json
{
  "review_id": "R4711",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4712 — 오메가몬 (1개)

상품 ID: 3247

- [디지몬 어드벤처 오메가몬](https://www.bnkrmall.co.kr/goods/detail.do?gno=96412460)

```json
{
  "review_id": "R4712",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4713 — 오버로드 BANPRESTO EVOLVE-Empress of Darkness-알베도 (1개)

상품 ID: 2587

- [오버로드 BANPRESTO EVOLVE-Empress of Darkness-알베도 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=91974816)

```json
{
  "review_id": "R4713",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4714 — 오버로드 Classical tuning 천일야화 (1개)

상품 ID: 3643

- [오버로드 Classical tuning 천일야화 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=72431459)

```json
{
  "review_id": "R4714",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4715 — 오버로드 IF 알베도 BIKINI ARMOR VER. (1개)

상품 ID: 3917

- [오버로드 IF 알베도 피규어 BIKINI ARMOR VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=56736649)

```json
{
  "review_id": "R4715",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4716 — 오버로드 IF 알베도 TEACHER STYLE VER. (1개)

상품 ID: 3976

- [오버로드 IF 알베도 피규어 TEACHER STYLE VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=31725861)

```json
{
  "review_id": "R4716",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4717 — 오버로드 아인즈 울 고운 (1개)

상품 ID: 4009

- [오버로드 아인즈 울 고운 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=6842866)

```json
{
  "review_id": "R4717",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4718 — 오버로드 알베도 (1개)

상품 ID: 4010

- [오버로드 알베도 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=87178305)

```json
{
  "review_id": "R4718",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4719 — 오이카와 토오루 (1개)

상품 ID: 3766

- [하이큐!! 오이카와 토오루 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=30839969)

```json
{
  "review_id": "R4719",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4720 — 올마이트&올포원 (가칭) (A:올마이트) (1개)

상품 ID: 3865

- [나의 히어로 아카데미아 피규어 올마이트&올포원 (가칭) (A:올마이트)](https://www.bnkrmall.co.kr/goods/detail.do?gno=64979589)

```json
{
  "review_id": "R4720",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4721 — 올마이트&올포원 (가칭) (B:올포원) (1개)

상품 ID: 3864

- [나의 히어로 아카데미아 피규어 올마이트&올포원 (가칭) (B:올포원)](https://www.bnkrmall.co.kr/goods/detail.do?gno=91021812)

```json
{
  "review_id": "R4721",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4722 — 와카츠키 니코 (1개)

상품 ID: 3903

- [위치 워치 피규어 와카츠키 니코](https://www.bnkrmall.co.kr/goods/detail.do?gno=66452627)

```json
{
  "review_id": "R4722",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4723 — 와카츠키 니코 vol.2 (1개)

상품 ID: 3878

- [위치 워치 피규어 와카츠키 니코 vol.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=11652338)

```json
{
  "review_id": "R4723",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4724 — 우마무스메 신데렐라 그레이 BANPRESTO EVOLVE 오구리 캡 (1개)

상품 ID: 2594

- [우마무스메 신데렐라 그레이 BANPRESTO EVOLVE 오구리 캡 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=25099191)

```json
{
  "review_id": "R4724",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4725 — 우마무스메 신데렐라 그레이 BANPRESTO EVOLVE 타마모 크로스 (1개)

상품 ID: 2533

- [우마무스메 신데렐라 그레이 BANPRESTO EVOLVE 타마모 크로스 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=37382511)

```json
{
  "review_id": "R4725",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4726 — 우마무스메 프리티더비 BoC'z we\n 베르시나 as Queen V (1개)

상품 ID: 3553

- [우마무스메 프리티더비 BoC'z we\n 베르시나 as Queen V 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=88666690)

```json
{
  "review_id": "R4726",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4727 — 우마무스메 프리티더비 BoC'z we\n 비블로스 as Lil♡V (1개)

상품 ID: 3477

- [우마무스메 프리티더비 BoC'z we\n 비블로스 as Lil♡V 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=67915176)

```json
{
  "review_id": "R4727",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4728 — 우마무스메 프리티더비 BoC'z we\n 슈발 그랑 as Marine C (1개)

상품 ID: 3552

- [우마무스메 프리티더비 BoC'z we\n 슈발 그랑 as Marine C 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=27275549)

```json
{
  "review_id": "R4728",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4729 — 우마무스메 프리티더비 BoC'z wen 나카야마 페스타 as AT MAHANE (1개)

상품 ID: 3399

- [우마무스메 프리티더비 BoC'z wen 나카야마 페스타 as AT MAHANE 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=51914434)

```json
{
  "review_id": "R4729",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4730 — 우마무스메 프리티더비 BoC'z wen 노스 플라이트 as F-Style (1개)

상품 ID: 3434

- [우마무스메 프리티더비 BoC'z wen 노스 플라이트 as F-Style 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=40995994)

```json
{
  "review_id": "R4730",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4731 — 우마무스메 프리티더비 BoC'z wen 라이스 샤워 as Oryza (1개)

상품 ID: 3398

- [우마무스메 프리티더비 BoC'z wen 라이스 샤워 as Oryza 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=6097234)

```json
{
  "review_id": "R4731",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4732 — 우마무스메 프리티더비 BoC'z wen 러브즈 온리 유 (1개)

상품 ID: 3433

- [우마무스메 프리티더비 BoC'z wen 러브즈 온리 유 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=3401990)

```json
{
  "review_id": "R4732",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4733 — 우마무스메 프리티더비 BoC＇z 라이스 샤워(오리자) (1개)

상품 ID: 3977

- [우마무스메 프리티더비 BoC＇z 라이스 샤워(오리자) 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=3898775)

```json
{
  "review_id": "R4733",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4734 — 우마무스메 프리티더비 BoC＇z 마치카네 탄호이저(816-n) (1개)

상품 ID: 3978

- [우마무스메 프리티더비 BoC＇z 마치카네 탄호이저(816-n) 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=70289501)

```json
{
  "review_id": "R4734",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4735 — 우마무스메 프리티더비 BoC＇z 미스터 시비 (캡 비) (1개)

상품 ID: 4013

- [우마무스메 프리티더비 BoC＇z 미스터 시비 (캡 비) 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=228730)

```json
{
  "review_id": "R4735",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4736 — 우마무스메 프리티더비 BoC＇z 슈발 그랑(마린C) (1개)

상품 ID: 3965

- [우마무스메 프리티더비 BoC＇z 슈발 그랑(마린C) 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=76593011)

```json
{
  "review_id": "R4736",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4737 — 우마무스메 프리티더비 BoC'z 홋코 타루마에(MACOtMai) (1개)

상품 ID: 3497

- [우마무스메 프리티더비 BoC'z 홋코 타루마에(MACOtMai) 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=39914939)

```json
{
  "review_id": "R4737",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4738 — 우마무스메 프리티더비 골드십 (1개)

상품 ID: 4475

- [우마무스메 프리티더비 골드십 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=58576)

```json
{
  "review_id": "R4738",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4739 — 우마무스메 프리티더비 그래스 원더 (1개)

상품 ID: 4172

- [우마무스메 프리티더비 그래스 원더 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=45694795)

```json
{
  "review_id": "R4739",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4740 — 우마무스메 프리티더비 나리타 탑 로드 (1개)

상품 ID: 4290

- [우마무스메 프리티더비 나리타 탑 로드 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=92468866)

```json
{
  "review_id": "R4740",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4741 — 우마무스메 프리티더비 나이스 네이처 (1개)

상품 ID: 4345

- [우마무스메 프리티더비 나이스 네이처 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=54418013)

```json
{
  "review_id": "R4741",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4742 — 우마무스메 프리티더비 다이와 스칼렛 (1개)

상품 ID: 4229

- [우마무스메 프리티더비 다이와 스칼렛 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=18285337)

```json
{
  "review_id": "R4742",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4743 — 우마무스메 프리티더비 다이타쿠 헬리오스 (1개)

상품 ID: 4384

- [우마무스메 프리티더비 다이타쿠 헬리오스 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59568)

```json
{
  "review_id": "R4743",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4744 — 우마무스메 프리티더비 라이스 샤워 (1개)

상품 ID: 4473

- [우마무스메 프리티더비 라이스 샤워 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=58588)

```json
{
  "review_id": "R4744",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4745 — 우마무스메 프리티더비 마루젠스키 (1개)

상품 ID: 4161

- [우마무스메 프리티더비 마루젠스키 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=26075883)

```json
{
  "review_id": "R4745",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4746 — 우마무스메 프리티더비 마야노 탑건 (1개)

상품 ID: 4400

- [우마무스메 프리티더비 마야노 탑건 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59548)

```json
{
  "review_id": "R4746",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4747 — 우마무스메 프리티더비 마치카네 탄호이저 (1개)

상품 ID: 4346

- [우마무스메 프리티더비 마치카네 탄호이저 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=25780847)

```json
{
  "review_id": "R4747",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4748 — 우마무스메 프리티더비 맨하탄 카페 (1개)

상품 ID: 4206

- [우마무스메 프리티더비 맨하탄 카페 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=57859831)

```json
{
  "review_id": "R4748",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4749 — 우마무스메 프리티더비 메이쇼 도토 (1개)

상품 ID: 4295

- [우마무스메 프리티더비 메이쇼 도토 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=35969971)

```json
{
  "review_id": "R4749",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4750 — 우마무스메 프리티더비 메지로 도베르 (1개)

상품 ID: 4352

- [우마무스메 프리티더비 메지로 도베르 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59971)

```json
{
  "review_id": "R4750",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4751 — 우마무스메 프리티더비 메지로 라이언 (1개)

상품 ID: 4351

- [우마무스메 프리티더비 메지로 라이언 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59972)

```json
{
  "review_id": "R4751",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4752 — 우마무스메 프리티더비 메지로 맥퀸 (1개)

상품 ID: 4405

- [우마무스메 프리티더비 메지로 맥퀸 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59535)

```json
{
  "review_id": "R4752",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4753 — 우마무스메 프리티더비 미스터 시비 (1개)

상품 ID: 4199

- [우마무스메 프리티더비 미스터 시비 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=19623021)

```json
{
  "review_id": "R4753",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4754 — 우마무스메 프리티더비 미호노 부르봉 (1개)

상품 ID: 4470

- [우마무스메 프리티더비 미호노 부르봉 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=58819)

```json
{
  "review_id": "R4754",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4755 — 우마무스메 프리티더비 보드카 (1개)

상품 ID: 4230

- [우마무스메 프리티더비 보드카 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=29314909)

```json
{
  "review_id": "R4755",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4756 — 우마무스메 프리티더비 사일런스 스즈카 (1개)

상품 ID: 4422

- [우마무스메 프리티더비 사일런스 스즈카 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59287)

```json
{
  "review_id": "R4756",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4757 — 우마무스메 프리티더비 사쿠라 로렐 (1개)

상품 ID: 4095

- [우마무스메 프리티더비 사쿠라 로렐 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=4487585)

```json
{
  "review_id": "R4757",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4758 — 우마무스메 프리티더비 사토노 다이아몬드 (1개)

상품 ID: 4366

- [우마무스메 프리티더비 사토노 다이아몬드 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59832)

```json
{
  "review_id": "R4758",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4759 — 우마무스메 프리티더비 스마트 팔콘 (1개)

상품 ID: 4254

- [우마무스메 프리티더비 스마트 팔콘 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=16526044)

```json
{
  "review_id": "R4759",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4760 — 우마무스메 프리티더비 스페셜 위크 (1개)

상품 ID: 4423

- [우마무스메 프리티더비 스페셜 위크 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59286)

```json
{
  "review_id": "R4760",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4761 — 우마무스메 프리티더비 심볼리 루돌프 (1개)

상품 ID: 4200

- [우마무스메 프리티더비 심볼리 루돌프 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=36851597)

```json
{
  "review_id": "R4761",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4762 — 우마무스메 프리티더비 아그네스 타키온 (1개)

상품 ID: 4207

- [우마무스메 프리티더비 아그네스 타키온 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=5062099)

```json
{
  "review_id": "R4762",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4763 — 우마무스메 프리티더비 어드마이어 베가 (1개)

상품 ID: 4296

- [우마무스메 프리티더비 어드마이어 베가 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=99208165)

```json
{
  "review_id": "R4763",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4764 — 우마무스메 프리티더비 에어 그루브 (1개)

상품 ID: 4175

- [우마무스메 프리티더비 에어 그루브 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=58982284)

```json
{
  "review_id": "R4764",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4765 — 우마무스메 프리티더비 에어 샤커 (1개)

상품 ID: 4260

- [우마무스메 프리티더비 에어 샤커 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=47675701)

```json
{
  "review_id": "R4765",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4766 — 우마무스메 프리티더비 에이신 플래시 (1개)

상품 ID: 4180

- [우마무스메 프리티더비 에이신 플래시 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=4518369)

```json
{
  "review_id": "R4766",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4767 — 우마무스메 프리티더비 엘 콘도르 파사 (1개)

상품 ID: 4171

- [우마무스메 프리티더비 엘 콘도르 파사 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=68400048)

```json
{
  "review_id": "R4767",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4768 — 우마무스메 프리티더비 오구리 캡 (1개)

상품 ID: 4427

- [우마무스메 프리티더비 오구리 캡 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59246)

```json
{
  "review_id": "R4768",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4769 — 우마무스메 프리티더비 이쿠노 딕터스 (1개)

상품 ID: 4335

- [우마무스메 프리티더비 이쿠노 딕터스 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=55566403)

```json
{
  "review_id": "R4769",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4770 — 우마무스메 프리티더비 카렌짱 (1개)

상품 ID: 4322

- [우마무스메 프리티더비 카렌짱 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=96399866)

```json
{
  "review_id": "R4770",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4771 — 우마무스메 프리티더비 키타산 블랙 (1개)

상품 ID: 4367

- [우마무스메 프리티더비 키타산 블랙 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59831)

```json
{
  "review_id": "R4771",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4772 — 우마무스메 프리티더비 토카이 테이오 (1개)

상품 ID: 4406

- [우마무스메 프리티더비 토카이 테이오 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=59534)

```json
{
  "review_id": "R4772",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4773 — 우마무스메 프리티더비 트윈 터보 (1개)

상품 ID: 4334

- [우마무스메 프리티더비 트윈 터보 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=68131851)

```json
{
  "review_id": "R4773",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4774 — 우마무스메 프리티더비 티엠 오페라 오 (1개)

상품 ID: 4314

- [우마무스메 프리티더비 티엠 오페라 오 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=55147874)

```json
{
  "review_id": "R4774",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4775 — 우마무스메 프리티더비 파인 모션 (1개)

상품 ID: 4259

- [우마무스메 프리티더비 파인 모션 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=63239367)

```json
{
  "review_id": "R4775",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4776 — 우미노 이루카 - 즐거운 한 때 (1개)

상품 ID: 4147

- [나루토 우미노 이루카 피규어 - 즐거운 한 때](https://www.bnkrmall.co.kr/goods/detail.do?gno=21463035)

```json
{
  "review_id": "R4776",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4777 — 우자키 양은 놀고 싶어! 이터널 로맨스 우자키 츠키 스웨터 수영복 ver. (1개)

상품 ID: 3576

- [우자키 양은 놀고 싶어! 이터널 로맨스 우자키 츠키 스웨터 수영복 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=46533606)

```json
{
  "review_id": "R4777",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4778 — 우자키 양은 놀고 싶어! 이터널 로맨스 우자키 하나 스웨터 수영복 ver. (1개)

상품 ID: 3577

- [우자키 양은 놀고 싶어! 이터널 로맨스 우자키 하나 스웨터 수영복 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=82681167)

```json
{
  "review_id": "R4778",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4779 — 우즈마키 나루토 (TV애니메이션 20주년 기념 의상) (1개)

상품 ID: 4271

- [나루토 질풍전 우즈마키 나루토 피규어 (TV애니메이션 20주년 기념 의상)](https://www.bnkrmall.co.kr/goods/detail.do?gno=68398568)

```json
{
  "review_id": "R4779",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4780 — 우즈마키 나루토 - 즐거운 한 때 (1개)

상품 ID: 4148

- [나루토 우즈마키 나루토 피규어 - 즐거운 한 때](https://www.bnkrmall.co.kr/goods/detail.do?gno=88580010)

```json
{
  "review_id": "R4780",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4781 — 우즈마키 나루토・나미카제 미나토 (B:나미카제 미나토) (1개)

상품 ID: 3489

- [나루토 질풍전 피규어 우즈마키 나루토・나미카제 미나토 (B:나미카제 미나토)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59435937)

```json
{
  "review_id": "R4781",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4782 — 우치하 마다라 (1개)

상품 ID: 3260

- [나루토 질풍전 피규어 우치하 마다라](https://www.bnkrmall.co.kr/goods/detail.do?gno=82865500)

```json
{
  "review_id": "R4782",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4783 — 우치하 사스케 & 우치하 이타치 (A:우치하 사스케) (1개)

상품 ID: 3660

- [나루토 질풍전 피규어 우치하 사스케 & 우치하 이타치 (A:우치하 사스케)](https://www.bnkrmall.co.kr/goods/detail.do?gno=84889270)

```json
{
  "review_id": "R4783",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4784 — 우치하 사스케 & 우치하 이타치 (B:우치하 이타치) (1개)

상품 ID: 3659

- [나루토 질풍전 피규어 우치하 사스케 & 우치하 이타치 (B:우치하 이타치)](https://www.bnkrmall.co.kr/goods/detail.do?gno=70594469)

```json
{
  "review_id": "R4784",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4785 — 우치하 사스케 (TV애니메이션 20주년 기념 의상) (1개)

상품 ID: 4270

- [나루토 질풍전 우치하 사스케 피규어 (TV애니메이션 20주년 기념 의상)](https://www.bnkrmall.co.kr/goods/detail.do?gno=51432315)

```json
{
  "review_id": "R4785",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4786 — 울티메이트 병사 SON GOKU (손오공) (1개)

상품 ID: 4661

- [드래곤볼 GT 울티메이트 병사 SON GOKU (손오공)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15906)

```json
{
  "review_id": "R4786",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4787 — 울티메이트 병사 SON GOKU (초사이어인 손오공) (1개)

상품 ID: 4658

- [드래곤볼 GT 울티메이트 병사 SON GOKU (초사이어인 손오공)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15907)

```json
{
  "review_id": "R4787",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4788 — 울티메이트 병사 TRUNKS (트랭크스) (1개)

상품 ID: 4501

- [드래곤볼 GT 울티메이트 병사 TRUNKS (트랭크스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57291)

```json
{
  "review_id": "R4788",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4789 — 원피스 클로니클 마스터 스타 피스 롤로노아 조로 (1개)

상품 ID: 3158

- [원피스 반프레스토 클로니클 마스터 스타 피스 롤로노아 조로](https://www.bnkrmall.co.kr/goods/detail.do?gno=56809)

```json
{
  "review_id": "R4789",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4790 — 원피스 클로니클 마스터 스타 피스 몽키 D 루피 (1개)

상품 ID: 3187

- [원피스 반프레스토 클로니클 마스터 스타 피스 몽키 D 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=55756)

```json
{
  "review_id": "R4790",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4791 — 원피스 클로니클 마스터 스타 피스 사보 (1개)

상품 ID: 3170

- [원피스 반프레스토 클로니클 마스터 스타 피스 사보](https://www.bnkrmall.co.kr/goods/detail.do?gno=56312)

```json
{
  "review_id": "R4791",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4792 — 원피스 클로니클 월드 콜로세움4 Vol.1 몽키 D 루피 (1개)

상품 ID: 3166

- [원피스 반프레스토 클로니클 월드 피규어 콜로세움4 Vol.1 몽키 D 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=56670)

```json
{
  "review_id": "R4792",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4793 — 원피스 클로니클 플래그 다이아몬드 쉽 보아 핸콕 (1개)

상품 ID: 3099

- [원피스 반프레스토 클로니클 플래그 다이아몬드 쉽 보아 핸콕](https://www.bnkrmall.co.kr/goods/detail.do?gno=59543)

```json
{
  "review_id": "R4793",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4794 — 유희왕 듀얼 몬스터즈 붉은 눈의 흑룡 (1개)

상품 ID: 4101

- [유희왕 듀얼 몬스터즈 붉은 눈의 흑룡 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=73096352)

```json
{
  "review_id": "R4794",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4795 — 유희왕 듀얼 몬스터즈 푸른 눈의 백룡 (1개)

상품 ID: 4102

- [유희왕 듀얼 몬스터즈 푸른 눈의 백룡 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=54055035)

```json
{
  "review_id": "R4795",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4796 — 유희왕 전광절경 블랙 매지션 걸 (1개)

상품 ID: 4066

- [유희왕 전광절경 블랙 매지션 걸](https://www.bnkrmall.co.kr/goods/detail.do?gno=12299171)

```json
{
  "review_id": "R4796",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4797 — 유희왕 전광절경 어둠의 유우기 (1개)

상품 ID: 4067

- [유희왕 전광절경 어둠의 유우기](https://www.bnkrmall.co.kr/goods/detail.do?gno=15555596)

```json
{
  "review_id": "R4797",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4798 — 은혼 3학년 Z반 긴파치 선생 데스크 사카타 긴파치 (1개)

상품 ID: 3781

- [은혼 3학년 Z반 긴파치 선생 데스크 피규어 사카타 긴파치](https://www.bnkrmall.co.kr/goods/detail.do?gno=8968208)

```json
{
  "review_id": "R4798",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4799 — 은혼 3학년 Z반 긴파치 선생 데스크 타카스기 신스케 (1개)

상품 ID: 3726

- [은혼 3학년 Z반 긴파치 선생 데스크 피규어 타카스기 신스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=85723256)

```json
{
  "review_id": "R4799",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4800 — 은혼 3학년 Z반 긴파치 선생 데스크 히지카타 토시로 (1개)

상품 ID: 3758

- [은혼 3학년 Z반 긴파치 선생 데스크 피규어 히지카타 토시로](https://www.bnkrmall.co.kr/goods/detail.do?gno=59273954)

```json
{
  "review_id": "R4800",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4801 — 은혼 사카타 긴토키 ANNIVERSARY VER. (1개)

상품 ID: 4083

- [은혼 사카타 긴토키 ANNIVERSARY VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=45725804)

```json
{
  "review_id": "R4801",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4802 — 은혼 피그라이프 언제나 마음에 한 자루의 드라이버 (1개)

상품 ID: 3624

- [은혼 피그라이프 언제나 마음에 한 자루의 드라이버](https://www.bnkrmall.co.kr/goods/detail.do?gno=3846670)

```json
{
  "review_id": "R4802",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4803 — 이노우에 타키나 (두사람의 여행) (1개)

상품 ID: 4088

- [리코리스 리코일 이노우에 타키나 (두사람의 여행)](https://www.bnkrmall.co.kr/goods/detail.do?gno=37064921)

```json
{
  "review_id": "R4803",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4804 — 이미지네이션 웍스 몽키 D 루피 (1개)

상품 ID: 2076

- [이미지네이션 웍스 몽키 D 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=58648)

```json
{
  "review_id": "R4804",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4805 — 이미지네이션 웍스 베지터 (1개)

상품 ID: 2122

- [이미지네이션 웍스 베지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=55048)

```json
{
  "review_id": "R4805",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4806 — 이블 빌런 DX 다비 (1개)

상품 ID: 3839

- [나의 히어로 아카데미아 이블 빌런 DX 다비](https://www.bnkrmall.co.kr/goods/detail.do?gno=54178533)

```json
{
  "review_id": "R4806",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4807 — 이블 빌런 DX 토가 히미코Ⅲ (1개)

상품 ID: 4097

- [나의 히어로 아카데미아 이블 빌런 DX 토가 히미코Ⅲ](https://www.bnkrmall.co.kr/goods/detail.do?gno=40430214)

```json
{
  "review_id": "R4807",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4808 — 이블 빌런 DX 토가 히미코 Ⅳ (1개)

상품 ID: 3870

- [나의 히어로 아카데미아 이블 빌런 DX 토가 히미코 Ⅳ](https://www.bnkrmall.co.kr/goods/detail.do?gno=60644500)

```json
{
  "review_id": "R4808",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4809 — 이블 빌런 VOL.3 (A:다비) (1개)

상품 ID: 4493

- [나의 히어로 아카데미아 이블 빌런 VOL.3 (A:다비)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57416)

```json
{
  "review_id": "R4809",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4810 — 이블 빌런 VOL.4 (1개)

상품 ID: 4439

- [나의 히어로 아카데미아 이블 빌런 VOL.4](https://www.bnkrmall.co.kr/goods/detail.do?gno=59225)

```json
{
  "review_id": "R4810",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4811 — 이블 빌런 VOL.6 (1개)

상품 ID: 4358

- [나의 히어로 아카데미아 이블 빌런 VOL.6](https://www.bnkrmall.co.kr/goods/detail.do?gno=59962)

```json
{
  "review_id": "R4811",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4812 — 이블 빌런 시가라키 토무라 (1개)

상품 ID: 4196

- [나의 히어로 아카데미아 이블 빌런 시가라키 토무라](https://www.bnkrmall.co.kr/goods/detail.do?gno=60738813)

```json
{
  "review_id": "R4812",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4813 — 이블 빌런 플러스 토가 히미코 (1개)

상품 ID: 4130

- [나의 히어로 아카데미아 이블 빌런 플러스 토가 히미코](https://www.bnkrmall.co.kr/goods/detail.do?gno=38268547)

```json
{
  "review_id": "R4813",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4814 — 이블 빌런 플러스 토가 히미코Ⅱ (1개)

상품 ID: 3810

- [나의 히어로 아카데미아 이블 빌런 플러스 토가 히미코Ⅱ](https://www.bnkrmall.co.kr/goods/detail.do?gno=96099872)

```json
{
  "review_id": "R4814",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4815 — 이치카와 레노 [THE METALLIC] (1개)

상품 ID: 4072

- [괴수 8호 이치카와 레노 (THE METALLIC)](https://www.bnkrmall.co.kr/goods/detail.do?gno=6002351)

```json
{
  "review_id": "R4815",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4816 — 이타도리 유지2 (1개)

상품 ID: 4372

- [주술회전 이타도리 유지2](https://www.bnkrmall.co.kr/goods/detail.do?gno=59822)

```json
{
  "review_id": "R4816",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4817 — 인계조형열전 나미카제 미나토 (1개)

상품 ID: 3646

- [나루토 질풍전 인계조형열전 나미카제 미나토](https://www.bnkrmall.co.kr/goods/detail.do?gno=822042)

```json
{
  "review_id": "R4817",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4818 — 인계조형열전 우즈마키 나루토 (1개)

상품 ID: 3333

- [나루토 질풍전 인계조형열전 우즈마키 나루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=81875063)

```json
{
  "review_id": "R4818",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4819 — 장송의 프리렌 피규어 (1개)

상품 ID: 3267

- [장송의 프리렌 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=26513578)

```json
{
  "review_id": "R4819",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4820 — 장착변신 쿠우가 마이티 폼 (1개)

상품 ID: 1753

- [장착변신 가면라이더 쿠우가 마이티 폼](https://www.bnkrmall.co.kr/goods/detail.do?gno=5366502)

```json
{
  "review_id": "R4820",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4821 — 전광절경 S-호크 (1개)

상품 ID: 3929

- [원피스 전광절경 S-호크](https://www.bnkrmall.co.kr/goods/detail.do?gno=1721242)

```json
{
  "review_id": "R4821",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4822 — 전광절경 도리 (1개)

상품 ID: 3738

- [원피스 전광절경 도리](https://www.bnkrmall.co.kr/goods/detail.do?gno=44718082)

```json
{
  "review_id": "R4822",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4823 — 전광절경 로브 루치 (1개)

상품 ID: 4240

- [원피스 전광절경 로브 루치](https://www.bnkrmall.co.kr/goods/detail.do?gno=17299547)

```json
{
  "review_id": "R4823",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4824 — 전광절경 로브 루치 고양고양 열매 모델 레오파드 각성폼 (1개)

상품 ID: 4093

- [원피스 전광절경 로브 루치 고양고양 열매 모델 레오파드 각성폼](https://www.bnkrmall.co.kr/goods/detail.do?gno=39405511)

```json
{
  "review_id": "R4824",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4825 — 전광절경 롤로노아 조로 (1개)

상품 ID: 4074

- [원피스 전광절경 롤로노아 조로](https://www.bnkrmall.co.kr/goods/detail.do?gno=5588612)

```json
{
  "review_id": "R4825",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4826 — 전광절경 롤로노아 조로 (에그 헤드 VER.) (1개)

상품 ID: 3930

- [원피스 전광절경 롤로노아 조로 (에그 헤드 VER.)](https://www.bnkrmall.co.kr/goods/detail.do?gno=92112614)

```json
{
  "review_id": "R4826",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4827 — 전광절경 마샬 D 티치 (1개)

상품 ID: 3988

- [원피스 전광절경 마샬 D 티치](https://www.bnkrmall.co.kr/goods/detail.do?gno=62360013)

```json
{
  "review_id": "R4827",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4828 — 전광절경 몽키 D 가프 (1개)

상품 ID: 3860

- [원피스 전광절경 몽키 D 가프](https://www.bnkrmall.co.kr/goods/detail.do?gno=57169237)

```json
{
  "review_id": "R4828",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4829 — 전광절경 몽키 D 루피 기어4 (1개)

상품 ID: 3663

- [원피스 전광절경 몽키 D 루피 기어4](https://www.bnkrmall.co.kr/goods/detail.do?gno=41947151)

```json
{
  "review_id": "R4829",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4830 — 전광절경 몽키 D 루피 기어5 (1개)

상품 ID: 4092

- [원피스 전광절경 몽키 D 루피 기어5](https://www.bnkrmall.co.kr/goods/detail.do?gno=96942523)

```json
{
  "review_id": "R4830",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4831 — 전광절경 볼사리노 (1개)

상품 ID: 3662

- [원피스 전광절경 볼사리노](https://www.bnkrmall.co.kr/goods/detail.do?gno=89194378)

```json
{
  "review_id": "R4831",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4832 — 전광절경 브로기 (1개)

상품 ID: 3737

- [원피스 전광절경 브로기](https://www.bnkrmall.co.kr/goods/detail.do?gno=54346695)

```json
{
  "review_id": "R4832",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4833 — 전광절경 야마토 (1개)

상품 ID: 4364

- [원피스 전광절경 야마토](https://www.bnkrmall.co.kr/goods/detail.do?gno=59943)

```json
{
  "review_id": "R4833",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4834 — 전광절경 쥬라큘 미호크 (1개)

상품 ID: 4073

- [원피스 전광절경 쥬라큘 미호크](https://www.bnkrmall.co.kr/goods/detail.do?gno=19805247)

```json
{
  "review_id": "R4834",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4835 — 전광절경 쥬얼리 보니 (1개)

상품 ID: 3411

- [원피스 전광절경 쥬얼리 보니](https://www.bnkrmall.co.kr/goods/detail.do?gno=42380045)

```json
{
  "review_id": "R4835",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4836 — 전광절경 쿠잔 (1개)

상품 ID: 3861

- [원피스 전광절경 쿠잔](https://www.bnkrmall.co.kr/goods/detail.do?gno=846884)

```json
{
  "review_id": "R4836",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4837 — 전광절경 트라팔가 로우 (1개)

상품 ID: 3989

- [원피스 전광절경 트라팔가 로우](https://www.bnkrmall.co.kr/goods/detail.do?gno=50296209)

```json
{
  "review_id": "R4837",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4838 — 전광절경 포트거스 D 에이스 (1개)

상품 ID: 4365

- [원피스 전광절경 포트거스 D 에이스](https://www.bnkrmall.co.kr/goods/detail.do?gno=59942)

```json
{
  "review_id": "R4838",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4839 — 점보 머신더 UFO로보 그렌다이저 (1개)

상품 ID: 1767

- [점보 머신더 UFO로보 그렌다이저](https://www.bnkrmall.co.kr/goods/detail.do?gno=61753818)

```json
{
  "review_id": "R4839",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4840 — 점보 머신더 슈퍼로봇 마하바론 (1개)

상품 ID: 1930

- [점보 머신더 슈퍼로봇 마하바론](https://www.bnkrmall.co.kr/goods/detail.do?gno=78903118)

```json
{
  "review_id": "R4840",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4841 — 점보 머신더 용자 라이딘 (1개)

상품 ID: 1840

- [점보 머신더 용자 라이딘](https://www.bnkrmall.co.kr/goods/detail.do?gno=51854544)

```json
{
  "review_id": "R4841",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4842 — 제08 MS소대 아이나 사하린 (1개)

상품 ID: 4158

- [기동전사 건담 제08 MS소대 아이나 사하린 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=22541413)

```json
{
  "review_id": "R4842",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4843 — 제로원 영웅용상 가면라이더 제로원 리얼라이징 호퍼 (1개)

상품 ID: 4549

- [가면라이더 제로원 영웅용상 가면라이더 제로원 리얼라이징 호퍼](https://www.bnkrmall.co.kr/goods/detail.do?gno=56766)

```json
{
  "review_id": "R4843",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4844 — 조형역전 (왕로) 손오공 (1개)

상품 ID: 4699

- [드래곤볼 Z 조형역전 (왕로) 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=15449)

```json
{
  "review_id": "R4844",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4845 — 죠죠의 기묘한 모험 STARDUST CRUSADERS Mometria 디오 (1개)

상품 ID: 3763

- [죠죠의 기묘한 모험 STARDUST CRUSADERS Mometria 디오](https://www.bnkrmall.co.kr/goods/detail.do?gno=94395680)

```json
{
  "review_id": "R4845",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4846 — 죠죠의 기묘한 모험 STARDUST CRUSADERS Mometria 쿠죠 죠타로 (1개)

상품 ID: 3764

- [죠죠의 기묘한 모험 STARDUST CRUSADERS Mometria 쿠죠 죠타로](https://www.bnkrmall.co.kr/goods/detail.do?gno=69999061)

```json
{
  "review_id": "R4846",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4847 — 죠죠의 기묘한 모험 다이아몬드는 부서지지 않는다 키라 요시카게 (1개)

상품 ID: 3453

- [죠죠의 기묘한 모험 다이아몬드는 부서지지 않는다 키라 요시카게](https://www.bnkrmall.co.kr/goods/detail.do?gno=18003121)

```json
{
  "review_id": "R4847",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4848 — 죠죠의 기묘한 모험 다이아몬드는 부서지지 않는다 피그라이프 킬러 퀸 (1개)

상품 ID: 3448

- [죠죠의 기묘한 모험 다이아몬드는 부서지지 않는다 피그라이프 킬러 퀸](https://www.bnkrmall.co.kr/goods/detail.do?gno=27762085)

```json
{
  "review_id": "R4848",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4849 — 죠죠의 기묘한 모험 다이아몬드는 부서지지 않는다 히가시카타 죠스케 (1개)

상품 ID: 3454

- [죠죠의 기묘한 모험 다이아몬드는 부서지지 않는다 히가시카타 죠스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=45354387)

```json
{
  "review_id": "R4849",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4850 — 죠죠의 기묘한 모험 스타더스트 크루세이더즈 Mometria 카쿄인 노리아키 (1개)

상품 ID: 3236

- [죠죠의 기묘한 모험 스타더스트 크루세이더즈 Mometria 카쿄인 노리아키](https://www.bnkrmall.co.kr/goods/detail.do?gno=59125644)

```json
{
  "review_id": "R4850",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4851 — 죠죠의 기묘한 모험 스타더스트 크루세이더즈 SOFVIMATES 이기 Fellowship Series 카쿄인 노리아키 (1개)

상품 ID: 3502

- [죠죠의 기묘한 모험 스타더스트 크루세이더즈 SOFVIMATES 이기 Fellowship Series 카쿄인 노리아키](https://www.bnkrmall.co.kr/goods/detail.do?gno=3067770)

```json
{
  "review_id": "R4851",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4852 — 죠죠의 기묘한 모험 스타더스트 크루세이더즈 SOFVIMATES 이기 VOL.3 (1개)

상품 ID: 4008

- [죠죠의 기묘한 모험 스타더스트 크루세이더즈 SOFVIMATES 이기 VOL.3](https://www.bnkrmall.co.kr/goods/detail.do?gno=47084104)

```json
{
  "review_id": "R4852",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4853 — 죠죠의 기묘한 모험 스타더스트 크루세이더즈 SOFVIMATES 이기 VOL.4 (1개)

상품 ID: 3702

- [죠죠의 기묘한 모험 스타더스트 크루세이더즈 SOFVIMATES 이기 VOL.4](https://www.bnkrmall.co.kr/goods/detail.do?gno=74102047)

```json
{
  "review_id": "R4853",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4854 — 죠죠의 기묘한 모험 스타더스트 크루세이더즈 클리어 이기 (ver.A) (1개)

상품 ID: 3351

- [죠죠의 기묘한 모험 스타더스트 크루세이더즈 클리어 피규어 이기 (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=32851604)

```json
{
  "review_id": "R4854",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4855 — 죠죠의 기묘한 모험 스타더스트 크루세이더즈 클리어 이기 (ver.B) (1개)

상품 ID: 3350

- [죠죠의 기묘한 모험 스타더스트 크루세이더즈 클리어 피규어 이기 (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=25028337)

```json
{
  "review_id": "R4855",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4856 — 죠죠의 기묘한 모험 스톤 오션 Mometria 엔리코 푸치 (1개)

상품 ID: 3685

- [죠죠의 기묘한 모험 스톤 오션 Mometria 엔리코 푸치](https://www.bnkrmall.co.kr/goods/detail.do?gno=44104696)

```json
{
  "review_id": "R4856",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4857 — 죠죠의 기묘한 모험 스톤 오션 Mometria 쿠죠 죠린 (1개)

상품 ID: 3686

- [죠죠의 기묘한 모험 스톤 오션 Mometria 쿠죠 죠린](https://www.bnkrmall.co.kr/goods/detail.do?gno=9576907)

```json
{
  "review_id": "R4857",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4858 — 죠죠의 기묘한 모험 스틸 볼 런 Mometria 자이로 체펠리 (1개)

상품 ID: 3419

- [죠죠의 기묘한 모험 스틸 볼 런 Mometria 자이로 체펠리](https://www.bnkrmall.co.kr/goods/detail.do?gno=20487976)

```json
{
  "review_id": "R4858",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4859 — 죠죠의 기묘한 모험 스틸 볼 런 Mometria 조니 죠스타 (1개)

상품 ID: 3420

- [죠죠의 기묘한 모험 스틸 볼 런 Mometria 조니 죠스타](https://www.bnkrmall.co.kr/goods/detail.do?gno=51816056)

```json
{
  "review_id": "R4859",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4860 — 죠죠의 기묘한 모험 전투조류 Mometria 시저 안토니오 체펠리 (1개)

상품 ID: 3296

- [죠죠의 기묘한 모험 전투조류 Mometria 시저 안토니오 체펠리](https://www.bnkrmall.co.kr/goods/detail.do?gno=88927664)

```json
{
  "review_id": "R4860",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4861 — 죠죠의 기묘한 모험 전투조류 MOMETRIA 죠셉 죠스타 (1개)

상품 ID: 3450

- [죠죠의 기묘한 모험 전투조류 MOMETRIA 죠셉 죠스타](https://www.bnkrmall.co.kr/goods/detail.do?gno=38948480)

```json
{
  "review_id": "R4861",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4862 — 죠죠의 기묘한 모험 전투조류 MOMETRIA 카즈 (1개)

상품 ID: 3899

- [죠죠의 기묘한 모험 전투조류 MOMETRIA 카즈](https://www.bnkrmall.co.kr/goods/detail.do?gno=1326591)

```json
{
  "review_id": "R4862",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4863 — 죠죠의 기묘한 모험 팬텀 블러드 Mometria 디오 브란도 (1개)

상품 ID: 3942

- [죠죠의 기묘한 모험 팬텀 블러드 Mometria 디오 브란도](https://www.bnkrmall.co.kr/goods/detail.do?gno=11478462)

```json
{
  "review_id": "R4863",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4864 — 죠죠의 기묘한 모험 팬텀 블러드 Mometria 윌 A. 체펠리 (1개)

상품 ID: 3389

- [죠죠의 기묘한 모험 팬텀 블러드 Mometria 윌 A. 체펠리](https://www.bnkrmall.co.kr/goods/detail.do?gno=25540695)

```json
{
  "review_id": "R4864",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4865 — 죠죠의 기묘한 모험 팬텀 블러드 Mometria 죠나단 죠스타 (1개)

상품 ID: 3943

- [죠죠의 기묘한 모험 팬텀 블러드 Mometria 죠나단 죠스타](https://www.bnkrmall.co.kr/goods/detail.do?gno=35086881)

```json
{
  "review_id": "R4865",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4866 — 죠죠의 기묘한 모험 팬텀 블러드 석가면 (1개)

상품 ID: 3642

- [죠죠의 기묘한 모험 팬텀 블러드 석가면](https://www.bnkrmall.co.kr/goods/detail.do?gno=76691144)

```json
{
  "review_id": "R4866",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4867 — 죠죠의 기묘한 모험 황금의 바람 Mometria 디아볼로 (1개)

상품 ID: 3715

- [죠죠의 기묘한 모험 황금의 바람 Mometria 디아볼로](https://www.bnkrmall.co.kr/goods/detail.do?gno=37603383)

```json
{
  "review_id": "R4867",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4868 — 죠죠의 기묘한 모험 황금의 바람 Mometria 죠르노 죠바나 (1개)

상품 ID: 3716

- [죠죠의 기묘한 모험 황금의 바람 Mometria 죠르노 죠바나](https://www.bnkrmall.co.kr/goods/detail.do?gno=7166053)

```json
{
  "review_id": "R4868",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4869 — 죠죠의 기묘한 모험 황금의 바람 피그라이프 메탈리카 (1개)

상품 ID: 3544

- [죠죠의 기묘한 모험 황금의 바람 피그라이프 메탈리카](https://www.bnkrmall.co.kr/goods/detail.do?gno=91352332)

```json
{
  "review_id": "R4869",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4870 — 주혼의 형 젠인 마키 & 스쿠나 (A:젠인 마키) (1개)

상품 ID: 4468

- [주술회전 주혼의 형 젠인 마키 & 스쿠나 (A:젠인 마키)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58823)

```json
{
  "review_id": "R4870",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4871 — 주혼의 형 젠인 마키 & 스쿠나 (B:스쿠나) (1개)

상품 ID: 4477

- [주술회전 주혼의 형 젠인 마키 & 스쿠나 (B:스쿠나)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58558)

```json
{
  "review_id": "R4871",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4872 — 주혼의 형 후시구로 메구미 & 나나미 켄토 (B:나나미 켄토) (1개)

상품 ID: 4373

- [주술회전 주혼의 형 후시구로 메구미 & 나나미 켄토 (B:나나미 켄토)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59821)

```json
{
  "review_id": "R4872",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4873 — 지라이야 (1개)

상품 ID: 3510

- [나루토 지라이야 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=2600284)

```json
{
  "review_id": "R4873",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4874 — 지옥선생 누베 누에노 메이스케 (1개)

상품 ID: 3470

- [지옥선생 누베 누에노 메이스케 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=37362341)

```json
{
  "review_id": "R4874",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4875 — 지옥선생 누베 타마모 쿄스케 (1개)

상품 ID: 3469

- [지옥선생 누베 타마모 쿄스케 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=49331894)

```json
{
  "review_id": "R4875",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4876 — 초사이어인3 베지터 (1개)

상품 ID: 3908

- [드래곤볼 DAIMA 초사이어인3 베지터 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=40003982)

```json
{
  "review_id": "R4876",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4877 — 초사이어인3 베지터(미니) 패널 (1개)

상품 ID: 3933

- [드래곤볼 DAIMA 초사이어인3 베지터(미니) 패널 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=50752006)

```json
{
  "review_id": "R4877",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4878 — 초전사열전 2 Vol.1 (손오공(ULTRA INSTINCT)) (1개)

상품 ID: 4707

- [드래곤볼 슈퍼 초전사열전 2 Vol.1 (손오공(ULTRA INSTINCT))](https://www.bnkrmall.co.kr/goods/detail.do?gno=15307)

```json
{
  "review_id": "R4878",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4879 — 초전사열전 2 Vol.2 (오공 블랙) (1개)

상품 ID: 4521

- [드래곤볼 슈퍼 초전사열전 2 Vol.2 (오공 블랙)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57253)

```json
{
  "review_id": "R4879",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4880 — 초전사열전 2 Vol.2 (초사이어인 트랭크스(미래)) (1개)

상품 ID: 4577

- [드래곤볼 슈퍼 초전사열전 2 Vol.2 (초사이어인 트랭크스(미래))](https://www.bnkrmall.co.kr/goods/detail.do?gno=56517)

```json
{
  "review_id": "R4880",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4881 — 초전사열전 2 Vol.5 (A: 초사이어인 베지터) (1개)

상품 ID: 4498

- [드래곤볼 슈퍼 초전사열전 2 Vol.5 (A: 초사이어인 베지터)](https://www.bnkrmall.co.kr/goods/detail.do?gno=57296)

```json
{
  "review_id": "R4881",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4882 — 초전사열전 2 Vol.5 (B: 버독) (1개)

상품 ID: 4552

- [드래곤볼 슈퍼 초전사열전 2 Vol.5 (B: 버독)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56760)

```json
{
  "review_id": "R4882",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4883 — 초전사열전 2 VOL.6 (A:손오공) (1개)

상품 ID: 4656

- [드래곤볼 슈퍼 초전사열전 2 VOL.6 (A:손오공)](https://www.bnkrmall.co.kr/goods/detail.do?gno=54213)

```json
{
  "review_id": "R4883",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4884 — 초전사열전 2 VOL.7 (A:초사이어인 갓 초사이어인 베지터(진화)) (1개)

상품 ID: 4615

- [드래곤볼 슈퍼 초전사열전 2 VOL.7 (A:초사이어인 갓 초사이어인 베지터(진화))](https://www.bnkrmall.co.kr/goods/detail.do?gno=55753)

```json
{
  "review_id": "R4884",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4885 — 초전사열전 3 Vol.1 (A:초사이어인 손오반) (1개)

상품 ID: 4418

- [드래곤볼 Z 초전사열전 3 Vol.1 (A:초사이어인 손오반)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59293)

```json
{
  "review_id": "R4885",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4886 — 초전사열전 3 Vol.1 (B:초사이어인 트랭크스) (1개)

상품 ID: 4417

- [드래곤볼 Z 초전사열전 3 Vol.1 (B:초사이어인 트랭크스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59294)

```json
{
  "review_id": "R4886",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4887 — 초전사열전 3 Vol.2 (A:베지터) (1개)

상품 ID: 4382

- [드래곤볼 Z 초전사열전 3 Vol.2 (A:베지터)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59790)

```json
{
  "review_id": "R4887",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4888 — 초전사열전 3 Vol.2 (B:트랭크스) (1개)

상품 ID: 4381

- [드래곤볼 Z 초전사열전 3 Vol.2 (B:트랭크스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=59791)

```json
{
  "review_id": "R4888",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4889 — 초전사열전 Vol.8 (초사이어인 오지터) (1개)

상품 ID: 4564

- [드래곤볼 슈퍼 초전사열전 Vol.8 (초사이어인 오지터)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56654)

```json
{
  "review_id": "R4889",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4890 — 초전사열전 Vol.8 (초사이어인 오천크스) (1개)

상품 ID: 4563

- [드래곤볼 슈퍼 초전사열전 Vol.8 (초사이어인 오천크스)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56655)

```json
{
  "review_id": "R4890",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4891 — 추아츄리 판런치 (1개)

상품 ID: 4233

- [기동전사 건담 수성의 마녀 추아츄리 판런치 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=30326191)

```json
{
  "review_id": "R4891",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4892 — 츠나데 (1개)

상품 ID: 3425

- [나루토 츠나데 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=37298542)

```json
{
  "review_id": "R4892",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4893 — 츠치카게 오오노키 오카게 집결!! (1개)

상품 ID: 3352

- [나루토 질풍전 츠치카게 오오노키 피규어 오카게 집결!!](https://www.bnkrmall.co.kr/goods/detail.do?gno=72892817)

```json
{
  "review_id": "R4893",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4894 — 치기리 효마 (1개)

상품 ID: 3496

- [블루 록 치기리 효마 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=75560334)

```json
{
  "review_id": "R4894",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4895 — 치비쿵 캐릭터 Vol.2 (캐스터/타마모노마에) (1개)

상품 ID: 4528

- [치비쿵 캐릭터 페이트/그랜드 오더 Vol.2 (캐스터/타마모노마에)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56851)

```json
{
  "review_id": "R4895",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4896 — 치비쿵 캐릭터 Vol.3 (포리너/카츠시카 호쿠사이) (1개)

상품 ID: 4530

- [치비쿵 캐릭터 페이트/그랜드 오더 Vol.3 (포리너/카츠시카 호쿠사이)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56849)

```json
{
  "review_id": "R4896",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4897 — 카가리 유라 아스하 여명의 수레바퀴 엔딩 ver. (1개)

상품 ID: 3377

- [기동전사 건담 SEED 카가리 유라 아스하 피규어 여명의 수레바퀴 엔딩 ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=55520193)

```json
{
  "review_id": "R4897",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4898 — 카드캡터 체리 BIG SOFVIMATES 케로 (1개)

상품 ID: 4090

- [카드캡터 체리 BIG SOFVIMATES 케로](https://www.bnkrmall.co.kr/goods/detail.do?gno=72368290)

```json
{
  "review_id": "R4898",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4899 — 카드캡터 체리 사쿠라 카드편 키노모토 사쿠라 (1개)

상품 ID: 3847

- [카드캡터 체리 사쿠라 카드편 피규어 키노모토 사쿠라](https://www.bnkrmall.co.kr/goods/detail.do?gno=93355975)

```json
{
  "review_id": "R4899",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4900 — 카드캡터 체리 크로우 카드 편 키노모토 사쿠라 (1개)

상품 ID: 3885

- [카드캡터 체리 크로우 카드 편 키노모토 사쿠라](https://www.bnkrmall.co.kr/goods/detail.do?gno=12688787)

```json
{
  "review_id": "R4900",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4901 — 카드캡터 체리 클리어 카드 키노모토 사쿠라 (1개)

상품 ID: 3407

- [카드캡터 체리 클리어 카드 피규어 키노모토 사쿠라](https://www.bnkrmall.co.kr/goods/detail.do?gno=56952387)

```json
{
  "review_id": "R4901",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4902 — 카제카게 가아라 오카게 집결!! (1개)

상품 ID: 3332

- [나루토 질풍전 카제카게 가아라 피규어 오카게 집결!!](https://www.bnkrmall.co.kr/goods/detail.do?gno=29859430)

```json
{
  "review_id": "R4902",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4903 — 케로로 중사 BIG SOFVIMATES 기로로 하사 (1개)

상품 ID: 3832

- [케로로 중사 BIG SOFVIMATES 기로로 하사](https://www.bnkrmall.co.kr/goods/detail.do?gno=99097890)

```json
{
  "review_id": "R4903",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4904 — 케로로 중사 BIG SOFVIMATES 도로로 병장 (1개)

상품 ID: 3802

- [케로로 중사 BIG SOFVIMATES 도로로 병장](https://www.bnkrmall.co.kr/goods/detail.do?gno=54105262)

```json
{
  "review_id": "R4904",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4905 — 케로로 중사 BIG SOFVIMATES 쿠루루 상사 (1개)

상품 ID: 3734

- [케로로 중사 BIG SOFVIMATES 쿠루루 상사](https://www.bnkrmall.co.kr/goods/detail.do?gno=93177273)

```json
{
  "review_id": "R4905",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4906 — 케로로 중사 공명하는 것입니다 기로로 하사 (1개)

상품 ID: 3230

- [케로로 중사 공명하는 것입니다 피규어 기로로 하사](https://www.bnkrmall.co.kr/goods/detail.do?gno=31342866)

```json
{
  "review_id": "R4906",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4907 — 케로로 중사 공명하는 것입니다 도로로 병장 (1개)

상품 ID: 3227

- [케로로 중사 공명하는 것입니다 피규어 도로로 병장](https://www.bnkrmall.co.kr/goods/detail.do?gno=70492333)

```json
{
  "review_id": "R4907",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4908 — 케로로 중사 공명하는 것입니다 케로로 중사 (1개)

상품 ID: 3231

- [케로로 중사 공명하는 것입니다 피규어 케로로 중사](https://www.bnkrmall.co.kr/goods/detail.do?gno=86711561)

```json
{
  "review_id": "R4908",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4909 — 케로로 중사 공명하는 것입니다 쿠루루 상사 (1개)

상품 ID: 3228

- [케로로 중사 공명하는 것입니다 피규어 쿠루루 상사](https://www.bnkrmall.co.kr/goods/detail.do?gno=37047996)

```json
{
  "review_id": "R4909",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4910 — 케로로 중사 공명하는 것입니다 타마마 이등병 (1개)

상품 ID: 3229

- [케로로 중사 공명하는 것입니다 피규어 타마마 이등병](https://www.bnkrmall.co.kr/goods/detail.do?gno=72778204)

```json
{
  "review_id": "R4910",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4911 — 케로로 중사 케로로 소대 vol.1 (1개)

상품 ID: 3787

- [케로로 중사 케로로 소대 피규어 vol.1](https://www.bnkrmall.co.kr/goods/detail.do?gno=80193907)

```json
{
  "review_id": "R4911",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4912 — 케로로 중사 케로로 소대 vol.2 (A: 타마마 이등병) (1개)

상품 ID: 3786

- [케로로 중사 케로로 소대 피규어 vol.2 (A: 타마마 이등병)](https://www.bnkrmall.co.kr/goods/detail.do?gno=37170441)

```json
{
  "review_id": "R4912",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4913 — 케로로 중사 케로로 소대 vol.2 (B: 기로로 하사) (1개)

상품 ID: 3785

- [케로로 중사 케로로 소대 피규어 vol.2 (B: 기로로 하사)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15319321)

```json
{
  "review_id": "R4913",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4914 — 케로로 중사 케로로 소대 vol.3 (A: 쿠루루 상사) (1개)

상품 ID: 3784

- [케로로 중사 케로로 소대 피규어 vol.3 (A: 쿠루루 상사)](https://www.bnkrmall.co.kr/goods/detail.do?gno=5895618)

```json
{
  "review_id": "R4914",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4915 — 케로로 중사 케로로 소대 vol.3 (B: 도로로 병장) (1개)

상품 ID: 3783

- [케로로 중사 케로로 소대 피규어 vol.3 (B: 도로로 병장)](https://www.bnkrmall.co.kr/goods/detail.do?gno=79610773)

```json
{
  "review_id": "R4915",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4916 — 콤비네이션 배틀2 가아라 (1개)

상품 ID: 3840

- [나루토 콤비네이션 배틀2 가아라](https://www.bnkrmall.co.kr/goods/detail.do?gno=11582296)

```json
{
  "review_id": "R4916",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4917 — 콤비네이션 배틀2 스쿠나 (1개)

상품 ID: 4370

- [주술회전 콤비네이션 배틀2 스쿠나](https://www.bnkrmall.co.kr/goods/detail.do?gno=59824)

```json
{
  "review_id": "R4917",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4918 — 콤비네이션 배틀2 우즈마키 나루토 (1개)

상품 ID: 3645

- [나루토 질풍전 콤비네이션 배틀2 우즈마키 나루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=78211810)

```json
{
  "review_id": "R4918",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4919 — 콤비네이션 배틀2 후시구로 메구미 (1개)

상품 ID: 4371

- [주술회전 콤비네이션 배틀2 후시구로 메구미](https://www.bnkrmall.co.kr/goods/detail.do?gno=59823)

```json
{
  "review_id": "R4919",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4920 — 콤비네이션 배틀 ALL FOR ONE (1개)

상품 ID: 4244

- [나의 히어로 아카데미아 콤비네이션 배틀 ALL FOR ONE](https://www.bnkrmall.co.kr/goods/detail.do?gno=82230433)

```json
{
  "review_id": "R4920",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4921 — 콤비네이션 배틀 루이 (1개)

상품 ID: 4116

- [귀멸의 칼날 콤비네이션 배틀 루이](https://www.bnkrmall.co.kr/goods/detail.do?gno=71909355)

```json
{
  "review_id": "R4921",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4922 — 콤비네이션 배틀 미도리야 이즈쿠 (1개)

상품 ID: 4218

- [나의 히어로 아카데미아 콤비네이션 배틀 미도리야 이즈쿠](https://www.bnkrmall.co.kr/goods/detail.do?gno=82396345)

```json
{
  "review_id": "R4922",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4923 — 콤비네이션 배틀 미도리야 이즈쿠 FINALE (1개)

상품 ID: 4061

- [나의 히어로 아카데미아 콤비네이션 배틀 미도리야 이즈쿠 FINALE](https://www.bnkrmall.co.kr/goods/detail.do?gno=54985051)

```json
{
  "review_id": "R4923",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4924 — 콤비네이션 배틀 바쿠고 카츠키 (1개)

상품 ID: 4217

- [나의 히어로 아카데미아 콤비네이션 배틀 바쿠고 카츠키](https://www.bnkrmall.co.kr/goods/detail.do?gno=94369650)

```json
{
  "review_id": "R4924",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4925 — 콤비네이션 배틀 사무라이 소드 (1개)

상품 ID: 4246

- [체인소 맨 콤비네이션 배틀 사무라이 소드](https://www.bnkrmall.co.kr/goods/detail.do?gno=23536620)

```json
{
  "review_id": "R4925",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4926 — 콤비네이션 배틀 시가라키 토무라 FINALE (1개)

상품 ID: 4060

- [나의 히어로 아카데미아 콤비네이션 배틀 시가라키 토무라 FINALE](https://www.bnkrmall.co.kr/goods/detail.do?gno=91394868)

```json
{
  "review_id": "R4926",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4927 — 콤비네이션 배틀 올마이트 (1개)

상품 ID: 4245

- [나의 히어로 아카데미아 콤비네이션 배틀 올마이트](https://www.bnkrmall.co.kr/goods/detail.do?gno=36819253)

```json
{
  "review_id": "R4927",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4928 — 콤비네이션 배틀 우즈마키 나루토 (1개)

상품 ID: 4086

- [나루토 콤비네이션 배틀 우즈마키 나루토](https://www.bnkrmall.co.kr/goods/detail.do?gno=69651473)

```json
{
  "review_id": "R4928",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4929 — 콤비네이션 배틀 우치하 이타치 (1개)

상품 ID: 3725

- [나루토 질풍전 콤비네이션 배틀 우치하 이타치](https://www.bnkrmall.co.kr/goods/detail.do?gno=44335528)

```json
{
  "review_id": "R4929",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4930 — 콤비네이션 배틀 이타도리 유지 (1개)

상품 ID: 4443

- [주술회전 콤비네이션 배틀 이타도리 유지](https://www.bnkrmall.co.kr/goods/detail.do?gno=59221)

```json
{
  "review_id": "R4930",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4931 — 콤비네이션 배틀 체인소 맨 (1개)

상품 ID: 4170

- [체인소 맨 콤비네이션 배틀 체인소 맨](https://www.bnkrmall.co.kr/goods/detail.do?gno=97767784)

```json
{
  "review_id": "R4931",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4932 — 콤비네이션 배틀 카마도 탄지로 (1개)

상품 ID: 4117

- [귀멸의 칼날 콤비네이션 배틀 카마도 탄지로](https://www.bnkrmall.co.kr/goods/detail.do?gno=3695510)

```json
{
  "review_id": "R4932",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4933 — 콤비네이션 배틀 토도 아오이 (1개)

상품 ID: 4420

- [주술회전 콤비네이션 배틀 토도 아오이](https://www.bnkrmall.co.kr/goods/detail.do?gno=59291)

```json
{
  "review_id": "R4933",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4934 — 콤비네이션 배틀 하나미 (1개)

상품 ID: 4389

- [주술회전 콤비네이션 배틀 하나미](https://www.bnkrmall.co.kr/goods/detail.do?gno=59559)

```json
{
  "review_id": "R4934",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4935 — 쿄야마 안나 (1개)

상품 ID: 4570

- [샤먼킹 쿄야마 안나](https://www.bnkrmall.co.kr/goods/detail.do?gno=56586)

```json
{
  "review_id": "R4935",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4936 — 쿠기사키 노바라 (1개)

상품 ID: 4539

- [주술회전 쿠기사키 노바라](https://www.bnkrmall.co.kr/goods/detail.do?gno=56791)

```json
{
  "review_id": "R4936",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4937 — 쿠라마 Ⅱ(VER.A) (1개)

상품 ID: 3974

- [나루토 질풍전 쿠라마 피규어Ⅱ(VER.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=47329087)

```json
{
  "review_id": "R4937",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4938 — 쿠라마 Ⅱ(VER.B) (1개)

상품 ID: 3973

- [나루토 질풍전 쿠라마 피규어Ⅱ(VER.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=32873523)

```json
{
  "review_id": "R4938",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4939 — 쿠로카와 아카네 브라이덜 드레스 (1개)

상품 ID: 4041

- [【최애의 아이】 쿠로카와 아카네 브라이덜 드레스 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=7566045)

```json
{
  "review_id": "R4939",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4940 — 쿠로카와 아카네 사야히메 VER. (1개)

상품 ID: 4036

- [【최애의 아이】 쿠로카와 아카네 사야히메 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=98493681)

```json
{
  "review_id": "R4940",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4941 — 퀘스 파라야 (1개)

상품 ID: 4302

- [기동전사 건담 역습의 샤아 퀘스 파라야 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=9260118)

```json
{
  "review_id": "R4941",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4942 — 킹덤 오기코 (1개)

상품 ID: 3457

- [킹덤 오기코 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=42330989)

```json
{
  "review_id": "R4942",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4943 — 타마시이 박스 Vol.1 SET (1개)

상품 ID: 1899

- [타마시이 박스 원피스 Vol.1 SET](https://www.bnkrmall.co.kr/goods/detail.do?gno=47314339)

```json
{
  "review_id": "R4943",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4944 — 타마시이 박스 Vol.2 SET (1개)

상품 ID: 1898

- [타마시이 박스 원피스 Vol.2 SET](https://www.bnkrmall.co.kr/goods/detail.do?gno=41591471)

```json
{
  "review_id": "R4944",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4945 — 타카바 후미히코 (1개)

상품 ID: 3588

- [주술회전 타카바 후미히코 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=94421684)

```json
{
  "review_id": "R4945",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4946 — 태고의 달인 SOFVIMATES～GOLD･SILVER～(A:태고의 달인(금)) (1개)

상품 ID: 3736

- [태고의 달인 SOFVIMATES～GOLD･SILVER～(A:태고의 달인(금))](https://www.bnkrmall.co.kr/goods/detail.do?gno=15126809)

```json
{
  "review_id": "R4946",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4947 — 태고의 달인 SOFVIMATES～GOLD･SILVER～(B:태고의 달인(은)) (1개)

상품 ID: 3735

- [태고의 달인 SOFVIMATES～GOLD･SILVER～(B:태고의 달인(은))](https://www.bnkrmall.co.kr/goods/detail.do?gno=76631432)

```json
{
  "review_id": "R4947",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4948 — 태그 파이터즈 초사이어인4 베지터 (1개)

상품 ID: 4487

- [드래곤볼 GT 태그 파이터즈 초사이어인4 베지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=57427)

```json
{
  "review_id": "R4948",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4949 — 태그 파이터즈 초사이어인4 손오공 (1개)

상품 ID: 4488

- [드래곤볼 GT 태그 파이터즈 초사이어인4 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=57426)

```json
{
  "review_id": "R4949",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4950 — 테쿠피쿠 게토 스구루 -주술고전 (1개)

상품 ID: 1923

- [테쿠피쿠 게토 스구루 -주술고전-](https://www.bnkrmall.co.kr/goods/detail.do?gno=65230191)

```json
{
  "review_id": "R4950",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4951 — 테쿠피쿠 고죠 사토루 -주술고전 (1개)

상품 ID: 1924

- [테쿠피쿠 고죠 사토루 -주술고전-](https://www.bnkrmall.co.kr/goods/detail.do?gno=82224825)

```json
{
  "review_id": "R4951",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4952 — 테쿠피쿠 세바스찬 미카엘리스 (1개)

상품 ID: 1991

- [테쿠피쿠 세바스찬 미카엘리스](https://www.bnkrmall.co.kr/goods/detail.do?gno=43408210)

```json
{
  "review_id": "R4952",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4953 — 테쿠피쿠 이타도리 유지 (1개)

상품 ID: 1910

- [테쿠피쿠 이타도리 유지](https://www.bnkrmall.co.kr/goods/detail.do?gno=46668064)

```json
{
  "review_id": "R4953",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4954 — 테쿠피쿠 쵸파 (ONE PIECE CHOPPER's) (1개)

상품 ID: 1711

- [테쿠피쿠 쵸파 (ONE PIECE CHOPPER's)](https://www.bnkrmall.co.kr/goods/detail.do?gno=11733279)

```json
{
  "review_id": "R4954",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4955 — 테쿠피쿠 츠키시마 케이 (1개)

상품 ID: 1873

- [테쿠피쿠 츠키시마 케이](https://www.bnkrmall.co.kr/goods/detail.do?gno=32293043)

```json
{
  "review_id": "R4955",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4956 — 테쿠피쿠 카마도 네즈코 (1개)

상품 ID: 1606

- [테쿠피쿠 카마도 네즈코](https://www.bnkrmall.co.kr/goods/detail.do?gno=7170922)

```json
{
  "review_id": "R4956",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4957 — 테쿠피쿠 카마도 탄지로 (1개)

상품 ID: 1607

- [테쿠피쿠 카마도 탄지로](https://www.bnkrmall.co.kr/goods/detail.do?gno=83255684)

```json
{
  "review_id": "R4957",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4958 — 테쿠피쿠 코즈메 켄마 (1개)

상품 ID: 1874

- [테쿠피쿠 코즈메 켄마](https://www.bnkrmall.co.kr/goods/detail.do?gno=14206725)

```json
{
  "review_id": "R4958",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4959 — 테쿠피쿠 쿠로오 테츠로 (1개)

상품 ID: 1875

- [테쿠피쿠 쿠로오 테츠로](https://www.bnkrmall.co.kr/goods/detail.do?gno=67109506)

```json
{
  "review_id": "R4959",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4960 — 테쿠피쿠 후시구로 메구미 (1개)

상품 ID: 1909

- [테쿠피쿠 후시구로 메구미](https://www.bnkrmall.co.kr/goods/detail.do?gno=79064565)

```json
{
  "review_id": "R4960",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4961 — 테쿠피쿠 히지카타 토시로 (1개)

상품 ID: 1849

- [테쿠피쿠 히지카타 토시로](https://www.bnkrmall.co.kr/goods/detail.do?gno=6233539)

```json
{
  "review_id": "R4961",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4962 — 토도로키 쇼토 (1개)

상품 ID: 3481

- [나의 히어로 아카데미아 피규어 토도로키 쇼토](https://www.bnkrmall.co.kr/goods/detail.do?gno=6714329)

```json
{
  "review_id": "R4962",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4963 — 토로와 친구들 SOFVIMATES 토로 (1개)

상품 ID: 3920

- [토로와 친구들 SOFVIMATES 토로](https://www.bnkrmall.co.kr/goods/detail.do?gno=83033206)

```json
{
  "review_id": "R4963",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4964 — 토키사키 쿠루미 Happy Birthday Present (1개)

상품 ID: 3818

- [데이트 어 라이브 토키사키 쿠루미 Happy Birthday Present 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=62107018)

```json
{
  "review_id": "R4964",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4965 — 토키사키 쿠루미 SWEET SILK WEAR VER. (1개)

상품 ID: 3451

- [데이트 어 라이브 토키사키 쿠루미 SWEET SILK WEAR VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=26310519)

```json
{
  "review_id": "R4965",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4966 — 토호 괴수 시리즈 괴수 포효 공격 고질라 (2001) (1개)

상품 ID: 3707

- [토호 괴수 시리즈 괴수 포효 공격 고질라 (2001)](https://www.bnkrmall.co.kr/goods/detail.do?gno=3270475)

```json
{
  "review_id": "R4966",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4967 — 토호 괴수 시리즈 아트 비네트 모스라 (1996) (1개)

상품 ID: 3289

- [토호 괴수 시리즈 아트 비네트 모스라 (1996)](https://www.bnkrmall.co.kr/goods/detail.do?gno=78768710)

```json
{
  "review_id": "R4967",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4968 — 톰과 제리 CRANE POP (A.톰) (1개)

상품 ID: 3440

- [톰과 제리 CRANE POP 피규어 (A.톰)](https://www.bnkrmall.co.kr/goods/detail.do?gno=68378751)

```json
{
  "review_id": "R4968",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4969 — 톰과 제리 CRANE POP (B.제리) (1개)

상품 ID: 3439

- [톰과 제리 CRANE POP 피규어 (B.제리)](https://www.bnkrmall.co.kr/goods/detail.do?gno=34858253)

```json
{
  "review_id": "R4969",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4970 — 톰과 제리 빅 소프비 Yummy Bread (1개)

상품 ID: 3774

- [톰과 제리 빅 소프비 피규어 Yummy Bread](https://www.bnkrmall.co.kr/goods/detail.do?gno=56434806)

```json
{
  "review_id": "R4970",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4971 — 톰과 제리 빅 소프비 카눌레 vol.1 (1개)

상품 ID: 3587

- [톰과 제리 빅 소프비 피규어 카눌레 vol.1](https://www.bnkrmall.co.kr/goods/detail.do?gno=81900438)

```json
{
  "review_id": "R4971",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4972 — 톰과 제리 빅 소프비 카눌레 vol.2 (1개)

상품 ID: 3310

- [톰과 제리 빅 소프비 피규어 카눌레 vol.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=27478459)

```json
{
  "review_id": "R4972",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4973 — 톰과 제리 소프비 Sweet Cupcake (1개)

상품 ID: 3815

- [톰과 제리 소프비 피규어 Sweet Cupcake](https://www.bnkrmall.co.kr/goods/detail.do?gno=80419217)

```json
{
  "review_id": "R4973",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4974 — 톰과 제리 소프비 VOL.3 (1개)

상품 ID: 4123

- [톰과 제리 소프비 피규어 VOL.3](https://www.bnkrmall.co.kr/goods/detail.do?gno=39611594)

```json
{
  "review_id": "R4974",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4975 — 톰과 제리 소프비 VOL.4 (1개)

상품 ID: 4021

- [톰과 제리 소프비 피규어 VOL.4](https://www.bnkrmall.co.kr/goods/detail.do?gno=34704040)

```json
{
  "review_id": "R4975",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4976 — 톰과 제리 콜렉션 ENJOY FLOAT (1개)

상품 ID: 4154

- [톰과 제리 피규어 콜렉션 ENJOY FLOAT](https://www.bnkrmall.co.kr/goods/detail.do?gno=70920866)

```json
{
  "review_id": "R4976",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4977 — 톰과 제리 피그라이프 제리&터피 (1개)

상품 ID: 3733

- [톰과 제리 피그라이프 제리&터피](https://www.bnkrmall.co.kr/goods/detail.do?gno=1639966)

```json
{
  "review_id": "R4977",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4978 — 톰과 제리 피그라이프 제리&터피 vol.2 (1개)

상품 ID: 3636

- [톰과 제리 피그라이프 제리&터피 vol.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=65395462)

```json
{
  "review_id": "R4978",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4979 — 투 러브 트러블 다크니스 냐루즈 콜렉션 금빛 어둠 (1개)

상품 ID: 3517

- [투 러브 트러블 다크니스 냐루즈 콜렉션 금빛 어둠](https://www.bnkrmall.co.kr/goods/detail.do?gno=53702673)

```json
{
  "review_id": "R4979",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4980 — 투 러브 트러블 다크니스 냐루즈 콜렉션 나나 아스타 데빌룩 (1개)

상품 ID: 3516

- [투 러브 트러블 다크니스 냐루즈 콜렉션 나나 아스타 데빌룩](https://www.bnkrmall.co.kr/goods/detail.do?gno=77217222)

```json
{
  "review_id": "R4980",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4981 — 투 러브 트러블 다크니스 냐루즈 콜렉션 라라 사타린 데빌룩 (1개)

상품 ID: 3355

- [투 러브 트러블 다크니스 냐루즈 콜렉션 라라 사타린 데빌룩](https://www.bnkrmall.co.kr/goods/detail.do?gno=17853782)

```json
{
  "review_id": "R4981",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4982 — 투 러브 트러블 다크니스 냐루즈 콜렉션 룬 엘시 쥬얼리아 (1개)

상품 ID: 3579

- [투 러브 트러블 다크니스 냐루즈 콜렉션 룬 엘시 쥬얼리아](https://www.bnkrmall.co.kr/goods/detail.do?gno=43341263)

```json
{
  "review_id": "R4982",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4983 — 투 러브 트러블 다크니스 냐루즈 콜렉션 모모 베리아 데빌룩 (1개)

상품 ID: 3280

- [투 러브 트러블 다크니스 냐루즈 콜렉션 모모 베리아 데빌룩](https://www.bnkrmall.co.kr/goods/detail.do?gno=37831282)

```json
{
  "review_id": "R4983",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4984 — 투 러브 트러블 다크니스 냐루즈 콜렉션 사이렌지 하루나 (1개)

상품 ID: 3342

- [투 러브 트러블 다크니스 냐루즈 콜렉션 사이렌지 하루나](https://www.bnkrmall.co.kr/goods/detail.do?gno=55099528)

```json
{
  "review_id": "R4984",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4985 — 투 러브 트러블 다크니스 냐루즈 콜렉션 유우키 미캉 (1개)

상품 ID: 3341

- [투 러브 트러블 다크니스 냐루즈 콜렉션 유우키 미캉](https://www.bnkrmall.co.kr/goods/detail.do?gno=38064492)

```json
{
  "review_id": "R4985",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4986 — 투 러브 트러블 다크니스 냐루즈 콜렉션 코테가와 유이 (1개)

상품 ID: 3580

- [투 러브 트러블 다크니스 냐루즈 콜렉션 코테가와 유이](https://www.bnkrmall.co.kr/goods/detail.do?gno=36960284)

```json
{
  "review_id": "R4986",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4987 — 투 러브 트러블 다크니스 냐루즈 콜렉션 쿠로사키 메아 (1개)

상품 ID: 3281

- [투 러브 트러블 다크니스 냐루즈 콜렉션 쿠로사키 메아](https://www.bnkrmall.co.kr/goods/detail.do?gno=16428944)

```json
{
  "review_id": "R4987",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4988 — 트레저 크루즈 월드 저니 Vol.4 네펠타리 비비 (1개)

상품 ID: 4688

- [원피스 트레저 크루즈 월드 저니 Vol.4 네펠타리 비비](https://www.bnkrmall.co.kr/goods/detail.do?gno=15600)

```json
{
  "review_id": "R4988",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4989 — 트레저 크루즈 월드 저니 Vol.4 레베카 (1개)

상품 ID: 4687

- [원피스 트레저 크루즈 월드 저니 Vol.4 레베카](https://www.bnkrmall.co.kr/goods/detail.do?gno=15601)

```json
{
  "review_id": "R4989",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4990 — 트레저 크루즈 월드 저니 Vol.5 마르코 (1개)

상품 ID: 4676

- [원피스 트레저 크루즈 월드 저니 Vol.5 마르코](https://www.bnkrmall.co.kr/goods/detail.do?gno=15777)

```json
{
  "review_id": "R4990",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4991 — 트레저 크루즈 월드 저니 Vol.5 포트거스 D 에이스 (1개)

상품 ID: 4678

- [원피스 트레저 크루즈 월드 저니 Vol.5 포트거스 D 에이스](https://www.bnkrmall.co.kr/goods/detail.do?gno=15776)

```json
{
  "review_id": "R4991",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4992 — 트레저 크루즈 월드 저니 VOL.6 코알라 (1개)

상품 ID: 4660

- [원피스 트레저 크루즈 월드 저니 VOL.6 코알라](https://www.bnkrmall.co.kr/goods/detail.do?gno=15901)

```json
{
  "review_id": "R4992",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4993 — 트리거 영웅용상 울트라맨 트리거 멀티 타입 VER.A (1개)

상품 ID: 4616

- [울트라맨 트리거 영웅용상 울트라맨 트리거 멀티 타입 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=55750)

```json
{
  "review_id": "R4993",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4994 — 트리거 영웅용상 트리거 다크 VER.A (1개)

상품 ID: 4596

- [울트라맨 트리거 영웅용상 트리거 다크 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=56280)

```json
{
  "review_id": "R4994",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4995 — 티가 영웅용상 울트라맨 티가 (A:울트라맨 티가) (1개)

상품 ID: 4582

- [울트라맨 티가 영웅용상 울트라맨 티가 (A:울트라맨 티가)](https://www.bnkrmall.co.kr/goods/detail.do?gno=56316)

```json
{
  "review_id": "R4995",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4996 — 티가 영웅용상 울트라맨 티가 DAY & NIGHT SPECIAL VER.A (1개)

상품 ID: 4540

- [울트라맨 티가 영웅용상 울트라맨 티가 DAY & NIGHT SPECIAL VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=56790)

```json
{
  "review_id": "R4996",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4997 — 티슈 (1개)

상품 ID: 3591

- [장송의 프리렌 티슈 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=4612016)

```json
{
  "review_id": "R4997",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4998 — 파워 (1개)

상품 ID: 3925

- [체인소 맨 파워 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=8459794)

```json
{
  "review_id": "R4998",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R4999 — 파워 2 (1개)

상품 ID: 4003

- [체인소 맨 파워 피규어2](https://www.bnkrmall.co.kr/goods/detail.do?gno=79320737)

```json
{
  "review_id": "R4999",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5000 — 팬지 패널 (1개)

상품 ID: 3932

- [드래곤볼 DAIMA 팬지 패널 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=17701695)

```json
{
  "review_id": "R5000",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5001 — 펜 프렌드 노노아 교복 VER. (1개)

상품 ID: 4106

- [2.5차원의 유혹 펜 프렌드 노노아 교복 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=44070125)

```json
{
  "review_id": "R5001",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5002 — 펜 프렌드 라스타롯테 환상의 의상 VER. (1개)

상품 ID: 3945

- [2.5차원의 유혹 펜 프렌드 라스타롯테 환상의 의상 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=14363587)

```json
{
  "review_id": "R5002",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5003 — 펜 프렌드 릴리엘 의무대 VER. (1개)

상품 ID: 3921

- [2.5차원의 유혹 펜 프렌드 릴리엘 의무대 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=19590167)

```json
{
  "review_id": "R5003",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5004 — 펜 프렌드 밀리엘라 의무대 VER. (1개)

상품 ID: 4035

- [2.5차원의 유혹 펜 프렌드 밀리엘라 의무대 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=34140917)

```json
{
  "review_id": "R5004",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5005 — 펜 프렌드 아마노 리리사 교복 VER. (1개)

상품 ID: 4038

- [2.5차원의 유혹 펜 프렌드 아마노 리리사 교복 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=34313500)

```json
{
  "review_id": "R5005",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5006 — 펜 프렌드 야토가미 토카 SWEET SILK WEAR VER. (1개)

상품 ID: 3902

- [데이트 어 라이브 펜 프렌드 야토가미 토카 SWEET SILK WEAR VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=36337263)

```json
{
  "review_id": "R5006",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5007 — 펜 프렌드 이콜라 퍼지 VER. (1개)

상품 ID: 4091

- [2.5차원의 유혹 펜 프렌드 이콜라 퍼지 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=14978704)

```json
{
  "review_id": "R5007",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5008 — 펜 프렌드 키사키 아리아 교복 VER. (1개)

상품 ID: 4105

- [2.5차원의 유혹 펜 프렌드 키사키 아리아 교복 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=56407770)

```json
{
  "review_id": "R5008",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5009 — 펜 프렌드 타치바나 미카리 교복 VER. (1개)

상품 ID: 3990

- [2.5차원의 유혹 펜 프렌드 타치바나 미카리 교복 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=93225407)

```json
{
  "review_id": "R5009",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5010 — 포징 미야 아츠무 (1개)

상품 ID: 3893

- [하이큐!! 포징 피규어 미야 아츠무](https://www.bnkrmall.co.kr/goods/detail.do?gno=27813243)

```json
{
  "review_id": "R5010",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5011 — 포징 미야 오사무 (1개)

상품 ID: 3892

- [하이큐!! 포징 피규어 미야 오사무](https://www.bnkrmall.co.kr/goods/detail.do?gno=45134048)

```json
{
  "review_id": "R5011",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5012 — 포징 보쿠토 코타로 (1개)

상품 ID: 4220

- [하이큐!! 포징 피규어 보쿠토 코타로](https://www.bnkrmall.co.kr/goods/detail.do?gno=19570671)

```json
{
  "review_id": "R5012",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5013 — 포징 아카아시 케이지 (1개)

상품 ID: 4219

- [하이큐!! 포징 피규어 아카아시 케이지](https://www.bnkrmall.co.kr/goods/detail.do?gno=26830272)

```json
{
  "review_id": "R5013",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5014 — 포징 오이카와 토오루&이와이즈미 하지메 (A:오이카와 토오루) (1개)

상품 ID: 3542

- [하이큐!! 포징 피규어 오이카와 토오루&이와이즈미 하지메 (A:오이카와 토오루)](https://www.bnkrmall.co.kr/goods/detail.do?gno=95746949)

```json
{
  "review_id": "R5014",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5015 — 포징 오이카와 토오루&이와이즈미 하지메 (B:이와이즈미 하지메) (1개)

상품 ID: 3541

- [하이큐!! 포징 피규어 오이카와 토오루&이와이즈미 하지메 (B:이와이즈미 하지메)](https://www.bnkrmall.co.kr/goods/detail.do?gno=19829003)

```json
{
  "review_id": "R5015",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5016 — 포징 코즈메 켄마・쿠로오 테츠로 세컨드 유니폼VER. (A:코즈메 켄마) (1개)

상품 ID: 3604

- [하이큐!! 포징 피규어 코즈메 켄마・쿠로오 테츠로 세컨드 유니폼VER. (A:코즈메 켄마)](https://www.bnkrmall.co.kr/goods/detail.do?gno=43384070)

```json
{
  "review_id": "R5016",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5017 — 포징 코즈메 켄마・쿠로오 테츠로 세컨드 유니폼VER. (B:쿠로오 테츠로) (1개)

상품 ID: 3603

- [하이큐!! 포징 피규어 코즈메 켄마・쿠로오 테츠로 세컨드 유니폼VER. (B:쿠로오 테츠로)](https://www.bnkrmall.co.kr/goods/detail.do?gno=84404727)

```json
{
  "review_id": "R5017",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5018 — 포징 키타 신스케 (1개)

상품 ID: 4188

- [하이큐!! 포징 피규어 키타 신스케](https://www.bnkrmall.co.kr/goods/detail.do?gno=32326889)

```json
{
  "review_id": "R5018",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5019 — 포피니카 제트 파일더 (1개)

상품 ID: 1650

- [포피니카 제트 파일더](https://www.bnkrmall.co.kr/goods/detail.do?gno=87998246)

```json
{
  "review_id": "R5019",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5020 — 포피니카 호버 파일더 (1개)

상품 ID: 1959

- [포피니카 호버 파일더](https://www.bnkrmall.co.kr/goods/detail.do?gno=80860363)

```json
{
  "review_id": "R5020",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5021 — 폭렬격전 10주년 기념 초사이어인 베지트 (1개)

상품 ID: 3792

- [드래곤볼 Z 폭렬격전 10주년 기념 피규어 초사이어인 베지트](https://www.bnkrmall.co.kr/goods/detail.do?gno=56228442)

```json
{
  "review_id": "R5021",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5022 — 폭렬격전 10주년 기념 초사이어인 오지터 (1개)

상품 ID: 3793

- [드래곤볼 Z 폭렬격전 10주년 기념 피규어 초사이어인 오지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=30821395)

```json
{
  "review_id": "R5022",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5023 — 폭렬격전 6주년 (1개)

상품 ID: 4685

- [드래곤볼 Z 폭렬격전 6주년 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=15656)

```json
{
  "review_id": "R5023",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5024 — 푸른 상자 쵸노 히나 VOL.2 (가칭) (1개)

상품 ID: 4015

- [푸른 상자 쵸노 히나 VOL.2 (가칭)](https://www.bnkrmall.co.kr/goods/detail.do?gno=84890508)

```json
{
  "review_id": "R5024",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5025 — 푸른 상자 쵸노 히나 교복 VER. (1개)

상품 ID: 4103

- [푸른 상자 쵸노 히나 교복 VER.](https://www.bnkrmall.co.kr/goods/detail.do?gno=39221558)

```json
{
  "review_id": "R5025",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5026 — 푸른 상자 카노 치나츠 VOL.2 (가칭) (1개)

상품 ID: 4016

- [푸른 상자 카노 치나츠 VOL.2 (가칭)](https://www.bnkrmall.co.kr/goods/detail.do?gno=86430308)

```json
{
  "review_id": "R5026",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5027 — 풀 스크래치 초사이어인4 손오공 (1개)

상품 ID: 4709

- [드래곤볼 GT 풀 스크래치 초사이어인4 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=15232)

```json
{
  "review_id": "R5027",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5028 — 프리렌 (1개)

상품 ID: 3790

- [장송의 프리렌 피규어 프리렌](https://www.bnkrmall.co.kr/goods/detail.do?gno=67029709)

```json
{
  "review_id": "R5028",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5029 — 프리미엄 골 D 로저 [THE BRUSH] (1개)

상품 ID: 3713

- [원피스 프리미엄 골 D 로저 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=30949881)

```json
{
  "review_id": "R5029",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5030 — 프리미엄 골 D 로저 [THE METALLIC] (1개)

상품 ID: 3888

- [원피스 프리미엄 골 D 로저 (THE METALLIC)](https://www.bnkrmall.co.kr/goods/detail.do?gno=26909241)

```json
{
  "review_id": "R5030",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5031 — 프리미엄 롤로노아 조로 [THE ANIME] (1개)

상품 ID: 3796

- [원피스 프리미엄 롤로노아 조로 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=72139249)

```json
{
  "review_id": "R5031",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5032 — 프리미엄 롤로노아 조로 [THE BRUSH] (1개)

상품 ID: 3688

- [원피스 프리미엄 롤로노아 조로 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=75022806)

```json
{
  "review_id": "R5032",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5033 — 프리미엄 사보 [THE BRUSH] (1개)

상품 ID: 3714

- [원피스 프리미엄 사보 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=81345351)

```json
{
  "review_id": "R5033",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5034 — 프리미엄 사보 [THE METALLIC] (1개)

상품 ID: 3770

- [원피스 프리미엄 사보 (THE METALLIC)](https://www.bnkrmall.co.kr/goods/detail.do?gno=79009827)

```json
{
  "review_id": "R5034",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5035 — 프리미엄 샹크스 [THE ANIME] (1개)

상품 ID: 4124

- [원피스 프리미엄 샹크스 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=93087103)

```json
{
  "review_id": "R5035",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5036 — 프리미엄 쥬라큘 미호크 [THE ANIME] (1개)

상품 ID: 3225

- [원피스 프리미엄 쥬라큘 미호크 (THE ANIME)](https://www.bnkrmall.co.kr/goods/detail.do?gno=90290306)

```json
{
  "review_id": "R5036",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5037 — 프리미엄 쥬라큘 미호크 [THE BRUSH] (1개)

상품 ID: 3226

- [원피스 프리미엄 쥬라큘 미호크 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=83706191)

```json
{
  "review_id": "R5037",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5038 — 프리미엄 쥬라큘 미호크 [THE METALLIC] (1개)

상품 ID: 3224

- [원피스 프리미엄 쥬라큘 미호크 (THE METALLIC)](https://www.bnkrmall.co.kr/goods/detail.do?gno=13784638)

```json
{
  "review_id": "R5038",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5039 — 프리미엄 트라팔가 로우 [THE BRUSH] (1개)

상품 ID: 3610

- [원피스 프리미엄 트라팔가 로우 (THE BRUSH)](https://www.bnkrmall.co.kr/goods/detail.do?gno=36392082)

```json
{
  "review_id": "R5039",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5040 — 플러피 퍼피 쵸파 & 카루 (A:토니토니 쵸파) (1개)

상품 ID: 4263

- [원피스 플러피 퍼피 쵸파 & 카루 (A:토니토니 쵸파)](https://www.bnkrmall.co.kr/goods/detail.do?gno=95767300)

```json
{
  "review_id": "R5040",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5041 — 플러피 퍼피 쵸파 VER.A (1개)

상품 ID: 4380

- [원피스 플러피 퍼피 쵸파 VER.A](https://www.bnkrmall.co.kr/goods/detail.do?gno=59810)

```json
{
  "review_id": "R5041",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5042 — 피그라이프 도우마 (1개)

상품 ID: 3812

- [귀멸의 칼날 피그라이프 도우마](https://www.bnkrmall.co.kr/goods/detail.do?gno=91122468)

```json
{
  "review_id": "R5042",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5043 — 피그라이프 모모 (1개)

상품 ID: 3485

- [단다단 피그라이프 모모](https://www.bnkrmall.co.kr/goods/detail.do?gno=23946581)

```json
{
  "review_id": "R5043",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5044 — 피그라이프 몽키 D 루피 기어5 VOL.1&VOL.2 (VER.A) (1개)

상품 ID: 3691

- [원피스 피그라이프 몽키 D 루피 기어5 VOL.1&VOL.2 (VER.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=58439834)

```json
{
  "review_id": "R5044",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5045 — 피그라이프 몽키 D 루피 기어5 VOL.1&VOL.2 (VER.B) (1개)

상품 ID: 3690

- [원피스 피그라이프 몽키 D 루피 기어5 VOL.1&VOL.2 (VER.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=89547597)

```json
{
  "review_id": "R5045",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5046 — 피그라이프 몽키 D 루피 기어5 VOL.3 (1개)

상품 ID: 3993

- [원피스 피그라이프 몽키 D 루피 기어5 VOL.3](https://www.bnkrmall.co.kr/goods/detail.do?gno=14922648)

```json
{
  "review_id": "R5046",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5047 — 피그라이프 몽키 D 루피 기어5 VOL.4 (1개)

상품 ID: 3968

- [원피스 피그라이프 몽키 D 루피 기어5 VOL.4](https://www.bnkrmall.co.kr/goods/detail.do?gno=77410053)

```json
{
  "review_id": "R5047",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5048 — 피그라이프 몽키 D 루피 기어5 VOL.5 (1개)

상품 ID: 3664

- [원피스 피그라이프 몽키 D 루피 기어5 VOL.5](https://www.bnkrmall.co.kr/goods/detail.do?gno=22346635)

```json
{
  "review_id": "R5048",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5049 — 피그라이프 무키무키 네즈미 (1개)

상품 ID: 3960

- [귀멸의 칼날 피그라이프 무키무키 네즈미](https://www.bnkrmall.co.kr/goods/detail.do?gno=46384593)

```json
{
  "review_id": "R5049",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5050 — 피그라이프 블랙홀!!! 마샬 D 티치 (1개)

상품 ID: 3889

- [원피스 피그라이프 블랙홀!!! 마샬 D 티치](https://www.bnkrmall.co.kr/goods/detail.do?gno=35012977)

```json
{
  "review_id": "R5050",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5051 — 피그라이프 사스케의 관 (1개)

상품 ID: 3799

- [나루토 피그라이프 사스케의 관](https://www.bnkrmall.co.kr/goods/detail.do?gno=61130326)

```json
{
  "review_id": "R5051",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5052 — 피그라이프 아오키지 쿠잔 (1개)

상품 ID: 3979

- [원피스 피그라이프 아오키지 쿠잔](https://www.bnkrmall.co.kr/goods/detail.do?gno=42877977)

```json
{
  "review_id": "R5052",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5053 — 피그라이프 아카이누 사카즈키 (1개)

상품 ID: 3931

- [원피스 피그라이프 아카이누 사카즈키](https://www.bnkrmall.co.kr/goods/detail.do?gno=62618511)

```json
{
  "review_id": "R5053",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5054 — 피그라이프 오카룽(변신) (1개)

상품 ID: 3765

- [단다단 피그라이프 오카룽(변신)](https://www.bnkrmall.co.kr/goods/detail.do?gno=16475783)

```json
{
  "review_id": "R5054",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5055 — 피그라이프 외도마상 (1개)

상품 ID: 3301

- [나루토 질풍전 피그라이프 외도마상](https://www.bnkrmall.co.kr/goods/detail.do?gno=81696374)

```json
{
  "review_id": "R5055",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5056 — 피그라이프 유스타스 키드 (1개)

상품 ID: 3836

- [원피스 피그라이프 유스타스 키드](https://www.bnkrmall.co.kr/goods/detail.do?gno=31150832)

```json
{
  "review_id": "R5056",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5057 — 피그라이프 종말의 계곡 센쥬 하시라마 (1개)

상품 ID: 3492

- [나루토 피그라이프 종말의 계곡 센쥬 하시라마](https://www.bnkrmall.co.kr/goods/detail.do?gno=70113591)

```json
{
  "review_id": "R5057",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5058 — 피그라이프 종말의 계곡 우치하 마다라 (1개)

상품 ID: 3493

- [나루토 피그라이프 종말의 계곡 우치하 마다라](https://www.bnkrmall.co.kr/goods/detail.do?gno=29509867)

```json
{
  "review_id": "R5058",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5059 — 피그라이프 키자루 볼사리노 (1개)

상품 ID: 3955

- [원피스 피그라이프 키자루 볼사리노](https://www.bnkrmall.co.kr/goods/detail.do?gno=63503543)

```json
{
  "review_id": "R5059",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5060 — 피그라이프 터보 할멈 (마네키네코) (1개)

상품 ID: 3344

- [단다단 피그라이프 터보 할멈 (마네키네코)](https://www.bnkrmall.co.kr/goods/detail.do?gno=43777852)

```json
{
  "review_id": "R5060",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5061 — 피그라이프 해적 사냥꾼 조로 (1개)

상품 ID: 3862

- [원피스 피그라이프 해적 사냥꾼 조로](https://www.bnkrmall.co.kr/goods/detail.do?gno=1015211)

```json
{
  "review_id": "R5061",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5062 — 피콜로 (미니) 패널 (1개)

상품 ID: 3957

- [드래곤볼 DAIMA 피콜로 (미니) 패널 피규어](https://www.bnkrmall.co.kr/goods/detail.do?gno=81454128)

```json
{
  "review_id": "R5062",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5063 — 필름 레드 더 그랜드라인 시리즈 프리미엄 몽키 D 루피 (1개)

상품 ID: 4214

- [원피스 필름 레드 더 그랜드라인 시리즈 프리미엄 몽키 D 루피](https://www.bnkrmall.co.kr/goods/detail.do?gno=12214706)

```json
{
  "review_id": "R5063",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5064 — 한계돌파 RX-78-2 건담 (1개)

상품 ID: 3410

- [기동전사 건담 한계돌파 RX-78-2 건담](https://www.bnkrmall.co.kr/goods/detail.do?gno=5419695)

```json
{
  "review_id": "R5064",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5065 — 한계돌파 스트라이크 건담 (1개)

상품 ID: 3584

- [기동전사 건담 SEED 한계돌파 스트라이크 건담](https://www.bnkrmall.co.kr/goods/detail.do?gno=32713523)

```json
{
  "review_id": "R5065",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5066 — 한계돌파 유니콘 건담 (디스트로이 모드) (1개)

상품 ID: 3242

- [기동전사 건담 UC 한계돌파 유니콘 건담 (디스트로이 모드)](https://www.bnkrmall.co.kr/goods/detail.do?gno=83091341)

```json
{
  "review_id": "R5066",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5067 — 해즈빈 호텔 모니터 탑 ～배기~(ver.A) (1개)

상품 ID: 3750

- [해즈빈 호텔 모니터 탑 피규어～배기~(ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=77270965)

```json
{
  "review_id": "R5067",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5068 — 해즈빈 호텔 모니터 탑 ～배기~(ver.B) (1개)

상품 ID: 3825

- [해즈빈 호텔 모니터 탑 피규어～배기~(ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=92914054)

```json
{
  "review_id": "R5068",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5069 — 해즈빈 호텔 모니터 탑 ～알래스터~(ver.A) (1개)

상품 ID: 3827

- [해즈빈 호텔 모니터 탑 피규어～알래스터~(ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=96945174)

```json
{
  "review_id": "R5069",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5070 — 해즈빈 호텔 모니터 탑 ～알래스터~(ver.B) (1개)

상품 ID: 3826

- [해즈빈 호텔 모니터 탑 피규어～알래스터~(ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=95707163)

```json
{
  "review_id": "R5070",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5071 — 해즈빈 호텔 모니터 탑 ～엔젤 더스트～(ver.A) (1개)

상품 ID: 3854

- [해즈빈 호텔 모니터 탑 피규어～엔젤 더스트～(ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=40233346)

```json
{
  "review_id": "R5071",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5072 — 해즈빈 호텔 모니터 탑 ～엔젤 더스트～(ver.B) (1개)

상품 ID: 3853

- [해즈빈 호텔 모니터 탑 피규어～엔젤 더스트～(ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=23788328)

```json
{
  "review_id": "R5072",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5073 — 해즈빈 호텔 모니터 탑 ~찰리 모닝스타~ (ver.A) (1개)

상품 ID: 3728

- [해즈빈 호텔 모니터 탑 피규어~찰리 모닝스타~ (ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=23083918)

```json
{
  "review_id": "R5073",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5074 — 해즈빈 호텔 모니터 탑 ~찰리 모닝스타~ (ver.B) (1개)

상품 ID: 3727

- [해즈빈 호텔 모니터 탑 피규어~찰리 모닝스타~ (ver.B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=83100175)

```json
{
  "review_id": "R5074",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5075 — 해즈빈 호텔 모니터 탑 ～허스크～(ver..B) (1개)

상품 ID: 3851

- [해즈빈 호텔 모니터 탑 피규어～허스크～(ver..B)](https://www.bnkrmall.co.kr/goods/detail.do?gno=84818013)

```json
{
  "review_id": "R5075",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5076 — 해즈빈 호텔 모니터 탑 ～허스크～(ver.A) (1개)

상품 ID: 3852

- [해즈빈 호텔 모니터 탑 피규어～허스크～(ver.A)](https://www.bnkrmall.co.kr/goods/detail.do?gno=87739227)

```json
{
  "review_id": "R5076",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5077 — 해즈빈 호텔 알래스터 라디오 악마 (1개)

상품 ID: 3546

- [해즈빈 호텔 알래스터 피규어 라디오 악마](https://www.bnkrmall.co.kr/goods/detail.do?gno=70853515)

```json
{
  "review_id": "R5077",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5078 — 호시나 소우시로 [THE METALLIC] (1개)

상품 ID: 4050

- [괴수 8호 호시나 소우시로 (THE METALLIC)](https://www.bnkrmall.co.kr/goods/detail.do?gno=17727340)

```json
{
  "review_id": "R5078",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5079 — 호카게 츠나데 오카게 집결!! (1개)

상품 ID: 3276

- [나루토 질풍전 호카게 츠나데 피규어 오카게 집결!!](https://www.bnkrmall.co.kr/goods/detail.do?gno=36209622)

```json
{
  "review_id": "R5079",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5080 — 혼 이펙트 바위 베이지 Ver. (1개)

상품 ID: 2024

- [혼 이펙트 바위 베이지 Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=97486990)

```json
{
  "review_id": "R5080",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5081 — 혼 이펙트 버닝 프레임 레드 Ver. (1개)

상품 ID: 2035

- [혼 이펙트 버닝 프레임 레드 Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=81695242)

```json
{
  "review_id": "R5081",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5082 — 혼 이펙트 썬더 옐로우 Ver. (1개)

상품 ID: 2019

- [혼 이펙트 썬더 옐로우 Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=42344168)

```json
{
  "review_id": "R5082",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5083 — 혼 이펙트 에너지 오라 옐로우 Ver. (1개)

상품 ID: 2036

- [혼 이펙트 에너지 오라 옐로우 Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=21600207)

```json
{
  "review_id": "R5083",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5084 — 혼 이펙트 에너지 오라 화이트 Ver. (1개)

상품 ID: 2018

- [혼 이펙트 에너지 오라 화이트 Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=70006627)

```json
{
  "review_id": "R5084",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5085 — 혼 이펙트 윈드 그린 Ver. (1개)

상품 ID: 2023

- [혼 이펙트 윈드 그린 Ver.](https://www.bnkrmall.co.kr/goods/detail.do?gno=37323728)

```json
{
  "review_id": "R5085",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5086 — 홀로라이브 #HOLOLIVE IF -holobabies- 라플라스 다크니스 (1개)

상품 ID: 3732

- [홀로라이브 #HOLOLIVE IF -holobabies- 라플라스 다크니스](https://www.bnkrmall.co.kr/goods/detail.do?gno=66638952)

```json
{
  "review_id": "R5086",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5087 — 홀로라이브 #HOLOLIVE IF -holobabies- 사쿠라 미코 (1개)

상품 ID: 3513

- [홀로라이브 #HOLOLIVE IF -holobabies- 사쿠라 미코](https://www.bnkrmall.co.kr/goods/detail.do?gno=46594816)

```json
{
  "review_id": "R5087",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5088 — 홀로라이브 #HOLOLIVE IF -holobabies- 코보 카나에루 (1개)

상품 ID: 3466

- [홀로라이브 #HOLOLIVE IF -holobabies- 코보 카나에루](https://www.bnkrmall.co.kr/goods/detail.do?gno=7606993)

```json
{
  "review_id": "R5088",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5089 — 홀로라이브 #HOLOLIVE IF -holobabies- 호쇼 마린 (1개)

상품 ID: 3467

- [홀로라이브 #HOLOLIVE IF -holobabies- 호쇼 마린](https://www.bnkrmall.co.kr/goods/detail.do?gno=10703413)

```json
{
  "review_id": "R5089",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5090 — 홀로라이브 #HOLOLIVE IF -holobabies- 히메모리 루나 (1개)

상품 ID: 3731

- [홀로라이브 #HOLOLIVE IF -holobabies- 히메모리 루나](https://www.bnkrmall.co.kr/goods/detail.do?gno=650010)

```json
{
  "review_id": "R5090",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5091 — 흉상 페른 (1개)

상품 ID: 4011

- [장송의 프리렌 흉상 피규어 페른](https://www.bnkrmall.co.kr/goods/detail.do?gno=73512737)

```json
{
  "review_id": "R5091",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5092 — 흉상 프리렌 (1개)

상품 ID: 3609

- [장송의 프리렌 흉상 피규어 프리렌](https://www.bnkrmall.co.kr/goods/detail.do?gno=68666513)

```json
{
  "review_id": "R5092",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5093 — 히스토리 박스 Vol.1 (손오공) (1개)

상품 ID: 4686

- [드래곤볼 Z 히스토리 박스 Vol.1 (손오공)](https://www.bnkrmall.co.kr/goods/detail.do?gno=15658)

```json
{
  "review_id": "R5093",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5094 — 히스토리 박스 Vol.10 (1개)

상품 ID: 4184

- [드래곤볼 Z 히스토리 박스 Vol.10](https://www.bnkrmall.co.kr/goods/detail.do?gno=80256436)

```json
{
  "review_id": "R5094",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5095 — 히스토리 박스 Vol.11 (1개)

상품 ID: 4155

- [드래곤볼 Z 히스토리 박스 Vol.11](https://www.bnkrmall.co.kr/goods/detail.do?gno=9653418)

```json
{
  "review_id": "R5095",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5096 — 히스토리 박스 Vol.12 (1개)

상품 ID: 4140

- [드래곤볼 Z 히스토리 박스 Vol.12](https://www.bnkrmall.co.kr/goods/detail.do?gno=49918801)

```json
{
  "review_id": "R5096",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5097 — 히스토리 박스 Vol.2 (1개)

상품 ID: 4610

- [드래곤볼 Z 히스토리 박스 Vol.2](https://www.bnkrmall.co.kr/goods/detail.do?gno=55771)

```json
{
  "review_id": "R5097",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5098 — 히스토리 박스 Vol.3 (1개)

상품 ID: 4446

- [드래곤볼 Z 히스토리 박스 Vol.3](https://www.bnkrmall.co.kr/goods/detail.do?gno=59217)

```json
{
  "review_id": "R5098",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5099 — 히스토리 박스 Vol.4 (1개)

상품 ID: 4386

- [드래곤볼 히스토리 박스 Vol.4](https://www.bnkrmall.co.kr/goods/detail.do?gno=59563)

```json
{
  "review_id": "R5099",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5100 — 히스토리 박스 Vol.5 (1개)

상품 ID: 4353

- [드래곤볼 Z 히스토리 박스 Vol.5](https://www.bnkrmall.co.kr/goods/detail.do?gno=59970)

```json
{
  "review_id": "R5100",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5101 — 히스토리 박스 Vol.6 (1개)

상품 ID: 4330

- [드래곤볼 Z 히스토리 박스 Vol.6](https://www.bnkrmall.co.kr/goods/detail.do?gno=46008119)

```json
{
  "review_id": "R5101",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5102 — 히스토리 박스 Vol.9 (1개)

상품 ID: 4209

- [드래곤볼 Z 히스토리 박스 Vol.9](https://www.bnkrmall.co.kr/goods/detail.do?gno=810294)

```json
{
  "review_id": "R5102",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5103 — 히스토리 박스 마인 베지터 (1개)

상품 ID: 3817

- [드래곤볼 Z 히스토리 박스 마인 베지터](https://www.bnkrmall.co.kr/goods/detail.do?gno=28014021)

```json
{
  "review_id": "R5103",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5104 — 히스토리 박스 마인 부우 (1개)

상품 ID: 3335

- [드래곤볼 Z 히스토리 박스 마인 부우](https://www.bnkrmall.co.kr/goods/detail.do?gno=52598182)

```json
{
  "review_id": "R5104",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5105 — 히스토리 박스 무천도사 (1개)

상품 ID: 3795

- [드래곤볼 히스토리 박스 무천도사](https://www.bnkrmall.co.kr/goods/detail.do?gno=4344086)

```json
{
  "review_id": "R5105",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5106 — 히스토리 박스 미스터 사탄 (1개)

상품 ID: 3471

- [드래곤볼 Z 히스토리 박스 미스터 사탄](https://www.bnkrmall.co.kr/goods/detail.do?gno=34396457)

```json
{
  "review_id": "R5106",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5107 — 히스토리 박스 베지트 (1개)

상품 ID: 3740

- [드래곤볼 Z 히스토리 박스 베지트](https://www.bnkrmall.co.kr/goods/detail.do?gno=63488277)

```json
{
  "review_id": "R5107",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5108 — 히스토리 박스 브루마 (1개)

상품 ID: 3807

- [드래곤볼 히스토리 박스 브루마](https://www.bnkrmall.co.kr/goods/detail.do?gno=82795005)

```json
{
  "review_id": "R5108",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5109 — 히스토리 박스 손오천&트랭크스 (1개)

상품 ID: 3683

- [드래곤볼 Z 히스토리 박스 손오천&트랭크스](https://www.bnkrmall.co.kr/goods/detail.do?gno=52862532)

```json
{
  "review_id": "R5109",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5110 — 히스토리 박스 신룡 (1개)

상품 ID: 3618

- [드래곤볼 히스토리 박스 신룡](https://www.bnkrmall.co.kr/goods/detail.do?gno=26202768)

```json
{
  "review_id": "R5110",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5111 — 히스토리 박스 야무치 (1개)

상품 ID: 3452

- [드래곤볼 히스토리 박스 야무치](https://www.bnkrmall.co.kr/goods/detail.do?gno=11843636)

```json
{
  "review_id": "R5111",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5112 — 히스토리 박스 인조인간 8호 (1개)

상품 ID: 3382

- [드래곤볼 히스토리 박스 인조인간 8호](https://www.bnkrmall.co.kr/goods/detail.do?gno=74587031)

```json
{
  "review_id": "R5112",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5113 — 히스토리 박스 초사이어인3 손오공 (1개)

상품 ID: 3560

- [드래곤볼 Z 히스토리 박스 초사이어인3 손오공](https://www.bnkrmall.co.kr/goods/detail.do?gno=68567070)

```json
{
  "review_id": "R5113",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5114 — 히스토리 박스 크리링 (1개)

상품 ID: 3753

- [드래곤볼 히스토리 박스 크리링](https://www.bnkrmall.co.kr/goods/detail.do?gno=13226330)

```json
{
  "review_id": "R5114",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```

## R5115 — 히스토리 박스 타오파이파이 (1개)

상품 ID: 3665

- [드래곤볼 히스토리 박스 타오파이파이](https://www.bnkrmall.co.kr/goods/detail.do?gno=59088339)

```json
{
  "review_id": "R5115",
  "approved": false,
  "value": null,
  "not_applicable": false,
  "note": ""
}
```
