import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents

convert :: String -> [[Coord3D]]
convert xs
  = map (map readCoord3D) xs'
  where
    xs' = map tail $ splitOn "" $ lines xs


solve :: [[Coord3D]] -> Int
solve xs
  = length $ nub $ concat allFeats
  where 
    allFeats = map genFeats xs


genFeats :: [Coord3D] -> [[Float]]
genFeats cs
  = map ((take 2). tail . sort . (\c -> map (getDist c) cs)) cs


getDist :: Coord3D -> Coord3D -> Float
getDist (x, y, z) (x', y', z')
  = (sqrt . fromIntegral) (dx ^ 2 + dy ^ 2 + dz ^ 2)
  where
    dx = x - x'
    dy = y - y'
    dz = z - z'




toRange :: String -> (Int, Int)
toRange xs
  = (read lb, read ub)
  where
    [lb, ub] = splitOn '.' xs


toBinary :: Int -> Int -> [Int]
toBinary bits i
  = map fst $ tail $ scanl (\(_, rem) j-> (div rem j, mod rem j)) (-1, i) ps
  where
    ps = map (2^) $ reverse [0..bits - 1]


toInt :: [Int] -> Int
toInt xs
  = sum $ map (\(i, p) -> i * 2 ^ p) $ zip xs $ reverse [0..length xs - 1]
    

combineCounts :: [(Char, Int)] -> [(Char, Int)] -> [(Char, Int)]
combineCounts cs cs'
  = map (\k -> (k, lookupOr k cs 0 + (lookupOr k cs' 0))) allKeys
  where
    allKeys = nub $ map fst cs ++ map fst cs'


readCoord :: String -> (Int, Int)
readCoord s
  = (read s1, read s2)
  where
    [s1, s2] = splitOn ',' s


type Coord3D = (Int, Int, Int)


readCoord3D :: String -> Coord3D
readCoord3D s
  = (read s1, read s2, read s3)
  where
    [s1, s2, s3] = splitOn ',' s


splitOn :: (Eq a) => a -> [a] -> [[a]]
splitOn _ [] = []
splitOn delimiter str = 
    let (start, rest) = break (== delimiter) str
        (_, remain) = span (== delimiter) rest
     in start : splitOn delimiter remain


lookupOr :: (Eq a) => a -> [(a, b)] -> b -> b
lookupOr x ps y
  = fromMaybe y $ lookup x ps


jLookup :: (Eq a) => a -> [(a, b)] -> b
jLookup x = (fromJust . lookup x)


lookupAll :: (Eq a) => a -> [(a, b)] -> [b]
lookupAll x xs
  = map snd $ filter (\p -> x == fst p) xs


countIn :: Eq a => a -> [a] -> Int
countIn x
  = length . filter (==x)

    
getAllInds :: [[a]] -> [(Int, Int)]
getAllInds xs
  = concatMap (\(i, js) -> map (\j -> (i, j)) js) $ zip [0..h-1] $ replicate h [0..w-1]
  where
    h = length xs
    w = length (xs !! 0)

adjacentIndices :: Int -> Int -> Int -> Int -> Bool -> [(Int, Int)]
adjacentIndices i j h w useDiag
  | useDiag   =  map (\[f, s] -> (f, s)) $ inds ++ validDiag
  | otherwise =  map (\[f, s] -> (f, s)) inds
  where
    inds = adjInd i j w ++ (map reverse $ adjInd j i h)
    adjInd :: Int -> Int -> Int -> [[Int]]
    adjInd f v max
      | v == 0       = [below]
      | v == max - 1 = [above]
      | otherwise    = [above, below]
      where
        above = [f, v - 1]
        below = [f, v + 1]
    adjDiag = concatMap (\[k, l] -> map (\d -> [k + d, l]) [-1, 1])
                        $ map (\d -> [i, j + d]) [-1, 1]
    validDiag = filter (\[k, l] -> 0 <= k && k < h && 0 <= l && l < w) adjDiag


splitBetween :: Int -> Int -> [a] -> ([a], [a], [a])
splitBetween i1 i2 xs
  = (first, second, third)
  where
    (first, remaining) = splitAt i1 xs
    (second, third)    = splitAt (i2 - i1 + 1) remaining


addToElem :: [Int] -> Int -> Int -> [Int]
addToElem xs i c 
  = xs' ++ ((x + c) : xs'')              
  where                                  
    (xs', x:xs'') = splitAt i xs


testInput1 :: String
testInput1 = unlines [
  "--- scanner 0 ---",
  "404,-588,-901",
  "528,-643,409",
  "-838,591,734",
  "390,-675,-793",
  "-537,-823,-458",
  "-485,-357,347",
  "-345,-311,381",
  "-661,-816,-575",
  "-876,649,763",
  "-618,-824,-621",
  "553,345,-567",
  "474,580,667",
  "-447,-329,318",
  "-584,868,-557",
  "544,-627,-890",
  "564,392,-477",
  "455,729,728",
  "-892,524,684",
  "-689,845,-530",
  "423,-701,434",
  "7,-33,-71",
  "630,319,-379",
  "443,580,662",
  "-789,900,-551",
  "459,-707,401",
  "",
  "--- scanner 1 ---",
  "686,422,578",
  "605,423,415",
  "515,917,-361",
  "-336,658,858",
  "95,138,22",
  "-476,619,847",
  "-340,-569,-846",
  "567,-361,727",
  "-460,603,-452",
  "669,-402,600",
  "729,430,532",
  "-500,-761,534",
  "-322,571,750",
  "-466,-666,-811",
  "-429,-592,574",
  "-355,545,-477",
  "703,-491,-529",
  "-328,-685,520",
  "413,935,-424",
  "-391,539,-444",
  "586,-435,557",
  "-364,-763,-893",
  "807,-499,-711",
  "755,-354,-619",
  "553,889,-390",
  "",
  "--- scanner 2 ---",
  "649,640,665",
  "682,-795,504",
  "-784,533,-524",
  "-644,584,-595",
  "-588,-843,648",
  "-30,6,44",
  "-674,560,763",
  "500,723,-460",
  "609,671,-379",
  "-555,-800,653",
  "-675,-892,-343",
  "697,-426,-610",
  "578,704,681",
  "493,664,-388",
  "-671,-858,530",
  "-667,343,800",
  "571,-461,-707",
  "-138,-166,112",
  "-889,563,-600",
  "646,-828,498",
  "640,759,510",
  "-630,509,768",
  "-681,-892,-333",
  "673,-379,-804",
  "-742,-814,-386",
  "577,-820,562",
  "",
  "--- scanner 3 ---",
  "-589,542,597",
  "605,-692,669",
  "-500,565,-823",
  "-660,373,557",
  "-458,-679,-417",
  "-488,449,543",
  "-626,468,-788",
  "338,-750,-386",
  "528,-832,-391",
  "562,-778,733",
  "-938,-730,414",
  "543,643,-506",
  "-524,371,-870",
  "407,773,750",
  "-104,29,83",
  "378,-903,-323",
  "-778,-728,485",
  "426,699,580",
  "-438,-605,-362",
  "-469,-447,-387",
  "509,732,623",
  "647,635,-688",
  "-868,-804,481",
  "614,-800,639",
  "595,780,-596",
  "",
  "--- scanner 4 ---",
  "727,592,562",
  "-293,-554,779",
  "441,611,-461",
  "-714,465,-776",
  "-743,427,-804",
  "-660,-479,-426",
  "832,-632,460",
  "927,-485,-438",
  "408,393,-506",
  "466,436,-512",
  "110,16,151",
  "-258,-428,682",
  "-393,719,612",
  "-211,-452,876",
  "808,-476,-593",
  "-575,615,604",
  "-485,667,467",
  "-680,325,-822",
  "-627,-443,-432",
  "872,-547,-609",
  "833,512,582",
  "807,604,487",
  "839,-516,451",
  "891,-625,532",
  "-652,-548,-490",
  "30,-46,-14"]


testData1 = convert testInput1
