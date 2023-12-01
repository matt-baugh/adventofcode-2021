import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents


convert :: String -> (Int, Int)
convert xs
  = (p1, p2)
  where
    [p1, p2] = map (read . last . words) $ lines xs


solve :: (Int, Int) -> Int
solve (p1Start, p2Start)
  = max p1C p2C
  where
    (_, (p1C, p2C)) = playFrom [] ((p1Start, 0), (p2Start, 0), True)


type GameState = ((Int, Int), (Int, Int), Bool)


gameOver :: GameState -> Bool
gameOver ((_, s1), (_, s2), _)
  = s1 > 20 || s2 > 20


playFromMemo :: [(GameState, (Int, Int))] -> GameState -> ([(GameState, (Int, Int))], (Int, Int))
playFromMemo resRec gs@((_, s1), (_, s2), _)
  | isJust mRes = (resRec, fromJust mRes)
  | gameOver gs = ((gs, res) : resRec, res)
  | otherwise   = ((gs, res') : resRec', res')
  where
    mRes            = lookup gs resRec
    res             = if s1 > s2 then (1, 0) else (0, 1)
    (resRec', res') = playFrom resRec gs


playFrom :: [(GameState, (Int, Int))] -> GameState -> ([(GameState, (Int, Int))], (Int, Int))
playFrom resRec state
  = (resRec'', foldl (\(acc1, acc2) ((s1, s2), c) -> (acc1 + c * s1, acc2 + c * s2)) (0, 0) $ zip possRes rollCounts)
  where
    (resRec'', possRes) = mapAccumL (\resRec' r -> playFromMemo resRec' (playRoll state r)) resRec possRolls


playRoll :: ((Int, Int), (Int, Int), Bool) -> Int -> ((Int, Int), (Int, Int), Bool)
playRoll ((p1Pos, p1Score), p2Info, True) mv
  = ((p1Pos'', p1Score + p1Pos''), p2Info, False)
  where
    p1Pos'  = p1Pos + mv
    p1Pos'' = if p1Pos' > 10 then p1Pos' - 10 else p1Pos'
playRoll (p1Info, (p2Pos, p2Score), False) mv
  = (p1Info, (p2Pos'', p2Score + p2Pos''), True)
  where
    p2Pos'  = p2Pos + mv
    p2Pos'' = if p2Pos' > 10 then p2Pos' - 10 else p2Pos'

rollDist ::[(Int, Int)]
rollDist = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]

possRolls = map fst rollDist
rollCounts = map snd rollDist

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
 "Player 1 starting position: 4",
 "Player 2 starting position: 8"]
testData1 = convert testInput1
