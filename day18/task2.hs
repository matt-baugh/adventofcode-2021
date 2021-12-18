import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents

convert :: String -> [SNum]
convert xs
  = map (fst . convert') $ lines xs
  where
    convert' :: String -> (SNum, String)
    convert' ('[':ys)
      = (Pair sN1 sN2, ys'')
      where
       (sN1, (',':ys'))  = convert' ys
       (sN2, (']':ys'')) = convert' ys'
    convert' ys
      = (Lit (read intS), rest)
      where
        (intS, rest) = break (\c -> c == ',' || c == ']') ys
       


data SNum = Pair SNum SNum | Lit Int
  deriving Eq

instance Show SNum where
  show (Lit i) = show i
  show (Pair sn1 sn2) = '[' : (show sn1 ++ "," ++ (show sn2) ++ "]")


solve :: [SNum] -> Int
solve xs
  = maximum $ concatMap (\(x1, xs') -> map (mag . (add x1)) xs') $ zip xs (repeat xs)


mag :: SNum -> Int
mag (Lit i)
  = i
mag (Pair sn1 sn2)
  = 3 * (mag sn1) + 2 * (mag sn2)


add :: SNum -> SNum -> SNum
add x y
  = reduce (Pair x y)


reduce :: SNum -> SNum
reduce sn
  | expld     = reduce sn'
  | splt      = reduce sn''
  | otherwise = sn''
  where
    (sn', expld) = maybeExplode sn
    (sn'', splt) = maybeSplit sn'

maybeExplode :: SNum -> (SNum, Bool)
maybeExplode sn
  = (res, changed)
  where
    (res, changed, _, _) = mExp sn 0
    mExp :: SNum -> Int -> (SNum, Bool, Maybe Int, Maybe Int)
    mExp (Pair (Lit n1) (Lit n2)) 4
      = (Lit 0, True, Just n1, Just n2)
    mExp (Lit i) _
      = (Lit i, False, Nothing, Nothing)
    mExp (Pair sn1 sn2) n
      | expld && isJust mI2  = (Pair sn1' (addToLeft sn2 (fromJust mI2)), expld, mI1, Nothing)
      | expld                = (Pair sn1' sn2, expld, mI1, mI2)
      | expld' && isJust mI3 = (Pair (addToRight sn1' (fromJust mI3)) sn2', expld', Nothing, mI4)
      | otherwise            = (Pair sn1' sn2', expld', mI3, mI4)
      where
        (sn1', expld, mI1, mI2)  = mExp sn1 (n + 1)
        (sn2', expld', mI3, mI4) = mExp sn2 (n + 1)

addToLeft :: SNum -> Int -> SNum
addToLeft (Lit i) j
  = Lit (i + j)
addToLeft (Pair sn1 sn2) i
  = Pair (addToLeft sn1 i) sn2

addToRight :: SNum -> Int -> SNum
addToRight (Lit i) j
  = Lit (i + j)
addToRight (Pair sn1 sn2) i
  = Pair sn1 $ addToRight sn2 i


maybeSplit :: SNum -> (SNum, Bool)
maybeSplit sn@(Lit i)
  | i >= 10   = (Pair (Lit h) (Lit (h + r)), True)
  | otherwise = (sn, False)
  where
    h = div i 2
    r = mod i 2
maybeSplit (Pair sn1 sn2)
  | hasSplit  = (Pair sn1' sn2, hasSplit)
  | otherwise = (Pair sn1' sn2', hasSplit')
  where
    (sn1', hasSplit)  = maybeSplit sn1
    (sn2', hasSplit') = maybeSplit sn2


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
testInput1 = unlines [
 "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
 "[[[5,[2,8]],4],[5,[[9,9],0]]]",
 "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
 "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
 "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
 "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
 "[[[[5,4],[7,7]],8],[[8,3],8]]",
 "[[9,3],[[9,9],[6,[4,9]]]]",
 "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
 "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"]

testData1 = convert testInput1
