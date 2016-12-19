-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: endor.cdzsqxtczzyl.us-west-2.rds.amazonaws.com:3306
-- Generation Time: Dec 18, 2016 at 10:36 AM
-- Server version: 5.6.23-log
-- PHP Version: 5.5.9-1ubuntu4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ostrichdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `arbor_inventory`
--

CREATE TABLE IF NOT EXISTS `arbor_inventory` (
  `inventory_id` int(6) NOT NULL AUTO_INCREMENT,
  `item_id` int(6) NOT NULL,
  `client` varchar(50) NOT NULL,
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `owner` varchar(50) NOT NULL DEFAULT 'ostrich',
  `date_removed` timestamp NULL DEFAULT NULL,
  `condition` varchar(50) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `in_stock` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`inventory_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=143 ;

--
-- Dumping data for table `arbor_inventory`
--

INSERT INTO `arbor_inventory` (`inventory_id`, `item_id`, `client`, `date_added`, `owner`, `date_removed`, `condition`, `price`, `in_stock`) VALUES
(13, 204, 'paypal', '2016-07-21 14:04:33', 'ostrich', NULL, 'New', NULL, 1),
(14, 60, 'paypal', '2016-07-21 14:04:33', 'ostrich', NULL, 'New', NULL, 1),
(15, 6109, 'paypal', '2016-07-21 14:04:33', 'ostrich', NULL, 'New', NULL, 1),
(16, 2521, 'paypal', '2016-07-21 14:04:33', 'ostrich', NULL, 'New', NULL, 1),
(18, 23692, 'paypal', '2016-07-21 14:04:33', 'ostrich', NULL, 'New', NULL, 1),
(19, 35, 'paypal', '2016-07-21 14:04:33', 'ostrich', NULL, 'New', NULL, 1),
(20, 2871, 'paypal', '2016-07-21 14:04:33', 'ostrich', NULL, 'New', NULL, 1),
(21, 88, 'paypal', '2016-07-21 14:04:33', 'ostrich', NULL, 'New', NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `arbor_orders`
--

CREATE TABLE IF NOT EXISTS `arbor_orders` (
  `order_id` int(6) NOT NULL AUTO_INCREMENT,
  `user_id` int(6) NOT NULL,
  `inventory_id` int(6) NOT NULL,
  `order_placed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `order_returned` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=89 ;

--
-- Dumping data for table `arbor_orders`
--

INSERT INTO `arbor_orders` (`order_id`, `user_id`, `inventory_id`, `order_placed`, `order_returned`) VALUES
(54, 330, 18, '2016-08-02 08:47:15', '2016-08-02 08:48:11'),
(55, 330, 18, '2016-08-02 08:48:00', '2016-08-02 08:48:11');

-- --------------------------------------------------------

--
-- Table structure for table `areas`
--

CREATE TABLE IF NOT EXISTS `areas` (
  `area_id` int(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `hours` int(1) DEFAULT NULL,
  `day` int(1) DEFAULT NULL,
  `slot` int(1) DEFAULT NULL,
  `alias_id` int(1) DEFAULT NULL,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`area_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=67 ;

--
-- Dumping data for table `areas`
--

INSERT INTO `areas` (`area_id`, `name`, `hours`, `day`, `slot`, `alias_id`, `active`) VALUES
(1, 'indiranagar', 6, NULL, NULL, NULL, 1),
(2, 'indira nagar', 6, NULL, NULL, 1, 1),
(3, 'koramangala', 6, NULL, NULL, NULL, 1),
(4, 'domlur', 6, NULL, NULL, NULL, 1),
(5, 'kodihalli', 6, NULL, NULL, 1, 1),
(6, 'binnamangala', 6, NULL, NULL, NULL, 1),
(7, 'doopanahalli', 6, NULL, NULL, NULL, 1),
(8, 'adugodi', 6, NULL, NULL, 3, 1),
(9, 'embassy golflinks', 6, NULL, NULL, NULL, 1),
(10, 'embassy golf links', 6, NULL, NULL, 9, 1),
(11, 'challaghatta', 6, NULL, NULL, NULL, 1),
(12, 'hsr', 6, NULL, NULL, NULL, 1),
(13, 'btm', 6, NULL, NULL, NULL, 1),
(14, 'madiwala', NULL, 1, 3, NULL, 1),
(15, 'jakkasandra', NULL, 2, 3, NULL, 1),
(16, 'victoria layout', NULL, 1, 3, NULL, 1),
(17, 'jayanagar', NULL, 1, 3, NULL, 1),
(18, 'bellandur', NULL, 1, 2, NULL, 0),
(19, 'banashankari', NULL, 1, 3, NULL, 1),
(20, 'sarjapur', NULL, 1, 3, NULL, 1),
(22, 'j p nagar', NULL, 1, 3, NULL, 1),
(23, 'mg road', NULL, 1, 3, 26, 1),
(24, 'trinity circle', NULL, 1, 3, NULL, 1),
(26, 'ashok nagar', NULL, 1, 3, NULL, 1),
(27, 'shanthala nagar', NULL, 1, 3, NULL, 1),
(28, 'craig park layout', NULL, 1, 3, 26, 1),
(29, 'craig park layout', NULL, 1, 3, 26, 1),
(30, 'yellappa chetty layout', NULL, 1, 3, 26, 1),
(31, 'mahatama gandhi road', NULL, 1, 3, 26, 1),
(32, 'mahatma gandhi road', NULL, 1, 3, 26, 1),
(33, 'church street', NULL, 1, 3, 26, 1),
(34, 'st marks rd', NULL, 1, 3, 26, 1),
(35, 'st. marks road', NULL, 1, 3, 26, 1),
(36, 'vittal mallya road', NULL, 1, 3, 26, 1),
(37, 'kasturba cross road', NULL, 1, 3, 26, 1),
(38, 'residency road', NULL, 1, 3, 26, 1),
(39, 'richmond road', NULL, 1, 3, 26, 1),
(40, 'brigade road', NULL, 1, 3, 26, 1),
(41, 'magrath road', NULL, 1, 3, 26, 1),
(42, 'brunton cross road', NULL, 1, 3, 26, 1),
(43, 'sadduguntepalya', NULL, 1, 3, 0, 1),
(44, 'cambridge layout', NULL, 1, 3, NULL, 1),
(45, 'kasturi nagar', NULL, 1, 4, NULL, 1),
(50, 'kaikondrahalli', NULL, 1, 3, NULL, 1),
(51, 'benniganahalli', NULL, 1, 4, NULL, 1),
(52, 'bennigana halli', NULL, 1, 4, NULL, 1),
(53, 'kasturi nagar', NULL, 1, 4, NULL, 1),
(54, 'kasthuri nagar', NULL, 1, 4, NULL, 1),
(55, 'sadanandanagar', NULL, 1, 4, NULL, 1),
(56, 'sadananda nagar', NULL, 1, 4, NULL, 1),
(57, 'rmz infinity', NULL, 1, 4, NULL, 1),
(58, 'jaya nagar', NULL, 1, 3, NULL, 1),
(59, 'cv raman nagar', NULL, 1, 3, 61, 1),
(60, 'cv ramannagar', NULL, 1, 3, 61, 1),
(61, 'c v raman nagar', NULL, 1, 3, NULL, 1),
(62, 'c v ramannagar', NULL, 1, 3, 61, 1),
(63, 'c.v. raman nagar', NULL, 1, 3, 61, 1),
(64, 'padmanabhanagar', NULL, 2, 3, NULL, 1),
(65, 'bendre nagar', NULL, 2, 3, NULL, 1),
(66, 'ejipura', NULL, 1, 4, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `b2b_users`
--

CREATE TABLE IF NOT EXISTS `b2b_users` (
  `user_id` int(4) NOT NULL AUTO_INCREMENT,
  `email` varchar(200) DEFAULT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `book_id` varchar(100) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `organization` varchar(50) DEFAULT NULL,
  `address` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=65 ;


--
-- Table structure for table `bs_items`
--

CREATE TABLE IF NOT EXISTS `bs_items` (
  `item_id` int(6) NOT NULL,
  `genre1` varchar(200) DEFAULT NULL,
  `genre2` varchar(200) DEFAULT NULL,
  `genre3` varchar(200) DEFAULT NULL,
  `meta_description` text,
  `for_whom` varchar(1000) DEFAULT NULL,
  `read_by` varchar(1000) NOT NULL,
  `trivia` text,
  `amzn_link` varchar(1000) DEFAULT NULL,
  `amzn_delivery` varchar(200) DEFAULT NULL,
  `amzn_price` int(5) DEFAULT NULL,
  `fk_link` varchar(1000) DEFAULT NULL,
  `fk_delivery` varchar(200) DEFAULT NULL,
  `fk_price` int(5) DEFAULT NULL,
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `bs_items`
--

INSERT INTO `bs_items` (`item_id`, `genre1`, `genre2`, `genre3`, `meta_description`, `for_whom`, `read_by`, `trivia`, `amzn_link`, `amzn_delivery`, `amzn_price`, `fk_link`, `fk_delivery`, `fk_price`, `date_added`) VALUES
(3, 'Classic', 'Romance ', 'Fiction', 'This book is about love and offcourse Pride of a man and Prejudice of a woman. Read this book to fall in love with it. ', 'Classic lovers, romance lovers, Teens, females', 'Saroj Tagore, Shruthi Poonina, Aparajitha Sikhdar, Ben Moe ', '', 'http://www.amazon.in/gp/product/0007350775/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0007350775&linkCode=as2&tag=boosho08d-21', '7 Days', 159, 'http://www.flipkart.com/pride-and-prejudice/p/itme9u4wx2yezhad?pid=9780553213102&al=OMyB%2FxBKMz44hn6jAk%2BQ4sldugMWZuE7mxWx381qOwRt1Oi7FhyS7CyGhdkLCIx5%2FPSTX2xchf4%3D&ref=L%3A1134458255283209293&srno=p_3&otracker=from-search&affid=achalkoth', '9 Days', 349, '2016-06-29 07:31:06'),
(4, 'Classic', 'Memoir', 'Biography', 'A diary discovered decades later, belonging to a 13year old Jewish girl confined to a home trying to escape the Nazi attack. ', 'Teens, Females, non fiction lovers, ', 'Natalie Portman, Greg Chappel, Alex Sanchez ', 'More than 25 million copies of The Diary of Anne Frank have been sold worldwide. The heart-wrenching diary that chronicled the two years Anne’s family spent in hiding in the attic of a warehouse in Amsterdam, Holland, because they were Jewish during World War II, has been translated into more than 50 languages.', 'http://www.amazon.in/gp/product/8172345194/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=8172345194&linkCode=as2&tag=boosho08d-21', '4 Days', 128, 'http://www.flipkart.com/diary-young-girl-english/p/itmegtbhthuc3zq2?pid=9788172345198&al=PsjjfdqsMLwKxrwdNai%2BNcldugMWZuE7mxWx381qOwSsYG%2BMPy8xhsrfoxvVSASRtiAlSNYAAFU%3D&ref=L%3A952543390995727950&srno=p_1&findingMethod=Search&otracker=start&affid=achalkoth', '5 Days', 144, '2016-06-29 07:31:06'),
(16, 'Fiction', 'Classic', '', 'This fiction set in the Nazi Germany is an unforgettable story of a girl and her books during the toughest of times. ', 'Fiction lover, Historic book reader, ', 'Samyak Hariskrishnan,Yashika Sachdeva, Dharmendra Malini, Murkund', '', 'http://www.amazon.in/gp/product/0552773891/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0552773891&linkCode=as2&tag=boosho08d-21', '4 Days', 399, 'http://www.flipkart.com/book-thief-english/p/itmegmtfeyvcpxdu?q=The+Book+Thief+%28English%29&as=on&as-show=on&otracker=start&as-pos=p_1_book+thi&pid=9780552773898&affid=achalkoth', '5 Days ', 332, '2016-06-29 07:31:06'),
(37, 'Classic', 'Fantasy', 'Spirituality', 'This book will inspire you in the most simple and yet most effective manner to follow your dreams. ', 'Young Readers, Adventure seekers, Looking for inspiration', 'Will Smith, Mellody Hobson,Deepanshu Jain, Monika Shrimal', '', 'http://www.amazon.in/gp/product/8172234988/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=8172234988&linkCode=as2&tag=boosho08d-21', '4 Days', 149, 'http://www.flipkart.com/the-alchemist/p/itme9xh8anaz78eg?pid=9780007155668&al=OMyB%2FxBKMz4OdV2E73OaQMldugMWZuE7mxWx381qOwRypXOL54IydfZf4FWH2nRUV0tEG5NHyLc%3D&ref=L%3A-20662867361708747&srno=p_1&findingMethod=Search&otracker=start&affid=achalkoth', '7 Days', 200, '2016-06-29 07:31:06'),
(71, 'Classic', 'Philosophy', 'Fiction', 'A man and his fight with himself and the society and the eventual triumph of human will and objectivity. Love it or hate it but you have to read it. ', 'Classic lovers, fiction lovers, bulky books readers,', 'Sir Michael Caine', '', 'http://www.amazon.in/gp/product/0965032191/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0965032191&linkCode=as2&tag=boosho08d-21', '4 Days', 399, 'http://www.flipkart.com/the-fountainhead/p/itmej3hshugfc5gg?pid=9780451191151&ref=L%3A2647998330804391597&srno=p_2&otracker=from-search&al=PsjjfdqsMLzhpn8GBGbon8ldugMWZuE7mxWx381qOwT97LboiYFHwnZT6GUmOWI6BSHNKNggbRw%3D&affid=achalkoth', '7 Days', 465, '2016-06-29 07:31:06'),
(143, 'Fiction', 'India', 'Adventure', 'Book can be a memoir, adventure, philosophical, romantic and fiction. This one is all of them.', 'Hardcore fiction lover, philosophical, can read bulky books', 'Misty Copeland,Jimmy Lai, VInita Ganguly, Pawan Sharma, Parul Negi', '', 'http://www.amazon.in/gp/product/0349117543/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0349117543&linkCode=as2&tag=boosho08d-21', '4 Days', 382, 'http://www.flipkart.com/shantaram-english/p/itmegmtffrg2456z?pid=9780349117546&al=PsjjfdqsMLzfg8Hn9pGwvcldugMWZuE7mxWx381qOwTlRBYGvy0lbmrPAuFphr6XiEhdNmk4HCg%3D&ref=L%3A-7702853509391366947&srno=p_1&otracker=from-search&affid=achalkoth', '8 Days', 419, '2016-06-29 07:31:06'),
(305, 'Autobiography', 'India', 'Inspirational', 'Journey of a son of boat owner to one of the best defense engineers and visionary of India. President Kalam''s biographical account', 'Entrepreneurs, changemakers, leaders, students', 'Achal Kothari, Malvika Joshi, Sanchi Shukla, Harshvardhan mittal', '', 'http://www.amazon.in/gp/product/8173711461/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=8173711461&linkCode=as2&tag=boosho08d-21', '4 Days', 162, 'http://www.flipkart.com/wings-fire-autobiography-english-1st/p/itmdyu8fezqmmvhe?pid=9788173711466&al=OMyB%2FxBKMz6%2BcpX7Wmwup8ldugMWZuE7mxWx381qOwSsYG%2BMPy8xhpPDKZuX9GPBR%2Foqi8WHuEs%3D&ref=L%3A-2901841234430050006&srno=p_3&otracker=from-search&affid=achalkoth', '7 Days', 96, '2016-06-29 07:31:06'),
(504, 'History', 'India', 'Politics', 'A political account of India and the major events shaping the subcontinent after independence. ', 'Interested in politics, Indian history,  ', 'Kanye West,Vikram Pandit, Shreya Gupta, Tilak Dhadda, Anuja PAndit', '', 'http://www.amazon.in/gp/product/0330505548/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0330505548&linkCode=as2&tag=boosho08d-21', '4 Days', 444, 'http://www.flipkart.com/india-after-gandhi-history-worlds-largest-democracy-english/p/itmegtbh4qzdyx8r?pid=9780330505543&ref=L%3A-5213897795200139057&srno=p_2&otracker=from-search&al=PsjjfdqsMLzdZWJzDRbF3cldugMWZuE7mxWx381qOwQ8diGDjv%2Be7FWtrtIBFjAWLMKsww3JA5c%3D&affid=achalkoth', '8 Days', 525, '2016-06-29 07:31:06'),
(796, 'Fantasy', 'Fiction', 'Epic', 'A gripping tale of action, thriller and blood with so many twists and turns leaving the reader only wishing for more. ', '', 'Anant Gupta, Robin Uthappa, Anita SArkeesian, Sharad D''suza', '', 'http://www.amazon.in/gp/product/0007428545/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0007428545&linkCode=as2&tag=boosho08d-21', '4 Days', 289, 'http://www.flipkart.com/game-of-thrones/p/itme9xmhh8knh2f3?pid=9780007428540&al=OMyB%2FxBKMz5M6730RoWBPMldugMWZuE7mxWx381qOwRypXOL54IydT3%2BLh%2BzZNXD9toDcjBbHUc%3D&ref=L%3A-4297777822218171226&srno=p_1&otracker=from-multi&affid=achalkoth', '3 Days', 357, '2016-06-29 07:31:06'),
(2132, 'Fantasy', 'Young Adult', 'Adventure', 'Now is the time to enter in the realm of magic', 'ficiton lover, magicians', 'Wayne Rooney, Roopesh Chuggani, Smriti Mahale', '', 'http://www.amazon.in/gp/product/1408855658/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=1408855658&linkCode=as2&tag=boosho08d-21', '7 Days', 399, 'http://www.flipkart.com/harry-potter-philosopher-s-stone-english/p/itme99sf4gd9rged?pid=9781408855652&al=PsjjfdqsMLzHYBWXP4EMYsldugMWZuE7mxWx381qOwRgFBPnvi05xQhDOHG%2BbHFCvZcLivyFFTg%3D&ref=L%3A-8719891111204728910&srno=p_9&findingMethod=Search&otracker=start&affid=achalkoth', '3 Days', 314, '2016-06-29 07:31:06'),
(2521, 'Fantasy', 'Cultural', 'Japanese Literature', 'A coming-of-age story that raises many questions about concepts such as good and evil, reality, time, and memory.', 'Fantasy lovers, Fiction lovers, Japanese culture enthusiasts', 'Yen Finshao, George Tiffiny, Marvin Attapattu ', '', 'http://www.amazon.in/gp/product/0099458322/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0099458322&linkCode=as2&tag=boosho08d-21', '4 Days', 277, 'http://www.flipkart.com/kafka-on-the-shore/p/itme9xrxrfvfqk9x?pid=9780099458326&al=OMyB%2FxBKMz6kSd%2Bw1wjC4MldugMWZuE7mxWx381qOwQ%2FrxqZxymvlh9WdC3eeA7utG%2Bj52N8h5E%3D&ref=L%3A-5641843926385080481&srno=p_1&otracker=from-search&affid=achalkoth', '5 days ', 349, '2016-06-29 07:31:06'),
(3387, 'Business', 'Entreprenuership', 'Management', 'Practical wisdom that is often counter intuitive, communicated so concisely and clearly in the book. ', 'Entrepreneurs, changemakers, leaders, students', 'Anant Gupta, Nikhil Chinnippa, Susy Matthew', '', 'http://www.amazon.in/gp/product/0091929784/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0091929784&linkCode=as2&tag=boosho08d-21', '4 Days', 429, 'http://www.flipkart.com/rework/p/itme9xqsc3srbqw9?pid=9780091929787&al=OMyB%2FxBKMz4dTMTUQ1wYRsldugMWZuE7mxWx381qOwQ%2FrxqZxymvlsWhBoWWEN2LSC6NiM0b8gw%3D&ref=L%3A7639103028620510483&srno=p_1&findingMethod=Search&otracker=start&affid=achalkoth', '5 Days', 455, '2016-06-29 07:31:06'),
(3682, 'Philosophy', 'History', 'Non fiction', 'Perhaps one of the most influential book on strategy. Conflict cant be avoided but managed. ', 'Leaders, politicians, managers, decision makers, people interested in politics, war, history and culture', 'Neelangana Noopur, Sharath Shrinivasna , Charles Hooper', '', 'http://www.amazon.in/gp/product/8184950888/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=8184950888&linkCode=as2&tag=boosho08d-21', '4 Days', 187, 'http://www.flipkart.com/art-war-english/p/itmegtbmyv7r6z24?pid=9788189497422&al=PsjjfdqsMLxL2AL09l2Y78ldugMWZuE7mxWx381qOwQI5ApZ7o5M2w8tGkj%2B%2BjEL5Jl1cbQ54lk%3D&ref=L%3A-450930594775545746&srno=p_1&findingMethod=Search&otracker=start&affid=achalkoth', '7 Days', 215, '2016-06-29 07:31:06'),
(3761, 'Business', 'Leadership', 'Self Help', 'Read this book to know what makes a person leader and then reread to become a leader. ', 'Changemakers, leaders, entrepreneurs', 'Divyank jain, Bengamin Frank, Sonia Chattopadhiyay', '', 'http://www.amazon.in/gp/product/1471131823/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=1471131823&linkCode=as2&tag=boosho08d-21', '3 Days', 170, 'http://www.flipkart.com/7-habits-highly-effective-people/p/itme9uyq9ckzfqwc?pid=9781451639612&al=PsjjfdqsMLxaCFZpPIG8AcldugMWZuE7mxWx381qOwREnhTJuYO6OR9GYkj1YnRQRhh7I%2Fz4Pkg%3D&ref=L%3A-3367927036144236157&srno=p_1&findingMethod=Search&otracker=start&affid=achalkoth', '7 Days', 197, '2016-06-29 07:31:06'),
(4051, 'Entrepreneurship', 'Business', 'Management', 'Classic read for anyone who wants to do a startup or is already running one', 'Entrepreneurs, changemakers, leaders, students', 'Peter Thiel, Tarun Mehta, Sachin Bansal', '', 'http://www.amazon.in/gp/product/0007350775/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0007350775&linkCode=as2&tag=boosho08d-21', '7 Days', 159, 'http://www.flipkart.com/pride-and-prejudice/p/itme9u4wx2yezhad?pid=9780553213102&al=OMyB%2FxBKMz44hn6jAk%2BQ4sldugMWZuE7mxWx381qOwRt1Oi7FhyS7CyGhdkLCIx5%2FPSTX2xchf4%3D&ref=L%3A1134458255283209293&srno=p_3&otracker=from-search&affid=achalkoth', '9 Days', 349, '2016-06-29 07:34:11'),
(4648, 'Entrepreneurship', 'Business', 'Management', 'Entrepreneurs who want to build the next Microsoft or Google or Facebook. ', 'Entrepreneurs, changemakers, leaders, students', 'Elon Musk, Sam Altman, Marc Andresseen, Jon Stark ', '', 'http://www.amazon.in/gp/product/0753555190/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0753555190&linkCode=as2&tag=boosho08d-21', '4 Days', 259, 'http://www.flipkart.com/zero-one-notes-start-ups-build-future-english/p/itmegmt2gzftkyht?pid=9780753555194&al=OMyB%2FxBKMz6psIYrV16x5sldugMWZuE7mxWx381qOwTTl5Dq00dx%2BoaRM%2BbIBN0MiJF%2Bwq%2BPv4c%3D&ref=L%3A7849176525323258399&srno=p_1&findingMethod=Search&otracker=start&affid=achalkoth', '3 Days', 365, '2016-06-29 07:31:06'),
(4650, '', '', '', 'Now is the time to enter in the realm of magic', 'ficiton lover, magicians', 'Wayne Rooney', '', 'http://www.amazon.in/Harry-Potter-Philosophers-Stone-Rowling/dp/1408855658', NULL, NULL, 'http://www.flipkart.com/harry-potter-philosopher-s-stone-english/p/itme99sf4gd9rged?pid=9781408855652&al=PsjjfdqsMLzHYBWXP4EMYsldugMWZuE7mxWx381qOwRgFBPnvi05xQhDOHG%2BbHFCvZcLivyFFTg%3D&ref=L%3A-8719891111204728910&srno=p_9&findingMethod=Search&otracker=start', '9 days', 339, '2016-06-29 07:31:06'),
(4725, 'Classic', 'Mystery', 'Detective', 'Love Sherlock? This is the set for you. From "Study in Scarlet" to "The Hound Of Baskervilles" this has it all.', 'Curious, suspense lovers,  ', 'Sahil Dave, Rishabh Agnihotri, John Right, Anil Kumble, Mohit Chouhan', 'Professor Moriarity was Sherlock Holmes'' archenemy.', 'http://www.amazon.in/gp/product/0553328255/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0553328255&linkCode=as2&tag=boosho08d-21', '4 Days', 357, 'http://www.flipkart.com/sherlock-holmes-complete-novels-stories-volume/p/itme9zrhczh6r34u?pid=9780553212419&al=PsjjfdqsMLwk38rOsijeosldugMWZuE7mxWx381qOwRt1Oi7FhyS7IhT2YPYqmZxCdBeGId%2FJ5k%3D&ref=L%3A2913357124741582221&srno=p_9&findingMethod=Search&otracker=start&affid=achalkoth', '5 Days ', 249, '2016-06-29 07:31:06'),
(11719, 'Business ', 'Management', 'Leadership', 'A book and an author, who have inspired hundreds of entrepreneurs. ', 'Entrepreneurs, changemakers, leaders, students', 'Ben Horowitz,Magnus MacFarlane-Barrow,Martin Blaser', '', 'http://www.amazon.in/gp/product/0679762884/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0679762884&linkCode=as2&tag=boosho08d-21', '4 Days', 462, 'http://www.flipkart.com/high-output-management-english/p/itmczyyxzmxrgzqg?pid=9780679762881&al=OMyB%2FxBKMz6yfoNhIJ9Hh8ldugMWZuE7mxWx381qOwTfw2BdFcUcrPJUzE6tyvS30H%2B%2Fp0MbVls%3D&ref=L%3A-5899599287441407426&srno=p_1&findingMethod=Search&otracker=start&affid=achalkoth', '4 Days', 961, '2016-06-29 07:31:06'),
(18406, 'Leadership', 'Management', 'Entrepreneurship', 'Good is the enemy of great! A critical account of what makes a company leap from being good or at times falling to become great. ', 'Entrepreneurs, CEOs, Senior managers', 'Jeff Bezos, Achal Kothari, Chriss Pratt, Neomi Devshish', '', 'http://www.amazon.in/gp/product/0712676090/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=0712676090&linkCode=as2&tag=boosho08d-21', '4 Days', 466, 'http://www.flipkart.com/good-great-english/p/itmegmt2cnujtmxz?pid=9780712676090&al=PsjjfdqsMLyRDsvU2D%2FeNsldugMWZuE7mxWx381qOwTPhiFLT71VZAbb%2B75tTn32uQF%2BvbL3SKM%3D&ref=L%3A-1602769414412350551&srno=p_1&otracker=from-search&affid=achalkoth', '8 Days', 629, '2016-06-29 07:31:06'),
(18550, 'Contemporary', 'Autobiography', 'Life', 'A person in pursuit of the larger questions of life and death, becomes a doctor and then a patient. Did he understand life well? Read to know. ', 'Doctors, medical professionals, people interested in higher questions of life and death ', 'Achal Kothari, John taker, Michal Snider ', '', 'http://www.amazon.in/gp/product/1847923674/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&camp=3626&creative=24790&creativeASIN=1847923674&linkCode=as2&tag=boosho08d-21', '5 Days', 388, 'http://www.flipkart.com/breath-becomes-air-english/p/itmeevavfhksghze?pid=9781847923677&al=PsjjfdqsMLxJQnaL0cU%2F5cldugMWZuE7mxWx381qOwSjJCBJ%2F2QOsSQOMuBaQiaz%2FR5T5Pu72BY%3D&ref=L%3A-6305912185953237230&srno=p_1&findingMethod=Search&otracker=start&affid=achalkoth', '8 Days', 419, '2016-06-29 07:31:06');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE IF NOT EXISTS `categories` (
  `category_id` int(6) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) DEFAULT NULL,
  `slug_url` varchar(50) DEFAULT NULL,
  `books` int(10) DEFAULT NULL,
  `web_display` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=857 ;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category_id`, `category_name`, `slug_url`, `books`, `web_display`) VALUES
(1, '10th Century', '10th-century', 1330, 0),
(2, '11th Century', '11th-century', 2551, 0),
(3, '12th Century', '12th-century', 4108, 0),
(4, '13th Century', '13th-century', 3395, 0),
(5, '14th Century', '14th-century', 6913, 0),
(6, '15th Century', '15th-century', 8331, 0),
(7, '16th Century', '16th-century', 21233, 0),
(8, '17th Century', '17th-century', 22741, 0),
(9, '18th Century', '18th-century', 39288, 0),
(10, '19th Century', '19th-century', 155362, 0),
(11, '1st Grade', '1st-grade', 21894, 0),
(12, '20th Century', '20th-century', 316464, 0),
(13, '21st Century', '21st-century', 195208, 0),
(14, '2nd Grade', '2nd-grade', 22173, 0),
(15, '40k', '40k', 4487, 0),
(16, 'Abuse', 'abuse', 169136, 0),
(17, 'Academia', 'academia', 60584, 0),
(18, 'Academic', 'academic', 142878, 0),
(19, 'Academics', 'academics', 21282, 0),
(20, 'Action', 'action', 355372, 1),
(21, 'Activism', 'activism', 16759, 0),
(22, 'Adaptations', 'adaptations', 22945, 0),
(23, 'Adolescence', 'adolescence', 52848, 0),
(24, 'Adoption', 'adoption', 25832, 0),
(25, 'Adult', 'adult', 1173964, 0),
(26, 'Adult Fiction', 'adult-fiction', 588218, 0),
(27, 'Adventure', 'adventure', 830952, 0),
(28, 'Adventurers', 'adventurers', 4044, 0),
(29, 'Africa', 'africa', 98553, 0),
(30, 'African American', 'african-american', 56729, 0),
(31, 'African American Literature', 'african-american-literature', 8577, 0),
(32, 'African American Romance', 'african-american-romance', 7563, 0),
(33, 'African Literature', 'african-literature', 10502, 0),
(34, 'Agriculture', 'agriculture', 8350, 0),
(35, 'Albanian Literature', 'albanian-literature', 981, 0),
(36, 'Alchemy', 'alchemy', 11067, 0),
(37, 'Alcohol', 'alcohol', 8813, 0),
(38, 'Algorithms', 'algorithms', 1863, 0),
(39, 'Aliens', 'aliens', 91380, 0),
(40, 'Alternate History', 'alternate-history', 72369, 0),
(41, 'Alternate Universe', 'alternate-universe', 38845, 0),
(42, 'Amateur Sleuth', 'amateur-sleuth', 8496, 0),
(43, 'American', 'american', 326968, 0),
(44, 'American Civil War', 'american-civil-war', 12965, 0),
(45, 'American Classics', 'american-classics', 38820, 0),
(46, 'American Fiction', 'american-fiction', 69055, 0),
(47, 'American History', 'american-history', 107958, 0),
(48, 'American Novels', 'american-novels', 20039, 0),
(49, 'Americana', 'americana', 77516, 0),
(50, 'Amish', 'amish', 29320, 0),
(51, 'Amish Fiction', 'amish-fiction', 8119, 0),
(52, 'Ancient', 'ancient', 35538, 0),
(53, 'Angels', 'angels', 132500, 0),
(54, 'Angola', 'angola', 1302, 0),
(55, 'Animal Fiction', 'animal-fiction', 14344, 0),
(56, 'Animals', 'animals', 269185, 0),
(57, 'Anime', 'anime', 28029, 0),
(58, 'Anthologies', 'anthologies', 101941, 0),
(59, 'Anthropology', 'anthropology', 78509, 0),
(60, 'Anthropomorphic', 'anthropomorphic', 12456, 0),
(61, 'Anti Racist', 'anti-racist', 1060, 0),
(62, 'Apocalyptic', 'apocalyptic', 71775, 0),
(63, 'Archeology', 'archeology', 5934, 0),
(64, 'Architecture', 'architecture', 44417, 0),
(65, 'Art', 'art', 322787, 0),
(66, 'Art And Photography', 'art-and-photography', 4498, 0),
(67, 'Art Books Monographs', 'art-books-monographs', 449, 0),
(68, 'Art Design', 'art-design', 11553, 0),
(69, 'Art History', 'art-history', 29982, 0),
(70, 'Arthurian', 'arthurian', 16021, 0),
(71, 'Asia', 'asia', 90770, 0),
(72, 'Asian Literature', 'asian-literature', 22747, 0),
(73, 'Astrology', 'astrology', 11145, 0),
(74, 'Astronomy', 'astronomy', 15098, 0),
(75, 'Atheism', 'atheism', 24321, 0),
(76, 'Australia', 'australia', 46850, 0),
(77, 'Autobiography', 'autobiography', 146231, 1),
(78, 'Babylon 5', 'babylon-5', 1445, 0),
(79, 'Back To School', 'back-to-school', 12747, 0),
(80, 'Bande DessinéE', 'bande-dessin%C3%A9e', 13830, 0),
(81, 'Bangladesh', 'bangladesh', 2936, 0),
(82, 'Banned Books', 'banned-books', 59112, 0),
(83, 'Baseball', 'baseball', 27042, 0),
(84, 'Basketball', 'basketball', 4641, 0),
(85, 'Batman', 'batman', 29351, 0),
(86, 'Battle Of Gettysburg', 'battle-of-gettysburg', 631, 0),
(87, 'Bdsm', 'bdsm', 272060, 0),
(88, 'Beading', 'beading', 1826, 0),
(89, 'Beauty And The Beast', 'beauty-and-the-beast', 10951, 0),
(90, 'Beer', 'beer', 4465, 0),
(91, 'Belgian', 'belgian', 3252, 0),
(92, 'Belgium', 'belgium', 7608, 0),
(93, 'Beverages', 'beverages', 948, 0),
(94, 'Biblical', 'biblical', 18858, 0),
(95, 'Biblical Fiction', 'biblical-fiction', 7901, 0),
(96, 'Biography', 'biography', 680203, 0),
(97, 'Biography Memoir', 'biography-memoir', 133655, 0),
(98, 'Biology', 'biology', 41964, 0),
(99, 'Bird Watching', 'bird-watching', 580, 0),
(100, 'Birds', 'birds', 21351, 0),
(101, 'Bisexual', 'bisexual', 9990, 0),
(102, 'Bizarro Fiction', 'bizarro-fiction', 2199, 0),
(103, 'Black Literature', 'black-literature', 3364, 0),
(104, 'Boarding School', 'boarding-school', 26398, 0),
(105, 'Bolivia', 'bolivia', 938, 0),
(106, 'Books About Books', 'books-about-books', 79672, 0),
(107, 'Booze', 'booze', 1854, 0),
(108, 'Boys Love', 'boys-love', 3970, 0),
(109, 'Brain', 'brain', 18094, 0),
(110, 'Brazil', 'brazil', 8754, 0),
(111, 'Brewing', 'brewing', 1584, 0),
(112, 'British Literature', 'british-literature', 133416, 0),
(113, 'Buddhism', 'buddhism', 44818, 0),
(114, 'Buffy The Vampire Slayer', 'buffy-the-vampire-slayer', 3986, 0),
(115, 'Bulgaria', 'bulgaria', 2071, 0),
(116, 'Bulgarian Literature', 'bulgarian-literature', 2187, 0),
(117, 'Business', 'business', 280998, 0),
(118, 'Butch Femme', 'butch-femme', 734, 0),
(119, 'Campus', 'campus', 3741, 0),
(120, 'Canada', 'canada', 51548, 0),
(121, 'Canadian Literature', 'canadian-literature', 15104, 0),
(122, 'Canon', 'canon', 108769, 0),
(123, 'Cartography', 'cartography', 2359, 0),
(124, 'Cartoon', 'cartoon', 7288, 0),
(125, 'Category Romance', 'category-romance', 27699, 0),
(126, 'Catholic', 'catholic', 34367, 0),
(127, 'Cats', 'cats', 44793, 0),
(128, 'Challenged Books', 'challenged-books', 7282, 0),
(129, 'Chancellorsville Campaign', 'chancellorsville-campaign', 11, 0),
(130, 'Chapter Books', 'chapter-books', 97355, 0),
(131, 'Chemistry', 'chemistry', 15706, 0),
(132, 'Chess', 'chess', 12331, 0),
(133, 'Chick Lit', 'chick-lit', 637805, 0),
(134, 'Children', 'children', 691091, 1),
(135, 'Childrens Classics', 'childrens-classics', 30822, 0),
(136, 'China', 'china', 63096, 0),
(137, 'Chinese Literature', 'chinese-literature', 7642, 0),
(138, 'Choose Your Own Adventure', 'choose-your-own-adventure', 3183, 0),
(139, 'Christian', 'christian', 570497, 0),
(140, 'Christian Contemporary Fiction', 'christian-contemporary-fiction', 2159, 0),
(141, 'Christian Fiction', 'christian-fiction', 206076, 0),
(142, 'Christian Historical Fiction', 'christian-historical-fiction', 11200, 0),
(143, 'Christian Non Fiction', 'christian-non-fiction', 31069, 0),
(144, 'Christian Romance', 'christian-romance', 28941, 0),
(145, 'Christian Romance Historical', 'christian-romance-historical', 855, 0),
(146, 'Christianity', 'christianity', 132617, 0),
(147, 'Christmas', 'christmas', 169025, 0),
(148, 'Church', 'church', 37837, 0),
(149, 'Church History', 'church-history', 15667, 0),
(150, 'Cinderella', 'cinderella', 6514, 0),
(151, 'Cities', 'cities', 17384, 0),
(152, 'Civil War', 'civil-war', 42769, 0),
(153, 'Civil War Eastern Theater', 'civil-war-eastern-theater', 221, 0),
(154, 'Civil War History', 'civil-war-history', 2420, 0),
(155, 'Civil War Western Theater', 'civil-war-western-theater', 78, 0),
(156, 'Class', 'class', 83667, 0),
(157, 'Class Issues', 'class-issues', 10273, 0),
(158, 'Classic Literature', 'classic-literature', 155001, 0),
(159, 'Classical Music', 'classical-music', 2198, 0),
(160, 'Classical Studies', 'classical-studies', 15291, 0),
(161, 'Classics', 'classics', 2026188, 1),
(162, 'Clean Romance', 'clean-romance', 39058, 0),
(163, 'Climate Change', 'climate-change', 4054, 0),
(164, 'Climbing', 'climbing', 3297, 0),
(165, 'Cocktails', 'cocktails', 1113, 0),
(166, 'Coding', 'coding', 4221, 0),
(167, 'Collections', 'collections', 109041, 0),
(168, 'College', 'college', 263289, 0),
(169, 'Comedy', 'comedy', 241033, 0),
(170, 'Comic Book', 'comic-book', 32338, 0),
(171, 'Comic Strips', 'comic-strips', 8380, 0),
(172, 'Comics', 'comics', 1014624, 1),
(173, 'Comics Manga', 'comics-manga', 46461, 0),
(174, 'Coming Of Age', 'coming-of-age', 234866, 0),
(175, 'Comix', 'comix', 33014, 0),
(176, 'Communication', 'communication', 22341, 0),
(177, 'Computer Reference', 'computer-reference', 954, 0),
(178, 'Computer Science', 'computer-science', 28027, 0),
(179, 'Computers', 'computers', 29933, 0),
(180, 'Contemporary', 'contemporary', 1853731, 0),
(181, 'Contemporary Romance', 'contemporary-romance', 755769, 0),
(182, 'Cookbooks', 'cookbooks', 225920, 0),
(183, 'Cooking', 'cooking', 118902, 0),
(184, 'Counter Culture', 'counter-culture', 5784, 0),
(185, 'Cozy Mystery', 'cozy-mystery', 117052, 0),
(186, 'Crafts', 'crafts', 36664, 0),
(187, 'Crafty', 'crafty', 7032, 0),
(188, 'Crime', 'crime', 639977, 0),
(189, 'Criticism', 'criticism', 85132, 0),
(190, 'Crochet', 'crochet', 7533, 0),
(191, 'Cross Dressing', 'cross-dressing', 5114, 0),
(192, 'Cthulhu Mythos', 'cthulhu-mythos', 3423, 0),
(193, 'Cuisine', 'cuisine', 3797, 0),
(194, 'Culinary', 'culinary', 14513, 0),
(195, 'Cult Classics', 'cult-classics', 16508, 0),
(196, 'Cults', 'cults', 7896, 0),
(197, 'Cultural', 'cultural', 137738, 0),
(198, 'Cultural Studies', 'cultural-studies', 46175, 0),
(199, 'Culture', 'culture', 178558, 0),
(200, 'Cyberpunk', 'cyberpunk', 31514, 0),
(201, 'Cycling', 'cycling', 5177, 0),
(202, 'Czech Literature', 'czech-literature', 6047, 0),
(203, 'Danish', 'danish', 31183, 0),
(204, 'Dark', 'dark', 282638, 0),
(205, 'Dark Fantasy', 'dark-fantasy', 80486, 0),
(206, 'Dc Comics', 'dc-comics', 29860, 0),
(207, 'Death', 'death', 210360, 0),
(208, 'Demons', 'demons', 130852, 0),
(209, 'Denmark', 'denmark', 6766, 0),
(210, 'Design', 'design', 61416, 0),
(211, 'Detective', 'detective', 170306, 0),
(212, 'Diary', 'diary', 17599, 0),
(213, 'Dictionaries', 'dictionaries', 5800, 0),
(214, 'Diets', 'diets', 1273, 0),
(215, 'Dinosaurs', 'dinosaurs', 9935, 0),
(216, 'Disability', 'disability', 46832, 0),
(217, 'Disability Studies', 'disability-studies', 2505, 0),
(218, 'Disabled Communities', 'disabled-communities', 705, 0),
(219, 'Disease', 'disease', 12567, 0),
(220, 'Divination', 'divination', 3483, 0),
(221, 'Doctor Who', 'doctor-who', 57757, 0),
(222, 'Dogs', 'dogs', 54867, 0),
(223, 'Drag', 'drag', 1497, 0),
(224, 'Dragonlance', 'dragonlance', 16311, 0),
(225, 'Dragons', 'dragons', 113663, 0),
(226, 'Drama', 'drama', 581238, 0),
(227, 'Drawing', 'drawing', 8070, 0),
(228, 'Drinking', 'drinking', 4385, 0),
(229, 'Dungeons And Dragons', 'dungeons-and-dragons', 8054, 0),
(230, 'Dungeons And Dragons Manuals', 'dungeons-and-dragons-manuals', 449, 0),
(231, 'Dutch Literature', 'dutch-literature', 13034, 0),
(232, 'Dying Earth', 'dying-earth', 1566, 0),
(233, 'Dystopia', 'dystopia', 432951, 0),
(234, 'Eastern Philosophy', 'eastern-philosophy', 8291, 0),
(235, 'Ecology', 'ecology', 16878, 0),
(236, 'Economics', 'economics', 138009, 0),
(237, 'Education', 'education', 188844, 0),
(238, 'Egypt', 'egypt', 27052, 0),
(239, 'Egyptian Literature', 'egyptian-literature', 1359, 0),
(240, 'Engineering', 'engineering', 23358, 0),
(241, 'English Literature', 'english-literature', 123109, 0),
(242, 'Environment', 'environment', 46920, 0),
(243, 'Epic', 'epic', 147868, 0),
(244, 'Epic Fantasy', 'epic-fantasy', 131077, 0),
(245, 'Epic Poetry', 'epic-poetry', 8336, 0),
(246, 'Erotic Historical Romance', 'erotic-historical-romance', 2166, 0),
(247, 'Erotic Horror', 'erotic-horror', 1536, 0),
(248, 'Erotic Paranormal Romance', 'erotic-paranormal-romance', 3035, 0),
(249, 'Erotic Romance', 'erotic-romance', 184090, 0),
(250, 'Erotica', 'erotica', 617566, 0),
(251, 'Esoterica', 'esoterica', 7360, 0),
(252, 'Esp', 'esp', 11205, 0),
(253, 'Espionage', 'espionage', 72415, 0),
(254, 'Essays', 'essays', 160652, 0),
(255, 'Ethnic', 'ethnic', 13465, 0),
(256, 'Ethnic Studies', 'ethnic-studies', 5295, 0),
(257, 'Ethnicity', 'ethnicity', 2295, 0),
(258, 'European History', 'european-history', 53933, 0),
(259, 'European Literature', 'european-literature', 85161, 0),
(260, 'Evolution', 'evolution', 23106, 0),
(261, 'F M F', 'f-m-f', 957, 0),
(262, 'Fables', 'fables', 20402, 0),
(263, 'Fae', 'fae', 65441, 0),
(264, 'Fairies', 'fairies', 51923, 0),
(265, 'Fairy Tale Retellings', 'fairy-tale-retellings', 27305, 0),
(266, 'Fairy Tales', 'fairy-tales', 148951, 0),
(267, 'Faith', 'faith', 100375, 0),
(268, 'Family', 'family', 395840, 0),
(269, 'Fandom', 'fandom', 16029, 0),
(270, 'Fantasy', 'fantasy', 5203307, 0),
(271, 'Fantasy Of Manners', 'fantasy-of-manners', 2702, 0),
(272, 'Fantasy Romance', 'fantasy-romance', 67976, 0),
(273, 'Fat', 'fat', 1933, 0),
(274, 'Fat Acceptance', 'fat-acceptance', 810, 0),
(275, 'Fat Studies', 'fat-studies', 920, 0),
(276, 'Feminism', 'feminism', 153798, 0),
(277, 'Feminist Studies', 'feminist-studies', 4513, 0),
(278, 'Feminist Theory', 'feminist-theory', 5347, 0),
(279, 'Femslash', 'femslash', 601, 0),
(280, 'Fiction', 'fiction', 5704559, 1),
(281, 'Field Guides', 'field-guides', 2797, 0),
(282, 'Figure Skating', 'figure-skating', 1007, 0),
(283, 'Film', 'film', 103983, 0),
(284, 'Finnish Literature', 'finnish-literature', 6933, 0),
(285, 'Fitness', 'fitness', 19902, 0),
(286, 'Flash Fiction', 'flash-fiction', 1521, 0),
(287, 'Folk Tales', 'folk-tales', 11726, 0),
(288, 'Folklore', 'folklore', 62744, 0),
(289, 'Food', 'food', 153131, 0),
(290, 'Food And Drink', 'food-and-drink', 20731, 0),
(291, 'Food And Wine', 'food-and-wine', 4825, 0),
(292, 'Food History', 'food-history', 2959, 0),
(293, 'Food Writing', 'food-writing', 7788, 0),
(294, 'Foodie', 'foodie', 17854, 0),
(295, 'Football', 'football', 16188, 0),
(296, 'Forgotten Realms', 'forgotten-realms', 24405, 0),
(297, 'Fractured Fairy Tales', 'fractured-fairy-tales', 5757, 0),
(298, 'France', 'france', 129388, 0),
(299, 'French Literature', 'french-literature', 59387, 0),
(300, 'French Revolution', 'french-revolution', 7165, 0),
(301, 'Frugal', 'frugal', 750, 0),
(302, 'Funnies', 'funnies', 16393, 0),
(303, 'Funny', 'funny', 319050, 0),
(304, 'Futuristic Romance', 'futuristic-romance', 6216, 0),
(305, 'Game Design', 'game-design', 2719, 0),
(306, 'Gamebooks', 'gamebooks', 3309, 0),
(307, 'Games', 'games', 25011, 0),
(308, 'Gaming', 'gaming', 19076, 0),
(309, 'Gaming Fiction', 'gaming-fiction', 1212, 0),
(310, 'Gardening', 'gardening', 42308, 0),
(311, 'Gastronomy', 'gastronomy', 3290, 0),
(312, 'Gay', 'gay', 113334, 0),
(313, 'Gay For You', 'gay-for-you', 15275, 0),
(314, 'Geek', 'geek', 23444, 0),
(315, 'Gender', 'gender', 56099, 0),
(316, 'Gender And Sexuality', 'gender-and-sexuality', 15178, 0),
(317, 'Gender Identity', 'gender-identity', 2528, 0),
(318, 'Gender Roles', 'gender-roles', 4761, 0),
(319, 'Gender Studies', 'gender-studies', 23835, 0),
(320, 'Genderfuck', 'genderfuck', 861, 0),
(321, 'Genetics', 'genetics', 9490, 0),
(322, 'Geography', 'geography', 40101, 0),
(323, 'Geology', 'geology', 6436, 0),
(324, 'Georgian Romance', 'georgian-romance', 4392, 0),
(325, 'German Literature', 'german-literature', 36155, 0),
(326, 'Germany', 'germany', 67710, 0),
(327, 'Ghost Stories', 'ghost-stories', 26626, 0),
(328, 'Ghosts', 'ghosts', 122709, 0),
(329, 'Glbt', 'glbt', 112424, 0),
(330, 'Global Warming', 'global-warming', 1625, 0),
(331, 'Gnosticism', 'gnosticism', 2068, 0),
(332, 'Go', 'go', 6254, 0),
(333, 'God', 'god', 23491, 0),
(334, 'Goddess', 'goddess', 4589, 0),
(335, 'Gods', 'gods', 32125, 0),
(336, 'Golden Age Mystery', 'golden-age-mystery', 6558, 0),
(337, 'Goth', 'goth', 9587, 0),
(338, 'Gothic', 'gothic', 137746, 0),
(339, 'Gothic Horror', 'gothic-horror', 27916, 0),
(340, 'Gothic Romance', 'gothic-romance', 13342, 0),
(341, 'Government', 'government', 31305, 0),
(342, 'Grad School', 'grad-school', 89281, 0),
(343, 'Graffiti', 'graffiti', 776, 0),
(344, 'Graphic Literature', 'graphic-literature', 3931, 0),
(345, 'Graphic Non Fiction', 'graphic-non-fiction', 1707, 0),
(346, 'Graphic Novels', 'graphic-novels', 847478, 0),
(347, 'Graphic Novels Comics', 'graphic-novels-comics', 84350, 0),
(348, 'Graphic Novels Comics Manga', 'graphic-novels-comics-manga', 13896, 0),
(349, 'Graphic Novels Manga', 'graphic-novels-manga', 29914, 0),
(350, 'Graphica', 'graphica', 4570, 0),
(351, 'Greece', 'greece', 30085, 0),
(352, 'Greek Mythology', 'greek-mythology', 28009, 0),
(353, 'Green', 'green', 43672, 0),
(354, 'Grimm', 'grimm', 3410, 0),
(355, 'Guidebook', 'guidebook', 2266, 0),
(356, 'Guides', 'guides', 14207, 0),
(357, 'Hackers', 'hackers', 2596, 0),
(358, 'Halloween', 'halloween', 42321, 0),
(359, 'Hard Boiled', 'hard-boiled', 15979, 0),
(360, 'Hard Science Fiction', 'hard-science-fiction', 8288, 0),
(361, 'Harlequin', 'harlequin', 120010, 0),
(362, 'Health', 'health', 140242, 0),
(363, 'Health Care', 'health-care', 3479, 0),
(364, 'Herbs', 'herbs', 3678, 0),
(365, 'Heroic Fantasy', 'heroic-fantasy', 20473, 0),
(366, 'High Fantasy', 'high-fantasy', 147196, 0),
(367, 'High School', 'high-school', 251246, 0),
(368, 'Hinduism', 'hinduism', 6429, 0),
(369, 'Hip Hop', 'hip-hop', 1572, 0),
(370, 'Historical', 'historical', 1002778, 0),
(371, 'Historical Fiction', 'historical-fiction', 1760187, 0),
(372, 'Historical Mystery', 'historical-mystery', 69572, 0),
(373, 'Historical Romance', 'historical-romance', 547887, 0),
(374, 'History', 'history', 1583108, 1),
(375, 'History American Civil War', 'history-american-civil-war', 1224, 0),
(376, 'History And Politics', 'history-and-politics', 17086, 0),
(377, 'History Civil War Eastern Theater', 'history-civil-war-eastern-theater', 446, 0),
(378, 'History Of Science', 'history-of-science', 11769, 0),
(379, 'Hockey', 'hockey', 9215, 0),
(380, 'Holiday', 'holiday', 74510, 0),
(381, 'Holland', 'holland', 3031, 0),
(382, 'Holocaust', 'holocaust', 49649, 0),
(383, 'Horror', 'horror', 919662, 0),
(384, 'Horse Racing', 'horse-racing', 2887, 0),
(385, 'Horses', 'horses', 33111, 0),
(386, 'Horticulture', 'horticulture', 2438, 0),
(387, 'How To', 'how-to', 44476, 0),
(388, 'Humanities', 'humanities', 42747, 0),
(389, 'Humor', 'humor', 676917, 0),
(390, 'Hungarian Literature', 'hungarian-literature', 2888, 0),
(391, 'Hungary', 'hungary', 7356, 0),
(392, 'Illness', 'illness', 31957, 0),
(393, 'India', 'india', 62982, 0),
(394, 'Indian Literature', 'indian-literature', 8666, 0),
(395, 'Indigenous History', 'indigenous-history', 628, 0),
(396, 'Indonesian Literature', 'indonesian-literature', 2366, 0),
(397, 'Informatics', 'informatics', 1235, 0),
(398, 'Information Science', 'information-science', 2860, 0),
(399, 'Inspirational', 'inspirational', 166626, 1),
(400, 'International', 'international', 113912, 0),
(401, 'International Literature', 'international-literature', 18107, 0),
(402, 'Internet', 'internet', 13390, 0),
(403, 'Interracial Romance', 'interracial-romance', 18978, 0),
(404, 'Intersex', 'intersex', 830, 0),
(405, 'Iran', 'iran', 14722, 0),
(406, 'Ireland', 'ireland', 50737, 0),
(407, 'Irish Literature', 'irish-literature', 12998, 0),
(408, 'Islam', 'islam', 48433, 0),
(409, 'Israel', 'israel', 14573, 0),
(410, 'Italian Literature', 'italian-literature', 15805, 0),
(411, 'Italy', 'italy', 68026, 0),
(412, 'Japan', 'japan', 92550, 0),
(413, 'Japanese Literature', 'japanese-literature', 25005, 0),
(414, 'Jazz', 'jazz', 6496, 0),
(415, 'Jewish', 'jewish', 38851, 0),
(416, 'Josei', 'josei', 9942, 0),
(417, 'Journal', 'journal', 14867, 0),
(418, 'Journaling', 'journaling', 1905, 0),
(419, 'Journalism', 'journalism', 45178, 0),
(420, 'Judaica', 'judaica', 15994, 0),
(421, 'Judaism', 'judaism', 27535, 0),
(422, 'Juvenile', 'juvenile', 190817, 0),
(423, 'Kazakhstan', 'kazakhstan', 844, 0),
(424, 'Kenya', 'kenya', 3163, 0),
(425, 'Knitting', 'knitting', 29856, 0),
(426, 'Komik', 'komik', 17458, 0),
(427, 'Labor', 'labor', 7993, 0),
(428, 'Landscaping', 'landscaping', 780, 0),
(429, 'Language', 'language', 109711, 0),
(430, 'Latin American', 'latin-american', 18915, 0),
(431, 'Latin American History', 'latin-american-history', 2897, 0),
(432, 'Latin American Literature', 'latin-american-literature', 11801, 0),
(433, 'Law', 'law', 53683, 0),
(434, 'Lds', 'lds', 21375, 0),
(435, 'Lds Fiction', 'lds-fiction', 11764, 0),
(436, 'Lds Non Fiction', 'lds-non-fiction', 2685, 0),
(437, 'Leadership', 'leadership', 80716, 0),
(438, 'Lebanon', 'lebanon', 5471, 0),
(439, 'Legal Thriller', 'legal-thriller', 17579, 0),
(440, 'Lesbian', 'lesbian', 43040, 0),
(441, 'Lesbian Fiction', 'lesbian-fiction', 9447, 0),
(442, 'Lesbian Romance', 'lesbian-romance', 7019, 0),
(443, 'Lesbotronic', 'lesbotronic', 555, 0),
(444, 'Librarianship', 'librarianship', 4201, 0),
(445, 'Library Science', 'library-science', 6040, 0),
(446, 'Light Novel', 'light-novel', 14061, 0),
(447, 'Literary Criticism', 'literary-criticism', 45987, 0),
(448, 'Literary Fiction', 'literary-fiction', 305476, 0),
(449, 'Literature', 'literature', 669984, 0),
(450, 'Logic', 'logic', 11292, 0),
(451, 'Love', 'love', 346474, 0),
(452, 'Love Inspired', 'love-inspired', 19463, 0),
(453, 'Love Inspired Historical', 'love-inspired-historical', 2538, 0),
(454, 'Love Inspired Suspense', 'love-inspired-suspense', 4381, 0),
(455, 'Love Story', 'love-story', 137443, 0),
(456, 'Lovecraftian', 'lovecraftian', 7500, 0),
(457, 'Loveswept', 'loveswept', 3146, 0),
(458, 'Low Fantasy', 'low-fantasy', 39204, 0),
(459, 'Luxemburg', 'luxemburg', 466, 0),
(460, 'M F F', 'm-f-f', 1266, 0),
(461, 'M F M', 'm-f-m', 14134, 0),
(462, 'M M Contemporary', 'm-m-contemporary', 27444, 0),
(463, 'M M F', 'm-m-f', 10565, 0),
(464, 'M M M', 'm-m-m', 12606, 0),
(465, 'M M M F', 'm-m-m-f', 1032, 0),
(466, 'M M Paranormal', 'm-m-paranormal', 20619, 0),
(467, 'M M Romance', 'm-m-romance', 144176, 0),
(468, 'Magic', 'magic', 518336, 0),
(469, 'Magical Realism', 'magical-realism', 130655, 0),
(470, 'Magick', 'magick', 27902, 0),
(471, 'Management', 'management', 40804, 0),
(472, 'Manga', 'manga', 1673964, 0),
(473, 'Manga Romance', 'manga-romance', 9236, 0),
(474, 'Manhwa', 'manhwa', 13625, 0),
(475, 'Mannerpunk', 'mannerpunk', 1605, 0),
(476, 'Maps', 'maps', 8364, 0),
(477, 'Marathi', 'marathi', 3942, 0),
(478, 'Maritime', 'maritime', 9806, 0),
(479, 'Marriage', 'marriage', 78448, 0),
(480, 'Marvel', 'marvel', 59281, 0),
(481, 'Mathematics', 'mathematics', 43577, 0),
(482, 'Media Tie In', 'media-tie-in', 37683, 0),
(483, 'Medical', 'medical', 70904, 0),
(484, 'Medicine', 'medicine', 49153, 0),
(485, 'Medieval', 'medieval', 106154, 0),
(486, 'Medieval Romance', 'medieval-romance', 8715, 0),
(487, 'Memoir', 'memoir', 395222, 0),
(488, 'Menage', 'menage', 108576, 0),
(489, 'Mental Health', 'mental-health', 79017, 0),
(490, 'Mental Illness', 'mental-illness', 83542, 0),
(491, 'Mermaids', 'mermaids', 22821, 0),
(492, 'Metaphysics', 'metaphysics', 30858, 0),
(493, 'Microhistory', 'microhistory', 7153, 0),
(494, 'Middle Grade', 'middle-grade', 258916, 0),
(495, 'Military', 'military', 224297, 0),
(496, 'Military History', 'military-history', 51149, 0),
(497, 'Military Science Fiction', 'military-science-fiction', 12190, 0),
(498, 'Mills And Boon', 'mills-and-boon', 11256, 0),
(499, 'Modern', 'modern', 235126, 0),
(500, 'Modern Classics', 'modern-classics', 119192, 0),
(501, 'Mormonism', 'mormonism', 4703, 0),
(502, 'Mountaineering', 'mountaineering', 5846, 0),
(503, 'Movies', 'movies', 123986, 0),
(504, 'Multicultural Literature', 'multicultural-literature', 9589, 0),
(505, 'Multiple Partners', 'multiple-partners', 10405, 0),
(506, 'Murder Mystery', 'murder-mystery', 103362, 0),
(507, 'Museology', 'museology', 646, 0),
(508, 'Music', 'music', 213897, 0),
(509, 'Music Biography', 'music-biography', 2254, 0),
(510, 'Musicals', 'musicals', 7142, 0),
(511, 'Musician Erotica', 'musician-erotica', 620, 0),
(512, 'Musicians', 'musicians', 21895, 0),
(513, 'Mystery', 'mystery', 2134333, 0),
(514, 'Mystery Thriller', 'mystery-thriller', 348907, 0),
(515, 'Mysticism', 'mysticism', 20057, 0),
(516, 'Mythology', 'mythology', 262778, 0),
(517, 'Natural History', 'natural-history', 21554, 0),
(518, 'Nature', 'nature', 111449, 0),
(519, 'Near Future', 'near-future', 18338, 0),
(520, 'Nerd', 'nerd', 15965, 0),
(521, 'Neuroscience', 'neuroscience', 18284, 0),
(522, 'New Adult', 'new-adult', 639642, 0),
(523, 'New Age', 'new-age', 24162, 0),
(524, 'New Weird', 'new-weird', 6148, 0),
(525, 'New York', 'new-york', 83107, 0),
(526, 'Noir', 'noir', 81409, 0),
(527, 'Non Fiction', 'non-fiction', 3026078, 0),
(528, 'Novella', 'novella', 210307, 0),
(529, 'Novels', 'novels', 739936, 0),
(530, 'Nsfw', 'nsfw', 4575, 0),
(531, 'Numismatics', 'numismatics', 584, 0),
(532, 'Nursery Rhymes', 'nursery-rhymes', 2454, 0),
(533, 'Nutrition', 'nutrition', 30743, 0),
(534, 'Occult', 'occult', 48794, 0),
(535, 'Occult Detective', 'occult-detective', 1635, 0),
(536, 'Oral History', 'oral-history', 2489, 0),
(537, 'Origami', 'origami', 2578, 0),
(538, 'Ornithology', 'ornithology', 1329, 0),
(539, 'Outdoors', 'outdoors', 21286, 0),
(540, 'Paganism', 'paganism', 13021, 0),
(541, 'Pakistan', 'pakistan', 8017, 0),
(542, 'Paranormal', 'paranormal', 1438895, 0),
(543, 'Paranormal Mystery', 'paranormal-mystery', 22877, 0),
(544, 'Paranormal Romance', 'paranormal-romance', 547767, 0),
(545, 'Paranormal Urban Fantasy', 'paranormal-urban-fantasy', 45578, 0),
(546, 'Parenting', 'parenting', 114897, 0),
(547, 'Peak Oil', 'peak-oil', 976, 0),
(548, 'Personal Development', 'personal-development', 66829, 0),
(549, 'Philosophy', 'philosophy', 642974, 0),
(550, 'Photography', 'photography', 68203, 0),
(551, 'Physics', 'physics', 41850, 0),
(552, 'Picture Books', 'picture-books', 590458, 0),
(553, 'Pirates', 'pirates', 32851, 0),
(554, 'Planetary Romance', 'planetary-romance', 3012, 0),
(555, 'Plants', 'plants', 6987, 0),
(556, 'Plays', 'plays', 198016, 0),
(557, 'Plus Size', 'plus-size', 3247, 0),
(558, 'Poetry', 'poetry', 622108, 0),
(559, 'Poland', 'poland', 12226, 0),
(560, 'Polish Literature', 'polish-literature', 10484, 0),
(561, 'Political Science', 'political-science', 46426, 0),
(562, 'Politics', 'politics', 374408, 0),
(563, 'Polyamorous', 'polyamorous', 1972, 0),
(564, 'Polyamory', 'polyamory', 4069, 0),
(565, 'Pop Culture', 'pop-culture', 54006, 0),
(566, 'Popular Science', 'popular-science', 25740, 0),
(567, 'Pornography', 'pornography', 1212, 0),
(568, 'Portugal', 'portugal', 9994, 0),
(569, 'Portuguese Literature', 'portuguese-literature', 6619, 0),
(570, 'Post Apocalyptic', 'post-apocalyptic', 120418, 0),
(571, 'Poverty', 'poverty', 27031, 0),
(572, 'Pre K', 'pre-k', 8523, 0),
(573, 'Prehistoric', 'prehistoric', 4009, 0),
(574, 'Prehistory', 'prehistory', 5569, 0),
(575, 'Presidents', 'presidents', 16104, 0),
(576, 'Princesses', 'princesses', 18533, 0),
(577, 'Productivity', 'productivity', 17734, 0),
(578, 'Professors', 'professors', 3037, 0),
(579, 'Programming', 'programming', 52836, 0),
(580, 'Programming Languages', 'programming-languages', 1222, 0),
(581, 'Prostitution', 'prostitution', 9102, 0),
(582, 'Psychological Thriller', 'psychological-thriller', 54632, 0),
(583, 'Psychology', 'psychology', 420380, 0),
(584, 'Pulp', 'pulp', 56685, 0),
(585, 'Pulp Adventure', 'pulp-adventure', 2681, 0),
(586, 'Pulp Noir', 'pulp-noir', 6123, 0),
(587, 'Punk', 'punk', 6812, 0),
(588, 'Punx', 'punx', 644, 0),
(589, 'Puzzles', 'puzzles', 5403, 0),
(590, 'Queer', 'queer', 74604, 0),
(591, 'Queer Lit', 'queer-lit', 11953, 0),
(592, 'Queer Studies', 'queer-studies', 3682, 0),
(593, 'Quilting', 'quilting', 11342, 0),
(594, 'Rabbits', 'rabbits', 4014, 0),
(595, 'Race', 'race', 48844, 0),
(596, 'Racing', 'racing', 3892, 0),
(597, 'Read For College', 'read-for-college', 33153, 0),
(598, 'Read For School', 'read-for-school', 183241, 0),
(599, 'Real Person Fiction', 'real-person-fiction', 569, 0),
(600, 'Realistic Fiction', 'realistic-fiction', 413374, 0),
(601, 'Realistic Young Adult', 'realistic-young-adult', 6544, 0),
(602, 'Recreation', 'recreation', 24850, 0),
(603, 'Reference', 'reference', 445698, 0),
(604, 'Regency', 'regency', 112495, 0),
(605, 'Regency Romance', 'regency-romance', 47240, 0),
(606, 'Relationships', 'relationships', 232658, 0),
(607, 'Religion', 'religion', 417378, 0),
(608, 'Research', 'research', 145679, 0),
(609, 'Retellings', 'retellings', 71438, 0),
(610, 'Road Trip', 'road-trip', 35562, 0),
(611, 'Robots', 'robots', 11653, 0),
(612, 'Rock N Roll', 'rock-n-roll', 7035, 0),
(613, 'Role Playing Games', 'role-playing-games', 5384, 0),
(614, 'Roman', 'roman', 169317, 0),
(615, 'Romance', 'romance', 3955618, 1),
(616, 'Romania', 'romania', 5937, 0),
(617, 'Romanian Literature', 'romanian-literature', 16792, 0),
(618, 'Romantic', 'romantic', 165379, 0),
(619, 'Romantic Suspense', 'romantic-suspense', 221854, 0),
(620, 'Russia', 'russia', 76671, 0),
(621, 'Russian Literature', 'russian-literature', 39694, 0),
(622, 'Satanism', 'satanism', 1539, 0),
(623, 'Scandinavian Literature', 'scandinavian-literature', 12848, 0),
(624, 'School', 'school', 462746, 0),
(625, 'School Stories', 'school-stories', 14420, 0),
(626, 'Science', 'science', 617576, 0),
(627, 'Science Fiction', 'science-fiction', 1413447, 0),
(628, 'Science Fiction Fantasy', 'science-fiction-fantasy', 208295, 0),
(629, 'Science Fiction Romance', 'science-fiction-romance', 15468, 0),
(630, 'Science Nature', 'science-nature', 16847, 0),
(631, 'Scores', 'scores', 1058, 0),
(632, 'Scotland', 'scotland', 47047, 0),
(633, 'Scripture', 'scripture', 7493, 0),
(634, 'Seinen', 'seinen', 17040, 0),
(635, 'Self Help', 'self-help', 235822, 0),
(636, 'Sequential Art', 'sequential-art', 42059, 0),
(637, 'Serbian Literature', 'serbian-literature', 1041, 0),
(638, 'Sewing', 'sewing', 10366, 0),
(639, 'Sex And Erotica', 'sex-and-erotica', 2050, 0),
(640, 'Sex Work', 'sex-work', 3875, 0),
(641, 'Sexuality', 'sexuality', 60782, 0),
(642, 'Shapeshifters', 'shapeshifters', 120159, 0),
(643, 'Shinigami', 'shinigami', 1244, 0),
(644, 'Shojo', 'shojo', 22196, 0),
(645, 'Shonen', 'shonen', 22835, 0),
(646, 'Short Stories', 'short-stories', 666064, 0),
(647, 'Short Story Collection', 'short-story-collection', 28214, 0),
(648, 'Shounen Ai', 'shounen-ai', 6278, 0),
(649, 'Silhouette', 'silhouette', 6220, 0),
(650, 'Skepticism', 'skepticism', 13949, 0),
(651, 'Slash Fiction', 'slash-fiction', 744, 0),
(652, 'Slice Of Life', 'slice-of-life', 74524, 0),
(653, 'Soccer', 'soccer', 4515, 0),
(654, 'Social', 'social', 112195, 0),
(655, 'Social Change', 'social-change', 7951, 0),
(656, 'Social Issues', 'social-issues', 78546, 0),
(657, 'Social Justice', 'social-justice', 41362, 0),
(658, 'Social Media', 'social-media', 7343, 0),
(659, 'Social Movements', 'social-movements', 3738, 0),
(660, 'Social Science', 'social-science', 56299, 0),
(661, 'Society', 'society', 112474, 0),
(662, 'Sociology', 'sociology', 159969, 0),
(663, 'Software', 'software', 12790, 0),
(664, 'Soldiers', 'soldiers', 12305, 0),
(665, 'Southern', 'southern', 48131, 0),
(666, 'Southern Gothic', 'southern-gothic', 12478, 0),
(667, 'Southern War For Independance', 'southern-war-for-independance', 465, 0),
(668, 'Space', 'space', 58362, 0),
(669, 'Space Opera', 'space-opera', 61775, 0),
(670, 'Spain', 'spain', 27904, 0),
(671, 'Spanish Literature', 'spanish-literature', 18151, 0),
(672, 'Speculative Fiction', 'speculative-fiction', 187556, 0),
(673, 'Spider Man', 'spider-man', 6559, 0),
(674, 'Spiritualism', 'spiritualism', 6399, 0),
(675, 'Spirituality', 'spirituality', 198548, 0),
(676, 'Splatterpunk', 'splatterpunk', 2651, 0),
(677, 'Sports', 'sports', 168818, 0),
(678, 'Sports And Games', 'sports-and-games', 3507, 0),
(679, 'Sports Romance', 'sports-romance', 24312, 0),
(680, 'Spy Thriller', 'spy-thriller', 19560, 0),
(681, 'Star Trek', 'star-trek', 58804, 0),
(682, 'Star Trek Deep Space Nine', 'star-trek-deep-space-nine', 1004, 0),
(683, 'Star Trek Enterprise', 'star-trek-enterprise', 672, 0),
(684, 'Star Trek Original Series', 'star-trek-original-series', 489, 0),
(685, 'Star Trek The Next Generation', 'star-trek-the-next-generation', 1618, 0),
(686, 'Star Trek Voyager', 'star-trek-voyager', 1305, 0),
(687, 'Star Wars', 'star-wars', 131077, 0),
(688, 'Steampunk', 'steampunk', 162654, 0),
(689, 'Steampunk Romance', 'steampunk-romance', 1898, 0),
(690, 'Storytime', 'storytime', 58713, 0),
(691, 'Street Art', 'street-art', 604, 0),
(692, 'Strippers', 'strippers', 1623, 0),
(693, 'Students', 'students', 13412, 0),
(694, 'Suisse', 'suisse', 728, 0),
(695, 'Sunday Comics', 'sunday-comics', 603, 0),
(696, 'Superheroes', 'superheroes', 63498, 0),
(697, 'Superman', 'superman', 7457, 0),
(698, 'Supernatural', 'supernatural', 461197, 0),
(699, 'Surreal', 'surreal', 34411, 0),
(700, 'Survival', 'survival', 128722, 0),
(701, 'Suspense', 'suspense', 556756, 0),
(702, 'Sustainability', 'sustainability', 14056, 0),
(703, 'Swashbuckling', 'swashbuckling', 9274, 0),
(704, 'Sweden', 'sweden', 18107, 0),
(705, 'Swedish Literature', 'swedish-literature', 10558, 0),
(706, 'Sword And Planet', 'sword-and-planet', 1598, 0),
(707, 'Sword And Sorcery', 'sword-and-sorcery', 27227, 0),
(708, 'Taoism', 'taoism', 3860, 0),
(709, 'Tarot', 'tarot', 5796, 0),
(710, 'Tasmania', 'tasmania', 1732, 0),
(711, 'Tea', 'tea', 4875, 0),
(712, 'Teachers', 'teachers', 13505, 0),
(713, 'Teaching', 'teaching', 92883, 0),
(714, 'Technical', 'technical', 28176, 0),
(715, 'Technology', 'technology', 71673, 0),
(716, 'Teen', 'teen', 325211, 0),
(717, 'Terrorism', 'terrorism', 16291, 0),
(718, 'Textbooks', 'textbooks', 102996, 0),
(719, 'The 1700S', 'the-1700s', 7135, 0),
(720, 'Theatre', 'theatre', 72840, 0),
(721, 'Thelema', 'thelema', 2570, 0),
(722, 'Theology', 'theology', 177825, 0),
(723, 'Theory', 'theory', 63531, 0),
(724, 'Theosophy', 'theosophy', 6021, 0),
(725, 'Threesome', 'threesome', 4264, 0),
(726, 'Thriller', 'thriller', 791811, 0),
(727, 'Time Travel', 'time-travel', 138605, 0),
(728, 'Time Travel Romance', 'time-travel-romance', 8277, 0),
(729, 'Traditional Regency', 'traditional-regency', 6026, 0),
(730, 'Tragedy', 'tragedy', 102792, 0),
(731, 'Trans', 'trans', 9043, 0),
(732, 'Transgender', 'transgender', 5105, 0),
(733, 'Transsexual', 'transsexual', 696, 0),
(734, 'Travel', 'travel', 314847, 0),
(735, 'Travelogue', 'travelogue', 14271, 0),
(736, 'Trivia', 'trivia', 12720, 0),
(737, 'True Crime', 'true-crime', 87616, 0),
(738, 'True Story', 'true-story', 37205, 0),
(739, 'Turkish', 'turkish', 23683, 0),
(740, 'Turkish Literature', 'turkish-literature', 14331, 0),
(741, 'Tv', 'tv', 30920, 0),
(742, 'Ukraine', 'ukraine', 5020, 0),
(743, 'Ukrainian Literature', 'ukrainian-literature', 1928, 0),
(744, 'Unicorns', 'unicorns', 7297, 0),
(745, 'United States', 'united-states', 116028, 0),
(746, 'Urban', 'urban', 84427, 0),
(747, 'Urban Fantasy', 'urban-fantasy', 721572, 0),
(748, 'Urban Legends', 'urban-legends', 732, 0),
(749, 'Urban Planning', 'urban-planning', 4728, 0),
(750, 'Urban Studies', 'urban-studies', 5277, 0),
(751, 'Urbanism', 'urbanism', 5312, 0),
(752, 'Us Presidents', 'us-presidents', 3903, 0),
(753, 'Usability', 'usability', 2137, 0),
(754, 'Utopia', 'utopia', 21029, 0),
(755, 'Vampire Hunters', 'vampire-hunters', 2403, 0),
(756, 'Vampires', 'vampires', 506274, 0),
(757, 'Vegan', 'vegan', 10245, 0),
(758, 'Vegetarian', 'vegetarian', 3770, 0),
(759, 'Vegetarianism', 'vegetarianism', 1658, 0),
(760, 'Victorian Romance', 'victorian-romance', 10170, 0),
(761, 'Victoriana', 'victoriana', 31370, 0),
(762, 'Video Games', 'video-games', 10089, 0),
(763, 'Viking Romance', 'viking-romance', 1149, 0),
(764, 'Visual Art', 'visual-art', 4227, 0),
(765, 'Walking', 'walking', 5629, 0),
(766, 'War', 'war', 292628, 0),
(767, 'Web', 'web', 16023, 0),
(768, 'Web Design', 'web-design', 4786, 0),
(769, 'Webcomic', 'webcomic', 2966, 0),
(770, 'Weird Fiction', 'weird-fiction', 31013, 0),
(771, 'Werecats', 'werecats', 2566, 0),
(772, 'Werewolves', 'werewolves', 136985, 0),
(773, 'Western', 'western', 122856, 0),
(774, 'Western Historical Romance', 'western-historical-romance', 4373, 0),
(775, 'Western Romance', 'western-romance', 21023, 0),
(776, 'Whodunit', 'whodunit', 32443, 0),
(777, 'Wicca', 'wicca', 14279, 0),
(778, 'Wilderness', 'wilderness', 10354, 0),
(779, 'Wildlife', 'wildlife', 7522, 0),
(780, 'Wine', 'wine', 6612, 0),
(781, 'Witchcraft', 'witchcraft', 31216, 0),
(782, 'Witches', 'witches', 129547, 0),
(783, 'Wizards', 'wizards', 31726, 0),
(784, 'Wolves', 'wolves', 32510, 0),
(785, 'Women And Gender Studies', 'women-and-gender-studies', 3707, 0),
(786, 'Womens', 'womens', 21491, 0),
(787, 'Womens Fiction', 'womens-fiction', 67692, 0),
(788, 'Womens Rights', 'womens-rights', 2315, 0),
(789, 'Womens Studies', 'womens-studies', 20540, 0),
(790, 'Wonder Woman', 'wonder-woman', 2738, 0),
(791, 'Words', 'words', 20757, 0),
(792, 'World History', 'world-history', 54152, 0),
(793, 'World Of Darkness', 'world-of-darkness', 1591, 0),
(794, 'World War I', 'world-war-i', 12957, 0),
(795, 'World War Ii', 'world-war-ii', 58572, 0),
(796, 'Writing', 'writing', 164680, 0),
(797, 'X Men', 'x-men', 15865, 0),
(798, 'Yaoi', 'yaoi', 41999, 0),
(799, 'Young Adult', 'young-adult', 2883327, 0),
(800, 'Young Adult Contemporary', 'young-adult-contemporary', 20995, 0),
(801, 'Young Adult Fantasy', 'young-adult-fantasy', 64535, 0),
(802, 'Young Adult Historical Fiction', 'young-adult-historical-fiction', 7236, 0),
(803, 'Young Adult Paranormal', 'young-adult-paranormal', 25775, 0),
(804, 'Young Adult Romance', 'young-adult-romance', 47927, 0),
(805, 'Young Adult Science Fiction', 'young-adult-science-fiction', 11535, 0),
(806, 'Young Readers', 'young-readers', 61897, 0),
(807, 'Yuri', 'yuri', 2231, 0),
(808, 'Zen', 'zen', 15545, 0),
(809, 'Zombies', 'zombies', 135611, 0),
(810, 'Startup', 'startup', 984, 0),
(811, 'Book Club', 'book-club', NULL, 0),
(812, 'Entrepreneurship', 'entrepreneurship', NULL, 0),
(813, 'Finances', 'finances', NULL, 0),
(814, 'Victorian', 'victorian', NULL, 0),
(815, 'Nonfiction', 'nonfiction', NULL, 0),
(816, 'Kids', 'kids', NULL, 0),
(817, 'Own', 'own', NULL, 0),
(818, 'Finance', 'finance', NULL, 0),
(819, 'Ancient History', 'ancient-history', NULL, 0),
(820, 'Buisness', NULL, NULL, 0),
(821, 'Childrens', 'childrens', NULL, 0),
(822, 'Russian History', 'russian-history', NULL, 0),
(823, 'Middle Ages', 'middle-ages', NULL, 0),
(824, 'Amazon', 'amazon', NULL, 0),
(825, 'Post Colonial', 'post-colonial', NULL, 0),
(826, 'Transport', 'transport', NULL, 0),
(827, 'Cars', 'cars', NULL, 0),
(828, 'Quantum Mechanics', 'quantum-mechanics', NULL, 0),
(829, 'Futuristic', 'futuristic', NULL, 0),
(830, 'Georgian', 'georgian', NULL, 0),
(831, 'Female Authors', 'female-authors', NULL, 0),
(832, 'Nobel Prize', 'nobel-prize', NULL, 0),
(833, 'Police', 'police', NULL, 0),
(834, 'Russian Revolution', 'russian-revolution', NULL, 0),
(835, 'Soviet Union', 'soviet-union', NULL, 0),
(836, 'Nursing', 'nursing', NULL, 0),
(837, 'Anarchism', 'anarchism', NULL, 0),
(854, 'Edwardian', 'edwardian', NULL, 0),
(855, 'Discipleship', 'discipleship', NULL, 0),
(856, 'Trains', 'trains', NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `category_relation`
--

CREATE TABLE IF NOT EXISTS `category_relation` (
  `parent_id` int(6) NOT NULL,
  `child_id` int(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `category_relation`
--

INSERT INTO `category_relation` (`parent_id`, `child_id`) VALUES
(6, 371),
(371, 142),
(371, 280),
(371, 372),
(371, 485),
(371, 573),
(371, 719),
(371, 761),
(142, 139),
(142, 141),
(142, 280),
(142, 485),
(142, 513),
(142, 573),
(142, 719),
(142, 761),
(139, 141),
(139, 143),
(139, 144),
(141, 51),
(141, 95),
(141, 140),
(141, 144),
(141, 373),
(141, 399),
(141, 452),
(141, 773),
(51, 140),
(51, 144),
(51, 399),
(51, 452),
(144, 95),
(144, 140),
(144, 373),
(144, 399),
(144, 452),
(144, 773),
(373, 324),
(373, 486);

-- --------------------------------------------------------

--
-- Table structure for table `collections`
--

CREATE TABLE IF NOT EXISTS `collections` (
  `collection_id` int(6) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `price` float DEFAULT NULL,
  `return_days` int(3) DEFAULT NULL,
  `image` varchar(1000) DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `date_edited` timestamp NULL DEFAULT NULL,
  `category_id` int(2) DEFAULT NULL,
  `partial_order` tinyint(1) NOT NULL DEFAULT '0',
  `slug_url` varchar(200) DEFAULT NULL,
  `more_url` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`collection_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=47 ;

--
-- Dumping data for table `collections`
--

INSERT INTO `collections` (`collection_id`, `name`, `description`, `date_added`, `price`, `return_days`, `image`, `active`, `date_edited`, `category_id`, `partial_order`, `slug_url`, `more_url`) VALUES
(3, 'Trending', 'Top Trending Books in Indian Market', '2016-04-02 09:42:48', 0, 0, NULL, 1, '2016-06-21 13:05:10', 0, 1, 'trending', NULL),
(4, 'Most Searched', 'Most Searched books by users', '2016-04-02 09:43:17', 0, 0, NULL, 1, '2016-07-05 16:00:48', 0, 1, 'most-searched', NULL),
(5, 'Ostrich Recommends', 'Curated List by Ostrich', '2016-04-02 09:43:54', 0, 0, NULL, 1, '2016-06-21 05:09:55', 0, 1, 'ostrich-recommends', NULL),
(27, 'Discoverer ', 'Every child is a discoverer, and books he reads are his first best friends. ', '2016-05-06 13:00:33', 350, 30, NULL, 1, '2016-05-06 13:02:17', 3, 0, NULL, NULL),
(28, 'Explorer ', 'For the most curious member of the family, little explorer.', '2016-05-06 13:29:48', 350, 30, NULL, 1, '2016-05-06 13:29:48', 3, 0, NULL, NULL),
(31, 'Discoverer', 'For the little discoverers among us ', '2016-05-06 14:05:31', 350, 30, NULL, 1, '2016-05-06 14:10:40', 4, 0, NULL, NULL),
(33, 'Explorer ', 'With books around, our young explorer can go places..', '2016-05-06 14:15:08', 350, 30, NULL, 1, '2016-05-06 14:15:08', 4, 0, NULL, NULL),
(34, 'Dreamer ', 'Time to dream. Dream big.', '2016-05-06 14:22:05', 350, 30, NULL, 1, '2016-05-06 14:22:05', 5, 0, NULL, NULL),
(35, 'Debonair', 'For your charming little one, we have some adventurous friends.', '2016-05-06 14:27:24', 350, 30, NULL, 1, '2016-05-06 14:27:57', 5, 0, NULL, NULL),
(36, 'Learner ', 'They are restless and responsible. Give them the best to go deep.', '2016-05-06 14:36:56', 350, 30, NULL, 1, '2016-05-06 14:36:56', 6, 0, NULL, NULL),
(37, 'Fabulous ', 'Kids might ask for pocket money, but you can give them something more precious', '2016-05-06 14:45:47', 350, 30, NULL, 1, '2016-05-06 14:45:47', 6, 0, NULL, NULL),
(38, 'Classic Graphic Novels', 'Because everyone needs a hero! ', '2016-05-27 06:15:45', 0, 0, 'Comic.png', 1, '2016-06-15 17:43:39', 0, 1, 'classic-graphic-novels', '/comics'),
(40, 'For the Perfect Weekend', '', '2016-05-27 06:23:06', 0, 0, 'Chill.png', 1, '2016-05-27 06:23:06', 0, 1, 'for-the-perfect-weekend', '/fiction'),
(41, 'Start the Entrepreneurial Journey', '', '2016-05-27 06:24:38', 0, 0, 'Startup.png', 1, '2016-05-27 06:28:21', 0, 1, 'start-the-entrepreneurial-journey', '/business'),
(42, 'It''s Never Too Early To Read', '', '2016-05-27 06:36:26', 0, 0, 'kid.png', 1, '2016-05-27 06:36:26', 0, 1, 'it-s-never-too-early-to-read', '/children'),
(46, 'Books at Rs. 45', 'Read Best. Pay Less. ', '2016-07-05 17:29:08', 0, 0, NULL, 1, '2016-07-08 06:42:35', 0, 1, 'books-at-rs-45', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `collections_category`
--

CREATE TABLE IF NOT EXISTS `collections_category` (
  `category_id` int(3) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(200) NOT NULL,
  `image` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `collections_category`
--

INSERT INTO `collections_category` (`category_id`, `category_name`, `image`) VALUES
(3, 'Toddler''s (ages 2-4)', 'https://d3i8lg6krdgeel.cloudfront.net/categories/Kids.png'),
(4, 'Young Reader (ages 4-7)', 'https://d3i8lg6krdgeel.cloudfront.net/categories/Kids.png'),
(5, 'Bright Child (ages 7-10)', 'https://d3i8lg6krdgeel.cloudfront.net/categories/Kids.png'),
(6, 'Pre Teen (ages 10-12)', 'https://d3i8lg6krdgeel.cloudfront.net/categories/Kids.png');

-- --------------------------------------------------------

--
-- Table structure for table `collections_items`
--

CREATE TABLE IF NOT EXISTS `collections_items` (
  `collection_id` int(6) NOT NULL,
  `item_id` int(6) NOT NULL,
  `sort_order` int(2) DEFAULT '0',
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_edited` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `collections_items`
--

INSERT INTO `collections_items` (`collection_id`, `item_id`, `sort_order`, `date_added`, `date_edited`) VALUES
(3, 18377, 2, '2016-04-02 09:47:19', '2016-06-21 13:05:10'),
(3, 87, 5, '2016-04-02 09:47:19', '2016-06-21 13:05:10'),
(4, 66, 2, '2016-04-02 09:49:13', '2016-07-05 16:00:48'),
(4, 143, 1, '2016-04-02 09:49:13', '2016-07-05 16:00:48'),
(4, 51, 8, '2016-04-02 09:49:13', '2016-07-05 16:00:48'),
(4, 2058, 7, '2016-04-02 09:49:13', '2016-07-05 16:00:48'),
(4, 1, 6, '2016-04-02 09:49:13', '2016-07-05 16:00:48'),
(4, 4051, 4, '2016-04-02 09:49:13', '2016-07-05 16:00:48'),
(4, 4648, 0, '2016-04-02 09:49:13', '2016-07-05 16:00:48'),
(4, 5788, 5, '2016-04-02 09:49:13', '2016-07-05 16:00:48'),
(4, 37, 3, '2016-04-02 09:49:13', '2016-07-05 16:00:48'),
(3, 3101, 3, '2016-04-14 09:24:50', '2016-06-21 13:05:10'),
(3, 4650, 7, '2016-04-18 09:03:56', '2016-06-21 13:05:10'),
(26, 18583, 0, '2016-05-06 12:59:23', NULL),
(26, 265, 1, '2016-05-06 12:59:23', NULL),
(26, 18671, 2, '2016-05-06 12:59:23', NULL),
(27, 18583, 0, '2016-05-06 13:00:33', '2016-05-06 13:02:17'),
(27, 265, 1, '2016-05-06 13:00:33', '2016-05-06 13:02:17'),
(27, 18671, 2, '2016-05-06 13:00:33', '2016-05-06 13:02:17'),
(28, 18672, 0, '2016-05-06 13:29:48', NULL),
(28, 1193, 1, '2016-05-06 13:29:48', NULL),
(28, 2869, 2, '2016-05-06 13:29:48', NULL),
(30, 40, 0, '2016-05-06 13:50:46', NULL),
(30, 34, 1, '2016-05-06 13:50:46', NULL),
(31, 40, 0, '2016-05-06 14:05:31', '2016-05-06 14:10:40'),
(31, 34, 1, '2016-05-06 14:05:31', '2016-05-06 14:10:40'),
(31, 17, 2, '2016-05-06 14:05:31', '2016-05-06 14:10:40'),
(31, 18675, 3, '2016-05-06 14:05:31', '2016-05-06 14:10:40'),
(32, 2071, 0, '2016-05-06 14:14:39', NULL),
(32, 5319, 1, '2016-05-06 14:14:39', NULL),
(32, 18315, 2, '2016-05-06 14:14:39', NULL),
(32, 4697, 3, '2016-05-06 14:14:39', NULL),
(33, 2071, 0, '2016-05-06 14:15:08', NULL),
(33, 5319, 1, '2016-05-06 14:15:08', NULL),
(33, 18315, 2, '2016-05-06 14:15:08', NULL),
(33, 4697, 3, '2016-05-06 14:15:08', NULL),
(34, 18450, 0, '2016-05-06 14:22:05', NULL),
(34, 2014, 1, '2016-05-06 14:22:05', NULL),
(34, 2083, 2, '2016-05-06 14:22:05', NULL),
(34, 394, 3, '2016-05-06 14:22:05', NULL),
(35, 20, 0, '2016-05-06 14:27:24', '2016-05-06 14:27:57'),
(35, 76, 1, '2016-05-06 14:27:24', '2016-05-06 14:27:57'),
(35, 4824, 2, '2016-05-06 14:27:24', '2016-05-06 14:27:57'),
(35, 6911, 3, '2016-05-06 14:27:24', '2016-05-06 14:27:57'),
(36, 4, 0, '2016-05-06 14:36:56', NULL),
(36, 3951, 1, '2016-05-06 14:36:56', NULL),
(36, 3156, 2, '2016-05-06 14:36:56', NULL),
(36, 88, 3, '2016-05-06 14:36:56', NULL),
(37, 4650, 0, '2016-05-06 14:45:47', NULL),
(37, 2702, 1, '2016-05-06 14:45:47', NULL),
(37, 151, 2, '2016-05-06 14:45:47', NULL),
(37, 18580, 3, '2016-05-06 14:45:47', NULL),
(3, 18406, 0, '2016-05-08 12:03:07', '2016-06-21 13:05:10'),
(3, 32, 1, '2016-05-08 12:03:07', '2016-06-21 13:05:10'),
(3, 2190, 4, '2016-05-08 12:03:07', '2016-06-21 13:05:10'),
(3, 18501, 6, '2016-05-08 12:03:07', '2016-06-21 13:05:10'),
(4, 3387, 9, '2016-05-08 12:06:50', '2016-07-05 16:00:48'),
(4, 296, 10, '2016-05-08 12:06:50', '2016-07-05 16:00:48'),
(4, 16, 11, '2016-05-08 12:06:50', '2016-07-05 16:00:48'),
(4, 5552, 12, '2016-05-08 12:06:50', '2016-07-05 16:00:48'),
(38, 323, 0, '2016-05-27 06:15:45', '2016-06-15 17:43:39'),
(38, 410, 1, '2016-05-27 06:15:45', '2016-06-15 17:43:39'),
(38, 217, 2, '2016-05-27 06:15:45', '2016-06-15 17:43:39'),
(38, 18660, 3, '2016-05-27 06:15:45', '2016-06-15 17:43:39'),
(38, 411, 4, '2016-05-27 06:15:45', '2016-06-15 17:43:39'),
(38, 18653, 5, '2016-05-27 06:15:45', '2016-06-15 17:43:39'),
(40, 177, 0, '2016-05-27 06:23:06', NULL),
(40, 205, 1, '2016-05-27 06:23:06', NULL),
(40, 3521, 2, '2016-05-27 06:23:06', NULL),
(40, 306, 3, '2016-05-27 06:23:06', NULL),
(40, 507, 4, '2016-05-27 06:23:06', NULL),
(40, 6809, 5, '2016-05-27 06:23:06', NULL),
(41, 14415, 1, '2016-05-27 06:24:38', '2016-05-27 06:28:21'),
(41, 4648, 0, '2016-05-27 06:27:11', '2016-05-27 06:28:21'),
(41, 4051, 2, '2016-05-27 06:27:20', '2016-05-27 06:28:21'),
(41, 3387, 3, '2016-05-27 06:28:21', NULL),
(41, 18372, 4, '2016-05-27 06:28:21', NULL),
(41, 402, 5, '2016-05-27 06:28:21', NULL),
(42, 40, 0, '2016-05-27 06:36:26', NULL),
(42, 34, 1, '2016-05-27 06:36:26', NULL),
(42, 18450, 2, '2016-05-27 06:36:26', NULL),
(42, 5161, 3, '2016-05-27 06:36:26', NULL),
(42, 299, 4, '2016-05-27 06:36:26', NULL),
(42, 2071, 5, '2016-05-27 06:36:26', NULL),
(5, 3164, 3, '2016-06-14 16:40:20', '2016-06-21 05:09:55'),
(5, 2708, 9, '2016-06-14 16:57:13', '2016-06-21 05:09:55'),
(5, 16, 5, '2016-06-21 04:39:58', '2016-06-21 05:09:55'),
(5, 9, 6, '2016-06-21 04:40:54', '2016-06-21 05:09:55'),
(5, 3, 7, '2016-06-21 04:41:56', '2016-06-21 05:09:55'),
(5, 224, 8, '2016-06-21 04:41:56', '2016-06-21 05:09:55'),
(5, 4724, 2, '2016-06-21 04:42:43', '2016-06-21 05:09:55'),
(5, 6043, 1, '2016-06-21 04:43:15', '2016-06-21 05:09:55'),
(5, 3758, 10, '2016-06-21 04:58:11', '2016-06-21 05:09:55'),
(5, 5504, 0, '2016-06-21 05:03:17', '2016-06-21 05:09:55'),
(5, 143, 11, '2016-06-21 05:05:55', '2016-06-21 05:09:55'),
(5, 165, 12, '2016-06-21 05:05:55', '2016-06-21 05:09:55'),
(5, 18651, 4, '2016-06-21 05:09:55', NULL),
(4, 238, 13, '2016-07-05 16:00:48', NULL),
(46, 9, 0, '2016-07-05 17:29:08', '2016-07-08 06:42:35'),
(46, 5788, 1, '2016-07-06 07:40:03', '2016-07-08 06:42:35'),
(46, 18727, 2, '2016-07-07 04:29:15', '2016-07-08 06:42:35'),
(46, 306, 3, '2016-07-07 04:30:01', '2016-07-08 06:42:35'),
(46, 4418, 4, '2016-07-07 04:30:01', '2016-07-08 06:42:35'),
(46, 281, 5, '2016-07-07 04:30:01', '2016-07-08 06:42:35'),
(46, 87, 6, '2016-07-07 04:31:51', '2016-07-08 06:42:35'),
(46, 3386, 7, '2016-07-07 04:31:51', '2016-07-08 06:42:35'),
(46, 2, 8, '2016-07-07 04:31:51', '2016-07-08 06:42:35'),
(46, 4445, 9, '2016-07-07 04:31:51', '2016-07-08 06:42:35'),
(46, 3789, 10, '2016-07-07 04:31:51', '2016-07-08 06:42:35'),
(46, 2466, 11, '2016-07-07 04:31:51', '2016-07-08 06:42:35'),
(46, 18431, 12, '2016-07-07 12:07:44', '2016-07-08 06:42:35'),
(46, 210, 13, '2016-07-07 12:07:44', '2016-07-08 06:42:35'),
(46, 24390, 14, '2016-07-07 12:07:44', '2016-07-08 06:42:35'),
(46, 18484, 15, '2016-07-07 12:07:44', '2016-07-08 06:42:35'),
(46, 194, 16, '2016-07-07 12:07:44', '2016-07-08 06:42:35'),
(46, 5545, 17, '2016-07-07 12:07:44', '2016-07-08 06:42:35'),
(46, 18341, 18, '2016-07-07 12:10:24', '2016-07-08 06:42:35'),
(46, 7696, 19, '2016-07-07 12:10:24', '2016-07-08 06:42:35'),
(46, 18430, 20, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 18840, 21, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 305, 22, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 522, 23, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 466, 24, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 4576, 25, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 5, 26, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 2202, 27, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 18425, 28, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 1819, 29, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 18372, 30, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 894, 31, '2016-07-08 06:42:11', '2016-07-08 06:42:35'),
(46, 247, 32, '2016-07-08 06:42:36', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `collections_metadata`
--

CREATE TABLE IF NOT EXISTS `collections_metadata` (
  `collection_id` int(6) NOT NULL,
  `meta_key` varchar(50) NOT NULL,
  `meta_value` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------


-- --------------------------------------------------------

--
-- Table structure for table `edit_order_log`
--

CREATE TABLE IF NOT EXISTS `edit_order_log` (
  `order_id` int(6) NOT NULL,
  `key` varchar(20) NOT NULL,
  `old_value` varchar(20) DEFAULT NULL,
  `new_value` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `edit_order_log`
--


-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE IF NOT EXISTS `inventory` (
  `inventory_id` int(6) NOT NULL AUTO_INCREMENT,
  `item_id` int(6) NOT NULL,
  `isbn_13` varchar(50) DEFAULT NULL,
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_removed` timestamp NULL DEFAULT NULL,
  `in_stock` int(1) NOT NULL DEFAULT '1',
  `price` float DEFAULT NULL,
  `item_condition` varchar(30) DEFAULT 'New',
  `fetched` tinyint(1) NOT NULL DEFAULT '0',
  `source` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`inventory_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=719 ;

--
-- Dumping data for table `inventory`
--


-- --------------------------------------------------------

--
-- Table structure for table `inventory_extended`
--

CREATE TABLE IF NOT EXISTS `inventory_extended` (
  `extended_id` int(6) NOT NULL AUTO_INCREMENT,
  `item_id` int(6) DEFAULT NULL,
  `isbn` varchar(20) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `mrp` int(6) DEFAULT NULL,
  PRIMARY KEY (`extended_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7515 ;

--
-- Dumping data for table `inventory_extended`
--


-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE IF NOT EXISTS `items` (
  `item_id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `item_name` varchar(200) NOT NULL,
  `price` int(6) unsigned DEFAULT NULL,
  `author` varchar(200) DEFAULT NULL,
  `ratings` float DEFAULT NULL,
  `num_ratings` varchar(10) DEFAULT NULL,
  `num_reviews` varchar(10) NOT NULL,
  `language` varchar(20) NOT NULL DEFAULT 'English',
  `img_small` varchar(500) DEFAULT NULL,
  `img_large` varchar(500) DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `asin` varchar(200) DEFAULT NULL,
  `goodreads_id` varchar(200) DEFAULT NULL,
  `summary` mediumtext,
  `slug_url` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`item_id`),
  KEY `item_name` (`item_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='Contains all items' AUTO_INCREMENT=24930 ;

--
-- Dumping data for table `items`
--

INSERT INTO `items` VALUES (1,'To Kill a Mockingbird',399,'Harper Lee',4.24,'25,95,957','58,486','English','thumbs/1.jpg',NULL,1,'2016-02-23 14:51:12','0446314730','2397465','Regarded as a masterpiece of American literature, this timeless story of growing up in the South became an instant bestseller when first published in 1960 and later was made into a classic film.','to-kill-a-mockingbird'),(2,'1984',195,'George Orwell',4.11,'16,12,605','33,161','English','thumbs/2.jpg',NULL,1,'2016-02-23 14:51:12','9381607796','25233603','There are only four ways in which a ruling group can fall from power. Either it is conquered from without or it governs so inefficiently that the masses are stirred to revolt or it allows a strong and discontented Middle group to come into being or it loses its own self- confidence and willingness to govern. These causes do not operate singly and as a rule all four of them are present in some degree. A ruling class which could guard against all of them would remain in power permanently. Ultimately the determining factors is the mental attitude of the ruling class itself.','1984'),(3,'Pride and Prejudice',199,'Jane Austen',4.23,'16,92,376','39,643','English','thumbs/3.jpg',NULL,1,'2016-02-23 14:51:12','8185944830','1927122','Jane Austen (1775-1817) was an English novelist whose works of romantic fiction, set among the landed gentry, earned her a place as one of the most widely read writers in English literature. Her realism, biting irony and social commentary as well as her acclaimed plots have gained her historical importance.First published in 1813, \"Pride and Prejudice,\" Jane Austen\'s witty comedy of manners - one of the most popular novels of all time - tells the story of Mr and Mrs Bennet\'s five unmarried daughters after the rich and eligible Mr Bingley and his status-conscious friend, Mr Darcy, have moved into their neighbourhood. \"It is a truth universally acknowledged, that a single man in possession of a good fortune must be in want of a wife.\" So begins the novel, that features splendidly civilized sparring between the proud Mr. Darcy and the prejudiced Elizabeth Bennet as they play out their spirited courtship in a series of eighteenth-century drawing-room intrigues.This brilliant novel is a must-read of classic literature and will delight readers of all ages.Enjoy all masterpieces by Jane Austen in a beautifully presented edition by \"Atlantic Editions\"  SENSE AND SENSIBILITY  MANSFIELD PARK  EMMA  NORTHANGER ABBEY  PERSUASION','pride-and-prejudice'),(4,'The Diary of a Young Girl',150,'Anne Frank',4.07,'16,24,978','16,484','English','thumbs/4.jpg',NULL,1,'2016-02-23 14:51:12','9380914318','25127513','The Diary of a Young Girl started two days before Anne Frank\'s thirteenth birthday. In 1942, the Nazis had occupied Holland, and her family left their home to go into hiding, as they were Jews. Anne Frank recorded daily events, her personal experiences and her feelings in her diary for the next two years. Cut off from the outside world, she and her family faced hunger, boredom, claustrophobia at living in confined quarters, and the ever-present threat of discovery and death. One day, she and her family were betrayed and taken away to the Bergen-Belsen concentration camp, where she eventually died.It is a record of a sensitive girl\'s tragic experience during one of the worst periods in human history. This diary is so powerful that it leaves a deep impact on the mind of its readers.http://www.amazon.com/gp/search/ref=s...','the-diary-of-a-young-girl'),(5,'Animal Farm',125,'George Orwell',3.82,'16,26,759','26,193','English','thumbs/5.jpg',NULL,1,'2016-02-23 14:51:12','0143416316','14060211','Tired of their servitude to man, a group of farm animals revolt and establish their own society, only to be betrayed into worse servitude by their leaders, the pigs, whose slogan becomes: \"All animals are equal, but some animals are more equal than others.\" This 1945 satire addresses the socialist/communist philosophy of Stalin in the Soviet Union.','animal-farm'),(9,'The Catcher in the Rye',350,'J.D. Salinger',3.78,'17,51,521','36,796','English','thumbs/9.jpg',NULL,1,'2016-02-23 14:51:12','0241950422','7967885','\"The Catcher in the Rye\" is J . D. Salinger\'s world-famous novel of disaffected youth. Holden Caulfield is a seventeen- year-old dropout who has just been kicked out of his fourth school. Navigating his way through the challenges of growing up, Holden dissects the \'phony\' aspects of society, and the \'phonies\' themselves: the headmaster whose affability depends on the wealth of the parents, his roommate who scores with girls using sickly-sweet affection. Written with the clarity of a boy leaving childhood behind, \"The Catcher in the Rye\" explores the world with disarming frankness and a warm, affecting charisma which has made this novel a universally loved classic of twentieth-century literature. J. D. Salinger was born in 1919 and died in January 2010. He grew up in New York City, and wrote short stories from an early age, but his breakthrough came in 1948 with the publication in The New Yorker of \"A Perfect Day for Bananafish\". \"The Catcher in the Rye\" was his first and only novel, published in 1951. It remains one of the most translated, taught and reprinted texts, and has sold some 65 million copies. His other works include the novellas \"Franny and Zooey\", \"For Esme with Love and Squalor\", and \"Raise High the Roof Beam, Carpenters, published with Seymour - An Introduction\".','the-catcher-in-the-rye'),(16,'The Book Thief',499,'Markus Zusak',4.35,'9,36,779','80,187','English','thumbs/16.jpg',NULL,1,'2016-02-23 14:51:12','0552773891','893136','It’s just a small story really, about among other things: a girl, some words, an accordionist, some fanatical Germans, a Jewish fist-fighter, and quite a lot of thievery. . . .Set during World War II in Germany, Markus Zusak’s groundbreaking new novel is the story of Liesel Meminger, a foster girl living outside of Munich. Liesel scratches out a meager existence for herself by stealing when she encounters something she can’t resist–books. With the help of her accordion-playing foster father, she learns to read and shares her stolen books with her neighbors during bombing raids as well as with the Jewish man hidden in her basement before he is marched to Dachau.This is an unforgettable story about the ability of books to feed the soul.','the-book-thief'),(17,'The Giving Tree',450,'Shel Silverstein',4.38,'5,74,855','12,321','English','thumbs/17.jpg',NULL,1,'2016-02-23 14:51:12','1846143837','10683499','The Giving Tree is a classic and moving story by Shel Silverstein.Once there was a little tree ... and she loved a little boy.So begins a story of unforgettable perception, beautifully written and illustrated by the gifted and versatile Shel Silverstein.Every day the boy would come to the tree to eat her apples, swing from her branches, or slide down her trunk ... and the tree was happy. But as the boy grew older he began to want more from the tree, and the tree gave and gave and gave.This is a tender story, touched with sadness, aglow with consolation. Shel Silverstein has created a moving parable for readers of all ages that offers an affecting interpretation of the gift of giving and a serene acceptance of another\'s capacity to love in return.Shel Silverstein\'s very first children\'s book Lafcadio, the Lion Who Shot Back was published in 1963, and followed the next year by two other books. The first of those, The Giving Tree, is a moving story about the love of a tree for a boy; it took four years before Harper Children\'s books decided to publish it. Shel returned to humour that same year withA Giraffe and a Half. His first collection of poems and drawings, Where the Sidewalk Ends, appeared in 1974, and his second, A Light in the Attic, in 1981. When he was a G.I. in Japan and Korea in the 1950, he learned to play the guitar and to write songs, including \'A Boy Named Sue\' for Johnny Cash. In 1984, Silverstein won a Grammy Award for Best Children\'s Album for Where the Sidewalk Ends - \'recited, sung and shouted\' by the author. He was also an accomplished playwright, including the 1981 hit, \'The Lady or the Tiger Show.\' The last book to be published before he died in 1999, was Falling Up (1996).','the-giving-tree'),(20,'Charlotte\'s Web',550,'E.B. White',4.12,'8,39,767','10,463','English','thumbs/20.jpg',NULL,1,'2016-02-23 14:51:12','0141354828','22654966','\"I don\'t want to die!Save me, somebody!Save me!\"The tale of how a little girl named Fern, with the help of a friendly spider, saved her pig Wilbur from the usual fate of nice fat little pigs.(From Puffin Books)An affectionate pig named Wilbur befriends a spider named Charlotte, who lives in the rafters above his pen. In this story of friendship, hardship, and the passing on into time, White reminds readers to open their eyes to the wonder and miracle found in the simplest of things.','charlotte-s-web'),(32,'The Hitchhiker\'s Guide to the Galaxy (Hitchhiker\'s Guide to the Galaxy, #1)',799,'Douglas Adams',4.19,'8,84,504','15,367','English','thumbs/32.jpg',NULL,1,'2016-02-23 14:51:12','0330316117','841628','Charting the whole of Arthur Dent\'s odyssey through space are:THE HITCHHIKER\'S GUIDE TO THE GALAXY.One Thursday lunchtime the Earth gets unexpectedly demolished to make way for a new hyperspace bypass. For Arthur Dent, who has only just had his house demolished that morning, this seems already to be more than he can cope with. Sadly, however, the weekend has only just begun, and the Galaxy is a very very very large and startling place.THE RESTAURANT AT THE END OF THE UNIVERSE.When all questions of space, time, matter and the nature of being have been resolved, only one question remains --- \"Where shall we have dinner?\" The Restaurant at the End of the Universe provides the ultimate gastronomic experience, and for once there is no morning after to worry about.LIFE, THE UNIVERSE AND EVERYTHING.In consequence of a number of stunning catastrophes, Arthur Dent is surprised to find himself living in a hideously miserable cave on prehistoric Earth. However, just as he thinks that things cannot possibly get any worse, they suddenly do. He discovers that the Galaxy is not only mind-boggling big and bewildering but also that most of the things that happen in it are staggeringly unfair.SO LONG, AND THANKS FOR ALL THE FISH.Just as Arthur Dent\'s sense of reality is in its dickiest state he suddenly finds the girl of his dreams. He finds her in the last place in the Universe in which he would expect to find anything at all, but which 3,976,000 people will find oddly familiar. They go in search of God\'s Final Message to His Creation and, in a dramatic break with tradition, actually find it.','the-hitchhiker-s-guide-to-the-galaxy-hitchhiker-s-guide-to-the-galaxy-1'),(34,'The Cat in the Hat',160,'Dr. Seuss',4.14,'2,91,029','3,546','English','thumbs/34.jpg',NULL,1,'2016-02-23 14:51:12','0007414161','21013285','About the Book: The Cat in the Hat When the Cat in the Hat steps in on the mat, Sally and her brother are in for a roller-coaster ride of havoc and mayhem! By combining the funniest stories, craziest creatures and zaniest pictures with his unique blend of rhyme, rhythm and repetition. Dr. Seuss helps children of all ages and abilities learn to read. Dr. Seuss makes reading Fun!','the-cat-in-the-hat'),(37,'The Alchemist',299,'Paulo Coelho',3.78,'10,54,094','44,047','English','thumbs/37.jpg',NULL,1,'2016-02-23 14:51:12','8186685693','25335123','Paulo Coelho\'s enchanting novel has inspired a devoted following around the world. This story, dazzling in its powerful simplicity and inspiring wisdom, is about an Andalusian shepherd boy named Santiago who travels from his homeland in Spain to the Egyptian desert in search of a treasure buried in the Pyramids. Along the way he meets a Gypsy woman, a man who calls himself king, and an alchemist, all of whom point Santiago in the direction of his quest. No one knows what the treasure is, or if Santiago will be able to surmount the obstacles along the way. But what starts out as a journey to find worldly goods turns into a discovery of the treasure found within. Lush, evocative, and deeply humane, the story of Santiago is an eternal testament to the transforming power of our dreams and the importance of listening to our hearts.','the-alchemist'),(40,'Where the Wild Things Are',299,'Maurice Sendak',4.22,'5,20,055','7,285','English','thumbs/40.jpg',NULL,1,'2016-02-23 14:51:12','0099408392','19543','One night Max puts on his wolf suit and makes mischief of one kind and another, so his mother calls him \'Wild Thing\' and sends him to bed without his supper. That night a forest begins to grow in Max\'s room and an ocean rushes by with a boat to take Max to the place where the wild things are. Max tames the wild things and crowns himself as their king, and then the wild rumpus begins. But when Max has sent the monsters to bed, and everything is quiet, he starts to feel lonely and realises it is time to sail home to the place where someone loves him best of all.','where-the-wild-things-are'),(51,'The Fellowship of the Ring (The Lord of the Rings, #1)',450,'J.R.R. Tolkien',4.31,'14,39,261','11,963','English','thumbs/51.jpg',NULL,1,'2016-02-23 14:51:12','0007488300','15923738','Continuing the story begun in The Hobbit, this is the first part of Tolkien’s epic masterpiece, The Lord of the Rings, featuring an exclusive cover image from the film, the definitive text, and a detailed map of Middle-earth.Sauron, the Dark Lord, has gathered to him all the Rings of Power – the means by which he intends to rule Middle-earth. All he lacks in his plans for dominion is the One Ring – the ring that rules them all – which has fallen into the hands of the hobbit, Bilbo Baggins.In a sleepy village in the Shire, young Frodo Baggins finds himself faced with an immense task, as his elderly cousin Bilbo entrusts the Ring to his care. Frodo must leave his home and make a perilous journey across Middle-earth to the Cracks of Doom, there to destroy the Ring and foil the Dark Lord in his evil purpose.To celebrate the release of the first of Peter Jackson’s two-part film adaptation of The Hobbit, THE HOBBIT: AN UNEXPECTED JOURNEY, this first part of The Lord of the Rings is available for a limited time with an exclusive cover image from Peter Jackson’s award-winning trilogy.','the-fellowship-of-the-ring-the-lord-of-the-rings-1'),(66,'The Fault in Our Stars',399,'John Green',4.34,'17,32,591','1,28,585','English','thumbs/66.jpg',NULL,1,'2016-02-23 14:51:12',NULL,NULL,'','the-fault-in-our-stars'),(76,'Charlie and the Chocolate Factory (Charlie Bucket, #1)',299,'Roald Dahl',4.09,'4,28,469','6,555','English','thumbs/76.jpg',NULL,1,'2016-02-23 14:51:12','0141346450','17242193','Willy Wonka\'s famous chocolate factory is opening at last!But only five lucky children will be allowed inside. And the winners are: Augustus Gloop, an enormously fat boy whose hobby is eating; Veruca Salt, a spoiled-rotten brat whose parents are wrapped around her little finger; Violet Beauregarde, a dim-witted gum-chewer with the fastest jaws around; Mike Teavee, a toy pistol-toting gangster-in-training who is obsessed with television; and Charlie Bucket, Our Hero, a boy who is honest and kind, brave and true, and good and ready for the wildest time of his life!','charlie-and-the-chocolate-factory-charlie-bucket-1'),(87,'And Then There Were None',199,'Agatha Christie',4.2,'3,15,126','11,222','English','thumbs/87.jpg',NULL,1,'2016-02-23 14:51:12',NULL,NULL,'Considered one of the greatest mysteries of all time, Christie\'s masterpiece of murder and suspense is available in this newly packaged paperback. Ten strangers, each with a dark secret, are gathered together on an isolated island by a mysterious host. One by one, they die--and before the weekend is out, there will be none.','and-then-there-were-none'),(88,'Oliver Twist',95,'Charles Dickens',3.83,'2,06,143','4,215','English','thumbs/88.jpg',NULL,1,'2016-02-23 14:51:12','1514640376','27718179','Oliver Twist, or The Parish Boy\'s Progress, is the second novel by Charles Dickens, and was first published as a serial 1837-9. The story is of the orphan Oliver Twist, who starts his life in a workhouse and is then apprenticed with an undertaker. He escapes from there and travels to London where he meets the Artful Dodger, a member of a gang of juvenile pickpockets, which is led by the elderly criminal Fagin. Oliver Twist is notable for Dickens\'s unromantic portrayal of criminals and their sordid lives, as well as exposing the cruel treatment of the many orphans in London in the mid-nineteenth century. The alternate title, The Parish Boy\'s Progress, alludes to Bunyan\'s The Pilgrim\'s Progress, as well as the 18th-century caricature series by William Hogarth, A Rake\'s Progress and A Harlot\'s Progress. An early example of the social novel, Dickens satirizes the hypocrisies of his time, including child labour, the recruitment of children as criminals, and the presence of street children. The novel may have been inspired by the story of Robert Blincoe, an orphan whose account of working as a child labourer in a cotton mill was widely read in the 1830s. It is likely that Dickens\'s own youthful experiences contributed as well. Oliver Twist has been the subject of numerous adaptations, for various media, including a highly successful musical play, Oliver!, and the multiple Academy Award winning 1968 motion picture.','oliver-twist'),(143,'Shantaram',599,'Gregory David Roberts',4.25,'83,616','8,443','English','thumbs/143.jpg',NULL,1,'2016-02-23 14:51:12','0349117543','816552','\"It took me a long time and most of the world to learn what I know about love and fate and the choices we make, but the heart of it came to me in an instant, while I was chained to a wall and being tortured.\"So begins this epic, mesmerizing first novel set in the underworld of contemporary Bombay. Shantaram is narrated by Lin, an escaped convict with a false passport who flees maximum security prison in Australia for the teeming streets of a city where he can disappear.Accompanied by his guide and faithful friend, Prabaker, the two enter Bombay\'s hidden society of beggars and gangsters, prostitutes and holy men, soldiers and actors, and Indians and exiles from other countries, who seek in this remarkable place what they cannot find elsewhere.As a hunted man without a home, family, or identity, Lin searches for love and meaning while running a clinic in one of the city\'s poorest slums, and serving his apprenticeship in the dark arts of the Bombay mafia. The search leads him to war, prison torture, murder, and a series of enigmatic and bloody betrayals. The keys to unlock the mysteries and intrigues that bind Lin are held by two people. The first is Khader Khan: mafia godfather, criminal-philosopher-saint, and mentor to Lin in the underworld of the Golden City. The second is Karla: elusive, dangerous, and beautiful, whose passions are driven by secrets that torment her and yet give her a terrible power.Burning slums and five-star hotels, romantic love and prison agonies, criminal wars and Bollywood films, spiritual gurus and mujaheddin guerrillas---this huge novel has the world of human experience in its reach, and a passionate lovefor India at its heart. Based on the life of the author, it is by any measure the debut of an extraordinary voice in literature.','shantaram'),(151,'Around the World in 80 Days',125,'Jules Verne',3.89,'1,18,392','3,259','English','thumbs/151.jpeg',NULL,1,'2016-02-23 14:51:12','8171674216','21286662','\n‘To go around the world...in such a short time and with the means of transport currently available, was not only impossible, it was madness’\nOne ill-fated evening at the Reform Club, Phileas Fogg rashly bets his companions £20,000 that he can travel around the entire globe in just eighty days—and he is determined not to lose. Breaking the well-established routine of his daily life, the reserved Englishman immediately sets off for Dover, accompanied by his hot-blooded French manservant Passepartout. Travelling by train, steamship, sailing boat, sledge and even elephant, they must overcome storms, kidnappings, natural disasters, Sioux attacks and the dogged Inspector Fix of Scotland Yard—who believes that Fogg has robbed the Bank of England—to win the extraordinary wager. Around the World in Eighty Days gripped audiences on its publication and remains hugely popular, combining exploration, adventure and a thrilling race against time.','around-the-world-in-80-days'),(165,'The Power of Now: A Guide to Spiritual Enlightenment',395,'Eckhart Tolle',4.08,'83,663','4,043','English','thumbs/165.jpeg',NULL,1,'2016-02-23 14:51:12','8190105914','387951','Ekhart Tolle\'s message is simple: living in the now is the truest path to happiness and enlightenment. And while this message may not seem stunningly original or fresh, Tolle\'s clear writing, supportive voice and enthusiasm make this an excellent manual for anyone who\'s ever wondered what exactly \"living in the now\" means. Foremost, Tolle is a world-class teacher, able to explain complicated concepts in concrete language. More importantly, within a chapter of reading this book, readers are already holding the world in a different container--more conscious of how thoughts and emotions get in the way of their ability to live in genuine peace and happiness.Tolle packs a lot of information and inspirational ideas into The Power of Now. (Topics include the source of Chi, enlightened relationships, creative use of the mind, impermanence and the cycle of life.) Thankfully, he\'s added markers that symbolise \"break time\". This is when readers should close the book and mull over what they just read. As a result, The Power of Now reads like the highly acclaimed A Course in Miracles--a spiritual guidebook that has the potential to inspire just as many study groups and change just as many lives for the better. --Gail Hudson','the-power-of-now-a-guide-to-spiritual-enlightenment'),(177,'The Girl on the Train',599,'Paula Hawkins',3.84,'4,05,614','47,294','English','thumbs/177.jpg',NULL,1,'2016-02-23 14:51:12','0857522329','23347055','EVERYDAY THE SAMERachel catches the same commuter train every morning. She knows it will wait at the same signal each time, overlooking a row of back gardens. She’s even started to feel like she knows the people who live in one of the houses. ‘Jess and Jason’, she calls them. Their life – as she sees it – is perfect. If only Rachel could be that happy.UNTIL TODAYAnd then she sees something shocking. It’s only a minute until the train moves on, but it’s enough.Now everything’s changed. Now Rachel has a chance to become a part of the lives she’s only watched from afar.Now they’ll see; she’s much more than just the girl on the train…','the-girl-on-the-train'),(194,'Fifty Shades of Grey (Fifty Shades, #1)',499,'E.L. James',3.69,'12,17,460','71,670','English','thumbs/194.jpg',NULL,1,'2016-02-23 14:51:12',NULL,NULL,NULL,'fifty-shades-of-grey-fifty-shades-1'),(205,'A Study in Scarlet (Sherlock Holmes, #1)',299,'Arthur Conan Doyle',4.13,'1,65,128','5,057','English','thumbs/205.jpg',NULL,1,'2016-02-23 14:51:12','0755334477','243093','\'There\'s the scarlet thread of murder running through the colourless skein of life, and our duty is to unravel it, and isolate it, and expose every inch of it\'. Arriving in the wilderness of London and in need of lodgings, Dr John Watson finds himself living at 221b Baker Street with one Sherlock Holmes. When a corpse is discovered in a derelict house Watston, fascinated by his brilliant, eccentric companion, is soon drawn into Holmes\' investigations. There\'s no sign of a struggle, no wounds on the body, yet scrawled in blood across the walls is the word RACHE - revenge. Watson is baffled but for Holmes the game is afoot...','a-study-in-scarlet-sherlock-holmes-1'),(210,'Kane and Abel (Kane and Abel, #1)',399,'Jeffrey Archer',4.24,'64,658','2,154','English','thumbs/210.jpg',NULL,1,'2016-02-23 14:51:12','0330509683','6975014','','kane-and-abel-kane-and-abel-1'),(217,'Batman: The Dark Knight Returns',1150,'Frank Miller',4.24,'1,21,900','2,309','English','thumbs/217.jpg',NULL,1,'2016-02-23 14:51:12','1563893428','57948','This masterpiece of modern comics storytelling brings to vivid life a dark world and an even darker man. Together with inker Klaus Janson and colorist Lynn Varley, writer/artist Frank Miller completely reinvents the legend of Batman in his saga of a near-future Gotham City gone to rot, ten years after the Dark Knight\'s retirement.Crime runs rampant in the streets, and the man who was Batman is still tortured by the memories of his parents\' murders. As civil society crumbles around him, Bruce Wayne\'s long-suppressed vigilante side finally breaks free of its self-imposed shackles.The Dark Knight returns in a blaze of fury, taking on a whole new generation of criminals and matching their level of violence. He is soon joined by this generation\'s Robin — a girl named Carrie Kelley, who proves to be just as invaluable as her predecessors.But can Batman and Robin deal with the threat posed by their deadliest enemies, after years of incarceration have made them into perfect psychopaths? And more important, can anyone survive the coming fallout of an undeclared war between the superpowers - or a clash of what were once the world\'s greatest superheroes?','batman-the-dark-knight-returns'),(224,'Steve Jobs',550,'Walter Isaacson',4.09,'3,45,372','13,248','English','thumbs/224.jpeg',NULL,1,'2016-02-23 14:51:12',NULL,NULL,NULL,'steve-jobs'),(238,'Me Before You (Me Before You, #1)',175,'Jojo Moyes',4.29,'2,69,380','34,993','English','thumbs/238.jpg',NULL,1,'2016-02-23 14:51:12','0718157834','12649718','Lou Clark knows lots of things. She knows how many footsteps there are between the bus stop and home. She knows she likes working in The Buttered Bun tea shop and she knows she might not love her boyfriend Patrick.What Lou doesn\'t know is she\'s about to lose her job or that knowing what\'s coming is what keeps her sane.Will Traynor knows his motorcycle accident took away his desire to live. He knows everything feels very small and rather joyless now and he knows exactly how he\'s going to put a stop to that.What Will doesn\'t know is that Lou is about to burst into his world in a riot of colour. And neither of them knows they\'re going to change the other for all time.','me-before-you-me-before-you-1'),(247,'Rich Dad, Poor Dad',575,'Robert T. Kiyosaki',3.82,'96,023','4,625','English','thumbs/247.jpeg',NULL,1,'2016-02-23 14:51:12',NULL,NULL,NULL,'rich-dad-poor-dad'),(265,'The Very Hungry Caterpillar',299,'Eric Carle',4.27,'2,46,206','4,815','English','thumbs/265.jpg',NULL,1,'2016-02-23 14:51:12','0140569324','105522','The classic edition of the bestselling story written for the very young. A newly hatched caterpillar eats his way through all kinds of food.','the-very-hungry-caterpillar'),(281,'The Secret of the Nagas (Shiva Trilogy #2)',295,'Amish Tripathi',3.94,'39,434','1,744','English','thumbs/281.jpg',NULL,1,'2016-02-23 14:51:12',NULL,NULL,NULL,'the-secret-of-the-nagas-shiva-trilogy-2'),(296,'The Power of Habit: Why We Do What We Do in Life and Business',550,'Charles Duhigg',3.97,'1,03,064','6,383','English','thumbs/296.jpg',NULL,1,'2016-02-23 14:51:12','1847946240','17248798','A young woman walks into a laboratory. Over the past two years, she has transformed almost every aspect of her life. She has quit smoking, run a marathon, and been promoted at work. The patterns inside her brain, neurologists discover, have fundamentally changed. Marketers at Procter & Gamble study videos of people making their beds. They are desperately trying to figure out how to sell a new product called Febreze, on track to be one of the biggest flops in company history. Suddenly, one of them detects a nearly imperceptible pattern—and with a slight shift in advertising, Febreze goes on to earn a billion dollars a year. An untested CEO takes over one of the largest companies in America. His first order of business is attacking a single pattern among his employees—how they approach worker safety—and soon the firm, Alcoa, becomes the top performer in the Dow Jones. What do all these people have in common? They achieved success by focusing on the patterns that shape every aspect of our lives.  They succeeded by transforming habits. In The Power of Habit, award-winning New York Times business reporter Charles Duhigg takes us to the thrilling edge of scientific discoveries that explain why habits exist and how they can be changed. With penetrating intelligence and an ability to distill vast amounts of information into engrossing narratives, Duhigg brings to life a whole new understanding of human nature and its potential for transformation.  Along the way we learn why some people and companies struggle to change, despite years of trying, while others seem to remake themselves overnight. We visit laboratories where neuroscientists explore how habits work and where, exactly, they reside in our brains. We discover how the right habits were crucial to the success of Olympic swimmer Michael Phelps, Starbucks CEO Howard Schultz, and civil-rights hero Martin Luther King, Jr. We go inside Procter & Gamble, Target superstores, Rick Warren’s Saddleback Church, NFL locker rooms, and the nation’s largest hospitals and see how implementing so-called keystone habits can earn billions and mean the difference between failure and success, life and death. At its core, The Power of Habit contains an exhilarating argument: The key to exercising regularly, losing weight, raising exceptional children, becoming more productive, building revolutionary companies and social movements, and achieving success is understanding how habits work.  Habits aren’t destiny. As Charles Duhigg shows, by harnessing this new science, we can transform our businesses, our communities, and our lives.','the-power-of-habit-why-we-do-what-we-do-in-life-and-business'),(299,'Diary of a Wimpy Kid (Diary of a Wimpy Kid, #1)',399,'Jeff Kinney',3.95,'1,72,590','10,907','English','thumbs/299.jpg',NULL,1,'2016-02-23 14:51:12','0141365099','29748990','Get ready, book 10 in the phenomenally bestselling Diary of a Wimpy Kid series is coming!Life was better in the old days. Or was it?That\'s the question Greg Heffley is asking as his town voluntarily unplugs and goes electronics-free. But modern life has its conveniences, and Greg isn\'t cut out for an old-fashioned world.With tension building inside and outside the Heffley home, will Greg find a way to survive? Or is going \'old school\' just too hard for a kid like Greg.','diary-of-a-wimpy-kid-diary-of-a-wimpy-kid-1'),(305,'Wings of Fire: An Autobiography',325,'A.P.J. Abdul Kalam',4.12,'18,988','566','English','thumbs/305.jpg',NULL,1,'2016-02-23 14:51:12','8173711461','634583','','wings-of-fire-an-autobiography'),(306,'The Immortals of Meluha (Shiva Trilogy, #1)',350,'Amish Tripathi',3.96,'50,054','3,253','English','thumbs/306.jpg',NULL,1,'2016-02-23 14:51:12','9380658826','13625240','Called “archetypal and stirring” by Deepak Chopra, The Immortals of Meluha heralds an exciting new wave of fantasy writing inspired by the ancient civilizations of the East.   Tripathi devoted years to the research of Hindu mythological stories and history, and discussions with his family about the destiny of the human body, mind and soul to create this sweeping and fascinating adaptation of ancient Hindu mythology for modern fantasy readers.   1900 BC in what modern Indians call the Indus Valley Civilization and the inhabitants called the land of Meluha: a near-perfect empire created many centuries earlier by Lord Ram—one of the greatest monarchs that ever lived—faces peril as its primary river, the Saraswati, is slowly drying to exctinction. The Suryavanshi rulers are challenged with devastating terrorist attacks from the east, the land of the Chandravanshis. To make matters worse, the Chandravanshis appear to have allied with the Nagas, an ostracized and sinister race of deformed humans with astonishing martial skills.    The only hope for the Suryavanshis is an ancient legend: When evil reaches epic proportions, when all seems lost, a hero will emerge. Is the unexpected, rough-hewn Tibetan immigrant Shiva that hero? Drawn suddenly to his destiny, duty, and by love, Shiva will attempt to move mountains and lead the Suryavanshi to destroy evil.From the Hardcover edition.','the-immortals-of-meluha-shiva-trilogy-1'),(323,'Batman: The Killing Joke',1099,'Alan Moore',4.36,'94,984','2,367','English','thumbs/323.jpeg',NULL,1,'2016-02-23 14:51:12','1401216676','2233549','Alan Moore cemented his reputation for unparalleled storytelling with wildly acclaimed books such as WATCHMEN and V FOR VENDETTA. Here he takes on some of DC\'s most classic characters, offering his unforgettable version of the disturbing relationship between the Dark Knight and his greatest foe, the Joker.In this groundbreaking work, Moore creates a twisted tale of insanity and human perseverance. Looking to prove that any man can be pushed past his breaking point to madness, the Joker attempts to drive Commissioner Gordon insane. Refusing to give up, Gordon struggles to maintain his sanity with the help of Batman in a desperate effort to best the madman.','batman-the-killing-joke'),(394,'A Christmas Carol',80,'Charles Dickens',3.99,'3,47,416','8,716','English','thumbs/394.jpg',NULL,1,'2016-02-23 14:51:12','1503212831','25239174','A Christmas Carol is a novella by English author Charles Dickens. It was first published by Chapman & Hall on 19 December 1843. Carol tells the story of a bitter old miser named Ebenezer Scrooge and his transformation resulting from a supernatural visit by the ghost of his former business partner Jacob Marley and the Ghosts of Christmases Past, Present and Yet to Come. The novella met with instant success and critical acclaim. The book was written and published in early Victorian era Britain, a period when there was strong nostalgia for old Christmas traditions together with the introduction of new customs, such as Christmas trees and greeting cards. Dickens\' sources for the tale appear to be many and varied, but are, principally, the humiliating experiences of his childhood, his sympathy for the poor, and various Christmas stories and fairy tales','a-christmas-carol'),(402,'Built to Last: Successful Habits of Visionary Companies',629,'James C. Collins',3.94,'29,294','325','English','thumbs/402.jpg',NULL,1,'2016-02-23 14:51:12','1417663847','2103218','This analysis of what makes great companies great has been hailed everywhere as an instant classic and one of the best business titles since In Search of Excellence. The authors, James C. Collins and Jerry I. Porras, spent six years in research, and they freely admit that their own preconceptions about business success were devastated by their actual findings--along with the preconceptions of virtually everyone else. Built to Last identifies 18 \"visionary\" companies and sets out to determine what\'s special about them. To get on the list, a company had to be world famous, have a stellar brand image, and be at least 50 years old. We\'re talking about companies that even a layperson knows to be, well, different: the Disneys, the Wal-Marts, the Mercks.  Whatever the key to the success of these companies, the key to the success of this book is that the authors don\'t waste time comparing them to business failures. Instead, they use a control group of \"successful-but-second-rank\" companies to highlight what\'s special about their 18 \"visionary\" picks. Thus Disney is compared to Columbia Pictures, Ford to GM, Hewlett Packard to Texas Instruments, and so on. The core myth, according to the authors, is that visionary companies must start with a great product and be pushed into the future by charismatic leaders. There are examples of that pattern, they admit: Johnson & Johnson, for one. But there are also just too many counterexamples--in fact, the majority of the \"visionary\" companies, including giants like 3M, Sony, and TI, don\'t fit the model. They were characterized by total lack of an initial business plan or key idea and by remarkably self-effacing leaders. Collins and Porras are much more impressed with something else they shared: an almost cult-like devotion to a \"core ideology\" or identity, and active indoctrination of employees into \"ideologically commitment\" to the company.  The comparison with the business \"B\"-team does tend to raise a significant methodological problem: which companies are to be counted as \"visionary\" in the first place? There\'s an air of circularity here, as if you achieve \"visionary\" status by ... achieving visionary status. So many roads lead to Rome that the book is less practical than it might appear. But that\'s exactly the point of an eloquent chapter on 3M. This wildly successful company had no master plan, little structure, and no prima donnas. Instead it had an atmosphere in which bright people were both keen to see the company succeed and unafraid to \"try a lot of stuff and keep what works.\" --Richard Farr','built-to-last-successful-habits-of-visionary-companies'),(410,'Batman: Year One',899,'Frank Miller',4.22,'1,21,772','1,504','English','thumbs/410.jpg',NULL,1,'2016-02-23 14:51:12','1401207529','59980','Lieutenant James Gordon takes up a new post in the crime-ridden and corrupt city of Gotham, while billionaire Bruce Wayne returns to the scene of his parents\' deaths, intent on punishing the criminal element.Collects BATMAN #404-407.','batman-year-one'),(411,'Batman: Hush',1499,'Jeph Loeb',4.28,'19,606','767','English','thumbs/411.jpg',NULL,1,'2016-02-23 14:51:12','1401223176','6375845','BATMAN: HUSH is a thrilling mystery of action, intrigue, and deception penned by Jeph Loeb (BATMAN: THE LONG HALLOWEEN) and illustrated by comics superstar Jim Lee (ALL STAR BATMAN & ROBIN, THE BOY WONDER) in which Batman sets out to discover the identity of a mysterious mastermind using the Joker, Riddler, Ra\'s al Ghul and the Dark Knight\'s other enemies - and allies - as pawns in a plan to wreak havoc. Volume 1 collects Batman #608 - #612, and volume 2 collects Batman #613 - #619.','batman-hush'),(466,'The Power of Positive Thinking',199,'Norman Vincent Peale',4.07,'43,279','618','English','thumbs/466.jpg',NULL,1,'2016-02-23 14:51:12','0091906385','17613606','\"This book is written with the sole objective of helping the reader achieve a happy, satisfying, and worthwhile life.\" -- Norman Vincent PealeThe precursor to The Secret, The Power of Positive Thinking has helped millions of men and women to achieve fulfillment in their lives. In this phenomenal bestseller, Dr. Peale demonstrates the power of faith in action. With the practical techniques outlined in this book, you can energize your life -- and give yourself the initiative needed to carry out your ambitions and hopes. You\'ll learn how to:  \n   Expect the best and get it \n  \n \n   Believe in yourself and in everything you do \n  \n \n   Develop the power to reach your goals \n  \n \n   Break the worry habit and achieve a relaxed life \n  \n \n   Improve your personal and professional relationships  \n  \n \n   Assume control over your circumstances \n  \n \n   Be kind to yourself \n  \n','the-power-of-positive-thinking'),(507,'Go Set a Watchman',800,'Harper Lee',3.33,'74,319','15,331','English','thumbs/507.jpg',NULL,1,'2016-02-23 14:51:12','1785150286','24831147','From Harper Lee comes a landmark new novel set two decades after her beloved Pulitzer Prize-winning masterpiece, To Kill a Mockingbird.Maycomb, Alabama. Twenty-six-year-old Jean Louise Finch--\"Scout\"--returns home from New York City to visit her aging father, Atticus. Set against the backdrop of the civil rights tensions and political turmoil that were transforming the South, Jean Louise\'s homecoming turns bittersweet when she learns disturbing truths about her close-knit family, the town and the people dearest to her. Memories from her childhood flood back, and her values and assumptions are thrown into doubt. Featuring many of the iconic characters from To Kill a Mockingbird, Go Set a Watchman perfectly captures a young woman, and a world, in a painful yet necessary transition out of the illusions of the past--a journey that can be guided only by one\'s conscience. Written in the mid-1950s, Go Set a Watchman imparts a fuller, richer understanding and appreciation of Harper Lee. Here is an unforgettable novel of wisdom, humanity, passion, humor and effortless precision--a profoundly affecting work of art that is both wonderfully evocative of another era and relevant to our own times. It not only confirms the enduring brilliance of To Kill a Mockingbird, but also serves as its essential companion, adding depth, context and new meaning to an American classic.','go-set-a-watchman'),(522,'The Power of Your Subconscious Mind',195,'Joseph Murphy',4.12,'15,020','693','English','thumbs/522.jpg',NULL,1,'2016-02-23 14:51:12','9380227582','13307199','Chapter after chapter, this astounding book combines ancient wisdom with modern science to bring its readers not only new insights but actual techniques they can use in daily living.','the-power-of-your-subconscious-mind'),(894,'Agatha Christie - Murder on the Orient Express',199,'Agatha Christie',4.12,'1,25,717','5,398','English','thumbs/894.jpg',NULL,1,'2016-02-23 14:51:12',NULL,NULL,NULL,'agatha-christie-murder-on-the-orient-express'),(1193,'Brown Bear, Brown Bear, What Do You See?',250,'Eric Carle',4.17,'1,12,737','2,227','English','thumbs/1193.jpg',NULL,1,'2016-02-23 14:51:12','0141501596','2936433','Exuberantly coloured artwork and favourite animals make this rhythmic story the perfect introduction to looking and learning about colours. Each spread leads seamlessly into the next and young children will delight in Eric\'s colourful collage animals and simple repetitive language.','brown-bear-brown-bear-what-do-you-see'),(1819,'Five Point Someone',176,'Chetan Bhagat',3.45,'57,321','1,505','English','thumbs/1819.jpg',NULL,1,'2016-02-23 14:51:12','8129135493','25359433','Five Point Someone is Chetan Bhagat\'s debut novel which revolves around the lives of Ryan, Alok, and Hari. The three lads become close friends while trying hard to survive in an exceedingly competitive environment. The three boys join IIT with a passion to excel and come out successfully as the best graduates. However, their life turns upside down when their grades fall lower than they had ever expected. Meanwhile, Hari falls in love with his professor\'s daughter, and Alok and Ryan cannot stop disputing each other. Five Point Someone was successfully able to strike a chord with the millions of youngsters across India. Hari, Alok and Ryan have to deal with unpleasant and cynical teachers, assignments and projects, stress of unending examinations, and a stringent academic schedule. Will they be able to survive the IITs? Or will they succumb to the tedious and age-old education system of India? Five Point Someone has been adapted into hugely successful motion pictures both in Tamil and Hindi.','five-point-someone'),(2014,'Geronimo Stilton - The Kingdom of Fantasy',499,'Geronimo Stilton',4.3,'2,137','154','English','thumbs/2014.jpg',NULL,1,'2016-02-23 14:51:12','935103951X','27071570','An adventure of epic proportions!I, Geronimo Stilton, had returned to the Kingdom of Fantasy on the wings of the Phoenix of Destiny! Blossom, Queen of the Fairies, needed my help once again.But Blossom was behaving strangely. She sent me off on quest after magical quest, each one more bizarre and dangerous than the last. It felt like my missions were building up to something truly terrible right under my snout. Could my friends and I put things right again? It\'s a story full of twists and turns, mazes and puzzles, and tons of fantastical creatures!','geronimo-stilton-the-kingdom-of-fantasy'),(2058,'The God of Small Things',450,'Arundhati Roy',3.89,'1,52,583','7,415','English','thumbs/2058.jpg',NULL,1,'2016-02-23 14:51:12','014302857X','1939864','\"Novel debutan seorang perempuan muda yang langsung mengorbit dan menimbulkan kontroversi!\"Sebuah kisah yang sanggup menghunjam sampai ke relung-relung emosi pembaca yang terdalam.... Beberapa kali saya berhenti untuk menarik napas karena terkejut sekali dengan karakter-karakter yang ditampilkan, atau saya harus membaca ulang suatu frasa atau halaman untuk menikmati keindahannya.MEERA SYAL, Sunday ExpressSetelah Anda menutup halaman terakhir, Anda seolah masih berada di dalamnya... Menghayati sebuah tragedi jauh sebelum kita menyadarinya.LAURA SHAPIRO, NewsweekMenyuguhkan sebuah kepedihan yang misterius dan magis, sehingga tidak heran, setelah menyelesaikan halaman terakhir, pembaca pasti akan memutuskan untuk mengulangi langsung sekali lagi.DEIRDA DONAHUE, USA TodayYang membuat novel ini disanjung para kritikus adalah strukturnya yang sangat rumit dan apik, gaya bahasa yang liris, sarat simile dan metafor, alusi, dan permainan kata yang lincah, penuh humor sekaligus menggigit.MELANI BUDIANTA','the-god-of-small-things'),(2071,'Grandma\'s Bag of Stories (English)',250,'Sudha Murty',NULL,NULL,'','English','thumbs/2071.jpeg',NULL,1,'2016-02-23 14:51:12','0143333623','25662311','When Grandma opens her bag of stories everyone gathers around. Who can resist a good story, especially when it\'s being told by Grandma? From her bag emerges tales of kings and cheats, monkeys and mice, bears and gods. Here comes the bear who ate some really bad dessert and got very angry a lazy man who would not put out a fire till it reached his beard a princess who got turned into an onion a queen who discovered silk and many more weird and wonderful people and animals. Grandma tells the stories over long summer days and nights, as seven children enjoy life in her little town. The stories entertain, educate and provide hours of enjoyment to them. So come, why don\'t you too join in the fun.','grandma-s-bag-of-stories-english'),(2083,'Great Stories for Children',195,'Ruskin Bond',3.88,'42','2','English','thumbs/2083.jpg',NULL,1,'2016-02-23 14:51:12','8129118920','16143582','Great Stories for Children is a potpourri of short stories that effectively transports the reader to the fascinating world of its endearing characters. The ensemble includes Tutu the monkey who is fond of troubling the no-nonsense Aunt Ruby, a pet python who makes sudden appearances at the most unusual places, a troublesome Pret who enjoys stirring up the household he resides in, three young children stranded on the Haunted Hill, Himalayan bears who feast on pumpkins, plums and apricots, a crafty thief who has a change of heart, and Ruskin Bond himself who meets a ghost at a resort in the middle of the night ...','great-stories-for-children'),(2190,'Hooked: How to Build Habit-Forming Products',599,'Nir Eyal',4.02,'4,113','369','English','thumbs/2190.jpg',NULL,1,'2016-02-23 14:51:12','0241184835','22935795','Why do some products capture our attention while others flop? What makes us engage with certain things out of sheer habit? Is there an underlying pattern to how technologies hook us?Nir Eyal answers these questions (and many more) with the Hook Model - a four-step process that, when embedded into products, subtly encourages customer behaviour. Through consecutive \"hook cycles,\" these products bring people back again and again without depending on costly advertising or aggressive messaging.Hooked is based on Eyal\'s years of research, consulting, and practical experience. He wrote the book he wished had been available to him as a start-up founder - not abstract theory, but a how-to guide for building better products. Hooked is written for product managers, designers, marketers, start-up founders, and anyone who seeks to understand how products influence our behaviour.Eyal provides readers with practical insights to create user habits that stick; actionable steps for building products people love; and riveting examples from the iPhone to Twitter, Pinterest and the Bible App.Nir Eyal spent years in the video gaming and advertising industries where he learned, applied, and at times rejected, techniques described in Hooked to motivate and influence users. He has taught courses on applied consumer psychology at the Stanford Graduate School of Business and the Hasso Plattner Institute of Design and is a frequent speaker at industry conferences and at Fortune 500 companies. His writing on technology, psychology, and business appears in the Harvard Business Review, The Atlantic, TechCrunch, and Psychology Today.Ryan Hoover\'s writing has appeared in Tech- Crunch, The Next Web, Forbes, and Fast Company. After working on Hooked with Nir Eyal, Hoover founded Product Hunt, a company that has been described as \"the place to discover the next big things in tech.\"','hooked-how-to-build-habit-forming-products'),(2202,'How I Braved Anu Aunty & Co-Founded a Million Dollar Company',195,'Varun Agarwal',3.71,'3,870','449','English','thumbs/2202.jpg',NULL,1,'2016-02-23 14:51:12','812911979X','14347714','How I Braved Anu Aunty and Co-Founded A Million Dollar Company by Varun Agarwal is a compelling and humorous account of the fulfilment of entrepreneurial dreams.How does an unfocused young person such as Varun Agarwal, become the co-founder of a million dollar company? How does he get pesky Anu Aunty off his trail? The book is an interesting real-life story of how the author, Varun Agarwal, managed to brave all odds to reach the peak of his career.Varun Agarwal is shown to be an unfocused human being, with no real interest in pursuing a career, even though he does harbour dreams of becoming a successful entrepreneur. Varun whiles away his time, hopping from pub to pub, spending time with friends and keeping a track of his love interest on Facebook.These traits worry his mother to the bone, compelling her to put the very meddlesome Anu Aunty on the job, to help get her son moving in the right direction in life. Anu Aunty does a rather good job of this, much to Varun\'s dismay. He then does all that he can to get her off his track, while pursuing his dreams to become an entrepreneur.How I Braved Anu Aunty and Co-Founded A Million Dollar Company is the author’s debut novel and is on its fourth reprint already. Having sold twenty thousand copies in only a month, the book has become a bestseller by national standards. It has also occupied a firm foothold on the bestseller charts for eighty days at a stretch. The author attained initial popularity with his Facebook blog posts, a few of which were sent to his publishers. The book was conceived once they demanded a full manuscript.','how-i-braved-anu-aunty-co-founded-a-million-dollar-company'),(2466,'It Started with a Friend Request',175,'Sudeep Nagarkar',3.65,'1,564','147','English','thumbs/2466.jpg',NULL,1,'2016-02-23 14:51:12','8184004206','18029845','A brand new love story and a story of friendship from the bestselling author of Few Things Left Unsaid and That’s the Way We Met! It will take every emotions to one step higher.Why don’t we feel the moment when we fall in love but always remember when it ends? Akash is young, single, and conservative with a preference for girls with brains than in miniskirts. One day, he runs into free-spirited Aleesha at a local discotheque. A Mass Media student, Aleesha is a pampered brat, the only child of her parents who dote on her. This brief meeting leads them to exchange their BlackBerry pins and they begin chatting regularly. As BlackBerry plays cupid, they fall in love. When they hit a rough patch in their life, Aditya, Akash’s close pal, guides them through it.But just when they are about to take their relationship to the next level, a sudden misfortune strikes. Can Aditya bring Akash’s derailed life back on track?It Started with a Friend Request is a true story which will make you believe in love like you never knew before.','it-started-with-a-friend-request'),(2702,'Malala: The Girl Who Stood Up for Education and Changed the World',299,'Malala Yousafzai',4,'1,19,509','9,086','English','thumbs/2702.jpg',NULL,1,'2016-02-23 14:51:12','1780622333','25516571','The Girl Who Stood Up for Education and was Shot by the Taliban.The highly anticipated memoir of Malala Yousafzai, the schoolgirl from Pakistan\'s Swat region who stood up to the Taliban.\'I come from a country that was created at midnight. When I almost died it was just after midday. We\'d finished for the day and I was on the open-back truck we use as a school bus. There were no windows, just thick plastic sheeting that flapped at the sides and a postage stamp of open sky at the back through which I caught a glimpse of a kite wheeling up and down. It was pink, my favourite colour.\'In 2009 Malala Yousafzai began writing an anonymous blog for BBC Urdu about life in the Swat Valley as the Taliban gained control, at times banning girls from attending school. When her identity was discovered, Malala began to appear in Pakistani and international media, campaigning for education for all. On 9 October 2012, Malala was shot at point-blank range by a member of the Taliban on the way home from school. Remarkably, she survived. In April 2013, Time magazine named her one of the 100 Most Influential People in the World.I Am Malala tells the inspiring story of a schoolgirl who was determined not to be intimidated by extremists, and faced the Taliban with immense courage. Malala speaks of her continuing campaign for every girl\'s right to an education, shining a light into the lives of those children who cannot attend school. This is just the beginning...','malala-the-girl-who-stood-up-for-education-and-changed-the-world'),(2708,'Man Who Mistook His Wife for a Hat (English)',450,'',4.02,'82,561','3,061','English','thumbs/2708.jpeg',NULL,1,'2016-02-23 14:51:12','1447275403','23075720','','man-who-mistook-his-wife-for-a-hat-english'),(2869,'Mr. Brown Can Moo! Can You?',99,'Dr. Seuss',4.11,'40,014','523','English','thumbs/2869.jpg',NULL,1,'2016-02-23 14:51:12','0007414145','24844143','Moo moo! Hoo hoo! Cock-a-doodle-doo! Oh, the wonderful sounds Mr. Brown can do. w see if you can do them too! This fabulous book is ideal for teaching young children all about noises! This delightful book forms part of the second stage in HarperCollins major Dr. Seuss rebrand programme. With the relaunch of 10 more titles in August 2003, such all-time favourites as How the Grinch Stole Christmas!, Mr. Brown Can Moo! Can You? and Dr. Seuss Sleep Book boast bright new covers that incorporate much needed guidance on reading levels: Blue Back Books are for parents to share with young children, Green Back Books are for budding readers to tackle on their own, and Yellow Back Books are for older, more fluent readers to enjoy. Mr. Brown Can Moo! Can You? belongs to the Blue Back Book range.','mr-brown-can-moo-can-you'),(3101,'Our Moon Has Blood Clots: A Memoir of a Lost Home in Kashmir',350,'Rahul Pandita',4.11,'1,611','246','English','thumbs/3101.jpg',NULL,1,'2016-02-23 14:51:12','818400513X','23261012','Rahul Pandita was fourteen years old in 1990 when he was forced to leave his home in Srinagar along with his family, who were Kashmiri Pandits: the Hindu minority within a Muslim majority Kashmir that was becoming increasingly agitated with the cries of ‘Azadi’ from India. The heartbreaking story of Kashmir has so far been told through the prism of the brutality of the Indian state, and the pro-independence demands of separatists. But there is another part of the story that has remained unrecorded and buried. Our Moon Has Blood Clots is the unspoken chapter in the story of Kashmir, in which it was purged of the Kashmiri Pandit community in a violent ethnic cleansing backed by Islamist militants. Hundreds of people were tortured and killed, and about 3,50,000 Kashmiri Pandits were forced to leave their homes and spend the rest of their lives in exile in their own country. Rahul Pandita has written a deeply personal, powerful and unforgettable story of history, home and loss.','our-moon-has-blood-clots-a-memoir-of-a-lost-home-in-kashmir'),(3156,'Percy Jackson and the Lightning Thief',350,'Rick Riordan',4.2,'10,99,798','37,809','English','thumbs/3156.jpg',NULL,1,'2016-02-23 14:51:12','0141329998','6692896','Percy Jackson is a 12-year-old boy with Dyslexia and ADHD, and he has been expelled from four schools, the last being Yancy Academy. Sally, Percy\'s mother, takes Percy on a trip to Long Island to get him away from his stepfather who mistreats him.Percy is attacked by a former teacher, Mrs. Dodds, who is revealed to be one of the Furies who are out to kill Percy. Sally and Percy are soon joined by Grover Underwood, Percy\'s closest friend from Yancy Academy. Sally takes the children to Camp Half-Blood, a camp for Demigods.There, Percy is put in the Hermes cabin in the charge of Counsellor Luke Castellan. During a game, the Ares cabin attacks Percy. But Percy is healed on entering the waters of a nearby river. Soon revelations follow regarding the relationship between Percy and Poseidon.Meanwhile, the Bolt of Zeus is stolen and Percy is accused of stealing it by Zeus. Percy is accompanied by his friends Grover and Annabeth.They eventually reach Hades\' palace after encountering many hassles on the way. There, Hades accuses Percy of stealing his Helm of Darkness. Percy now has to find the helm as well as the bolt. The story further reveals the following. Will Percy be successful in finding both the bolt and helm? If Percy is innocent, who is the actual thief?About Rick RiordanRick Riordan is an American writer who had previously written books for adults - the award winning Tres Navarre Mystery series.The story inspired a series of books. The first book in the Percy Jackson series, Percy Jackson and The Lightning Thief, was published in 2005.Riordan was born in 1964 in San Antonio, Texas. He studied at Alamo Heights High School and graduated fro the University of Texas with majors in English and Social Studies. Rick Riordan entertained his sons by telling them stories from Greek mythology. Soon, he ran out of stories and started making up his own stories. He created a character called Percy Jackson, who was the son of the Greek God Poseidon and also created a st','percy-jackson-and-the-lightning-thief'),(3164,'Persepolis',599,'Marjane Satrapi',2.67,'3','1','English','thumbs/3164.jpg',NULL,1,'2016-02-23 14:51:12',NULL,NULL,NULL,'persepolis'),(3386,'Revolution 2020: Love.Corruption.Ambition',176,'Chetan Bhagat',3.08,'34,782','1,412','English','thumbs/3386.jpg',NULL,1,'2016-02-23 14:51:12','8129118807','12615008','Book Summary of Revolution 2020 Once upon a time, in small-town India, there lived two intelligent boys. One wanted to use his intelligence to make money. One wanted to use his intelligence to create a revolution. The problem was, they both loved the same girl. Welcome to Revolution 2020. A story about childhood friends Gopal, Raghav and Aarti who struggle to find success and love in Varanasi. However, it isn\'t easy to achieve this in an unfair society that rewards the corrupt. As Gopal gives in to the system, and Raghav fights it, who will win? From the bestselling author of Five Point Someone, one night @ the call center, The Three Mistakes of My Life and 2 States, comes another gripping tale from the heartland of India. Are you ready for the revolution?','revolution-2020-love-corruption-ambition'),(3387,'ReWork: Change the Way You Work Forever',650,'Jason Fried, David Heinemeier Hansson',3.92,'64,280','2,290','English','thumbs/3387.jpg',NULL,1,'2016-02-23 14:51:12','0091929784','7861053','From the founders of the trailblazing software company 37signals, here is a different kind of business book - one that explores a new reality. Today, anyone can be in business. Tools that used to be out of reach are now easily accessible. Technology that cost thousands is now just a few pounds or even free. Stuff that was impossible just a few years ago is now simple.That means anyone can start a business. And you can do it without working miserable 80-hour weeks or depleting your life savings. You can start it on the side while your day job provides all the cash flow you need. Forget about business plans, meetings, office space - you don\'t need them.With its straightforward language and easy-is-better approach, Rework is the perfect playbook for anyone who\'s ever dreamed of doing it on their own. Hardcore entrepreneurs, small-business owners, people stuck in day jobs who want to get out, and artists who don\'t want to starve anymore will all find valuable inspiration and guidance in these pages.It\'s time to rework work.','rework-change-the-way-you-work-forever'),(3521,'Sita: Daughter of the Earth (Mythology)',250,'Saraswati Nagpal',NULL,NULL,'','English','thumbs/3521.jpg',NULL,1,'2016-02-23 14:51:12','9380028377','10440586','In an ancient age, when gods and goddesses walked with mortals......Sita is the kind-hearted and intelligent princess of the kingdom of Videha. Married to Rama, prince of Ayodhya, her journey in life takes her from exhilaration to anguish.Along the way, she has to leave behind the luxury of royal comforts and live the simple, harsh life of a forest dweller, where danger is lurking in every shadow.Ensnared in the evil plans of the wicked demon-king Ravana, Sita is abducted and hidden away in Lanka. Will Rama muster up a strong army to rescue Sita from the demon\'s clutches? Will Sita return to Ayodhya to become queen of the land... or is she destined to be mistrusted and live alone for the rest of her life?Adapted from the ancient Indian epic, the Ramayana, this is a touching tale of love, honor, and sacrifice that reveals one woman\'s shining strength in an unforgiving world.','sita-daughter-of-the-earth-mythology'),(3758,'The 4-Hour Body: An Uncommon Guide To Rapid Fat-Loss, Incredible Sex And Becoming Superhuman',799,'Timothy Ferriss',3.73,'15,613','1,121','English','thumbs/3758.jpg',NULL,1,'2016-02-23 14:51:12','0091939526','9512557','Thinner, bigger, faster, stronger... which 150 pages will you read?  Is it possible to:  Reach your genetic potential in 6 months? Sleep 2 hours per day and perform better than on 8 hours? Lose more fat than a marathoner by bingeing?  Indeed, and much more. This is not just another diet and fitness book.  \"The 4-Hour Body\" is the result of an obsessive quest, spanning more than a decade, to hack the human body. It contains the collective wisdom of hundreds of elite athletes, dozens of MDs, and thousands of hours of jaw-dropping personal experimentation. From Olympic training centers to black-market laboratories, from Silicon Valley to South Africa, Tim Ferriss, the #1 \"New York Times\" bestselling author of \"The 4-Hour Workweek, \" fixated on one life-changing question:  For all things physical, what are the tiniest changes that produce the biggest results?  Thousands of tests later, this book contains the answers for both men and women.  From the gym to the bedroom, it\'s all here, and it all works.  YOU WILL LEARN (in less than 30 minutes each):  How to lose those last 5-10 pounds (or 100+ pounds) with odd combinations of food and safe chemical cocktails. * How to prevent fat gain while bingeing (X-mas, holidays, weekends) * How to increase fat-loss 300% with a few bags of ice * How Tim gained 34 pounds of muscle in 28 days, without steroids, and in four hours of \"total\" gym time * How to sleep 2 hours per day and feel fully rested * How to produce 15-minute female orgasms * How to triple testosterone and double sperm count* How to go from running 5 kilometers to 50 kilometers in 12 weeks * How to reverse \"permanent\" injuries * How to add 150+ pounds to your lifts in 6 months * How to pay for a beach vacation with one hospital visit  And that\'s just the tip of the iceberg. There are more than 50 topics covered, all with real-world experiments, many including more than 200 test subjects.  You don\'t need better genetics or more discipline. You need immediate results that compel you to continue.  That\'s exactly what \"The 4-Hour Body\" delivers.','the-4-hour-body-an-uncommon-guide-to-rapid-fat-loss-incredible-sex-and-becoming-superhuman'),(3789,'The Art of War',295,'Sun Tzu',3.94,'1,51,692','4,476','English','thumbs/3789.jpg',NULL,1,'2016-02-23 14:51:12','0486460061','2598340','An eyewitness to most of the important battles of the Napoleonic Wars, Baron Antoine Henri de Jomini served with both the French and the Anglo-Allied armies. His firsthand accounts of the conflicts are the most authoritative ever written, hailed by experts as both accurate and insightful. It endures as the definitive work on strategy and tactics and as a fundamental source of modern military thought. In fact, generals on both sides of the American Civil War were well schooled in The Art of War. Jomini approaches warfare from several directions, including strategy, tactics, logistics, engineering, and diplomacy. He examines each in turn, and he offers an analysis of strategic problems posed by a variety of theaters and terrains, the tactics of attack and defense, surprise maneuvers, special operations, the importance of reconnaissance, and the deployment of forces.Few can match the breadth of advice offered by the man who was critical to the success of both Napoleon and Czar Alexander I. Unsurpassed in its influence on military thinking, doctrine, and vocabulary, Jomini\'s classic remains both a historic and practical guide to students of warfare.','the-art-of-war'),(3951,'The Gita: For Children',299,'Roopa Pai',4.67,'15','5','English','thumbs/3951.jpg',NULL,1,'2016-02-23 14:51:12','9351950123','27838195','It’s one of the oldest books in the world and India’s biggest blockbuster bestseller! — But isn’t it meant only for religious old people? — But isn’t it very long... and, erm, super difficult to read? — But isn’t the stuff it talks about way too complex for regular folks to understand? Prepare to besurprised. Roopa Pai’s spirited, one-of-a-kind retelling of the epic conversation between Pandava prince Arjuna and his mentor and friendKrishna busts these and other such myths about the Bhagavad Gita. Lucid, thought-provoking and brimming with fun trivia, this book will staywith you long after you have turned the last page. Why haven’t you read it yet?','the-gita-for-children'),(4051,'The Lean Startup: How Today\'s Entrepreneurs Use Continuous Innovation to Create Radically Successful Businesses',650,'Eric Ries',4.01,'40,790','1,237','English','thumbs/4051.jpg',NULL,1,'2016-02-23 14:51:12','0307887898','10127019','Most startups fail. But many of those failures are preventable.  The Lean Startup is a new approach being adopted across the globe, changing the way companies are built and new products are launched. Eric Ries defines a startup as an organization dedicated to creating something new under conditions of extreme uncertainty. This is just as true for one person in a garage or a group of seasoned professionals in a Fortune 500 boardroom. What they have in common is a mission to penetrate that fog of uncertainty to discover a successful path to a sustainable business. The Lean Startup approach fosters companies that are both more capital efficient and that leverage human creativity more effectively.  Inspired by lessons from lean manufacturing, it relies on “validated learning,” rapid scientific experimentation, as well as a number of counter-intuitive practices that shorten product development cycles, measure actual progress without resorting to vanity metrics, and learn what customers really want. It enables a company to shift directions with agility, altering plans inch by inch, minute by minute. Rather than wasting time creating elaborate business plans, The Lean Startup offers entrepreneurs - in companies of all sizes - a way to test their vision continuously, to adapt and adjust before it’s too late. Ries provides a scientific approach to creating and managing successful startups in a age when companies need to innovate more than ever.','the-lean-startup-how-today-s-entrepreneurs-use-continuous-innovation-to-create-radically-successful-businesses'),(4418,'Train to Pakistan',250,'Khushwant Singh',3.82,'9,623','564','English','thumbs/4418.jpg',NULL,1,'2016-02-23 14:51:12','0143065882','9500142','','train-to-pakistan'),(4445,'Turning Point: A Journey through Challenges',225,'A.P.J. Abdul Kalam',3.99,'1,886','97','English','thumbs/4445.jpg',NULL,1,'2016-02-23 14:51:12','9350293471','15735106','It was like any other day on the Anna University campus in Chennai. I had delivered a lecture \'Vision to Mission\' and the session got extended from one hour to two. I had lunch with a group of research students and went back to class. As I was returning to my rooms in the evening the vice-chancellor, Prof. A. Kalanidhi, fell in step with me. Someone had been frantically trying to get in touch with me through the day, he said. Indeed, the phone was ringing when I entered the room. When I answered, a voice at the other end said, \'The prime minister wants to talk with you ...\' Some months earlier, I had left my post as principal scientific adviser to the government of India, a Cabinet-level post, to return to teaching. Now, as I spoke to the PM, Atal Bihari Vajpayee, my life was set for an unexpected change. Turning Points takes up the incredible Kalam story from where Wings of Fire left off. It brings together details from his career and presidency that are not generally known as he speaks out for the first time on certain points of controversy. It offers insight not only into an extraordinary personality but also a vision of how a country with a great heritage can become great in accomplishment, skills and abilities through effort, perseverance and confidence. It is a continuing saga, above all, of a journey, individual and collective, that will take India to 2020 and beyond as a developed nation.','turning-point-a-journey-through-challenges'),(4576,'Who Will Cry When You Die?',175,'Robin S. Sharma',3.89,'6,405','378','English','thumbs/4576.jpg',NULL,1,'2016-02-23 14:51:12','8179922324','1285114','Would you like to replace that empty feeling inside you with a deep sense of peace, passion, and purpose? Are you hoping that your life will not only be successful but significant? Are you ready to have the very best within you shine through and create a rich legacy in the process? If so, this potent little book, with its powerful life lessons and its gentle but profound wisdom, is exactly what you need to rise to your next level of living.Offering 101 simple solutions to life\'s most frustrating challenges, bestselling author and life leadership guru Robin Sharma will show you exactly how to recreate your life so that you feel strikingly happy, beautifully fulfilled, and deeply peaceful. This is a truly remarkable book that readers will treasure for a lifetime','who-will-cry-when-you-die'),(4648,'Zero to One: Notes on Start Ups, or How to Build the Future',499,'Peter Thiel, Blake Masters',4.15,'22,459','1,434','English','thumbs/4648.jpg',NULL,1,'2016-02-23 14:51:12','0753555190','18070752','Peter Thiel is the co-founder of PayPal and the first outside investor in Facebook. In the Spring of 2012, he gave a lecture course at Stanford for software engineers, calling on them to think boldly and broadly about how they might use their skills to shape the future, and imparting the lessons he has gleaned from his own experience. One of the students in that class - Blake Masters - took notes and posted them online. The blog posts became a huge success, with hundreds of thousands of hits, and became the basis for Zero to One.We live in an age of technological stagnation, even if we\'re too distracted by our new mobile devices to notice. Progress has stalled in every industry except computers, and globalization is hardly the revolution people think it is. It\'s true that the world can get marginally richer by building new copies of old inventions, making horizontal progress from \'1 to n\'. But true innovators have nothing to copy. The most valuable companies of the future will make vertical progress from \'0 to 1\', creating entirely new industries and products that have never existed before. Zero to One is about how to build these companies.A business book that also provides insight into the world of start-ups from a Silicon Valley icon, Thiel shows how to pursue your goals using the most important, most difficult, and most underrated skill in every job or industry: thinking for yourself.','zero-to-one-notes-on-start-ups-or-how-to-build-the-future'),(4650,'Harry Potter and the Sorcerer\'s Stone (Harry Potter, #1)',831,'J.K. Rowling',4.4,'35,59,756','52,885','English','thumbs/4650.jpg',NULL,1,'2016-02-23 14:51:12',NULL,NULL,'','harry-potter-and-the-sorcerer-s-stone-harry-potter-1'),(4697,'The Wonderful Wizard of Oz (Oz, #1)',56,'L. Frank Baum',3.97,'2,29,504','6,925','English','thumbs/4697.jpg',NULL,1,'2016-02-23 14:51:12','9380028075','8648915','Follow the yellow brick road!Dorothy thinks she\'s lost forever when a tornado whirls her and her dog, Toto, into a magical world. To get home, she must find the wonderful wizard in the Emerald City of Oz. On the way she meets the Scarecrow, the Tin Woodman and the Cowardly Lion. But the Wicked Witch of the West has her own plans for the new arrival - will Dorothy ever see Kansas again?','the-wonderful-wizard-of-oz-oz-1'),(4724,'Walden',125,'Henry David Thoreau',3.79,'98,926','2,836','English','thumbs/4724.jpg',NULL,1,'2016-02-23 14:51:12','9350330776','24278866','Walden by Henry David Thoreau is a gripping account of personal independence and details more than two years of the author’s experiences living in a cabin near Walden Pond. The book uses the four seasons as themes to represent the development and spiritual discovery.Inspired heavily by transcendental philosophy,Walden details the rich benefits obtained by the soul on account of a humble lifestyle. Thoreau was allowed to build a cabin and maintain a garden by his close friend and mentor Ralph Waldo Emerson, and would earn his keep by performing various chores around the woodland. The book is an attempt to delink intellectual and moral superiority from poverty. Some other areas covered in the book include classical literature and its benefits, support for philosophers and wise individuals, recollections of the author’s former places of residence and human existence free from social and societal obligations. Thoreau also places particular importance on the wonderfulness of human solitude and loneliness. Societal escape is seen as pleasurable amidst nature and all its benefits.WALDEN could sell only two thousand copies in five years, but the book came to be regarded as a classic later on. The book is now one of the most acclaimed and celebrated literary works in America. The book has remained popular owing to its promise of a better life for the reader.','walden'),(4824,'The House at Pooh Corner (Winnie-the-Pooh, #2)',199,'A.A. Milne',4.35,'63,654','680','English','thumbs/4824.jpg',NULL,1,'2016-02-23 14:51:12','1405280840','29611124','\"Nearly eleven o\'clock,\" said Pooh happily... \"Time for a little smackerel of something.\"Pooh and Piglet are adventuring again with their friends in Hundred Acre Wood. Tigger finds out what Tiggers like, Piglet does a Very Grand Thing and Christopher Robin and Pooh discover a wonderful Enchanted Place.','the-house-at-pooh-corner-winnie-the-pooh-2'),(5161,'Fox in Socks (Dr Seuss - Green Back Book)',157,'Dr. Seuss',4.01,'35,706','870','English','thumbs/5161.jpg',NULL,1,'2016-02-23 14:51:12','0007414196','25275504','In this hilarious book, the irrepressible Fox in Socks teaches a baffled Mr. Knox some of the slickest, quickest tongue-twisters in town. With his unique combination of hilarious stories, zany pictures and riotous rhymes, Dr. Seuss has been delighting young children and helping them learn to read for over fifty years. Creator of the wonderfully anarchic Cat in the Hat, and ranked among the UK\'s top ten favourite children\'s authors, Seuss is firmly established as a global best-seller, with nearly half a billion books sold worldwide. As the first step in a major rebrand programme, HarperCollins is relaunching 17 of Dr. Seuss\'s best-selling books, including such perennial favourites as The Cat in the Hat, Green Eggs and Ham and Fox in Socks. In response to consumer demand, the bright new cover designs incorporate much needed guidance on reading levels, with the standard paperbacks divided into three reading strands -- Blue Back Books for parents to share with young children, Green Back Books for budding readers to tackle on their own, and Yellow Back Books for older, more fluent readers to enjoy. Fox in Socks belongs to the Green Back Book range.','fox-in-socks-dr-seuss-green-back-book'),(5319,'The Jungle Book',199,'Rudyard Kipling',3.98,'67,798','1,427','English','thumbs/5319.jpg',NULL,1,'2016-02-23 14:51:12','1509808361','30213960','The wild adventures of Mowgli in Rudyard Kipling\'s The Jungle Book are well-loved, timeless tales of growing up and finding a place in the world. First Stories: The Jungle Book is a perfect introduction for young children to this classic story and its host of animal characters. Push, pull and slide mechanisms to bring the story to life and see favourite scenes in action. Mowgli, Baloo, Bagheera and of course the fearsome tiger Shere Khan are all beautifully imagined by Miriam Bos in her bold, appealing illustrations.','the-jungle-book'),(5504,'A Suitable Boy (A Suitable Boy, #1)',995,'Vikram Seth',4.08,'30,449','1,426','English','thumbs/5504.jpg',NULL,1,'2016-02-23 14:51:12',NULL,NULL,NULL,'a-suitable-boy-a-suitable-boy-1'),(5545,'The Twilight Saga (Twilight, #1-4)',399,'Stephenie Meyer',3.88,'85,605','3,332','English','thumbs/5545.jpg',NULL,1,'2016-02-23 14:51:12',NULL,NULL,NULL,'the-twilight-saga-twilight-1-4'),(5552,'For One More Day',299,'Mitch Albom',4.07,'94,098','5,717','English','thumbs/5552.jpeg',NULL,1,'2016-02-23 14:51:12','0751537535','2977413','Charley Benetto is a broken man, his life destroyed by alcohol and regret. He loses his job. He leaves his family. He hits rock bottom after discovering he won\'t be invited to his only daughter\'s wedding. And he decides to take his own life.Charley takes a midnight ride to his small hometown: his final journey. But as he staggers into his old house, he makes an astonishing discovering. His mother - who died eight years earlier - is there, and welcomes Charley home as if nothing had ever happened.What follows is the one seemingly ordinary day so many of us year for: a chance to make good with a lost parent, to explain the family secrets and to seek forgiveness.','for-one-more-day'),(5788,'Think and Grow Rich',150,'Napoleon Hill',4.13,'84,705','2,178','English','thumbs/5788.jpg',NULL,1,'2016-02-23 14:51:12','817234564X','28458682','BOOKS','think-and-grow-rich'),(6043,'The 4-Hour Workweek',699,'Timothy Ferriss',3.78,'53,392','3,055','English','thumbs/6043.jpg',NULL,1,'2016-02-23 14:51:12','0307465357','6444424','More than 100 pages of new, cutting-edge content. Forget the old concept of retirement and the rest of the deferred-life plan there is no need to wait and every reason not to, especially in unpredictable economic times. Whether your dream is escaping the rat race, experiencing high-end world travel, earning a monthly five-figure income with zero management, or just living more and working less, The 4-Hour Workweek is the blueprint. This step-by-step guide to luxury lifestyle design teaches:  How Tim went from $40,000 per year and 80 hours per week to $40,000 per month and 4 hours per week. How to outsource your life to overseas virtual assistants for $5 per hour and do whatever you want How blue-chip escape artists travel the world without quitting their jobs How to eliminate 50% of your work in 48 hours using the principles of a forgotten Italian economist How to trade a long-haul career for short work bursts and frequent mini-retirements The new expanded edition of Tim Ferriss The 4-Hour Workweek includes:  More than 50 practical tips and case studies from readers (including families) who have doubled income, overcome common sticking points, and reinvented themselves using the original book as a starting point Real-world templates you can copy for eliminating e-mail, negotiating with bosses and clients, or getting a private chef for less than $8 a meal How Lifestyle Design principles can be suited to unpredictable economic times The latest tools and tricks, as well as high-tech shortcuts, for living like a diplomat or millionaire without being either\"','the-4-hour-workweek'),(6809,'Fantastic Beasts and Where to Find Them',496,'Newt Scamander',3.94,'1,59,986','2,686','English','thumbs/6809.jpg',NULL,1,'2016-02-23 14:51:12','0545850568','24612590','Straight from the library at Hogwarts School of Witchcraft and Wizardry, a book of magical creatures that no Harry Potter fan should be without!A copy of Fantastic Beasts & Where to Find Them resides in almost every wizarding household in the country. Now Muggles too have the chance to discover where the Quintaped lives, what the Puffskein eats, and why it is best not to leave milk out for a Knarl.Proceeds from the sale of this book will go to Comic Relief, which means that the dollars and Galleons you exchange for it will do magic beyond the powers of any wizard. If you feel that this is insufficient reason to part with your money, I can only hope that passing wizards feel more charitable if they see you being attacked by a Manticore.--Albus Dumbledore','fantastic-beasts-and-where-to-find-them'),(6911,'Fantastic Mr. Fox',350,'Roald Dahl',4,'57,235','2,075','English','thumbs/6911.jpg',NULL,1,'2016-02-23 14:51:12','0141346442','17242192','Nobody outfoxes Fantastic Mr. Fox!Someone\'s been stealing from the three meanest farmers around, and they know the identity of the thief—it\'s Fantastic Mr. Fox! Working alone they could never catch him; but now fat Boggis, squat Bunce, and skinny Bean have joined forces, and they have Mr. Fox and his family surrounded. What they don\'t know is that they\'re not dealing with just any fox—Mr. Fox would rather die than surrender. Only the most fantastic plan can save him now.','fantastic-mr-fox'),(7696,'A Painted House',399,'John Grisham',3.64,'55,921','2,907','English','thumbs/7696.jpg',NULL,1,'2016-02-23 14:51:12','0099416158','45149','The hill people and the Mexicans arrived on the same day. It was a Wednesday, early in September 1952. The Cardinals were five games behind the Dodgers with two weeks to go, and the season looked hopeless. The cotton, however, was waist high to my father, almost over my head, and he and my grandfather could be heard before supper whispering words that were seldom heard. It could be a \"good crop.\" Thus begins the new novel from John Grisham, a story inspired by his own childhood in rural Arkansas. The narrator is a seven year old farm boy named Luke Chandler, who lives in the cotton fields with his parents and grandparents in a little house that\'s never been painted. The Chandlers farm eighty acres that they rent, not own, and when the cotton is ready they hire a truckload of Mexicans and a family from the Ozarks to help harvest it.For six weeks they pick cotton, battling the heat, the rain, the fatigue, and sometimes, each other. As the weeks pass Luke sees and hears things no seven year old could possibly be prepared for, and finds himself keeping secrets that not only threaten the crop but will change the lives of the Chandlers forever. A Painted House is a moving story of one boy\'s journey from innocence to experience.','a-painted-house'),(14415,'The Hard Thing About Hard Things: Building a Business When There Are No Easy Answers',699,'Ben Horowitz',4.13,'9,747','631','English','thumbs/14415.jpg',NULL,1,'2016-02-23 14:51:12','1483002888','21509468','Ben Horowitz, cofounder of Andreessen Horowitz and one of Silicon Valley s most respected and experienced entrepreneurs, offers essential advice on building and running a startup practical wisdom for managing the toughest problems business school doesn t cover, based on his popular blog.While many people talk about how great it is to start a business, very few are honest about how difficult it is to run one. Ben Horowitz analyzes the problems that confront leaders every day, sharing the insights he s gained developing, managing, selling, buying, investing in, and supervising technology companies. A lifelong rap fanatic, he amplifies business lessons with lyrics from his favorite songs, telling it straight about everything from firing friends to poaching competitors, from cultivating and sustaining a CEO mentality to knowing the right time to cash in.Filled with his trademark humor and straight talk, \"The Hard Thing about Hard Things\" is invaluable for veteran entrepreneurs as well as those aspiring to their own new ventures, drawing from Horowitz s personal and often humbling experiences.\"','the-hard-thing-about-hard-things-building-a-business-when-there-are-no-easy-answers'),(18315,'Pinocchio (Puffin Classics)',198,'Carlo Collodi',3.84,'46,780','1,078','English','thumbs/18315.jpg',NULL,1,'2016-02-23 14:51:12','0142437069','245757','Pinocchio plays pranks upon the kindly woodcarver Geppetto, is duped by the Fox and the Cat, kills the pedantic Talking Cricket, and narrowly escapes death, with the help of the blue-haired Fairy. A wooden puppet without strings, Pinocchio is a tragicomic figure, a poor, illiterate, naughty peasant boy who has few choices in life but usually chooses to shirk his responsibilities and get into trouble. This sly and imaginative novel, alternately catastrophic and ridiculous, takes Pinocchio from one predicament to the next, and finally to an optimistic, if uncertain, ending. In his compelling introduction, Jack Zipes places Pinocchio within the traditions of the oral folk tale and the literary fairy tale, showing how Collodi subverts those traditions while raising questions about \"how we \'civilize\' children in uncivilized times.\"For more than seventy years, Penguin has been the leading publisher of classic literature in the English-speaking world. With more than 1,700 titles, Penguin Classics represents a global bookshelf of the best works throughout history and across genres and disciplines. Readers trust the series to provide authoritative texts enhanced by introductions and notes by distinguished scholars and contemporary authors, as well as up-to-date translations by award-winning translators.','pinocchio-puffin-classics'),(18341,'The Testament',193,'John Grisham',3.81,'77,858','1,934','English','thumbs/18341.jpg',NULL,1,'2016-02-23 14:51:12','0099245027','832625','Troy Phelen is a self-made billionaire, one of the richest men in the United States. He is also eccentric, reclusive, confined to a wheelchair, and looking for a way to die.Nate O\'Riley is a high-octane Washington litigator who\'s lived too hard, too fast, for too long. Emerging from his fourth stay in rehab he knows returning to the real world is always difficult, but this time it\'s going to be murder.Rachel Lane is a young woman who chose to give her life to God, who walked away from the modern world with all its strivings and trappings and encumbrances, and went to live and work with a primitive tribe of Indians in the deepest jungles of Brazil.In a story that mixes legal suspense with a remarkable adventure, their lives are forever altered by the startling secret of The Testament.','the-testament'),(18372,'Stay Hungry Stay Foolish',142,'Rashmi Bansal',3.6,'7,170','244','English','thumbs/18372.jpg',NULL,1,'2016-02-23 14:51:12','9381626715','4765642','The inspiring stories of 25 IIM Ahmedabad graduates who chose the rough road of entrepreneurship. They are diverse in age, in outlook and the industries they made a mark in. But they have one thing in common: they believed in the power of their dreams. This book seeks to inspire young graduates to look beyond placements and salaries. To believe in their dreams.','stay-hungry-stay-foolish'),(18377,'Playing It My Way',337,'Sachin Tendulkar',3.68,'3,052','378','','thumbs/18377.jpg',NULL,1,'2016-02-23 14:51:12','1473605202','23150337','The Record setting blockbuster is back… for another innings! \"I knew that if I agreed to write my story, I would have to be completely honest, as that’s the way I have always played the game, and that would mean talking about a number of things I have not addressed in public before. So here I am, at the end of my final innings, having taken that last walk back to the pavilion, ready to recount as many incidents as I can remember since first picking up a cricket bat as a child in Mumbai thirty-five years ago.\". -- Sachin Tendulkar\nThe greatest run-scorer in the history of cricket, Sachin Tendulkar retired in 2013 after an astonishing 24 years at the top. The most celebrated Indian cricketer of all time, he received the Bharat Ratna - India\'s highest civilian honour - on the day of his retirement. Now Sachin Tendulkar tells his own remarkable story - from his first Test cap at the age of 16 to his 100th international century and the emotional final farewell that brought his country to a standstill. When a boisterous Mumbai youngster\'s excess energies were channelled into cricket, the result was record-breaking schoolboy batting exploits that launched the career of a cricketing phenomenon. Before long Sachin Tendulkar was the cornerstone of India\'s batting line-up, his every move watched by a cricket-mad nation\'s devoted followers.\n  His many achievements with India include winning the World Cup and topping the world Test rankings. Yet he has also known his fair share of frustration and failure - from injuries and early World Cup exits to stinging criticism from the press, especially during his unhappy tenure as captain.\n Despite his celebrity status, Sachin Tendulkar has always remained a very private man, devoted to his family and his country. Now, for the first time, he provides a fascinating insight into his personal life and gives a frank and revealing account of a sporting life like no other.\nThe book is in Sachin\'s own words as told to his co-writer Boria Majumdar who worked closely with Sachin.','playing-it-my-way'),(18406,'Good To Great: Why Some Companies Make the Leap...And Others Don\'t',584,'James C. Collins',4.01,'69,581','2,517','English','thumbs/18406.jpg',NULL,1,'2016-02-23 14:51:12','1591397758','122236','In 1996, John P. Kotter\'s Leading Change became a runaway best seller, outlining an eight-step program for organizational change that was embraced by executives around the world. Then, Kotter and co-author Dan Cohen\'s The Heart of Change introduced the revolutionary \"see-feel-change\" approach, which helped executives understand the crucial role of emotion in successful change efforts. Now, The Heart of Change Field Guide provides leaders and managers tools, frameworks, and advice for bringing these breakthrough change methods to life within their own organizations. Written by Dan Cohen and with a foreword by John P. Kotter, the guide provides a practical framework for implementing each step in the change process, as well as a new three-phase approach to execution: creating a climate for change, engaging and enabling the whole organization, and implementing and sustaining change. Hands-on diagnostics—including a crucial \"change readiness module\"—reveal the dynamics that will help or hinder success at each phase of the change process. Both flexible and scaleable, the frameworks presented in this guide can be tailored for any size or type of change initiative. Filled with practical tools, checklists, and expert commentary, this must-have guide translates the most powerful approaches available for creating successful change into concrete, actionable steps for you and your organization. Dan Cohen is the co-author, with John P. Kotter, of The Heart of Change, and a principal with Deloitte Consulting, LLC.','good-to-great-why-some-companies-make-the-leap-and-others-don-t'),(18425,'Our Impossible Love',86,'Durjoy Datta',3.53,'96','20','English','thumbs/18425.jpg',NULL,1,'2016-02-23 14:51:12','0143424610','28794287','','our-impossible-love'),(18430,'Life is What You Make it',60,'Preeti Shenoy',3.51,'8,889','578','English','thumbs/18430.jpg',NULL,1,'2016-02-23 14:51:12','9380349300','11256293','','life-is-what-you-make-it'),(18431,'My Gita',147,'Devdutt Pattanaik',4.15,'266','49','English','thumbs/18431.jpg',NULL,1,'2016-02-23 14:51:12','8129137704','27318490','','my-gita'),(18450,'Tales of Krishna: 3 in 1 (Amar Chitra Katha)',129,'Anant Pai',0,'0','0','English','thumbs/18450.jpg',NULL,1,'2016-02-23 14:51:12','8184820666','26232061','- India\'s leading comic book series on History, Mythology and Folklore - 90 million copies sold over 40 years in 20 languages - Teaches children Indian stories and culture, and enjoyed by adults as well Includes the following titles: KrishnaKrishna and RukminiThe Syamantaka Gem','tales-of-krishna-3-in-1-amar-chitra-katha'),(18484,'Shall We Tell the President?',399,'Jeffrey Archer',3.65,'11,857','371','English','thumbs/18484.jpg',NULL,1,'2016-03-03 23:28:02','1447221842','21031922','','shall-we-tell-the-president'),(18501,'Search & Social: The Definitive Guide to Real-Time Content Marketing',499,'Rob Garner',0,'0','0','',NULL,NULL,1,'2016-03-12 11:27:19','1846041244','17304997','Psychiatrist Viktor Frankl\'s memoir has riveted generations of readers with its descriptions of life in Nazi death camps and its lessons for spiritual survival. Between 1942 and 1945, Frankl labored in four different camps, including Auschwitz, while his parents, brother, and pregnant wife perished. Based on his own experience and the experiences of others he treated later in his practice, Frankl argues that we cannot avoid suffering, but we can choose how to cope with it, find meaning in it, and move forward with renewed purpose. Frankl\'s theory--known as logotherapy, from the Greek word logos (\"meaning\")--holds that our primary drive in life is not pleasure, as Freud maintained, but the discovery and pursuit of what we personally find meaningful.At the time of Frankl\'s death in 1997, Man\'s Search for Meaning had sold more than 10 million copies in twenty-four languages. A 1991 reader survey for the Library of Congress that asked readers to name a \"book that made a difference in your life\" found Man\'s Search for Meaning among the ten most influential books in America.','search-social-the-definitive-guide-to-real-time-content-marketing'),(18580,'Fun in Devlok Omnibus',399,'Devdutt Pattanaik',3.62,'8','0','',NULL,NULL,1,'2016-04-13 08:20:54','0143333445','25647292','Why is Indra an unhappy god? Why is the cow such a cool animal? Who is the demon of forgetfulness? Master storyteller Devdutt Pattnaik answers these curious questions and reveals many more secrets of the world of gods and demons in this delightfully illustrated omnibus, featuring all six tales in the Fun in Devlok series.Follow Harsha as he discovers the secret to happiness, listen to Gauri’s fascinating conversation with a talking cow, play dumb charades with Shiva, find out why identity cards are important even for Krishna, join the fight between between Kama and Yama, and learn why the river Saraswati disappeared mysteriously. Jump right in. The gates of Devlok are open.','fun-in-devlok-omnibus'),(18583,'Old Hat New Hat (Bright & Early Board Books(TM))',250,'Stan Berenstain',4.28,'1,701','76','English','thumbs/18583.jpg',NULL,1,'2016-04-13 08:26:54','0679886303','1963060','Brother Bear explores the concepts of size and shape as he shops for a new hat. He tries on frilly hats and silly hats, bumpy hats and lumpy hats, until he finds the most perfect hat of all--his own!  ','old-hat-new-hat-bright-early-board-books-tm'),(18651,'The Whole-Brain Child: 12 Revolutionary Strategies to Nurture Your Child\'s Developing Mind',799,'Daniel J. Siegel',4.1,'4,153','458','English','thumbs/18651.jpg',NULL,1,'2016-04-30 08:50:53','0553386697','13584326','NEW YORK TIMES BESTSELLER“Simple, smart, and effective solutions to your child’s struggles.”—Harvey Karp, M.D.  “Daniel Siegel and Tina Payne Bryson have created a masterly, reader-friendly guide to helping children grow their emotional intelligence. This brilliant method transforms everyday interactions into valuable brain-shaping moments. Anyone who cares for children—or who loves a child—should read The Whole-Brain Child.”—Daniel Goleman, author of Emotional Intelligence   In this pioneering, practical book, Daniel J. Siegel, neuropsychiatrist and author of the bestselling Mindsight, and parenting expert Tina Payne Bryson offer a revolutionary approach to child rearing with twelve key strategies that foster healthy brain development, leading to calmer, happier children. The authors explain—and make accessible—the new science of how a child’s brain is wired and how it matures. The “upstairs brain,” which makes decisions and balances emotions, is under construction until the mid-twenties. And especially in young children, the right brain and its emotions tend to rule over the logic of the left brain. No wonder kids throw tantrums, fight, or sulk in silence. By applying these discoveries to everyday parenting, you can turn any outburst, argument, or fear into a chance to integrate your child’s brain and foster vital growth.                Complete with age-appropriate strategies for dealing with day-to-day struggles and illustrations that will help you explain these concepts to your child, The Whole-Brain Child shows you how to cultivate healthy emotional and intellectual development so that your children can lead balanced, meaningful, and connected lives. “[A] useful child-rearing resource for the entire family . . . The authors include a fair amount of brain science, but they present it for both adult and child audiences.”—Kirkus Reviews\n \n“Strategies for getting a youngster to chill out [with] compassion.”—The Washington Post\n \n“This erudite, tender, and funny book is filled with fresh ideas based on the latest neuroscience research. I urge all parents who want kind, happy, and emotionally healthy kids to read The Whole-Brain Child. This is my new baby gift.”—Mary Pipher, Ph.D., author of Reviving Ophelia and The Shelter of Each Other“Gives parents and teachers ideas to get all parts of a healthy child’s brain working together.”—Parent to Parent','the-whole-brain-child-12-revolutionary-strategies-to-nurture-your-child-s-developing-mind'),(18653,'Watchmen: International Edition',1199,'Alan Moore',4.33,'354,556','9,719','English','thumbs/18653.jpg',NULL,1,'2016-05-02 06:05:36','1401248195','18373361','In an alternate world where the mere presence of American superheroes changed history, the US won the Vietnam War, Nixon is still president, and the cold war is in full effect.  WATCHMEN begins as a murder-mystery, but soon unfolds into a planet-altering conspiracy. As the resolution comes to a head, the unlikely group of reunited heroes--Rorschach, Nite Owl, Silk Spectre, Dr. Manhattan and Ozymandias--have to test the limits of their convictions and ask themselves where the true line is between good and evil. In the mid-eighties, Alan Moore and Dave Gibbons created WATCHMEN, changing the course of comics\' history and essentially remaking how popular culture perceived the genre. Popularly cited as the point where comics came of age, WATCHMEN\'s sophisticated take on superheroes has been universally acclaimed for its psychological depth and realism.WATCHMEN is collected here with a new cover, sketches, extra bonus material and a new introduction by series artist Dave Gibbons.','watchmen-international-edition'),(18660,'Transmetropolitan Vol. 1: Back on the Street',899,'Warren Ellis',4.22,'32,084','701','English','thumbs/18660.jpg',NULL,1,'2016-05-04 08:28:33','1401220843','3931645','After years of self-imposed exile from a civilization rife with degradation and indecency, cynical journalist Spider Jerusalem is forced to return to a job that he hates and a city that he loathes. Working as an investigative reporter for the newspaper The Word, Spider attacks the injustices of his surreal 23rd Century surroundings. Combining black humor, life-threatening situations, and moral ambiguity, this book is the first look into the mind of an outlaw journalist and the world he seeks to destroy.','transmetropolitan-vol-1-back-on-the-street'),(18671,'Time for Bed',424,'Mem Fox',4.15,'12,610','305','English','thumbs/18671.jpg',NULL,1,'2016-05-06 12:57:32','0152010661','835495','Darkness is falling everywhere and little ones are getting sleepy, feeling cozy, and being tucked in. It’s time for a wide yawn, a big hug, and a snuggle under the covers--sleep tight! “Working beautifully with the soothingly repetitive text, each painting conveys a warm feeling of safety and affection.”--School Library Journal','time-for-bed'),(18672,'How Do Dinosaurs Count to Ten? (Scholastic Question & Answer)',367,'Jane Yolen',4.03,'1,334','43','English','thumbs/18672.jpg',NULL,1,'2016-05-06 13:24:20','0439649498','122105','The bestselling, award-winning team of Yolen and Teague present their beloved dinosaurs in a new format with this fun, read-aloud board book that teaches young children to count from one to ten!Come along for some BIG fun as your favorite dinosaurs delight young readers with their playful antics. How do dinosaurs count to ten? Over and over and over again!This brand new board book format brings the gigantic humor of bestselling, award-winning team Jane Yolen and Mark Teague to the youngest readers, helping them learn to count from one to ten with a simple, rhyming text and laugh-out-loud illustrations! A perfect companion book to the other HOW DO DINOSAURS tales, and a great baby gift as well.','how-do-dinosaurs-count-to-ten-scholastic-question-answer'),(18675,'Don\'t Let the Pigeon Drive the Bus',245,'Mo Willems',4.29,'53,883','2,445','English','thumbs/18675.jpg',NULL,1,'2016-05-06 14:04:40','1844285138','899775','When the driver leaves the bus temporarily, he gives the reader just one instruction: Don\'t let the pigeon drive the bus! But, boy, that pigeon tries every trick in the book to get in that driving seat: he whines, wheedles, fibs and flatters. Will you let him drive? Told entirely in speech bubbles, this is a brilliantly original book.','don-t-let-the-pigeon-drive-the-bus'),(18727,'Forget Me Not, Stranger',175,'Novoneel Chakraborty',3.69,'228','42','','thumbs/18727.jpg',NULL,1,'2016-05-21 16:58:46','8184007302','29351209','I m Rivanah Bannerjee 23 F Mumbai. Some of you might already know how my life is on a razor edge. Those of you who don t just know this I may be killed soon . . . by the Stranger. I don t know who or what he is a ghost a person or a figment of my imagination? All I know is he isn t just one thing he is sexy and scary terrific and terrifying. What I don t understand is why a young harmless girl like me who works in a big city stays away from her parents and has a screwed-up love life would be of any interest to him. Unless there is something about my own story that I do not know . . .In the hotly anticipated final instalment of the Stranger trilogy Rivanah will learn the answers to her many questions What is it that binds her to the dead Hiya? Who is the Stranger? Why has he been following her all this while? leading to an intense breathtaking climax. About the AuthorNovoneel Chakraborty is the bestselling author of six romantic thrillers. Forget Me Not Stranger is his seventh novel and third in the immensely popular Stranger trilogy. He works in the Indian films and television industry penning popular shows like Million Dollar Girl Twist Wala Love and Secret Diaries for Channel V. He lives in Mumbai.','forget-me-not-stranger'),(18840,'She Swiped Right into My Heart',175,'Sudeep Nagarkar',3.76,'49','12','','thumbs/18840.jpg',NULL,1,'2016-06-16 08:13:59','8184007450','29772476','Every girl needs just one man to prove that not all men are the same!! Shibani, an extreme feminist who feels all men are same is a biker by passion and a BFF to Geet, one of the most unpopular girls in the college who is often tagged as a ‘Nerd’ or a ‘Freak’. To win the popularity vote, Geet strikes an unusual deal with college hottie Rudra – to be her ‘Fake Boyfriend’. Will the deal backfire?Tushita, deceived by love only finds her prince in the diary she writes. Vivaan, an endangered species of ‘Friend’ who can accept even your candy crush request. Do people like them even exist? An unlikely truth about Shibani unfolds and as misunderstandings and jealousies take centre stage, each one of them must make a decision that will not just affect their own life, but also those of their loved ones! She Swiped Right Into My Heart is an unconventional story not just about love or relationship but which will send chills down your spine breaking preconceived notion of a stereotypical society that you are Straight!','she-swiped-right-into-my-heart'),(24390,'Ignited Minds',199,'A.P.J. Abdul Kalam',3.9,'6,565','214','English','thumbs/24390.jpg',NULL,1,'2016-07-06 12:33:20','0143424122','27259470','When A.P.J. Abdul Kalam wrote India 2020: A Vision for the New Millennium with Y.S. Rajan in 1998, little did they expect the magnitude of the response they would get. The idea that India could actually be a developed nation in a short time rather than remain condemned to a subsistence diet of marginal improvements and promises struck a chord among readers. The book continues to be a bestseller. Ignited Minds: Unleashing the Power Within India goes the logical next step and examines why, given all our skills, resources and talents, we, so obviously capable of being the best, settle so often for the worst. What is it that we as a nation are missing? For at the heart of Ignited Minds is an irresistible premise: the people of a nation have the power, by dint of hard work, to realize their dream of a truly good life.  Kalam offers no formulaic prescription in Ignited Minds. Instead, he takes up different issues and themes that struck him on his pilgrimage around the country as he met thousands of school children, teachers, scientists and saints and seers in the course of two years: the necessity for a patriotism that transcends religion and politics; for role models who point out the path to take; and for confidence in ourselves and in our strengths.  Who was he to write on so large a theme, he wondered as he started writing this book. But at the end, Kalam\'s humility notwithstanding, this may well prove to be the book that motivates us to get back on the winning track and unleash the energy within a nation that hasn\'t allowed itself full rein.','ignited-minds');

-- --------------------------------------------------------

--
-- Table structure for table `items_categories`
--

CREATE TABLE IF NOT EXISTS `items_categories` (
  `item_id` int(20) NOT NULL,
  `category_id` int(3) DEFAULT NULL,
  UNIQUE KEY `item_cat` (`item_id`,`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `items_categories`
--

INSERT INTO `items_categories` VALUES (1,18),(1,161),(1,280),(1,371),(1,449),(2,161),(2,280),(2,449),(2,627),(3,161),(3,280),(3,371),(3,449),(3,615),(4,77),(4,96),(4,161),(4,374),(4,487),(4,527),(5,161),(5,270),(5,280),(5,449),(5,627),(9,18),(9,161),(9,280),(9,449),(9,799),(16,280),(16,370),(16,371),(16,799),(17,134),(17,161),(17,280),(17,552),(17,558),(20,134),(20,161),(20,270),(20,280),(20,799),(32,161),(32,270),(32,280),(32,389),(32,627),(34,134),(34,161),(34,280),(34,552),(34,558),(37,161),(37,270),(37,280),(37,549),(40,134),(40,161),(40,270),(40,280),(40,552),(51,161),(51,270),(51,280),(66,180),(66,280),(66,600),(66,615),(66,799),(76,134),(76,161),(76,270),(76,280),(76,799),(87,161),(87,188),(87,280),(87,513),(88,161),(88,280),(88,371),(88,449),(143,27),(143,197),(143,280),(143,529),(143,734),(151,27),(151,161),(151,280),(151,449),(151,627),(165,527),(165,549),(165,583),(165,635),(165,675),(177,188),(177,280),(177,513),(177,701),(177,726),(205,161),(205,188),(205,211),(205,280),(205,513),(210,226),(210,280),(210,371),(210,513),(210,726),(217,170),(217,172),(217,280),(217,346),(217,636),(224,96),(224,117),(224,374),(224,527),(224,626),(224,715),(238,25),(238,133),(238,180),(238,280),(238,615),(238,787),(247,117),(247,399),(247,527),(247,548),(247,635),(265,56),(265,134),(265,161),(265,280),(265,552),(281,270),(281,280),(281,516),(296,117),(296,527),(296,548),(296,583),(296,635),(299,134),(299,280),(299,389),(299,600),(299,799),(305,77),(305,96),(305,197),(305,527),(306,270),(306,280),(306,371),(306,516),(323,172),(323,280),(323,346),(323,636),(394,161),(394,280),(394,371),(394,380),(394,449),(402,117),(402,437),(402,471),(402,527),(402,635),(410,172),(410,280),(410,346),(410,636),(411,170),(411,172),(411,346),(411,636),(411,696),(466,117),(466,527),(466,548),(466,583),(466,635),(507,26),(507,161),(507,280),(507,370),(507,448),(522,527),(522,548),(522,583),(522,635),(522,675),(1193,56),(1193,134),(1193,161),(1193,280),(1193,552),(2058,180),(2058,197),(2058,280),(2058,449),(2058,529),(2190,117),(2190,527),(2202,117),(2202,303),(2202,389),(2202,527),(2466,197),(2466,280),(2466,451),(2466,615),(2869,134),(2869,161),(2869,270),(2869,280),(2869,552),(3386,197),(3386,280),(3386,529),(3386,615),(3387,810),(3758,362),(3758,527),(3758,533),(3758,603),(3758,635),(3789,161),(3789,374),(3789,527),(3789,549),(4051,117),(4051,471),(4051,527),(4051,810),(4418,161),(4418,197),(4418,280),(4418,371),(4648,810),(4650,27),(4650,134),(4650,270),(4650,280),(4650,468),(4650,799),(4697,134),(4697,161),(4697,270),(4697,280),(4697,799),(4724,77),(4724,161),(4724,242),(4724,487),(4724,518),(4724,527),(4724,549),(4824,56),(4824,134),(4824,161),(4824,270),(4824,280),(5161,134),(5161,161),(5161,280),(5161,552),(5161,558),(5319,134),(5319,161),(5319,270),(5319,280),(5504,161),(5504,197),(5504,280),(5504,371),(5545,270),(5545,542),(5545,615),(5545,756),(5545,799),(5552,25),(5552,180),(5552,280),(5552,399),(5552,529),(5788,527),(5788,548),(5788,549),(5788,583),(5788,635),(6043,117),(6043,527),(6043,548),(6043,635),(6809,134),(6809,270),(6809,280),(6809,799),(6911,134),(6911,161),(6911,270),(6911,280),(6911,799),(7696,280),(7696,371),(7696,513),(7696,701),(7696,726),(14415,117),(14415,437),(14415,471),(14415,527),(14415,810),(18315,18),(18315,134),(18315,161),(18315,197),(18315,259),(18315,266),(18315,270),(18315,449),(18315,529),(18315,799),(18341,27),(18341,188),(18341,226),(18341,280),(18341,513),(18341,529),(18341,607),(18341,701),(18341,726),(18372,96),(18372,117),(18372,471),(18372,527),(18372,635),(18377,77),(18377,96),(18377,527),(18377,678),(18406,437),(18406,471),(18406,527),(18406,635),(18430,133),(18430,180),(18430,197),(18430,280),(18430,399),(18430,583),(18430,615),(18430,618),(18430,635),(18430,787),(18431,197),(18431,270),(18431,516),(18431,527),(18431,675),(18484,188),(18484,226),(18484,280),(18484,371),(18484,513),(18484,514),(18484,529),(18484,562),(18484,701),(18484,726),(18583,56),(18583,134),(18583,161),(18583,280),(18583,422),(18583,552),(18583,690),(18583,816),(18651,24),(18651,134),(18651,237),(18651,268),(18651,521),(18651,546),(18651,583),(18651,626),(18651,635),(18651,815),(18653,161),(18653,172),(18653,233),(18653,270),(18653,280),(18653,346),(18653,347),(18653,513),(18653,627),(18653,696),(18660,170),(18660,172),(18660,175),(18660,200),(18660,233),(18660,280),(18660,346),(18660,347),(18660,389),(18660,627),(18671,11),(18671,56),(18671,134),(18671,268),(18671,280),(18671,552),(18671,558),(18671,572),(18671,690),(18671,816),(18672,134),(18672,215),(18672,280),(18672,481),(18672,552),(18672,572),(18672,690),(18675,56),(18675,100),(18675,134),(18675,270),(18675,280),(18675,303),(18675,389),(18675,552),(18675,690),(18675,816),(18727,726),(24390,96),(24390,393),(24390,399),(24390,815);

-- --------------------------------------------------------

--
-- Table structure for table `item_isbn`
--

CREATE TABLE IF NOT EXISTS `item_isbn` (
  `item_id` int(6) NOT NULL,
  `isbn_10` varchar(20) DEFAULT NULL,
  `isbn_13` varchar(20) DEFAULT NULL,
  `publisher` varchar(100) DEFAULT NULL,
  `publication_year` varchar(100) DEFAULT NULL,
  `dimensions` varchar(50) DEFAULT NULL,
  `num_pages` int(6) DEFAULT NULL,
  `binding_type` varchar(20) DEFAULT NULL,
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `item_isbn`
--


-- --------------------------------------------------------

--
-- Table structure for table `item_requests`
--

CREATE TABLE IF NOT EXISTS `item_requests` (
  `id` int(3) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `author` varchar(20) DEFAULT NULL,
  `user_id` int(6) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `query` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=71 ;

--
-- Dumping data for table `item_requests`
--

-- --------------------------------------------------------

--
-- Table structure for table `lenders`
--

CREATE TABLE IF NOT EXISTS `lenders` (
  `lender_id` int(6) NOT NULL AUTO_INCREMENT,
  `item_id` int(6) NOT NULL,
  `inventory_id` int(10) unsigned NOT NULL,
  `user_id` int(6) NOT NULL,
  `status_id` int(6) NOT NULL DEFAULT '1',
  `order_placed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `delivery_date` timestamp NULL DEFAULT NULL,
  `pickup_date` timestamp NULL DEFAULT NULL,
  `delivery_slot` int(2) NOT NULL,
  `pickup_slot` int(2) NOT NULL,
  `address_id` int(2) NOT NULL,
  PRIMARY KEY (`lender_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=106 ;

--
-- Dumping data for table `lenders`
--

-- --------------------------------------------------------

--
-- Table structure for table `mongo_mapping`
--



-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE IF NOT EXISTS `orders` (
  `order_id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(6) unsigned NOT NULL,
  `address_id` int(6) NOT NULL,
  `order_placed` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `order_status` int(11) NOT NULL DEFAULT '1' COMMENT '1:placed;2:pickupUpl;3:enroute;4:delivered;5:return enroute;6:returned',
  `order_return` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '1 week from order by default',
  `charge` int(3) NOT NULL DEFAULT '0',
  `delivery_date` timestamp NULL DEFAULT NULL,
  `delivery_slot` tinyint(1) DEFAULT NULL,
  `pickup_slot` tinyint(1) DEFAULT NULL,
  `payment_mode` enum('wallet','cash') NOT NULL DEFAULT 'cash',
  `parent_id` int(6) DEFAULT '0',
  `from_collection` int(3) DEFAULT NULL,
  `bought` tinyint(1) NOT NULL DEFAULT '0',
  `bought_on` timestamp NULL DEFAULT NULL,
  `source` enum('web','android') NOT NULL DEFAULT 'android',
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=684 ;

--
-- Dumping data for table `orders`
--



-- --------------------------------------------------------

--
-- Table structure for table `orders_admin_notes`
--

CREATE TABLE IF NOT EXISTS `orders_admin_notes` (
  `order_id` int(6) NOT NULL,
  `admin_id` int(3) DEFAULT NULL,
  `comment` varchar(1000) NOT NULL,
  `order_type` enum('borrow','lend') NOT NULL,
  `edited` tinyint(1) NOT NULL DEFAULT '0',
  `delivered_by` varchar(100) DEFAULT NULL,
  `delivery_amount` int(3) DEFAULT NULL,
  `picked_by` varchar(100) DEFAULT NULL,
  `pickup_amount` int(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `orders_admin_notes`
--



-- --------------------------------------------------------

--
-- Table structure for table `order_history`
--

CREATE TABLE IF NOT EXISTS `order_history` (
  `inventory_id` int(6) NOT NULL,
  `item_id` int(6) NOT NULL,
  `order_id` int(6) NOT NULL,
  UNIQUE KEY `inv_order` (`inventory_id`,`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `order_history`
--



-- --------------------------------------------------------

--
-- Table structure for table `preregisters`
--

CREATE TABLE IF NOT EXISTS `preregisters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `referrals`
--

CREATE TABLE IF NOT EXISTS `referrals` (
  `referral_id` int(6) NOT NULL AUTO_INCREMENT,
  `referrer_id` int(6) DEFAULT NULL,
  `google_uuid` varchar(100) DEFAULT NULL,
  `referent_id` int(6) DEFAULT NULL,
  `activated` tinyint(1) NOT NULL DEFAULT '0',
  `referral_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `activation_date` timestamp NULL DEFAULT NULL,
  `incentive_amount` int(6) NOT NULL DEFAULT '200',
  `source` enum('phone','invite_code') DEFAULT NULL,
  `source_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`referral_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE IF NOT EXISTS `reviews` (
  `review_id` int(6) NOT NULL AUTO_INCREMENT,
  `user_id` int(6) NOT NULL,
  `item_id` int(6) NOT NULL,
  `order_id` int(6) NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `edited` tinyint(1) NOT NULL DEFAULT '0',
  `date_edited` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`review_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=99 ;

--
-- Dumping data for table `reviews`
--

--
-- Table structure for table `reviews_edit_log`
--

CREATE TABLE IF NOT EXISTS `reviews_edit_log` (
  `review_id` int(6) NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `reviews_edit_log`
--

--
-- Table structure for table `search_fails`
--

CREATE TABLE IF NOT EXISTS `search_fails` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `user_id` int(6) DEFAULT NULL,
  `query` varchar(100) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `type` varchar(20) DEFAULT NULL,
  `flow` varchar(10) DEFAULT NULL,
  `item_id` int(6) DEFAULT NULL,
  `refined_query` varchar(100) DEFAULT NULL,
  `gcm_id` varchar(200) DEFAULT NULL,
  `gcm_token` varchar(200) DEFAULT NULL,
  `uuid` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2494 ;

--
-- Dumping data for table `search_fails`
--

-- --------------------------------------------------------

--
-- Table structure for table `temp_address`
--

-- --------------------------------------------------------

--
-- Table structure for table `time_slots`
--

CREATE TABLE IF NOT EXISTS `time_slots` (
  `slot_id` tinyint(1) NOT NULL AUTO_INCREMENT,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`slot_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `time_slots`
--

INSERT INTO `time_slots` (`slot_id`, `start_time`, `end_time`, `active`) VALUES
(1, '08:00:00', '10:00:00', 1),
(2, '13:00:00', '15:00:00', 0),
(3, '17:00:00', '19:00:00', 1),
(4, '20:00:00', '22:00:00', 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(6) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `google_id` varchar(500) DEFAULT NULL,
  `gcm_id` varchar(1000) DEFAULT NULL,
  `picture_url` varchar(500) DEFAULT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_app_version` varchar(20) DEFAULT NULL,
  `last_used_timestamp` timestamp NULL DEFAULT NULL,
  `source` varchar(20) NOT NULL DEFAULT 'android',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=739 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `name`, `email`, `phone`, `google_id`, `gcm_id`, `picture_url`, `date_created`, `last_app_version`, `last_used_timestamp`, `source`) VALUES
(1, 'anant718@gmail.com', '', 'Anant Gupta', 'anant718@gmail.com', '9654009368', '117352240705527072265', '', 'https://lh3.googleusercontent.com/-3Pviu-Bl59o/AAAAAAAAAAI/AAAAAAAACJ4/5GzVEEZ8Ods/photo.jpg', '2016-01-07 05:53:52', '11049904', '2016-10-12 13:11:39', 'paypal');

-- --------------------------------------------------------

--
-- Table structure for table `users_unregistered`
--

CREATE TABLE IF NOT EXISTS `users_unregistered` (
  `mixpanel_id` varchar(200) DEFAULT NULL,
  `gcm_id` varchar(200) DEFAULT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_addresses`
--

CREATE TABLE IF NOT EXISTS `user_addresses` (
  `address_id` int(6) NOT NULL AUTO_INCREMENT,
  `user_id` int(6) NOT NULL,
  `address` varchar(1000) NOT NULL,
  `description` varchar(200) NOT NULL,
  `locality` varchar(200) NOT NULL,
  `landmark` varchar(200) NOT NULL,
  `latitude` varchar(20) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL,
  `is_valid` tinyint(1) NOT NULL DEFAULT '1',
  `delivery_message` varchar(500) DEFAULT NULL,
  `time_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `distance` float DEFAULT NULL,
  PRIMARY KEY (`address_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=660 ;

--
-- Dumping data for table `user_addresses`
--

INSERT INTO `user_addresses` (`address_id`, `user_id`, `address`, `description`, `locality`, `landmark`, `latitude`, `longitude`, `is_valid`, `delivery_message`, `time_added`, `distance`) VALUES
(1, 1, '3431, 3rd Cross Rd, Stage 3, Indiranagar, Bengaluru, Karnataka 560038', '3431, 3rd Cross Rd', 'Indiranagar', '', '12.9751307', '77.6393388', 1, 'Delivery Available', '2016-01-07 05:53:52', 5.03);
-- --------------------------------------------------------

--
-- Table structure for table `user_invite_codes`
--

CREATE TABLE IF NOT EXISTS `user_invite_codes` (
  `code_id` int(6) NOT NULL AUTO_INCREMENT,
  `user_id` int(6) NOT NULL,
  `invite_code` varchar(4) NOT NULL,
  `counter` int(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`code_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=738 ;

--
-- Dumping data for table `user_invite_codes`
--



-- --------------------------------------------------------

--
-- Table structure for table `user_wallet`
--

CREATE TABLE IF NOT EXISTS `user_wallet` (
  `wallet_id` int(6) NOT NULL AUTO_INCREMENT,
  `user_id` int(6) NOT NULL,
  `amount` int(11) NOT NULL,
  PRIMARY KEY (`wallet_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=157 ;

--
-- Dumping data for table `user_wallet`
--

INSERT INTO `user_wallet` (`wallet_id`, `user_id`, `amount`) VALUES
(1, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `wallet_transactions`
--

CREATE TABLE IF NOT EXISTS `wallet_transactions` (
  `transaction_id` int(6) NOT NULL AUTO_INCREMENT,
  `user_id` int(6) NOT NULL,
  `transaction_type` enum('credit','debit') NOT NULL,
  `amount` int(11) NOT NULL,
  `source_type` enum('order','referral','coupon','cancellation','signup','lend') NOT NULL,
  `source_id` varchar(40) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=413 ;

--
-- Dumping data for table `wallet_transactions`
--

INSERT INTO `wallet_transactions` (`transaction_id`, `user_id`, `transaction_type`, `amount`, `source_type`, `source_id`, `timestamp`) VALUES
(1, 1, 'credit', 200, 'signup', '1', '2016-01-07 05:53:52');

-- --------------------------------------------------------

--
-- Table structure for table `wishlist`
--

CREATE TABLE IF NOT EXISTS `wishlist` (
  `list_id` int(6) NOT NULL AUTO_INCREMENT,
  `user_id` int(6) NOT NULL,
  `item_id` int(6) NOT NULL,
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_edited` timestamp NULL DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`list_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=740 ;

--
-- Dumping data for table `wishlist`
--


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
