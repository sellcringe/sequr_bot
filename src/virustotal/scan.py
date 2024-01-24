import asyncio
import io

import vt
import aiohttp

KEY = ["03360b99d34d72810299eec0c5d20e31330439a336bb9de893181bad59e72918"]

async def scan_file(file):
    async with vt.Client(KEY[0]) as client, aiohttp.ClientSession() as session:
        async with session.get(file) as response:

            if response.status == 200:
                print(response)
                with io.BytesIO(await response.read()) as file_stream:
                    analysis = await client.scan_file_async(file_stream, wait_for_completion=True)

                    if analysis.status == 'completed':

                        analysis_id = analysis.id

                        print(analysis_id)
                        info = await get_scan_result(analysis_id, client)
                        return info



async def get_scan_result(id, client):


    # analysis = await client.get_object_async("/analyses/{}", id)
    # for engine_name, detection in analysis.attributes['stats']['malicious'].items():
    #     if detection:
    #         print(f"Malicious detection by {engine_name}: {detection}")
    # return analysis

    analysis = await client.get_object_async(f"/analyses/{id}")
    analysis = analysis.to_dict()
    print(analysis)
    # Убедитесь, что анализ завершен и содержит результаты
    while True:

        if analysis['attributes']['status'] == 'completed' and 'stats' in analysis['attributes']:
            stats = analysis['attributes']['stats']
            stats_message = "Результаты сканирования файла:\n"
            stats_message += f"Безвредных: {stats.get('harmless', 0)}\n"
            stats_message += f"Тип не поддерживается: {stats.get('type-unsupported', 0)}\n"
            stats_message += f"Подозрительных: {stats.get('suspicious', 0)}\n"
            stats_message += f"Не определены: {stats.get('undetected', 0)}\n"
            stats_message += f"Вредоносных: {stats.get('malicious', 0)}\n"
            stats_message += f"Сбои: {stats.get('failure', 0)}\n"
            stats_message += f"Таймауты: {stats.get('timeout', 0)}\n"
            stats_message += f"Подтвержденные таймауты: {stats.get('confirmed-timeout', 0)}\n"
            return stats_message
        else:
            await asyncio.sleep(5)


async def scan_url(url):
    async with vt.Client(KEY[0]) as client:
        analysis = await client.scan_url_async(url, wait_for_completion=True)
        analysis_id = analysis.id

        data = await client.get_object_async("/analyses/{}", analysis_id)
        data = data.to_dict()

        while True:
            if data['attributes']['status'] == 'completed' and 'stats' in data['attributes']:
                stats = data['attributes']['stats']

                stats_message = "Результаты сканирования URL:\n"
                stats_message += f"Безвредных: {stats.get('harmless', 0)}\n"
                stats_message += f"Тип не поддерживается: {stats.get('type-unsupported', 0)}\n"
                stats_message += f"Подозрительных: {stats.get('suspicious', 0)}\n"
                stats_message += f"Не определены: {stats.get('undetected', 0)}\n"
                stats_message += f"Вредоносных: {stats.get('malicious', 0)}\n"
                stats_message += f"Сбои: {stats.get('failure', 0)}\n"
                stats_message += f"Таймауты: {stats.get('timeout', 0)}\n"
                stats_message += f"Подтвержденные таймауты: {stats.get('confirmed-timeout', 0)}\n"
                return stats_message
            else:
                await asyncio.sleep(5)





