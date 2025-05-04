from typing import Dict, List

class BraveSearchClient:
    @staticmethod
    def extract_search_results(search_results: Dict) -> List[Dict]:
        """Extract relevant information from search results."""
        results = []
        try:
            # 检查搜索结果格式
            if not isinstance(search_results, dict):
                print(f"Warning: search_results is not a dict: {type(search_results)}")
                return []
                
            # 检查是否有web字段
            if 'web' not in search_results:
                print(f"Warning: 'web' key not found in search_results")
                return []
                
            # 检查web字段是否为字典
            if not isinstance(search_results['web'], dict):
                print(f"Warning: search_results['web'] is not a dict: {type(search_results['web'])}")
                return []
                
            # 检查是否有results字段
            if 'results' not in search_results['web']:
                print(f"Warning: 'results' key not found in search_results['web']")
                return []
                
            # 检查results字段是否为列表
            if not isinstance(search_results['web']['results'], list):
                print(f"Warning: search_results['web']['results'] is not a list: {type(search_results['web']['results'])}")
                return []
            
            for item in search_results['web']['results']:
                # 安全地提取每个字段
                result = {
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'snippet': item.get('description', '')
                }
                results.append(result)
        except Exception as e:
            print(f"Error in extract_search_results: {e}")
        return results 