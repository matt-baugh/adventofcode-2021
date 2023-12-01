import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents

convert :: String -> [Int]
convert xs
  = concatMap ((toBinary 4) . convert') xs
  where
    convert' :: Char -> Int
    convert' c
      | isDigit c = ord c - ord '0'
      | otherwise = ord c - ord 'A' + 10


data Packet = Literal Int Int | Operator Int Int [Packet]
  deriving Show


solve :: [Int] -> Int
solve xs
  = solve' p
  where
    (p, _) = toPacket xs
    solve' :: Packet -> Int
    solve' (Literal v _)
      = v
    solve' (Operator v _ ps)
      = v + sum ( map solve' ps)


toPacket :: [Int] -> (Packet, [Int])
toPacket xs
  | pType == 4 = (Literal version val, rm)
  | otherwise  = (Operator version pType ps, rm')
  where
    (v, xs')  = splitAt 3 xs
    (t, xs'') = splitAt 3 xs'
    version   = toInt v
    pType     = toInt t
    (val, rm) = litVal xs''
    (ps, rm') = opContents xs''


opContents :: [Int] -> ([Packet], [Int])
opContents (0:xs)
  = (ps, xs'')
  where
    (l, xs')    = splitAt 15 xs
    pLen        = toInt l
    (cur, xs'') = splitAt pLen xs'
    ps          = getAll cur
    getAll :: [Int] -> [Packet]
    getAll []
      = []
    getAll ys
      = p : getAll ys'
      where
        (p, ys') = toPacket ys
opContents (1:xs)
  = getN xs' pNum
  where
    (l, xs') = splitAt 11 xs
    pNum     = toInt l
    getN :: [Int] -> Int -> ([Packet], [Int])
    getN ys 0
      = ([], ys)
    getN ys i
      = (p:ps, ys'')
      where
        (p, ys')   = toPacket ys
        (ps, ys'') = getN ys' (i - 1)



litVal :: [Int] -> (Int, [Int])
litVal xs
  = (toInt bVal, xs')
  where
    (bVal, xs') = litVal' xs
    litVal' :: [Int] -> ([Int], [Int])
    litVal' (0:ys)
      = splitAt 4 ys
    litVal' (1:ys)
      = (zs ++ zs', ys'')
      where
        (zs, ys')   = splitAt 4 ys
        (zs', ys'') = litVal' ys'




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
testInput1 = "8A004A801A8002F478"
testInput2 = "620080001611562C8802118E34"
testInput3 = "C0015000016115A2E0802F182340"
testInput4 = "A0016C880162017C3686B18A3D4780"

testData1 = convert testInput1
testData2 = convert testInput2
testData3 = convert testInput3
testData4 = convert testInput4
