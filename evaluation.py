from util import *  # noqa
import numpy as np
# from collections import dequeue

# Add your import statements here


class Evaluation:
    def queryPrecision(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
                Computation of precision of the Information Retrieval System
                at a given value of k for a single query
        Parameters
                ----------
                arg1 : list
                    A list of integers denoting the IDs of documents in
                    their predicted order of relevance to a query
                arg2 : int
                    The ID of the query in question
                arg3 : list
                    The list of IDs of documents relevant to the query (ground truth)
                arg4 : int
                    The k value

                Returns
                -------
                float
                    The precision value as a number between 0 and 1
        """

        true_pos = len(list(set(query_doc_IDs_ordered[:k]).intersection(true_doc_IDs)))
        return (true_pos) / k

    def meanPrecision(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of precision of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The mean precision value as a number between 0 and 1
        """

        precision_accum = 0

        for query_no in range(len(query_ids)):
            big_true_IDs = list(
                map(
                    lambda v: int(v["id"]),
                    sorted(
                        list(filter(lambda q: query_no == int(q["query_num"]), qrels)),
                        key=lambda q: q["position"],
                    ),
                )
            )
            precision_accum += self.queryPrecision(
                doc_IDs_ordered[query_no], query_ids[query_no], big_true_IDs, k
            )

        return precision_accum / len(query_ids)

    def queryRecall(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of recall of the Information Retrieval System
        at a given value of k for a single query

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of IDs of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The recall value as a number between 0 and 1
        """

        true_pos = len(list(set(query_doc_IDs_ordered[:k]).intersection(true_doc_IDs)))
        if len(true_doc_IDs) == 0:
            return 0
        return (true_pos) / len(true_doc_IDs)

    def meanRecall(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of recall of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The mean recall value as a number between 0 and 1
        """

        recall_accum = 0

        for query_no in range(len(query_ids)):
            big_true_IDs = list(
                map(
                    lambda v: int(v["id"]),
                    sorted(
                        list(filter(lambda q: query_no == int(q["query_num"]), qrels)),
                        key=lambda q: q["position"],
                    ),
                )
            )
            recall_accum += self.queryRecall(
                doc_IDs_ordered[query_no], query_ids[query_no], big_true_IDs, k
            )

        return recall_accum / len(query_ids)

    def queryFscore(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of fscore of the Information Retrieval System
        at a given value of k for a single query

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of IDs of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The fscore value as a number between 0 and 1
        """

        fscore = 0
        precision = self.queryPrecision(
            query_doc_IDs_ordered, query_id, true_doc_IDs, k
        )
        recall = self.queryRecall(query_doc_IDs_ordered, query_id, true_doc_IDs, k)
        if [precision, recall] == [0, 0]:
            fscore = 0
        else:
            fscore = 2 * ((precision * recall) / (precision + recall))
        return fscore

    def meanFscore(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of fscore of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The mean fscore value as a number between 0 and 1
        """

        fscore_accum = 0

        for query_no in range(len(query_ids)):
            big_true_IDs = list(
                map(
                    lambda v: int(v["id"]),
                    sorted(
                        list(filter(lambda q: query_no == int(q["query_num"]), qrels)),
                        key=lambda q: q["position"],
                    ),
                )
            )
            fscore_accum += self.queryFscore(
                doc_IDs_ordered[query_no], query_ids[query_no], big_true_IDs, k
            )

        return fscore_accum / len(query_ids)

    def get_inverted_rel(self, qrels, query_num, doc_num):
        print(f"Doc num is {doc_num} and query num is {query_num}")
        for qrel in qrels:
            if (doc_num == int(qrel["id"])) and (query_num == int(qrel["query_num"])):
                return qrel["position"]

    def get_relevance_match_docs(
        self, query_num, query_doc_IDs_ordered, true_doc_IDs, qrels, k
    ):
        relevances = []
        for i in range(len(query_doc_IDs_ordered)):
            if query_doc_IDs_ordered[i] in true_doc_IDs:
                inverted_relevance = self.get_inverted_rel(
                    qrels, query_num + 1, query_doc_IDs_ordered[i] + 1
                )
                print(inverted_relevance)
                relevances.append(1 / inverted_relevance)
            else:
                relevances.append(0.0)
        return relevances

    def get_top_k_ideal(self, query_num, qrels, k):
        query_pos_docid_map = {}
        for qrel in qrels:
            query_number = int(qrel["query_num"])
            position = qrel["position"]
            if query_number not in query_pos_docid_map:
                query_pos_docid_map[query_number] = {}
                query_pos_docid_map[query_number][position] = [int(qrel["id"])]
            else:
                if position not in query_pos_docid_map[query_number]:
                    query_pos_docid_map[query_number][position] = [int(qrel["id"])]
                else:
                    query_pos_docid_map[query_number][position].append(int(qrel["id"]))

        buffer = []
        for position in sorted(list(query_pos_docid_map[query_num].keys())):
            buffer += query_pos_docid_map[query_num][position]
        return buffer[:k]

    def dcg(self, relevances):
        dcg_score = 0
        for i in range(len(relevances)):
            dcg_score += relevances[i] / (np.log2(i + 2))
        return dcg_score

    def queryNDCG(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k, qrels):
        """
        Computation of nDCG of the Information Retrieval System
        at given value of k for a single query

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of IDs of documents relevant to the query (ground truth)
        arg4 : int
            The k value
        arg5: list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary


        Returns
        -------
        float
            The nDCG value as a number between 0 and 1
        """

        # relevance_k = self.get_relevance_match_docs(
        #    query_id, query_doc_IDs_ordered, true_doc_IDs, qrels, k
        # )
        # dcgs = self.dcg(relevance_k)

        # top_k_ideal = self.get_top_k_ideal(query_id, qrels, k)
        # ideal_dcgs = self.dcg(top_k_ideal)

        # return dcgs / ideal_dcgs

    def meanNDCG(self, doc_IDs_ordered, query_ids, qrels, k):
        """
        Computation of nDCG of the Information Retrieval System
        at a given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries for which the documents are ordered
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The mean nDCG value as a number between 0 and 1
        """

        sum_ndcg = 0
        for query_num in range(len(query_ids)):
            sum_ndcg += self.queryNDCG(
                doc_IDs_ordered[query_num],
                query_ids[query_num],
                list(
                    map(
                        lambda v: int(v["id"]),
                        sorted(
                            list(
                                filter(
                                    lambda q: query_num == int(q["query_num"]), qrels
                                )
                            ),
                            key=lambda q: q["position"],
                        ),
                    )
                ),
                k,
                qrels,
            )
        return sum_ndcg / len(query_ids)

    def queryAveragePrecision(self, query_doc_IDs_ordered, query_id, true_doc_IDs, k):
        """
        Computation of average precision of the Information Retrieval System
        at a given value of k for a single query (the average of precision@i
                                                  values for i such that the ith document is truly relevant)

        Parameters
        ----------
        arg1 : list
            A list of integers denoting the IDs of documents in
            their predicted order of relevance to a query
        arg2 : int
            The ID of the query in question
        arg3 : list
            The list of documents relevant to the query (ground truth)
        arg4 : int
            The k value

        Returns
        -------
        float
            The average precision value as a number between 0 and 1
        """

        avgPrecision = 0

        # Fill in code here

        return avgPrecision

    def meanAveragePrecision(self, doc_IDs_ordered, query_ids, q_rels, k):
        """
        Computation of MAP of the Information Retrieval System
        at given value of k, averaged over all the queries

        Parameters
        ----------
        arg1 : list
            A list of lists of integers where the ith sub-list is a list of IDs
            of documents in their predicted order of relevance to the ith query
        arg2 : list
            A list of IDs of the queries
        arg3 : list
            A list of dictionaries containing document-relevance
            judgements - Refer cran_qrels.json for the structure of each
            dictionary
        arg4 : int
            The k value

        Returns
        -------
        float
            The MAP value as a number between 0 and 1
        """

        meanAveragePrecision = 0

        # Fill in code here

        return meanAveragePrecision
