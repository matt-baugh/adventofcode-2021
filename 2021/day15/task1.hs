import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents

convert :: String -> [[Int]]
convert xs
  = map (map (\c -> ord c - ord '0')) $ lines xs


solve :: [[Int]] -> [[Int]]
solve rMap
  = findPath initFs trMap (rMap, h, w)
  where
    h        = length rMap
    w        = length (rMap !! 0)
    (si, sj) = (0, 0)
    adjs     = adjacentIndices si sj h w False
    initFs   = sort $ map (\p@(i, j) -> ((rMap !! i) !! j, p)) adjs
    trMap    = (0 : replicate (w - 1) (-1)) : replicate (h - 1) (replicate w (-1))


findPath :: [(Int, (Int, Int))] -> [[Int]] -> ([[Int]], Int, Int) -> [[Int]]
findPath [] trMap _
  = trMap
findPath ((r, (i, j)):fs) trMap m@(rMap, rH, rW)
  = findPath fs'' trMap' m
  where
    (rs, row:rs') = splitAt i trMap
    trMap'        = rs ++ (addToElem row j (r + 1) : rs')
    adjs          = adjacentIndices i j rH rW False
    validAdjs     = filter (\(k, l) -> (trMap' !! k) !! l == -1) adjs
    (update, fs') = partition (\(_, c) -> elem c validAdjs) fs
    update'       = map (\(r', c@(k, l)) -> (min r' (r + ((rMap !! k) !! l)), c)) update
    updateCs      = map snd update
    newCs         = filter (flip notElem updateCs) validAdjs
    newCRs        = map (\c@(k, l) -> (r + ((rMap !! k) !! l), c)) newCs
    fs''          = foldl (flip insert) fs' (update' ++ newCRs)


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



testInput :: String
testInput = unlines ["1163751742",
 "1381373672",
 "2136511328",
 "3694931569",
 "7463417111",
 "1319128137",
 "1359912421",
 "3125421639",
 "1293138521",
 "2311944581"]
testData = convert testInput
