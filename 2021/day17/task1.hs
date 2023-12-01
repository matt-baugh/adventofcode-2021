import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents

convert :: String -> ((Int, Int), (Int, Int))
convert xs
  = (toRange xR', toRange yR)
  where
    [_, xR, yR ] = splitOn '=' xs
    [xR', _]     = splitOn ',' xR


data Packet = Literal Int Int | Operator Int Int [Packet]
  deriving Show


solve :: ((Int, Int), (Int, Int)) -> Int
solve (xR, (ymin, ymax))
  = div (xY * (xY + 1)) 2
  where
    xV = calcXV xR
    xY = (abs ymin) - 1

-- Find x velocity that just about makes it to range
calcXV :: (Int, Int) -> Int
calcXV (xTMin, xTMax)
  = calcXV' 1 1
  where
    xBs = [xTMin..xTMax]
    calcXV' :: Int -> Int -> Int
    calcXV' curr acc
      | elem acc xBs = curr
      | otherwise    = calcXV' next (acc + next)
      where
        next = curr + 1
    


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
testInput1 = "target area: x=20..30, y=-10..-5"

testData1 = convert testInput1
