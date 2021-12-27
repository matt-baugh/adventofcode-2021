import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents


convert :: String -> [(Int, (Int, Int), (Int, Int), (Int, Int))]
convert xs
  = mapMaybe readCommand $ lines xs
  where
    minC = -50
    maxC = 50
    readCommand :: String -> Maybe (Int, (Int, Int), (Int, Int), (Int, Int))
    readCommand c
      | outOfBounds  = Nothing
      | val == "on"  = Just (1, xr, yr, zr)
      | val == "off" = Just (0, xr, yr, zr)
      where
        [val, rsStrs] = words c
        rs            = map (toRange . (drop 2)) $ splitOn ',' rsStrs
        outOfBounds   = any (\(lb, ub) -> lb > maxC || ub < minC) rs
        [xr, yr, zr]  = map (\(lb, ub) -> (50 + max lb minC, 50 + min ub maxC)) rs


solve :: [(Int, (Int, Int), (Int, Int), (Int, Int))] -> Int
solve xs
  = sum $ concat $ concat finalGrid
  where
    initGrid  = replicate 101 $ replicate 101 $ replicate 101 0
    finalGrid = foldl setCubes initGrid xs


setCubes :: [[[Int]]] -> (Int, (Int, Int), (Int, Int), (Int, Int)) -> [[[Int]]]
setCubes grid (v, (xLb, xUb), (yLb, yUb), (zLb, zUb))
  = zs1 ++ zs2' ++ zs3
  where
    (zs1, zs2, zs3)    = splitBetween zLb zUb grid
    (zys1, zys2, zys3) = unzip3 $ map (splitBetween yLb yUb) zs2
    zys2'              = map (map (splitBetween xLb xUb)) zys2
    zys2''             = map (map (\(xs1, xs2, xs3) -> xs1 ++ (replicate (length xs2) v) ++ xs3)) zys2'
    zs2'               = map (\(ys1, ys2, ys3) -> ys1 ++ ys2 ++ ys3) $ zip3 zys1 zys2'' zys3
 
 


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
 "on x=-20..26,y=-36..17,z=-47..7",
 "on x=-20..33,y=-21..23,z=-26..28",
 "on x=-22..28,y=-29..23,z=-38..16",
 "on x=-46..7,y=-6..46,z=-50..-1",
 "on x=-49..1,y=-3..46,z=-24..28",
 "on x=2..47,y=-22..22,z=-23..27",
 "on x=-27..23,y=-28..26,z=-21..29",
 "on x=-39..5,y=-6..47,z=-3..44",
 "on x=-30..21,y=-8..43,z=-13..34",
 "on x=-22..26,y=-27..20,z=-29..19",
 "off x=-48..-32,y=26..41,z=-47..-37",
 "on x=-12..35,y=6..50,z=-50..-2",
 "off x=-48..-32,y=-32..-16,z=-15..-5",
 "on x=-18..26,y=-33..15,z=-7..46",
 "off x=-40..-22,y=-38..-28,z=23..41",
 "on x=-16..35,y=-41..10,z=-47..6",
 "off x=-32..-23,y=11..30,z=-14..3",
 "on x=-49..-5,y=-3..45,z=-29..18",
 "off x=18..30,y=-20..-8,z=-3..13",
 "on x=-41..9,y=-7..43,z=-33..15",
 "on x=-54112..-39298,y=-85059..-49293,z=-27449..7877",
 "on x=967..23432,y=45373..81175,z=27513..53682"]

testData1 = convert testInput1
